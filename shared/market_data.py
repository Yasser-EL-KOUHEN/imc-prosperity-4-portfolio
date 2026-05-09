from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


PRICE_LEVEL_COLUMNS = [
    "bid_price_1",
    "bid_price_2",
    "bid_price_3",
    "ask_price_1",
    "ask_price_2",
    "ask_price_3",
]

VOLUME_LEVEL_COLUMNS = [
    "bid_volume_1",
    "bid_volume_2",
    "bid_volume_3",
    "ask_volume_1",
    "ask_volume_2",
    "ask_volume_3",
]

MARKET_FILE_RE = re.compile(r"^(prices|trades)_round_(-?\d+)_day_(-?\d+)$")


@dataclass(frozen=True)
class MarketFile:
    path: Path
    round_id: int
    day: int


def parse_market_file(path: Path) -> MarketFile:
    match = MARKET_FILE_RE.match(path.stem)
    if match is None:
        raise ValueError(f"Unrecognized market data filename: {path.name}")
    _, round_id, day = match.groups()
    return MarketFile(path=path, round_id=int(round_id), day=int(day))


def discover_files(
    data_dir: Path,
    round_filter: int | None = None,
    day_filter: int | None = None,
    recursive: bool = True,
) -> tuple[list[Path], list[Path]]:
    iterator = data_dir.rglob("prices_*.csv") if recursive else data_dir.glob("prices_*.csv")
    price_files: list[Path] = []
    trade_files: list[Path] = []

    for path in sorted(iterator):
        meta = parse_market_file(path)
        if round_filter is not None and meta.round_id != round_filter:
            continue
        if day_filter is not None and meta.day != day_filter:
            continue
        price_files.append(path)
        trade_files.append(path.with_name(f"trades_round_{meta.round_id}_day_{meta.day}.csv"))

    return price_files, trade_files

def load_prices(paths: list[Path]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in paths:
        meta = parse_market_file(path)
        df = pd.read_csv(path, sep=";", dtype={"timestamp": int})
        df["round"] = meta.round_id
        df["day"] = meta.day
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)
    df.sort_values(["round", "day", "timestamp", "product"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    df["mid_price"] = pd.to_numeric(df["mid_price"], errors="coerce")
    for column in PRICE_LEVEL_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    for column in VOLUME_LEVEL_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).astype(int)

    df["spread"] = df["ask_price_1"] - df["bid_price_1"]
    df["obi"] = (
        (df["bid_volume_1"] - df["ask_volume_1"])
        / (df["bid_volume_1"] + df["ask_volume_1"] + 1e-9)
    )
    df["has_two_sided_book"] = df["bid_price_1"].notna() & df["ask_price_1"].notna()
    return df


def load_trades(paths: list[Path]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in paths:
        meta = parse_market_file(path)
        df = pd.read_csv(path, sep=";")
        df["round"] = meta.round_id
        df["day"] = meta.day
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)
    df["timestamp"] = df["timestamp"].astype(int)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["product"] = df["symbol"].astype(str)
    df.sort_values(["round", "day", "timestamp", "product"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def load_round_data(
    data_dir: Path,
    round_filter: int,
    day_filter: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    price_files, trade_files = discover_files(
        data_dir=data_dir,
        round_filter=round_filter,
        day_filter=day_filter,
        recursive=True,
    )
    return load_prices(price_files), load_trades(trade_files)


def join_trades_to_books(
    trades: pd.DataFrame,
    prices: pd.DataFrame,
    direction: str = "backward",
) -> pd.DataFrame:
    if trades.empty or prices.empty:
        return trades.copy()

    book_columns = [
        "round",
        "day",
        "timestamp",
        "product",
        "bid_price_1",
        "ask_price_1",
        "mid_price",
        "spread",
        "obi",
    ]
    group_columns = ["round", "day", "product"]
    trade_df = trades.copy()
    trade_df["_orig_index"] = np.arange(len(trade_df))
    trade_df.sort_values(group_columns + ["timestamp"], inplace=True)
    book_df = prices[book_columns].copy()
    book_df.sort_values(group_columns + ["timestamp"], inplace=True)

    merged_groups: list[pd.DataFrame] = []
    grouped_books = {
        key: group.drop(columns=group_columns).copy()
        for key, group in book_df.groupby(group_columns, sort=False)
    }

    for key, trade_group in trade_df.groupby(group_columns, sort=False):
        book_group = grouped_books.get(key)
        if book_group is None or book_group.empty:
            merged_group = trade_group.copy()
            merged_group["bid_price_1"] = np.nan
            merged_group["ask_price_1"] = np.nan
            merged_group["mid_price"] = np.nan
            merged_group["spread"] = np.nan
            merged_group["obi"] = np.nan
        else:
            merged_group = pd.merge_asof(
                trade_group.sort_values("timestamp"),
                book_group.sort_values("timestamp"),
                on="timestamp",
                direction=direction,
                allow_exact_matches=True,
            )
        merged_groups.append(merged_group)

    if not merged_groups:
        return trades.copy()

    merged = pd.concat(merged_groups, ignore_index=True)
    merged.sort_values("_orig_index", inplace=True)
    merged.drop(columns="_orig_index", inplace=True)
    merged.reset_index(drop=True, inplace=True)
    return merged


def classify_trade_side(joined: pd.DataFrame) -> pd.DataFrame:
    if joined.empty:
        frame = joined.copy()
        frame["trade_side"] = pd.Series(dtype="object")
        return frame

    frame = joined.copy()
    conditions = [
        np.isclose(frame["price"], frame["bid_price_1"], equal_nan=False),
        np.isclose(frame["price"], frame["ask_price_1"], equal_nan=False),
        frame["price"].between(frame["bid_price_1"], frame["ask_price_1"], inclusive="neither"),
    ]
    choices = ["bid", "ask", "between"]
    frame["trade_side"] = np.select(conditions, choices, default="outside")
    missing_mask = frame["bid_price_1"].isna() | frame["ask_price_1"].isna()
    frame.loc[missing_mask, "trade_side"] = "unknown"
    return frame

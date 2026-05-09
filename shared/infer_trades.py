"""
infer_trades.py — Synthetic trade inference from order-book level changes.

For each pair of consecutive price-snapshot ticks (t, t+next), any ask or bid
level whose volume shrank between the two snapshots must have been (partially)
consumed by a crossing order.  We record those consumption events as synthetic
trade rows, which prosperity3bt can then use for passive fill matching.

Usage (standalone):
    python research/shared/infer_trades.py \\
        --prices data/round3/prices_round_3_day_3.csv \\
        --out    data/round3/trades_round_3_day_3.csv

The output file is in the same semicolon-delimited format as the official
trades CSVs:
    timestamp;buyer;seller;symbol;currency;price;quantity
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def _parse_ob_snapshot(row: list[str]) -> tuple[dict[int, int], dict[int, int]]:
    """Return ({bid_price: volume}, {ask_price: volume}) from a price-CSV row."""
    def _levels(price_cols: list[str], vol_cols: list[str]) -> dict[int, int]:
        out: dict[int, int] = {}
        for p_str, v_str in zip(price_cols, vol_cols):
            if not p_str:
                break
            out[int(p_str)] = int(v_str)
        return out

    bid_prices = [row[3], row[5], row[7]]
    bid_vols   = [row[4], row[6], row[8]]
    ask_prices = [row[9],  row[11], row[13]]
    ask_vols   = [row[10], row[12], row[14]]
    return _levels(bid_prices, bid_vols), _levels(ask_prices, ask_vols)


def infer_trades(prices_path: Path) -> list[tuple[int, str, float, int]]:
    """
    Return list of (timestamp, symbol, price, quantity) synthetic trade events.

    A trade event is generated whenever a bid or ask level's volume shrank
    between two consecutive snapshots for the same product.  The event is
    timestamped at the LATER snapshot (when the shrinkage is observable).

    Limitations and mitigations:
      - Bot order cancellations also shrink OB levels → false trades.
        Mitigation: cancellations are rare for liquid products; and since
        the synthetic trade is at an OB price, it can only trigger our
        passive fills when our quote is at a better-or-equal price — which
        is already a conservative match condition.
      - Bot order additions can mask shrinkage (net volume unchanged even
        though a trade occurred) → false negatives.
        This is accepted; the inference is a lower-bound on trade activity.
    """
    # prev_snap[product] = (bids_dict, asks_dict) at previous timestamp
    prev_snap: dict[str, tuple[dict[int,int], dict[int,int]]] = {}
    prev_ts:   dict[str, int] = {}

    events: list[tuple[int, str, float, int]] = []

    with prices_path.open(encoding="utf-8") as fh:
        reader = csv.reader(fh, delimiter=";")
        next(reader)  # skip header

        for row in reader:
            ts      = int(row[1])
            product = row[2]

            bids, asks = _parse_ob_snapshot(row)

            if product in prev_snap:
                prev_bids, prev_asks = prev_snap[product]

                # Ask side: volume decrease → someone bought (crossed to ask)
                for price, prev_vol in prev_asks.items():
                    cur_vol = asks.get(price, 0)
                    if cur_vol < prev_vol:
                        events.append((ts, product, float(price), prev_vol - cur_vol))

                # Bid side: volume decrease → someone sold (crossed to bid)
                for price, prev_vol in prev_bids.items():
                    cur_vol = bids.get(price, 0)
                    if cur_vol < prev_vol:
                        events.append((ts, product, float(price), prev_vol - cur_vol))

            prev_snap[product] = (bids, asks)
            prev_ts[product]   = ts

    return events


def write_trades_csv(events: list[tuple[int, str, float, int]], out_path: Path) -> int:
    """Write synthetic trades to CSV; return row count written."""
    # Sort by timestamp then symbol for deterministic output
    events_sorted = sorted(events, key=lambda e: (e[0], e[1]))

    with out_path.open("w", encoding="utf-8", newline="") as fh:
        fh.write("timestamp;buyer;seller;symbol;currency;price;quantity\n")
        for ts, symbol, price, qty in events_sorted:
            fh.write(f"{ts};;;{symbol};XIRECS;{price:.1f};{qty}\n")

    return len(events_sorted)


def infer_and_write(prices_path: Path, out_path: Path) -> int:
    events = infer_trades(prices_path)
    return write_trades_csv(events, out_path)


def _stats(events: list[tuple[int, str, float, int]]) -> None:
    from collections import Counter
    prod_count: Counter[str] = Counter()
    prod_vol:   Counter[str] = Counter()
    for _, sym, _, qty in events:
        prod_count[sym] += 1
        prod_vol[sym]   += qty
    print(f"  Total synthetic trade events : {len(events):,}")
    print(f"  {'Product':30s}  {'events':>8}  {'total_vol':>10}")
    print("  " + "-" * 55)
    for sym in sorted(prod_count):
        print(f"  {sym:30s}  {prod_count[sym]:>8,}  {prod_vol[sym]:>10,}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infer synthetic trades from OB changes")
    parser.add_argument("--prices", required=True, help="prices CSV path")
    parser.add_argument("--out",    required=True, help="output trades CSV path")
    parser.add_argument("--stats",  action="store_true", help="print per-product stats")
    args = parser.parse_args()

    prices_path = Path(args.prices)
    out_path    = Path(args.out)

    print(f"Reading prices : {prices_path}")
    events = infer_trades(prices_path)

    if args.stats:
        _stats(events)

    n = write_trades_csv(events, out_path)
    print(f"Written {n:,} synthetic trade rows -> {out_path}")

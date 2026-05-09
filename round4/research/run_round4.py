"""
run_round4.py -- prosperity3bt wrapper for Round 4
==================================================

Uses round4 data (days 1, 2, 3) and vault/round4_trader.py by default.

Usage
-----
    python research/round4/run_round4.py             # all days (1, 2, 3)
    python research/round4/run_round4.py --day 1     # single day
    python research/round4/run_round4.py --trader vault/some_trader.py
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.shared.prosperity_bootstrap import ROUND3_LIMITS, run_prosperity3bt_cli

BACKTESTS_DIR = ROOT / "backtests"

DEFAULT_TRADER = ROOT / "vault" / "round4_trader.py"
DATA_DIR = ROOT / "data"
ROUND = 4
ALL_DAYS = [1, 2, 3]
# TTE: Round 4 starts at 7d on day 1, counts down
HISTORICAL_TTE_DAYS = {1: 7.0, 2: 6.0, 3: 5.0}

PAT_TOTAL = re.compile(r"^Total profit:\s+([\d,\-]+)", re.MULTILINE)
PAT_PRODUCT = re.compile(r"^([A-Z_0-9]+):\s+([\d,\-]+)\s*$", re.MULTILINE)


def _run_one_day(day: int, trader: Path, args) -> tuple[int, str]:
    cli_args = [
        str(trader),
        f"{ROUND}-{day}",
        "--data", str(DATA_DIR),
        "--match-trades", args.match_trades,
        "--merge-pnl",
        "--print",
    ]
    if args.no_out:
        cli_args.append("--no-out")
    elif args.out:
        cli_args.extend(["--out", args.out])
    else:
        cli_args.append("--no-out")
    if args.no_progress:
        cli_args.append("--no-progress")

    saved_env = os.environ.get("BT_INITIAL_TTE_DAYS")
    os.environ["BT_INITIAL_TTE_DAYS"] = str(HISTORICAL_TTE_DAYS[day])
    buf = StringIO()
    try:
        with redirect_stdout(buf):
            rc = run_prosperity3bt_cli(cli_args=cli_args, extra_limits=ROUND3_LIMITS)
    finally:
        if saved_env is None:
            os.environ.pop("BT_INITIAL_TTE_DAYS", None)
        else:
            os.environ["BT_INITIAL_TTE_DAYS"] = saved_env
    return rc, buf.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description="Round 4 backtester wrapper")
    parser.add_argument("--day", type=int, default=None)
    parser.add_argument("--trader", type=str, default=str(DEFAULT_TRADER))
    parser.add_argument("--out", type=str, default=None)
    parser.add_argument("--no-out", action="store_true")
    parser.add_argument("--match-trades", type=str, default="all",
                        choices=["all", "worse", "none"])
    parser.add_argument("--no-progress", action="store_true")
    args = parser.parse_args()

    trader = Path(args.trader)
    if not trader.is_absolute():
        trader = ROOT / trader

    days = [args.day] if args.day is not None else ALL_DAYS

    per_day_total: dict[int, int] = {}
    per_day_products: dict[int, dict[str, int]] = {}
    aggregate_products: dict[str, int] = {}

    for day in days:
        tte = HISTORICAL_TTE_DAYS[day]
        print(f"\n=== Round 4 day {day}  (BT_INITIAL_TTE_DAYS={tte}) ===")
        rc, output = _run_one_day(day, trader, args)
        print(output, end="")
        if rc != 0:
            print(f"prosperity3bt returned exit code {rc}")
            sys.exit(rc)

        m_total = PAT_TOTAL.search(output)
        if m_total:
            per_day_total[day] = int(m_total.group(1).replace(",", ""))
        end = m_total.start() if m_total else len(output)
        block = output[max(0, end - 1500):end]
        prods = {p: int(v.replace(",", "")) for p, v in PAT_PRODUCT.findall(block)}
        per_day_products[day] = prods
        for p, v in prods.items():
            aggregate_products[p] = aggregate_products.get(p, 0) + v

    print("\n" + "=" * 64)
    print("MERGED ROUND 4 SUMMARY (per-day TTE-correct backtest)")
    print("=" * 64)
    for day in days:
        print(f"  day {day} (TTE={HISTORICAL_TTE_DAYS[day]}d): "
              f"{per_day_total.get(day, 0):>10,}")
    grand = sum(per_day_total.values())
    print(f"  {'GRAND TOTAL':>20}: {grand:>10,}")

    print(f"\n  Per-product (sum across days):")
    for p in sorted(aggregate_products.keys()):
        v = aggregate_products[p]
        if v != 0:
            print(f"    {p:30s} {v:>10,}")


if __name__ == "__main__":
    main()

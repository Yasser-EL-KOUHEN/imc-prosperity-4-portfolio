---
type: concept
tags: [safety, limits, compliance, round3]
sources: [rounds/round3/trader.py, backtests/phase9_safety.md, backtests/phase4_position_limit.md, .planning/REQUIREMENTS.md]
updated: 2026-04-27
---

# Position Limits

## What They Are

Position limits are **hard constraints** on how much of each product the trader can hold at any time. In Prosperity, they are enforced structurally — if you submit orders that would breach the limit, excess fills are rejected.

| Product | Limit |
|---------|-------|
| HYDROGEL_PACK | ±200 |
| VELVETFRUIT_EXTRACT | ±200 |
| VEV_* vouchers (all strikes) | ±300 |

## Enforcement Pattern

Every tick, before generating orders:

```python
buy_cap = self.LIMIT - pos    # max additional units we can buy
sell_cap = self.LIMIT + pos   # max units we can sell short

# Example: if pos = 150, LIMIT = 200
#   buy_cap = 50  (can buy 50 more before hitting +200)
#   sell_cap = 350  (can sell 350 before hitting -200)

qty = min(desired_qty, buy_cap, max_order_size)
```

This structural pattern ensures **no order can ever breach the limit** regardless of market conditions. Orders are sized down to respect the cap, not rejected after the fact.

## Safety Gate (Phase 9 — SAFE-01)

Phase 9 verified all limits via static code inspection:

```
HydrogelMM.LIMIT = 200       ✅
VEVUnderlying.LIMIT = 200    ✅
VoucherTrader.LIMIT = 300    ✅
```

Pattern `buy_cap = self.LIMIT - pos` and `sell_cap = self.LIMIT + pos` matched **3 times each** in trader.py source (one per class).

## Position Under --merge-pnl

In the backtester with `--merge-pnl`, positions at logged timestamps appear as 0 because:
- End-of-day settlement liquidates all open positions at fair value
- The position time series shows intraday positions, but the CSV snapshot captures post-settlement state

The HYDROGEL strategy does take intraday positions (the PnL comes from fills); they just close out each day. The limit enforcement is confirmed by the structural `buy_cap` / `sell_cap` pattern — not by observing non-zero positions in the timeseries.

## Why Hard Limits Matter

1. **Competition rules:** Exceeding limits on a tick can disqualify that tick's trades or crash the submission
2. **Risk management:** Unlimited position buildup is catastrophic in a trending market
3. **Fill model consistency:** The local backtest honours limits; the official simulator does too

## Interaction with Inventory Skew

Soft inventory management ([[Concepts/inventory_risk]]) complements hard limits:
- Skew softly pushes position toward zero via price incentives
- Hard cap ensures position never actually breaches the limit structurally

Together: soft management handles normal inventory; hard cap is the failsafe.

## Links

[[Concepts/inventory_risk]] · [[Backtests/Phase9_Safety]] · [[Products/HYDROGEL_PACK]] · [[Parameters/HYDROGEL_Params]]

---
type: concept
tags: [core, inventory, position-limits, risk]
sources: [rounds/round3/trader.py, backtests/phase4_inv_skew_sweep.md, backtests/phase4_position_limit.md]
updated: 2026-04-27
---

# Inventory Risk

## What It Is

When a market maker fills one side more than the other, they accumulate a **directional position** (inventory). This is risky because:

1. **Price risk:** If the market moves against the position, losses mount
2. **Limit risk:** Position limits cap inventory at ±200/300 — breaching them means no more fills

**ML analogy:** Inventory risk is like L2 regularization. Unregularized market making → position drifts → overfits to short-term noise → high variance in PnL. Regularizing (skewing fair value against position) keeps position near zero and reduces variance — at the cost of slightly lower expected PnL.

## Mechanism: Inventory Skew

The standard solution is to **skew the fair value** against the position:

```python
adjusted_fair = fair - inv_skew * pos    # inv_skew = 0.03
```

- If `pos > 0` (long): `adjusted_fair < fair` → our ask moves down (easier to sell), our bid moves down (harder to buy) → inventory drains
- If `pos < 0` (short): `adjusted_fair > fair` → our bid moves up, ask moves up → inventory drains

The skew creates a **soft incentive** to reduce position without forcing hard sells at bad prices.

## Calibrated Inventory Skew (HYDROGEL)

Phase 4 sweep over `inv_skew ∈ {0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08}`:

| skew | d0 | d1 | d2 | total | max_regression | passes |
|------|----|----|-----|-------|----------------|--------|
| 0.00 | 67,476 | 30,985 | 32,594 | 131,055 | 34.0% | ❌ |
| 0.02 | 56,181 | 42,629 | 41,354 | 140,164 | 9.3% | ❌ |
| **0.03** | 52,941 | 47,432 | 42,302 | **142,675** | **-0.8%** | **✅** |
| 0.04 | 49,393 | 49,545 | 40,774 | 139,712 | 4.6% | ❌ |
| 0.05 | 43,804 | 47,831 | 40,492 | 132,127 | 15.4% | ❌ |

**Winner: inv_skew = 0.03.** Too low (0.00-0.02) → inventory builds up, day 1/2 collapse. Too high (0.04+) → over-corrects, day 0 collapses.

The gate requires: `3d total ≥ 140,748 AND max single-day regression ≤ 2.0%`. Only skew=0.03 passes.

## Hard Position Limits

Every tick, before sending orders, we compute:

```python
buy_cap = LIMIT - pos      # how much more we can buy
sell_cap = LIMIT + pos     # how much more we can sell
qty = min(desired_qty, buy_cap, 60)   # cap at limit headroom
```

This structurally prevents any order from breaching the limit. Phase 9 verified:
- `HydrogelMM.LIMIT = 200` ✅
- `VEVUnderlying.LIMIT = 200` ✅
- `VoucherTrader.LIMIT = 300` ✅
- Buy/sell cap pattern matched 3 occurrences each ✅

See [[Concepts/Position_Limits]].

## Position in HYDROGEL Backtest

Interestingly, recorded max position = 0 across all days in `--merge-pnl` mode. This is because end-of-day settlement liquidates open positions — positions exist intraday but are zeroed at settlement. The strategy **does** take intraday positions; they just don't persist across days.

## Links

[[Strategies/market_making]] · [[Concepts/Position_Limits]] · [[Products/HYDROGEL_PACK]] · [[Backtests/Phase4_Rho_Sweep]] · [[Parameters/HYDROGEL_Params]]

---
type: product
tags: [round3, options, delta-hedge, passive]
sources: [rounds/round3/trader.py, backtests/phase5_vev_passive_comparison.md, backtests/phase5_delta_hedge.md, .planning/STATE.md]
updated: 2026-04-27
---

# VELVETFRUIT_EXTRACT

**Rounds:** 3 | **Position limit:** ±200 | **Type:** Options underlying (spot); hedge vehicle

## Role in Strategy

VELVETFRUIT_EXTRACT is the **underlying asset** for all VEV voucher options (VEV_4000 through VEV_6500). We do **not** trade it for alpha — we use it exclusively to **delta hedge** our options book.

**The key decision (v2 → v3 lesson):** Spread-crossing for aggressive hedging lost **−90,000 XIREC on day 2 alone** in v2. v3 is passive-only.

## Strategy: Passive Delta Hedge

```python
VEV_PASSIVE_ONLY = True  # Hard constraint — never cross the spread

# Target position: -aggregate_options_delta * spot
# Only join at best bid or best ask (passive fill)
# Never send orders that cross the spread
```

**ML analogy:** Think of this as a constraint-satisfying optimizer. We want `position ≈ -Δ_options` but only through passive price points. We sacrifice optimality (exact hedge) to avoid the execution cost of crossing the spread.

### What "Passive Only" Means

- **Allowed:** Post a bid at `best_bid` (join the queue)
- **Allowed:** Post an ask at `best_ask` (join the queue)
- **Forbidden:** Post a bid at `best_ask` or higher (aggressive buy)
- **Forbidden:** Post an ask at `best_bid` or lower (aggressive sell)

## Backtest: Passive vs Aggressive (Phase 5)

| Config | Day 0 | Day 1 | Day 2 | 3d Total | VEV Standalone |
|--------|-------|-------|-------|----------|---------------|
| Baseline (aggressive allowed) | 52,941 | 47,432 | 42,302 | 142,675 | 7,031 |
| Passive-only | **53,780** | **47,432** | **42,302** | **143,514** | **7,612** |
| Delta (passive − baseline) | **+839** | 0 | 0 | **+839** | **+581** |

- **Gate:** All-days-win (passive ≥ baseline each day) → **PASS**
- **Improvement:** +839 total, entirely from day 0 (+581 VEV standalone + rest from better HYDROGEL execution when VEV doesn't consume limit)
- Days 1/2 tied: aggressive sections didn't fire those days (delta stayed below cap)

## Per-Day VEV PnL (Phase 10 Final)

| Day | VEV PnL |
|-----|---------|
| 0 | 4,154 |
| 1 | 1,044 |
| 2 | 138 |
| **Total** | **5,336** |

VEV contributes positively on all days but is intentionally small — it's a cost center (hedge), not an alpha source.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| LIMIT | 200 |
| VEV_PASSIVE_ONLY | True (locked) |
| Delta cap (hard) | From options book aggregate |

## Why This Product Is Not Alpha-Generating

1. We have no edge in predicting VELVETFRUIT spot direction
2. Our alpha comes from options spread capture (via VEV_* quoting)
3. The hedge cost is offset by better option fills (we can quote options more aggressively when we know we can hedge)

## Links

[[Strategies/Delta_Hedging]] · [[Products/Options/VEV_5300]] · [[Products/Options/VEV_5400]] · [[Concepts/Implied_Volatility]] · [[Backtests/Phase5_VEV_Passive]] · [[Parameters/VELVETFRUIT_Params]] · [[Rounds/Round3_findings]]

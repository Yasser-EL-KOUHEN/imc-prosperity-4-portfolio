---
type: product
tags: [round3, mean-reversion, calibrated, options]
sources: [rounds/round3/trader.py, backtests/phase3_fair_value_trace.md, backtests/phase4_rho_sweep.md, backtests/phase4_inv_skew_sweep.md, backtests/phase3_obi_experiment.md, backtests/phase3_rho_experiment.md, .planning/STATE.md]
updated: 2026-04-27
---

# HYDROGEL_PACK

**Rounds:** 3 | **Position limit:** ±200 | **Type:** Stationary delta-1, mean-reverting

## Market Characteristics

- **Fair value anchor:** ≈ 10,000 (simulator pulls price toward this)
- **Mid-price range (day 1):** 9,908.5 – 10,079.0 (range = 170.5 ticks)
- **Mid-price mean (day 1):** 9,992.06, stdev = 37.61
- **Mean-reversion:** Confirmed — lag-1 ACF = **−0.1292** (mean-reverting regime)
- **AR(1) coefficient (calibrated):** small moves = −0.094, large moves = −0.237
- **Spread:** Wide (≥16 ticks triggers passive quote logic)
- **OBI signal:** Present (β=11.2, R²=0.089, t=31) but **disabled in production** — net-negative in backtest

## Strategy: EMA Mean-Reversion Market Making

**ML analogy:** This is a time-series AR(1) model. The "label" at time t is the next mid-price. The feature is the current deviation from the EMA. We quote aggressively toward the mean and passively inside the spread.

### Fair Value Model (`EMAReversionModel`)

```python
# EMA smoothed mid-price
ema = alpha * mid + (1 - alpha) * ema       # alpha = 0.35

# Anchor pull toward 10000
fair = (1 - anchor_w) * ema + anchor_w * 10000   # anchor_w = 0.20

# Magnitude-bucketed reversion adjustment
dmid = mid - last_mid
if abs(dmid) >= 5.0:                        # large move threshold
    fair -= large_rho * dmid                # large_rho = 0.42
elif abs(dmid) >= 2.0:                      # small move threshold
    fair -= small_rho * dmid                # small_rho = 0.08

# OBI overlay (disabled by default)
fair += obi_beta * OBI(order_depth)         # obi_beta = 0.0
```

### Quoting Logic

1. **Aggressive taking:** If best ask/bid is far enough from fair (threshold=2.5 ticks), take up to 30 (or 60 if edge ≥5) units
2. **Passive quoting:** When spread ≥ 16 ticks, post bid at (best_bid+1) and ask at (best_ask-1) with size 32, adjusted by inventory skew
3. **Inventory skew:** `adjusted_fair = fair − 0.03 × pos` — shifts our fair value against our position to encourage rebalancing

## Calibrated Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| EMA alpha | 0.35 | v6 sweep (hydrogel_sweep.py) |
| anchor_weight | **0.20** | v6 sweep — NOT 0.0 despite planning doc ⚠️ |
| anchor_price | 10,000 | Fixed |
| small_move_threshold | 2.0 ticks | Empirical |
| large_move_threshold | 5.0 ticks | Empirical |
| small_move_rho | **0.08** | Phase 4 grid winner |
| large_move_rho | **0.42** | Phase 4 grid winner |
| take_threshold | 2.5 | v6 sweep |
| passive_edge | 1.2 | Fixed |
| inv_skew | **0.03** | Phase 4 inv_skew sweep winner |
| obi_beta | 0.0 (disabled) | Phase 3 experiment — net-negative |

> ⚠️ **Planning doc contradiction:** `.planning/PROJECT.md` and `STATE.md` list "anchor_weight=0.0 — Locked" but trader.py v6 uses `anchor_w=0.20` (the dominant improvement in v6). The planning doc is stale. See [[Research/Decisions_Log]].

## Backtest Performance

| Metric | Value |
|--------|-------|
| Day 0 HYDROGEL PnL (Phase 4) | 50,942 |
| Day 1 HYDROGEL PnL (Phase 4) | 43,735 |
| Day 2 HYDROGEL PnL (Phase 4) | 36,963 |
| 3-day HYDROGEL total (Phase 4) | **131,640** |
| cum_pnl correlation with time (day 1) | 0.9576 — steady earner |
| Max drawdown (day 1) | −9,729 (recovers to +43,281) |
| Max position ever recorded | 0 (position closes between ticks in --merge-pnl) |

## OBI Disabled — Why

OBI was tested in Phase 3:
- β=11.2 is statistically significant (t=31) but explains only R²=8.9% of variance
- Net backtest impact: **−5,218** over 3 days (hurt days 0 and 2 significantly)
- Root cause: OBI shifts quotes away from the fair value's passive-edge zone; the anchor pull earns more than OBI adjusts

See [[Backtests/Phase3_HYDROGEL_FV]], [[Strategies/OBI_Signal]].

## Box-and-Lines Signal (Phase 11 — Null Result)

A support/resistance box signal (N-period min/max) was researched but rejected:
- Grid of 9 configs (N∈{100,200,500} × alpha∈{0.3,0.5,0.7}) tested
- Best result: N=100, alpha=0.7 → 153,568 (only 1/3 days improved, gate requires ≥2/3)
- Signal wired in code with default `HYDRO_BOX_ALPHA=0.0` (no behavioral change)
- Baseline 153,566 preserved

See [[Backtests/Phase11_Box_Signal]].

## Links

[[Strategies/Mean_Reversion]] · [[Strategies/OBI_Signal]] · [[Concepts/inventory_risk]] · [[Concepts/fair_value]] · [[Parameters/HYDROGEL_Params]] · [[Backtests/Phase4_Rho_Sweep]] · [[Rounds/Round3_findings]]

---
type: strategy
tags: [round3, hydrogel, ar1, calibrated]
sources: [rounds/round3/trader.py, backtests/phase3_fair_value_trace.md, backtests/phase3_rho_experiment.md, backtests/phase4_rho_sweep.md, backtests/phase4_bucketed_vs_flat.md]
updated: 2026-04-27
---

# Mean Reversion Strategy

## What It Is

Mean reversion exploits the statistical tendency of a price to return toward its long-run average after a deviation. For HYDROGEL_PACK, this tendency is confirmed:
- Lag-1 ACF = **−0.1292** (negative → mean-reverting)
- 28/50 lags are negative in the autocorrelation function

**ML analogy:** This is an autoregressive time-series model (AR(1)):
`mid_{t+1} ≈ fair_t - ρ × (mid_t - mid_{t-1})`

The reversion coefficient ρ tells us how much of a price move is expected to reverse. Higher ρ = stronger reversion.

## AR(1) Model for HYDROGEL

From `research/round3/hydrogel_audit.py`:

| Move type | Threshold | AR(1) coefficient | Interpretation |
|-----------|-----------|-------------------|---------------|
| Small move | 2–5 ticks | **−0.094** | 9.4% of a small move reverses |
| Large move | ≥5 ticks | **−0.237** | 23.7% of a large move reverses |

Larger moves revert more strongly — this is the **magnitude-bucketed** design.

## Implementation: EMAReversionModel

```python
class EMAReversionModel:
    def fair_value(self, mid: float) -> float:
        # 1. Update EMA
        ema = alpha * mid + (1 - alpha) * ema    # alpha = 0.35

        # 2. Anchor pull toward 10,000
        fair = (1 - anchor_w) * ema + anchor_w * 10000  # anchor_w = 0.20

        # 3. Reversion adjustment
        dmid = mid - last_mid
        if abs(dmid) >= 5.0:
            fair -= 0.42 * dmid     # large_rho = 0.42
        elif abs(dmid) >= 2.0:
            fair -= 0.08 * dmid     # small_rho = 0.08

        return fair
```

### Why anchor_weight = 0.20 (Not 0.0)

The anchor pull toward 10,000 was the **dominant improvement** in v6. The simulator pulls HYDROGEL toward 10,000, so incorporating this pull in our fair value generates many more passive fills inside the 16-wide spread.

> ⚠️ Planning docs (`PROJECT.md`, `STATE.md`) list "anchor_weight=0.0 — Locked". This is stale. v6 deliberately set anchor_w=0.20. The code is authoritative.

## Calibrated AR(1) vs Sweep Winner

Phase 3 experiment: tested calibrated AR(1) values (0.094/0.237) vs v6 sweep winner (0.12/0.48):

| Config | Day 0 | Day 1 | Day 2 | Total |
|--------|-------|-------|-------|-------|
| Calibrated (0.094/0.237) | 53,827 | 47,352 | 39,944 | 141,123 |
| Sweep winner (0.12/0.48) | 51,788 | 46,978 | 41,982 | 140,748 |

**Decision:** Kept sweep winner (0.12/0.48) — must improve ALL 3 days. Calibrated hurts day 2.

**Phase 4 fine grid** then found the true winner: small=0.08, large=0.42 → 142,675 total. The sweep over-reverts relative to AR(1) theory, which acts as a profit multiplier on the specific market structure of HYDROGEL.

## Backtest Evidence

- **Cumulative PnL corr with time (day 1):** 0.9576 — earnings accrue steadily, not from luck
- **Day 1 trajectory:** 0 → 13,739 → 12,733 → 27,729 → 35,145 → 43,281 (monotone with noise)
- **Max drawdown (day 1):** −9,729 (fully recovered)

## Inventory Skew Interaction

The mean-reversion model sets fair value. Inventory skew shifts this fair value based on position:
```python
adjusted_fair = fair - 0.03 * pos
```
Best inventory skew (Phase 4 sweep): **0.03** — the only value that passes the all-days gate with total = 142,675.

## Links

[[Products/HYDROGEL_PACK]] · [[Strategies/market_making]] · [[Concepts/fair_value]] · [[Concepts/inventory_risk]] · [[Parameters/HYDROGEL_Params]] · [[Backtests/Phase3_HYDROGEL_FV]] · [[Backtests/Phase4_Rho_Sweep]]

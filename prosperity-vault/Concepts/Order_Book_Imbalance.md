---
type: concept
tags: [obi, microstructure, signal, round3]
sources: [rounds/round3/trader.py, backtests/phase3_obi_experiment.md, backtests/phase8_obi_sweep.md, research/round3/microstructure_eda.py]
updated: 2026-04-27
---

# Order Book Imbalance (OBI)

## Definition

OBI measures the relative pressure of buyers vs sellers at the top of the order book:

```
OBI = (bid_size - ask_size) / (bid_size + ask_size)    ∈ [-1, +1]
```

- `+1`: only buyers (all volume on bid) — strong upward pressure
- `−1`: only sellers (all volume on ask) — strong downward pressure
- `0`: perfectly balanced

We use only **top-of-book** (best bid/ask sizes) — not the full depth.

**ML analogy:** OBI is a single-feature input `x` to a linear model `fair = BS_fair + β × x`. Calibration finds the `β` that minimizes price prediction error. The feature captures order flow imbalance — an established microstructure predictor.

## Statistical Calibration

From `research/round3/microstructure_eda.py`:

| Product | β | R² | t-stat | Interpretation |
|---------|---|----|----|-----|
| HYDROGEL_PACK | 11.2 | 0.089 | 31 | Strong signal, statistically |
| VELVETFRUIT_EXTRACT | 0.80 | 0.079 | 29 | Moderate |
| VEV_5300 | **0.65** | **0.125** | **38** | Strongest among options |
| VEV_5400 | 0.46 | 0.075 | 28 | Moderate |
| VEV_5500 | 0.49 | 0.081 | 30 | Moderate |

All t-statistics > 28 → statistically significant at any conventional level. But R² = 7–13% → OBI is a weak signal in terms of variance explained.

## Implementation

```python
def top_obi(order_depth: OrderDepth) -> float:
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return 0.0
    best_bid = max(order_depth.buy_orders.keys())
    best_ask = min(order_depth.sell_orders.keys())
    bid_vol = order_depth.buy_orders[best_bid]
    ask_vol = -order_depth.sell_orders[best_ask]   # sell side stored negative
    total = bid_vol + ask_vol
    return (bid_vol - ask_vol) / total if total > 0 else 0.0
```

Applied as: `fair += obi_beta * top_obi(order_depth)`

## When OBI Helps vs Hurts

### Hurts (HYDROGEL) — Disabled

Phase 3 experiment showed OBI (β=11.2) is net-negative for HYDROGEL:
- −5,218 over 3 days vs no-OBI baseline
- Reason: mean-reversion dominates; OBI shifts quotes away from the reversion target, causing missed fills

### Neutral (Options) — Sub-Resolution

Phase 8 sweep: all 8 beta configs (±20% perturbations) produce identical PnL (146,415). OBI adjustment (~0.3–0.65 × OBI) is small vs passive_edge constants (0.35–1.3 ticks) → same price level quoted regardless of beta.

Conclusion: OBI is structurally live in production but PnL-neutral on this backtest dataset.

## Why OBI Can Be Misleading

The key trap: **statistical significance ≠ economic significance**. A t-stat of 38 tells you the coefficient is real (not noise). An R² of 0.125 tells you it explains 12.5% of price variance. But in a MM context, the relevant question is whether using OBI generates *better fills* — and for HYDROGEL, the answer is no.

## Comparison with Other Signals

| Signal | Used For | Status |
|--------|----------|--------|
| OBI | FV adjustment | Options: live (neutral). HYDROGEL: disabled |
| Mean reversion (AR1) | FV adjustment | HYDROGEL: active, +1,927 vs Phase 3 |
| IV z-score | Passive sizing bias | Options: live |
| Box-and-lines | Quoting size scaling | All: rejected (null result) |

## Links

[[Strategies/OBI_Signal]] · [[Products/HYDROGEL_PACK]] · [[Products/Options/VEV_5300]] · [[Research/Round3_Scripts]] · [[Backtests/Phase8_OBI_Sweep]]

---
type: strategy
tags: [round3, signal, microstructure, obi, calibrated]
sources: [rounds/round3/trader.py, backtests/phase3_obi_experiment.md, backtests/phase8_obi_sweep.md, .planning/STATE.md, report/report.tex §v7]
updated: 2026-04-27
---

# Order Book Imbalance (OBI) Signal

## What OBI Measures

Order Book Imbalance is a microstructure signal derived from the best bid and ask sizes:

```python
OBI = (bid_size - ask_size) / (bid_size + ask_size)    # ∈ [-1, +1]
```

- **OBI > 0:** More volume on the bid side → buying pressure → price likely to rise → shift our fair value up
- **OBI < 0:** More volume on the ask side → selling pressure → price likely to fall → shift our fair value down
- **OBI = 0:** Balanced book → no adjustment

**ML analogy:** OBI is an input feature to the fair value regression. It's a proxy for informed order flow — an order book skewed toward buyers suggests private information about upward price movement.

## Calibrated Betas (from microstructure_eda.py, ~9,000 ticks)

| Product | β | R² | t-stat | Notes |
|---------|---|----|--------|-------|
| HYDROGEL_PACK | **11.2** | 0.089 | 31.3 | Disabled in production (net-negative) |
| VELVETFRUIT_EXTRACT | 0.80 | 0.079 | 29.2 | Not used (passive hedge leg) |
| VEV_5300 | **0.65** | **0.125** | **37.7** | Active in production |
| VEV_5500 | 0.49 | 0.081 | 29.7 | Active in production |
| VEV_5200 | 0.64 | 0.082 | 29.9 | NOT used — bid-only strike, conservative 0.30 in code |
| VEV_5400 | 0.46 | 0.075 | 28.3 | Active in production |

Sign-match rates 0.78–0.98 at H=1 tick. All t-statistics ≥ 28 — statistically significant. R² 7–13% — small but real.

**VEV_5000/5100/5200 production config: β=0.30 (conservative)** — bid-only strikes with lower liquidity; calibrated EDA betas not used for these because they are structurally different (bid-hit asymmetry changes OBI interpretation).

---

## OBI for HYDROGEL — Disabled

Despite significant beta (11.2, t=31), OBI was **disabled** for HYDROGEL in production (`obi_beta=0.0`):

| Day | Without OBI (β=0) | With OBI (β=11.2) | Delta |
|-----|-------------------|-------------------|-------|
| 0 | 51,788 | 50,389 | **−1,399** |
| 1 | 46,978 | 47,175 | +197 |
| 2 | 41,982 | 37,966 | **−4,016** |
| Total | 140,748 | 135,530 | **−5,218** |

**Why OBI hurts despite significance:** The OBI overlay shifts quotes away from the mean-reversion target, causing missed fills during strong reversion moves. The anchor pull (anchor_w=0.20) earns more than OBI adjusts.

---

## v7 Microstructure Overlay — Catastrophic Full Deployment

Before the GSD phase system, a v7 trader was tested with full OBI deployment on all products simultaneously (calibrated betas everywhere). Result: **−14,487 regression vs v6 baseline (143,543 → 129,056)**:

| Product | v6 | v7 (full β) | Δ |
|---------|-----|-------------|---|
| HYDROGEL_PACK | 129,713 | 124,494 | **−5,219** |
| VELVETFRUIT_EXTRACT | −746 | −15,319 | **−14,573** |
| Voucher complex | 14,576 | 19,880 | **+5,304** |
| **Total** | **143,543** | **129,056** | **−14,487** |

**Root cause:** The voucher OBI *works* (+5.3K) — but the additional voucher trades it generates expand the option book's delta exposure. The VEV hedger then fires more often, paying the 5-tick spread on each cross. The cumulative slippage (−14.6K on VEV) dwarfs the voucher gain.

**v7b/v7c attempts (shrinkage):**
- v7b: HYDROGEL β halved to 5.5, VEV OBI off, vouchers kept → 135,936 (−7,607 vs v6)
- v7c: HYDROGEL β halved, all voucher OBI off → 143,065 (−478 vs v6)

**Verdict:** Even shrunk HYDROGEL OBI is marginally net-negative. The execution cost outweighs the captured edge. **Shipped as v6 with OBI infrastructure at defaults=0.**

---

## OBI for Options — Live but Sub-Resolution

OBI betas are active for VEV_5300/5400/5500 in production. Phase 8 sweep:
- All 8 beta configs (calibrated ± 20% perturbations) produce **identical 3-day PnL: 146,415**
- Root cause: The OBI adjustment term (β × OBI ≈ 0.30–0.65 × [−1,1]) is smaller than passive_edge constants (0.35–1.3). Discrete order-book price levels mean the same quotes fire regardless of the small OBI shift.

**Implication for live trading:** OBI may differentiate in live trading where the order book is noisier and tick frequency is lower (OBI has more time to matter before the next tick).

---

## Production Implementation

```python
def top_obi(order_depth: OrderDepth) -> float:
    best_bid = max(order_depth.buy_orders.keys())
    best_ask = min(order_depth.sell_orders.keys())
    bid_vol = order_depth.buy_orders[best_bid]
    ask_vol = -order_depth.sell_orders[best_ask]   # stored negative
    total = bid_vol + ask_vol
    return (bid_vol - ask_vol) / total if total > 0 else 0.0

# Applied as:
fair += obi_beta * top_obi(order_depth)
```

---

## Links

[[Concepts/Order_Book_Imbalance]] · [[Products/HYDROGEL_PACK]] · [[Products/Options/VEV_5300]] · [[Backtests/Phase8_OBI_Sweep]] · [[Research/Round3_Scripts]] · [[Research/Decisions_Log]]

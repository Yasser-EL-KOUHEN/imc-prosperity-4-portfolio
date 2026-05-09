---
type: concept
tags: [statistics, ar1, autocorrelation, mean-reversion, random-walk, round3, round5]
sources:
  - round5/research/eda.py (ar1_rho function, ar1_rho_mean column)
  - round3/research/hydrogel_audit.py
  - report/report.tex (§Short-Term Returns: AR(1) Structure; §Tutorial TOMATOES)
updated: 2026-05-06
---

# AR(1) Process — Autoregressive Model for Price Returns

## Definition

An **AR(1)** (first-order autoregressive) model for price returns says:

$$r_t = \phi \cdot r_{t-1} + \varepsilon_t, \qquad \varepsilon_t \sim \text{i.i.d.}(0, \sigma^2)$$

where $r_t = m_t - m_{t-1}$ is the tick-level mid-price return and $\phi$ is the **lag-1 autocorrelation coefficient**.

The model has two qualitatively different regimes:

| $\phi$ | Name | Implication |
|---|---|---|
| $\phi < 0$ | **Mean-reverting** | Last tick's up-move predicts a down-move; price oscillates around a level |
| $\phi \approx 0$ | **IID** | No predictability from last tick |
| $\phi \approx +1$ | **Near-unit-root / random walk with drift** | Price has strong momentum; each move persists |
| $\phi = +1$ | **Unit root** (random walk) | Price is non-stationary; no long-run mean to revert to |

## The Critical R3 vs R5 Contrast

| Product / round | $\hat\phi$ | Regime | Strategy implication |
|---|---|---|---|
| TOMATOES (Tutorial) | −0.413 | Mean-reverting | AR(1)-corrected fair value; tick-level alpha |
| HYDROGEL_PACK (R3) | −0.495 | Strong mean-reversion | Passive MM around EMA; AR(1) FV correction critical |
| **All 50 R5 products** | **≈ +0.999** | **Near-unit root** | No tick-level mean-reversion; directional hold only |

The R5 EDA (`round5/research/eda.py`) computes `ar1_rho_mean` per product across the 3 training days. The mean across all 50 products is ≈ 0.999. **This single number explains the entire R5 strategy architecture.**

## Why ≈ 0.999 Rules Out Market Making

In a standard MM strategy, the alpha source is **lag-1 mean reversion**: when the price goes up 1 tick, you shade your fair value estimate down (because $\hat\phi < 0$) and your bid is cheaper / ask is more aggressive. With $\hat\phi \approx +0.999$, this FV correction operates in the **wrong direction**: it would shade your estimate up on an up-move, making you buy when prices are rising (chasing) and sell when they're falling (fleeing).

Alternatively, with $\hat\phi \approx 0$ you'd disable the correction and run symmetric quotes — but then adverse selection wipes you out on the products with strong one-directional counterparties.

The only profitable tick-level strategy for a near-unit-root process with a directional drift is to **hold a position in the direction of the drift and let the drift accumulate**. This is Directional Holding.

## Why +0.999 ≠ Trend Following

A common confusion: "AR(1) ≈ 0.999 means strong positive autocorrelation → trend follow per-tick." But:

- At AR(1) = 0.999, the **lag-1 autocorrelation of returns** is 0.999, meaning each return is almost identical to the previous one — prices move at nearly constant velocity.
- Over 1M ticks this means price just walks steadily in one direction per day. It's a very slow drift, not a trend you can trade per-tick.
- The **signal-to-noise ratio per tick** is: $\phi / \sqrt{1 - \phi^2} \approx 22$ for $\phi = 0.999$ — but the signal magnitude (drift per tick) is tiny (~0.001 ticks/tick). You need to hold for 100K+ ticks to see it accumulate.
- **Position limit = ±10** amplifies this: hold ±10 × (full-day drift) instead of trying to turn over N times at ±1.

## Formal Test: Augmented Dickey-Fuller

The null hypothesis of a unit root ($H_0: \phi = 1$) is tested via the ADF statistic. For R5 products, the ADF test **fails to reject** the unit root null for nearly all 50 products. This is the statistical confirmation of "mean reversion is not exploitable here." `round5/research/eda.py` reports the ADF results alongside `ar1_rho_mean`.

For HYDROGEL (R3), the ADF strongly rejects the unit root — confirming stationary mean-reversion.

## ML Analogy

The AR(1) coefficient is directly analogous to the **momentum term** in SGD with momentum. The momentum hyperparameter $\beta$ controls how much the previous gradient update influences the current step — exactly like $\phi$ controlling how much the previous return influences the next.

- HYDROGEL ($\phi = -0.495$): momentum = −0.5 → the optimizer oscillates, correcting itself every step. Strong convergence to a fixed point (the fair value).
- R5 products ($\phi = +0.999$): momentum = +0.999 → the optimizer moves in nearly a straight line. Once momentum is established, it barely changes. The "fixed point" is infinite — there is none.

In sequence modelling terms: HYDROGEL is a **stationary time series** (mean-reverting AR(1)) while R5 products are **integrated time series** (near I(1)). The correct preprocessing for the former is level-stationarity (subtract the mean); for the latter it's differencing ($r_t = m_t - m_{t-1}$, which is I(0)).

## Practical Consequence for R5

```
if ar1_rho ≈ -0.5:  → Use passive MM with AR(1) FV correction (HYDROGEL style)
if ar1_rho ≈ +0.999: → Use directional hold at ±LIMIT (Directional Holding style)
if ar1_rho ≈ 0:     → Use symmetric MM without FV correction
```

v34's initial strategy for R5 assumed some products might have intermediate $\phi$ values and tested OBI/FV corrections — all found negligible effect (Phase 14 EDA Analysis A-E). The near-unit-root finding from Phase 13's initial EDA is the single diagnostic that short-circuits the entire exploratory tree.

## Links

[[Concepts/Adverse_Selection]] · [[Concepts/Market_Microstructure]] · [[Strategies/Directional_Holding]] · [[Strategies/Mean_Reversion]] · [[Strategies/market_making]] · [[Products/HYDROGEL_PACK]] · [[Backtests/Phase13_R5_Directional]] · [[Research/Round5_Scripts]]

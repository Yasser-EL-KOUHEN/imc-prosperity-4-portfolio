---
type: product
tags: [round4, manual, underlying, gbm, high-vol]
sources: [context/Round 4/Manual Challenge.txt, report/report.tex §Round 4 Manual]
updated: 2026-04-28
---

# AETHER_CRYSTAL — Manual Round 4 Underlying

**Round:** 4 (manual only) · **Type:** Spot · **Position limit:** ±200 · **Bid:** 49.975 · **Ask:** 50.025

## Description

> Aether Crystals (AETHER-CRYSTAL) are precision-grown minerals formed under controlled electromagnetic conditions. Each crystal stores and stabilizes ambient energy fluctuations, making them invaluable in advanced communication systems, architectural harmonics, and precision instrumentation.

## Simulation Specs

| Parameter | Value |
|---|---|
| Process | Geometric Brownian Motion |
| Risk-neutral drift | 0 |
| Annualised volatility σ | **2.51 (251%)** |
| Time grid | 4 steps per trading day |
| Trading days/year | 252 |
| Discrete-step σ | σ × √(1/(252×4)) = 0.0791 (~8% per step) |

## Time-to-Expiry Conversions

| Period | Days | Years | σ√T |
|---|---|---|---|
| 2 weeks | 10 | 0.03968 | 0.500 |
| 3 weeks | 15 | 0.05952 | 0.612 |

The 50% log-return std over 2 weeks is the central pricing driver: tails dominate. At 3 weeks, the price could realistically end anywhere in [25, 100].

## Trade Decision

**No trade.** The bid-ask spread (0.05) gives −0.025 edge either side. Portfolio delta is balanced via the call/put structure of the option positions; no need to hold the underlying for hedging.

## ML Analogy

GBM with σ=2.51 is functionally **a heavy-tailed prior over terminal price**. Black-Scholes for European-style payoffs computes the exact expectation under this prior. Discrete monitoring (4 steps/day) creates small deviations from continuous-time formulas only for path-dependent payoffs (e.g., the knock-out put).

## Links

[[Rounds/Round4_findings]] · [[Concepts/Black_Scholes]] · [[Strategies/Structural_Hedging]]

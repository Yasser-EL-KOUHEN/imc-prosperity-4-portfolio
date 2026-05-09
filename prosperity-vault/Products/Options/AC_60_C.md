---
type: product
tags: [round4, manual, vanilla-call, otm, skipped]
sources: [report/report.tex §Round 4 Manual]
updated: 2026-04-28
---

# AC_60_C — Vanilla Call, K=60, T=21d (Manual)

**Round:** 4 manual · **Strike:** 60 · **Expiry:** 3 weeks · **Bid:** 8.80 · **Ask:** 8.85 · **Volume cap:** 50

## Black-Scholes Fair Value (r=0)

S=50, K=60, σ=2.51, T=15/252:
- ln(50/60) = −0.182
- d₁ = 0.0084, d₂ = −0.604
- N(0.0084) = 0.5034, N(−0.604) = 0.273
- **C = 50 × 0.5034 − 60 × 0.273 = 8.796**

## Edges

| Action | Price | Edge |
|---|---|---|
| BUY | 8.85 | −0.054 |
| **SELL** | 8.80 | +0.004 |

## Portfolio Role

**No trade.** Despite a tiny +0.004 sell edge, selling this OTM call would create a **naked short call with unbounded loss**. With σ=2.51 and σ√T=0.612, the underlying could reach 100+ in 3 weeks. No available vanilla strike (K=60 is the highest) lets us cap the upside — so a short call here is a structurally uncovered tail bet.

The advisor principle "do not let the position control you" rules this out. The 0.004 edge per unit (max +0.2 pre-mul = 600 XIRECs) is nowhere near worth the unbounded tail.

## Links

[[Strategies/Structural_Hedging]]

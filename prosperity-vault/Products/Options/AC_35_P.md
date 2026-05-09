---
type: product
tags: [round4, manual, vanilla-put, otm, ko-hedge]
sources: [report/report.tex §Round 4 Manual]
updated: 2026-04-28
---

# AC_35_P — Vanilla Put, K=35, T=21d (Manual)

**Round:** 4 manual · **Strike:** 35 · **Expiry:** 3 weeks · **Bid:** 4.33 · **Ask:** 4.35 · **Volume cap:** 50

## Black-Scholes Fair Value (r=0)

S=50, K=35, σ=2.51, T=15/252:
- ln(50/35) = 0.357
- d₁ = 0.889, d₂ = 0.276
- N(0.889) = 0.813, N(0.276) = 0.609
- C = 50 × 0.813 − 35 × 0.609 = 19.355
- **P = C − S + K = 19.355 − 50 + 35 = 4.355**

## Edges

| Action | Price | Edge |
|---|---|---|
| BUY | 4.35 | +0.005 |
| SELL | 4.33 | −0.025 |

Essentially fair-priced. Buy-side is marginally positive.

## Portfolio Role

**BUY 50** — partial hedge for the AC_45_KO knockout scenario. When the KO put gets knocked out (path went below barrier 35), it pays 0; if subsequently S_T < 35, this P(K=35) provides offsetting payoff. Free hedge (~0 edge cost).

Coverage: only the (knockout AND S_T < 35) sub-region. Not a full hedge for the knockout cliff.

## Links

[[Products/Options/AC_45_KO]] · [[Concepts/Knockout_Option]] · [[Strategies/Structural_Hedging]]

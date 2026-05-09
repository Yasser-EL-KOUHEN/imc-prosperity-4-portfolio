---
type: product
tags: [round4, manual, vanilla-put, otm, downside-hedge]
sources: [report/report.tex §Round 4 Manual]
updated: 2026-04-28
---

# AC_45_P — Vanilla Put, K=45, T=21d (Manual)

**Round:** 4 manual · **Strike:** 45 · **Expiry:** 3 weeks · **Bid:** 9.05 · **Ask:** 9.10 · **Volume cap:** 50

## Black-Scholes Fair Value (r=0)

S=50, K=45, σ=2.51, T=15/252:
- ln(50/45) = 0.105
- d₁ = 0.478, d₂ = −0.134
- N(0.478) = 0.684, N(−0.134) = 0.447
- C = 50 × 0.684 − 45 × 0.447 = 14.085
- **P = C − S + K = 9.085**

## Edges

| Action | Price | Edge |
|---|---|---|
| BUY | 9.10 | −0.015 |
| SELL | 9.05 | −0.035 |

## Portfolio Role

**BUY 50** — general portfolio downside hedge. Below the binary-spread coverage zone (which pays 0 below S=40), P(K=45) provides linear protection in the (0, 45) range for:
- 2w call (loses cost if S_14 < 50)
- KO put (knockout loss bounded at premium)
- Chooser arb residual variance when S_T < S_14

Cost: −0.75 pre-mul. Insurance against down-tail scenarios.

## Links

[[Products/Options/AC_45_KO]] · [[Strategies/Structural_Hedging]]

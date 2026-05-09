---
type: product
tags: [round4, manual, vanilla-call, atm, 3w]
sources: [report/report.tex §Round 4 Manual]
updated: 2026-04-28
---

# AC_50_C — Vanilla Call, K=50, T=21d (Manual)

**Round:** 4 manual · **Strike:** 50 · **Expiry:** 3 weeks · **Bid:** 12.00 · **Ask:** 12.05 · **Volume cap:** 50

## Black-Scholes Fair Value (r=0)

For ATM call with σ=2.51, T=15/252:
- σ√T = 0.612
- d₁ = 0.306, d₂ = −0.306
- N(0.306) = 0.6203, N(−0.306) = 0.3797
- **C = 50 × (0.6203 − 0.3797) = 12.03**

## Edges

| Action | Price | Edge |
|---|---|---|
| BUY | 12.05 | −0.02 |
| SELL | 12.00 | −0.03 |

Both within bid-ask spread of fair → essentially **fair-priced**.

## Portfolio Role

**BUY 50** — used as the call leg of the chooser arbitrage replication: `Chooser(K=50, T=21) = C(K=50, 21d) + P(K=50, 14d)`. The −1.0 pre-mul cost is more than offset by the chooser's +0.30 sell edge.

## Links

[[Products/Options/AC_50_P]] · [[Products/Options/AC_50_CO]] · [[Concepts/Chooser_Option]] · [[Concepts/Black_Scholes]]

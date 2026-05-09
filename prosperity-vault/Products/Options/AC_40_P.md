---
type: product
tags: [round4, manual, vanilla-put, otm, binary-spread-leg]
sources: [report/report.tex §Round 4 Manual]
updated: 2026-04-28
---

# AC_40_P — Vanilla Put, K=40, T=21d (Manual)

**Round:** 4 manual · **Strike:** 40 · **Expiry:** 3 weeks · **Bid:** 6.50 · **Ask:** 6.55 · **Volume cap:** 50

## Black-Scholes Fair Value (r=0)

S=50, K=40, σ=2.51, T=15/252:
- ln(50/40) = 0.223
- d₁ = 0.671, d₂ = 0.058
- N(0.671) = 0.7488, N(0.058) = 0.5232
- C = 50 × 0.7488 − 40 × 0.5232 = 16.51
- **P = C − S + K = 16.51 − 50 + 40 = 6.506**

## Edges

| Action | Price | Edge |
|---|---|---|
| BUY | 6.55 | −0.044 |
| SELL | 6.50 | −0.006 |

## Portfolio Role

**SELL 50** — short leg of the **bull put spread** binary hedge. The combined position `Sell binary + Buy P50 + Sell P40` cancels the binary's −10 cliff at S=40, replacing it with a bounded tent payoff.

Contribution: −0.30 pre-mul (small cost) but enables a 9× variance reduction on the binary trade.

## Links

[[Products/Options/AC_40_BP]] · [[Products/Options/AC_50_P]] · [[Strategies/Structural_Hedging]] · [[Concepts/Binary_Option]]

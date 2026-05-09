---
type: product
tags: [round4, manual, vanilla-put, atm, 3w]
sources: [report/report.tex §Round 4 Manual]
updated: 2026-04-28
---

# AC_50_P — Vanilla Put, K=50, T=21d (Manual)

**Round:** 4 manual · **Strike:** 50 · **Expiry:** 3 weeks · **Bid:** 12.00 · **Ask:** 12.05 · **Volume cap:** 50

## Black-Scholes Fair Value (r=0)

By put-call parity (r=0): **P = C = 12.03** at ATM.

## Edges

| Action | Price | Edge |
|---|---|---|
| BUY | 12.05 | −0.02 |
| SELL | 12.00 | −0.03 |

Fair-priced.

## Portfolio Role

**BUY 50** — long leg of the **bull put spread** that hedges the binary cliff. Combined with `SELL 50 AC_40_P` and `SELL 50 AC_40_BP`, the joint position pays a tent payoff with maximum loss bounded at −0.55/pair (vs −5/pair for naked binary).

The combined per-unit-pair payoff:
```
S > 50:   0
40 < S < 50:  50 - S    (ramp 0 → 10)
S < 40:   0    (binary loss exactly cancelled by spread)
```

## Links

[[Products/Options/AC_40_P]] · [[Products/Options/AC_40_BP]] · [[Strategies/Structural_Hedging]] · [[Concepts/Binary_Option]]

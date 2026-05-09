---
type: product
tags: [round4, manual, exotic, binary, digital, hedged]
sources: [report/report.tex §Round 4 Manual, Concepts/Binary_Option]
updated: 2026-04-28
---

# AC_40_BP — Binary Put, K=40, payout 10, T=21d

**Round:** 4 manual · **Strike:** 40 · **Payout:** 10 · **Expiry:** 3 weeks · **Bid:** 5.00 · **Ask:** 5.10 · **Volume cap:** 50

## Mechanism

Pays 10 if S_T < 40 at expiry, else 0. Pure European-style payoff (no path dependency).

## Black-Scholes Fair Value (r=0)

For GBM with r=0:

$$\mathbb{P}(S_T < K) = N\!\left(\frac{\ln(K/S_0) - \frac{1}{2}\sigma^2 T}{\sigma\sqrt T}\right) = N(-d_2^{\text{call}})$$

For K=40: d₂ = (ln(50/40) − 0.187) / 0.612 = 0.058
- P(S_T < 40) = N(−0.058) = **0.4768**
- **E[payoff] = 10 × 0.4768 = 4.768**

## Edges

| Action | Price | Edge |
|---|---|---|
| BUY | 5.10 | −0.33 |
| **SELL** | 5.00 | **+0.232** ✓ |

## Portfolio Role

**SELL 50** — overpriced by ~5%. The naked sell would have:
- E[PnL] = +11.6 pre-mul
- Worst case = −250 pre-mul (50 × −5 if all hit)
- Sharpe = ~0.46 single-sim, ~4.6 with 100-sim averaging

### Structural Hedge

Following the advisor's binary guidance, we overlay a **bull put spread** (long P50, short P40):

| S_T | Combined payoff (binary + spread) | Per-pair PnL (cash −0.55) |
|---|---|---|
| > 50 | 0 | −0.55 |
| 40 < S < 50 | 50 − S (ramp 0 → 10) | (50−S) − 0.55 |
| 40 (boundary) | 10 | +9.45 |
| < 40 | 0 (binary cancelled by spread) | −0.55 |

Maximum loss collapses from −5/unit (naked) to −0.55/pair (hedged) — **9× variance reduction** at +0.026 edge cost per pair.

Net contribution: **+10.3 pre-mul** with bounded downside.

## Links

[[Products/Options/AC_50_P]] · [[Products/Options/AC_40_P]] · [[Concepts/Binary_Option]] · [[Strategies/Structural_Hedging]]

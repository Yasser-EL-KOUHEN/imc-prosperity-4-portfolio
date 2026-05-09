---
type: product
tags: [round4, manual, exotic, chooser, arbitrage, primary-edge]
sources: [report/report.tex §Round 4 Manual, Concepts/Chooser_Option]
updated: 2026-04-28
---

# AC_50_CO — Chooser Option, K=50, T=21d (choice at T+14)

**Round:** 4 manual · **Strike:** 50 · **Expiry:** 3 weeks · **Choice time:** 2 weeks · **Bid:** 22.20 · **Ask:** 22.30 · **Volume cap:** 50

## Mechanism

> After 14 Solvenarian Days, the buyer chooses the side (PUT or CALL). At that point, the contract automatically converts to the side that is "in the money". After the remaining 7 Solvenarian Days, the contract expires like a standard PUT or CALL option.

## Black-Scholes Fair Value (r=0)

For r=0, by put-call parity at the choice time, the chooser admits a **static replication**:

$$\text{Chooser}_0 = C(K, T_{\text{expiry}}, S_0) + P(K, T_{\text{choice}}, S_0)$$

For our case (K=50, T=21d, T_c=14d, S_0=50, σ=2.51):
- C(K=50, 21d) = 12.03 (from [[AC_50_C]])
- P(K=50, 14d) = 9.87 (from [[AC_50_P_2]])
- **Chooser₀ = 12.03 + 9.87 = 21.90**

See [[Concepts/Chooser_Option]] for the derivation.

## Edges

| Action | Price | Edge |
|---|---|---|
| BUY | 22.30 | −0.40 |
| **SELL** | 22.20 | **+0.30** ✓ |

The chooser is **overpriced by 0.30**. Selling captures the market's overestimation of the chooser's "flexibility premium".

## Portfolio Role

**SELL 50** — main exotic trade. Combined with the replicating legs (BUY 50 AC_50_C + BUY 50 AC_50_P_2), the structure provides:

- Edge per unit: +0.30 (chooser) − 0.02 (call leg) + 0.121 (put leg) = **+0.40**
- Total: **+20.05 pre-mul = +60,150 XIRECs**

### Residual Variance

The replication is exact in **expectation** but not pathwise. The chooser pays only at T=21; the replication pays max(50-S_14, 0) at T=14 then max(S_21-50, 0) at T=21. Pathwise residual:

$$R = (S_T - S_{T_c}) \cdot \mathbf{1}\{S_{T_c} < 50\}, \qquad \mathbb{E}[R] = 0$$

by the Q-martingale property. Per-unit residual std ≈ 11.8.

## Links

[[Products/Options/AC_50_C]] · [[Products/Options/AC_50_P_2]] · [[Concepts/Chooser_Option]] · [[Concepts/Black_Scholes]] · [[Strategies/Structural_Hedging]]

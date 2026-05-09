---
type: concept
tags: [exotic, chooser, replication, put-call-parity, arbitrage]
sources: [report/report.tex §Chooser, Hull §26.8]
updated: 2026-04-28
---

# Chooser Option

## Definition

A chooser option lets the holder choose at time $T_c$ (the **choice time**, $T_c < T$) whether the contract becomes a vanilla call or a vanilla put with strike $K$ and remaining maturity $T - T_c$.

If the contract specifies "in-the-money" choice (most common), the holder picks the side that has positive intrinsic value at $T_c$.

## Static Replication for r=0

For zero risk-free rate (or more generally when interest rates are zero in the risk-neutral measure), the chooser admits an exact static replication using two vanilla options:

$$\boxed{\text{Chooser}_0 = C(K, T, S_0) + P(K, T_c, S_0)}$$

That is: a 3-week chooser with 2-week choice time = a 3-week vanilla call **plus** a 2-week vanilla put (both at the same strike).

### Derivation

At $T_c$, the holder's decision value is $\max(C_{T_c}, P_{T_c})$. By put-call parity for r=0:
$$C_{T_c} - P_{T_c} = S_{T_c} - K$$

So:
- $S_{T_c} > K$: $C_{T_c} > P_{T_c}$ → choose call → value = $C_{T_c}$
- $S_{T_c} < K$: $C_{T_c} < P_{T_c}$ → choose put → value = $P_{T_c} = C_{T_c} + (K - S_{T_c})$

Both cases unify as:
$$V_{T_c} = C_{T_c} + \max(K - S_{T_c}, 0)$$

Taking expectations at $t=0$ under $\mathbb{Q}$ (using the tower property for the call):
$$\text{Chooser}_0 = \mathbb{E}^\mathbb{Q}[C_{T_c}] + \mathbb{E}^\mathbb{Q}[\max(K - S_{T_c}, 0)] = C(K, T, S_0) + P(K, T_c, S_0)$$

The first term is the price-now of the underlying call; the second is a vanilla European put expiring at $T_c$.

## Pathwise Replication Residual

The replication matches **expected value** but **not pathwise cashflows**:

| | Chooser | Replication |
|---|---|---|
| Cashflow at $T_c$ | None | $\max(K - S_{T_c}, 0)$ |
| Cashflow at $T$ | depends on choice | $\max(S_T - K, 0)$ |

Net residual at expiry per unit of "sell chooser + buy replication":

$$R = (S_T - S_{T_c}) \cdot \mathbf{1}\{S_{T_c} < K\}$$

By the $\mathbb{Q}$-martingale property, $\mathbb{E}[R] = 0$. Conditional variance:
$$\text{Var}(R \mid S_{T_c}, S_{T_c} < K) = S_{T_c}^2 (e^{\sigma^2 (T - T_c)} - 1)$$

This residual variance is the **cost of pseudo-arbitrage** — the chooser arb captures expected edge but is not riskless pathwise.

## Application in Round 4 Manual

For AC_50_CO (K=50, T=21d, T_c=14d, σ=2.51, r=0):
- C(K=50, 21d) = 12.03
- P(K=50, 14d) = 9.87
- **Chooser fair = 21.90**
- Market sell at 22.20 → edge **+0.30/unit**

See [[Products/Options/AC_50_CO]] for portfolio sizing.

## ML Analogy

The chooser packages a **non-trivial decision rule** (pick the higher-value leg at $T_c$). Replicating it with two simpler vanilla "base learners" is analogous to **ensemble distillation** in ML — capturing the same expected output with a simpler model. The market's overpricing of the chooser corresponds to overestimating the value of the ensemble's decision flexibility.

## Links

[[Products/Options/AC_50_CO]] · [[Concepts/Black_Scholes]] · [[Strategies/Structural_Hedging]]

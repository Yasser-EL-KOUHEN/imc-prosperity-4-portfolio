---
type: strategy
tags: [round4, manual, hedging, exotic, replication, advisor-principle]
sources: [report/report.tex §Round 4 Manual, advisor advice on exotics]
updated: 2026-04-28
---

# Structural Hedging for Discontinuous Payoffs

## The Principle

> "When payoffs are discontinuous, risk management becomes structural rather than occasional. Structure your risk accordingly."
> — Round 4 advisor (Rook-E1)

> "A carefully constructed vanilla position can soften the abrupt payoff cliff of the binary. It can provide a buffer against the knock-out trigger before it becomes an irreversible outcome."

The core idea: **don't manage exotic risk after the fact**. Layer vanilla options at the same time you take the exotic, so that the combined position has a **predictable, bounded payoff** under all paths — not just under expected scenarios.

## Three Common Exotic Risks and Their Structural Hedges

### 1. Binary Cliff → Bull Put Spread Overlay

**Problem:** Selling a binary put creates a $-A$ cliff at the strike. A small unfavourable move triggers the full liability.

**Structural fix:** Add a bull put spread at the same strike (long P at strike, short P at lower strike covering payout):

```
Sell binary(K=40, A=10) + Buy P(K=50) + Sell P(K=40)
```

The combined payoff:
- $S_T > 50$: 0 (cash cost only)
- $40 < S_T < 50$: $50 - S_T$ (positive ramp)
- $S_T < 40$: $0$ (cliff cancelled)

Maximum loss collapses from $-A$ per unit (naked) to the **net cash cost of the spread** (≈ $-0.55$/pair in our case). 9× variance reduction.

See [[Concepts/Binary_Option]] for derivation.

### 2. Chooser Flexibility Premium → Static Replication

**Problem:** A chooser bundles call + put optionality. Markets often overprice this "flexibility".

**Structural fix:** For r=0, replicate exactly with two vanillas:
$$\text{Chooser}(K, T, T_c) = C(K, T) + P(K, T_c)$$

Selling the chooser and buying the replication legs locks in any overprice as a static arbitrage. Residual variance comes only from cashflow timing mismatch (zero in expectation by martingale property).

See [[Concepts/Chooser_Option]] for derivation.

### 3. Knockout Path Dependence → Premium Cap

**Problem:** A knockout option's value can vanish before resolution if the path touches the barrier — even if the path returns to favourable territory afterward.

**Structural mitigations:**
- **Buy** instead of sell — your maximum loss is bounded by the premium paid (no path-dependent obligation).
- Add a vanilla put at the barrier strike — provides offsetting payoff in the (knockout AND $S_T <$ barrier) sub-region. Not a complete hedge but reduces the "knockout AND end-deep-OTM" loss component.

See [[Concepts/Knockout_Option]] for the closed-form valuation.

## Generic Recipe

For any new exotic, before sizing the trade:

1. **Plot the payoff** as a function of $S_T$ (and any path-dependent variable).
2. **Identify the discontinuities** — cliffs, kinks, knockouts.
3. **Find the smallest vanilla portfolio** that, when combined with the exotic, **smooths or eliminates** each discontinuity.
4. **Compute the combined PnL** in the worst-case scenario for each region. If unbounded, abandon the trade or reduce size.
5. **Check the edge after hedging** — sometimes the hedge cost eats more than the exotic edge.

## Applied in Round 4 Manual

| Exotic | Structural hedge | Edge after hedge | Variance reduction |
|---|---|---|---|
| AC_50_CO sell (chooser) | Buy C(21d) + Buy P(14d) (replication) | +0.40/unit (vs +0.30 naked) | Large (most variance eliminated) |
| AC_40_BP sell (binary) | Buy P50 + Sell P40 (bull spread) | +0.206/pair (vs +0.232 naked) | 9× (worst case −0.55 vs −5) |
| AC_45_KO buy (knockout) | Buy P35 (partial knockout hedge) | +0.045/unit (free hedge) | Moderate (covers the deepest tail) |

Total portfolio: **+58.4 pre-mul = +175,200 XIRECs** with **bounded downside on every position**.

## What Structural Hedging Is NOT

Structural hedging is **not delta hedging** — that's continuous risk management as the underlying moves. Structural hedging is **one-shot at trade initiation**: you build the hedge structure once and hold to expiry. It's appropriate when:
- You can't trade dynamically (manual challenge in Round 4)
- The discontinuities are at known levels (strikes, barriers)
- Vanilla strikes are available near the exotic's discontinuity points

When discontinuities are at non-traded levels, you accept residual cliff risk or reduce position size.

## ML Analogy

Structural hedging is **ensemble regularisation**: combine the high-variance "specialist" (the exotic) with simpler base learners (vanillas) chosen so that the combination has a **smoother loss surface**. The advisor's principle "don't let the position control you" maps to **bounding model gradients** — preferring a model whose worst-case behaviour is predictable, even if average performance is slightly lower.

## Links

[[Concepts/Chooser_Option]] · [[Concepts/Binary_Option]] · [[Concepts/Knockout_Option]] · [[Strategies/Delta_Hedging]] · [[Rounds/Round4_findings]]

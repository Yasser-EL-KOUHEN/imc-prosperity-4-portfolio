---
type: concept
tags: [exotic, binary, digital, cliff, discontinuous-payoff]
sources: [report/report.tex §Binary Put, Hull §26.5]
updated: 2026-04-28
---

# Binary (Digital) Option

## Definition

A binary option pays a **fixed amount** if a condition on the underlying is met at expiry, and zero otherwise.

| Type | Payoff |
|---|---|
| Cash-or-nothing call | $A$ if $S_T > K$, else 0 |
| Cash-or-nothing put | $A$ if $S_T < K$, else 0 |

## Black-Scholes Pricing (r=0)

Under risk-neutral GBM:
$$\text{Cash-or-nothing put price} = A \cdot \mathbb{P}(S_T < K) = A \cdot N(-d_2)$$
where $d_2 = \frac{\ln(S/K) - \frac{1}{2}\sigma^2 T}{\sigma\sqrt T}$ (with r=0).

Equivalently: a binary is the **derivative of a vanilla** with respect to strike. A digital paying $\$1$ ≈ tightest possible put spread divided by spread width.

## The Cliff Risk

The binary's defining feature is its **discontinuous payoff at the strike**: above $K$, zero; below $K$, the full payout $A$. Plotted, this is a step function, not a smooth ramp.

The discontinuity creates a fundamentally different risk profile from a vanilla:
- A vanilla put's loss is gradient-distributed across price levels
- A binary put's loss is **concentrated entirely at one threshold**

For a seller, this means: a small unfavourable move that crosses the threshold triggers the full liability; a large favourable move provides only the upfront premium.

## Vertical Spread Replication (Approximate)

A digital paying $\$A$ at strike $K$ can be approximated by a put spread:
$$\text{Digital}(K, A) \approx \tfrac{A}{\Delta} \cdot \big[P(K) - P(K - \Delta)\big]$$

The approximation pays $A$ for $S < K - \Delta$, ramps linearly between $K - \Delta$ and $K$, and pays 0 above $K$. As $\Delta \to 0$, the spread converges to the digital.

In Round 4 manual we have $\Delta = 5$ (strikes 35, 40), making the spread coarse but usable.

## Application in Round 4 Manual: Cliff Elimination

AC_40_BP pays 10 if $S_T < 40$. To **eliminate the cliff** for a short binary position, layer a bull put spread (long P50, short P40):

| $S_T$ region | Binary obligation (short) | P50 long | P40 short | Combined |
|---|---|---|---|---|
| $> 50$ | 0 | 0 | 0 | **0** |
| $40 < S < 50$ | 0 | $50 - S$ | 0 | $50 - S$ (ramp 0→10) |
| $S = 40$ | 0 | 10 | 0 | **10** |
| $< 40$ | $-10$ | $50 - S$ | $-(40 - S)$ | $-10 + 10 = $ **0** |

The binary's $-10$ cliff is **exactly cancelled** by the spread's $+10$ payoff below 40. The combined position pays a tent peaking at $S = 40$ (height 10) and is bounded below by 0.

**Effect on portfolio risk:** Maximum loss collapses from $-5$/unit (naked short binary) to $-0.55$/pair (spread cash cost) — a 9× variance reduction at +0.026 edge cost per pair.

See [[Strategies/Structural_Hedging]] and [[Products/Options/AC_40_BP]].

## ML Analogy

A binary payoff is a **step-function classifier**: above threshold, one class; below, another. Sharp decision boundary = high variance under perturbation. The vertical spread overlay is the analogue of **temperature softening / Platt scaling**: replace the step with a calibrated ramp, preserving the expected probability output but smoothing the gradient.

## Links

[[Products/Options/AC_40_BP]] · [[Strategies/Structural_Hedging]] · [[Concepts/Black_Scholes]]

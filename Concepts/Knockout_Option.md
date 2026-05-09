---
type: concept
tags: [exotic, barrier, knockout, path-dependent, broadie-glasserman]
sources: [report/report.tex §KO, Hull §26.9, Broadie-Glasserman 1997]
updated: 2026-04-28
---

# Knock-Out (Barrier) Option

## Definition

A knock-out option behaves like its vanilla counterpart **unless the underlying touches a barrier $H$ during the life of the option**, in which case it immediately becomes worthless.

| Variant | Active when | Knocked out if |
|---|---|---|
| **Down-and-out put (DOP)** | $S$ stays above $H < S_0$ | $\min_{t \leq T} S_t \leq H$ |
| Down-and-out call (DOC) | $S$ stays above $H < S_0$ | $\min_{t \leq T} S_t \leq H$ |
| Up-and-out put (UOP) | $S$ stays below $H > S_0$ | $\max_{t \leq T} S_t \geq H$ |
| Up-and-out call (UOC) | $S$ stays below $H > S_0$ | $\max_{t \leq T} S_t \geq H$ |

## Closed-Form Pricing (Continuous Monitoring, r=0)

For a down-and-out put with $K > H$, $S > H$, $r = q = 0$:

$$\text{DOP} = P(K) - \text{DIP}(K, H)$$

where the down-and-in put (DIP) is given by:

$$\text{DIP} = -S \cdot N(-x_1) + K \cdot N(-x_1 + \sigma\sqrt T) + S \cdot \left(\tfrac{H}{S}\right)^{2\lambda} [N(y) - N(y_1)] - K \cdot \left(\tfrac{H}{S}\right)^{2\lambda - 2} [N(y - \sigma\sqrt T) - N(y_1 - \sigma\sqrt T)]$$

with:
- $\lambda = (r + \sigma^2/2)/\sigma^2 = 0.5$ for $r = 0$
- $x_1 = \ln(S/H)/(\sigma\sqrt T) + \lambda \sigma\sqrt T$
- $y = \ln(H^2/(SK))/(\sigma\sqrt T) + \lambda \sigma\sqrt T$
- $y_1 = \ln(H/S)/(\sigma\sqrt T) + \lambda \sigma\sqrt T$

## Probability of No Breach (Useful Sanity Check)

For arithmetic Brownian motion $X_t = \mu t + \sigma W_t$ with $\mu = -\sigma^2/2$ (the drift of $\ln S$ under r=0 GBM) and $b = \ln(H/S_0) < 0$:

$$\mathbb{P}\big(\min_{0 \leq t \leq T} X_t > b\big) = N\!\left(\frac{-b + \mu T}{\sigma\sqrt T}\right) - e^{2\mu b/\sigma^2} \cdot N\!\left(\frac{b + \mu T}{\sigma\sqrt T}\right)$$

Use this to gut-check whether a barrier is "easy" or "hard" to hit relative to the option's life.

## Discrete Monitoring Correction (Broadie–Glasserman)

The closed-form DOP assumes **continuous monitoring** of the barrier. In practice (and in Prosperity), the barrier is checked only at a finite set of times. The discrete monitoring **overestimates the option's value** vs continuous (fewer chances to breach).

**Broadie–Glasserman (1997) correction:** Shift the effective barrier by:
$$H_{\text{eff}} = H \cdot \exp(\beta \cdot \sigma \sqrt{\Delta t})$$
where $\beta \approx -0.5826$ for a down barrier (lowering the effective barrier compensates for the discrete monitoring's under-detection of breaches).

For Round 4 KO at $\Delta t = 1/(252 \cdot 4)$:
- $\sigma\sqrt{\Delta t} = 0.0791$
- Shift factor: $\exp(-0.5826 \cdot 0.0791) = 0.955$
- $H_{\text{eff}} = 35 \cdot 0.955 = 33.4$

Replace $H$ with $H_{\text{eff}}$ in the closed-form formula to get the discrete-monitoring price.

## Application in Round 4 Manual: AC_45_KO

K=45, H=35, T=21d, σ=2.51:
- P(no breach, continuous) = 0.342
- DOP_continuous ≈ 0.12
- DOP with H_eff = 33.4 ≈ **0.22**
- Market: bid 0.15, ask 0.175 → buy edge **+0.045**

The fair value is model-dependent; my estimate carries ±50% uncertainty due to the discrete-correction approximation. **Maximum loss is bounded by the premium paid** (0.175 × 500 = 87.5 pre-mul), so even if the edge is wrong, the downside is contained.

See [[Products/Options/AC_45_KO]].

## ML Analogy

A knock-out option is a **path-dependent classifier with early stopping**: the entire sample (path) is invalidated if it crosses a threshold at any monitoring point. This makes the option's value sensitive to **sampling frequency** (continuous vs discrete), analogous to how validation-loss-checkpointed training can give different stopping points depending on validation interval.

## Links

[[Products/Options/AC_45_KO]] · [[Strategies/Structural_Hedging]] · [[Concepts/Black_Scholes]]

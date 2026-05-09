---
type: product
tags: [round4, manual, exotic, knockout, barrier, path-dependent]
sources: [report/report.tex §Round 4 Manual, Concepts/Knockout_Option]
updated: 2026-04-28
---

# AC_45_KO — Knock-Out Put, K=45, Barrier 35, T=21d

**Round:** 4 manual · **Strike:** 45 · **Barrier:** 35 · **Expiry:** 3 weeks · **Bid:** 0.15 · **Ask:** 0.175 · **Volume cap:** 500

## Mechanism

Behaves like a vanilla put at K=45 unless the underlying ever trades **below 35** at any of the 60 discrete monitoring points. If the barrier is breached at any point, the option immediately becomes worthless.

## Black-Scholes Fair Value (r=0)

Using the Merton down-and-out put formula with λ = (r + σ²/2)/σ² = 0.5:

$$\text{DOP} = P(K) - \text{DIP}(K, H)$$

**Probability of no breach** (continuous monitoring) for ABM running min with μ = −σ²/2 = −3.15, b = ln(35/50) = −0.357:

$$\mathbb{P}(\min S_t > H) = N\!\left(\tfrac{-b + \mu T}{\sigma\sqrt T}\right) - e^{2\mu b/\sigma^2} N\!\left(\tfrac{b + \mu T}{\sigma\sqrt T}\right) = 0.342$$

**Discrete monitoring correction (Broadie–Glasserman):** With 60 monitoring points, σ√Δt = 0.0791. Effective barrier shift:
$$H_{\text{eff}} = H \cdot \exp(-0.5826 \cdot \sigma\sqrt{\Delta t}) = 35 \cdot 0.955 = 33.4$$

Recomputed DOP with H_eff = 33.4: **DOP ≈ 0.22** (model-dependent estimate).

## Edges

| Action | Price | Edge (model-dependent) |
|---|---|---|
| **BUY** | 0.175 | **+0.045** ✓ |
| SELL | 0.15 | −0.07 |

## Portfolio Role

**BUY 500** (max volume) — underpriced by ~25% if my model is correct.

### Risk Profile

- Expected: **+22.5 pre-mul = +67,500 XIRECs**
- Maximum loss: 500 × 0.175 = 87.5 pre-mul = −262,500 XIRECs (entire premium burnt if knockout occurs)
- Probability of knockout: ~66% (1 − 0.342 survival)

The maximum loss is **bounded by the premium paid**, so even if my fair value is wrong by 50%, the downside is contained. Take full volume.

### Partial Hedge

Long P(K=35) provides offsetting payoff in the (knockout AND S_T < 35) sub-region. See [[AC_35_P]].

## Links

[[Products/Options/AC_35_P]] · [[Products/Options/AC_45_P]] · [[Concepts/Knockout_Option]] · [[Strategies/Structural_Hedging]]

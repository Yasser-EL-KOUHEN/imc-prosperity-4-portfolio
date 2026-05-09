---
type: manual
tags: [round2, manual, optimization, allocation, log-linear-rank, grid-search]
sources:
  - report/report.tex (§Round 2 Part C: Manual Invest & Expand optimization)
  - context/Round 2/# Round 2 - "Growing Your Outpost".txt
updated: 2026-05-06
---

# Round 2 Manual — "Invest & Expand"

**Submitted (final):** $(x_R, x_S, x_V) = (18, 60, 22)$ · **Realized: +153,345** · **Method:** Exhaustive integer grid search + multi-prior sensitivity → bottom-heavy-tilt allocation

**Pillar naming:** the third pillar's official Prosperity label is **Speed** (not "Visibility" as some earlier vault references used). Always cite as Speed.

> **Verified result (Prosperity result page, 2026-05-08):** **+153,345 realized**.
>
> **Pillar-by-pillar Prosperity-reported breakdown:**
> - Research (logarithmic): 18% invested → Strategy XIRECs **127,600**
> - Scale (linear): 60% invested → Multiplier **×4.2**
> - Speed (rank-based): 22% invested → Hit rate **0.38** with rank **#2,801**
> - Subtotal: 127,600 × 4.2 × 0.38 ≈ 203,345
> - Budget: −50,000 → **Net P&L = +153,345**
>
> **Realized V(22) = 0.38**, between uniform-rank (0.276) and bottom-heavy (0.900) — peer-prior was meaningfully bottom-heavy as anticipated. Submitting (18, 60, 22) over the FOC (16, 48, 36) **over-performed the FOC theoretical** by **+43,280**.
>
> **Speed-investment peer distribution** (`performance/manual trading/round 2/Distribution Speed Competitors/`): a large mode at 0% (~450 teams, non-investors), the densest single bucket at **22%** (~600 teams — exactly where we sat), with secondary modes at 10%, 30%, 35–40%, 50%. Rank #2,801 reflects the ~2,800 teams below us in the rank-based Speed scoring. End-of-R2 cumulative manual rank #801.

## The Mechanic

Allocate percentages $(x_R, x_S, x_V) \in [0, 100]$ with $x_R + x_S + x_V \leq 100$ across three pillars. Budget cost = $500 \times (x_R + x_S + x_V)$.

**Pillar reward functions:**

| Pillar | Symbol | Functional form | Shape |
|---|---|---|---|
| Research | $R(x)$ | $200{,}000 \times \ln(1+x)/\ln(101)$ | Log, saturates at 200K at $x=100$ |
| Scale | $S(x)$ | $0.07 \, x$ | Linear, maximum 7 at $x=100$ |
| Visibility | $V(x)$ | Rank-based multiplier $\in [0.1, 0.9]$ | Competitive; depends on peer allocations |

**Objective:**
$$\max_{x_R, x_S, x_V} \; R(x_R) \cdot S(x_S) \cdot V(x_V) - 500(x_R + x_S + x_V)$$

## Structural Properties

Three qualitatively different shapes drive the allocation:
- **Research (log):** High marginal return early (first few % very valuable), rapidly diminishing — never allocate beyond ~20.
- **Scale (linear):** Constant marginal return — allocate as much as leftover budget allows.
- **Visibility (rank-based):** Competitive; your percentile rank among all players determines $V$. Unknown before submission.

The **full-budget constraint binds**: partial allocations ($x_R + x_S + x_V < 100$) are strictly worse because $S$ is linear with positive slope — adding more $x_S$ always pays $0.07 \times$ the marginal product $R \times V > 0$.

## Solution Under Uniform-Rank Prior

If peer $x_V$ allocations are uniformly distributed on $[0, 100]$, a rank proxy is $V(x) \approx 0.1 + 0.008 \, x$.

**Exhaustive integer grid search** over all $(x_R, x_S, x_V)$ with $\sum = 100$:

$$\boxed{x_R = 16, \quad x_S = 48, \quad x_V = 36, \quad \text{PnL} = 110{,}065 \text{ XIREC}}$$

## First-Order Intuition

At the interior optimum, marginal returns per dollar equalize across all pillars:

$$\partial_{x_R}:\; \frac{43{,}337}{1+x_R} \cdot S(x_S) \cdot V(x_V) = 500$$
$$\partial_{x_S}:\; 0.07 \cdot R(x_R) \cdot V(x_V) = 500$$
$$\partial_{x_V}:\; 0.008 \cdot R(x_R) \cdot S(x_S) = 500$$

Solving numerically (without discretization): $x_V \approx 35.7$, $x_R \approx 16.1$, $x_S \approx 48.2$. The grid search answer $(16, 48, 36)$ matches to within rounding. The shape falls out of the log/linear/linear structure alone — no personalisation is involved.

## Sensitivity to Peer Behaviour

$V$ is the only peer-dependent term. Four prior scenarios:

| Peer prior for $V$ | $x_R$ | $x_S$ | $x_V$ | PnL (XIREC) |
|---|---|---|---|---|
| Uniform (default) | 16 | 48 | 36 | 110,065 |
| Bottom-heavy (peers under-invest in $x_V$; saturates at $x_V \geq 20$) | 19 | 61 | 20 | 448,908 |
| Top-heavy (peers cluster high on $x_V$; hard to get high rank) | similar | similar | ~40 | lower |
| **Minimax robust** (worst-case positive) | 20 | 70 | 10 | $+14{,}649$ (never negative) |

Key insight: if you suspect peers over-invest in visibility, **shift $x_V$ down and $x_S$ up**. If you suspect peers under-invest (more common), **a uniform prior is right and the $(16, 48, 36)$ solution stands**.

## Final Recommendation

Post-analysis with additional peer-distribution assumptions:

$$\boxed{(x_R, x_S, x_V) = (18, 60, 22)}$$

Best expected value across plausible peer distributions; positive PnL in three of four scenarios. **Fallback (minimax safe):** $(20, 70, 10)$ — the only allocation that never goes negative under any peer-$V$ scenario.

The submitted $(16, 48, 36)$ is the pure uniform-rank optimum. Both $(15, 50, 35)$ and $(16, 48, 36)$ give ~110K at the symmetric NE but cost ~8K if peers cluster high on $x_V$.

## Realized Outcome

Round 2 manual PnL ≈ **155,000 XIREC** (rounded; this includes both the allocation reward and any interaction with the algo's 91K). See [[User_Reported_Anchors]] for confirmed numbers once available.

## ML Analogy

This is a **multiplicative objective with heterogeneous reward curves** — directly analogous to multi-channel budget allocation in digital advertising (Research ≡ targeting a fat-tail curve; Scale ≡ linear reach; Visibility ≡ competitive auction). The log pillar plays the role of **diminishing returns on precision**; the linear pillar is **pure reach**.

The uniform-rank proxy for $V$ is a **prior distribution over a hidden parameter** (peer behaviour). The sensitivity analysis is a **Bayesian robustness check**: how much does the optimal allocation shift as the prior moves? Answer: $x_R$ and $x_V$ are moderately sensitive; $x_S$ is the most stable (always wants maximum remaining budget due to linearity).

The exact FOC system (set marginal returns equal across all pillars) is the continuous-relaxation NLP. The grid search is the brute-force integer programming solution. They agree to within $\pm 2$ integer steps — confirming the global optimum is smooth and the integer relaxation cost is negligible.

## Links

[[Rounds/Round2_findings]] · [[Manuals/MAF]] · [[Manuals/Bio_Pods]] · [[Strategies/manual_trading]] · [[User_Reported_Anchors]] · [[Research/Decisions_Log]] · [[Performance/Manual_Per_Round]]

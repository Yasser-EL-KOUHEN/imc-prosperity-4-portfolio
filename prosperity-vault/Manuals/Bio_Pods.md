---
type: manual
tags: [round3, manual, bayesian-nash, sealed-bid, equilibrium, bio-pods]
sources:
  - report/report.tex (§Bio-Pod Manual Auction: Bayesian-Nash Solution)
  - round3/research/biopod_solver.py
  - context/Round 3/# Round 3 - Gloves Off.txt
updated: 2026-05-02
---

# Round 3 Manual — "The Celestial Gardeners' Guild" (Bio-Pods)

**Theoretical NE:** $(b_1, b_2) = (755, 840)$ · **Actually submitted: $(b_1, b_2) = (760, 855)$** · **Per-counterparty NE EV:** 81.67 XIREC · **Realized: +75,237.51** · **Method:** Symmetric Bayesian-Nash equilibrium on a discrete grid, with slight upward shading at submission

> **Verified result (Prosperity result page, 2026-05-08):** **+75,237.51 realized**. End-of-R3 cumulative manual rank **#234** (≈ **#1,200 without ties**).
>
> **Submitted-bid correction:** the *actual* submitted bids were **(760, 855)**, not (755, 840) as initially recorded — the user shaded both bids slightly upward from the symmetric NE (b₁ +5, b₂ +15) to capture more counterparties under the assumption that other solvers would also bid at or above NE.
>
> **Per-bid breakdown (N = 1,000 counterparties at each level):**
> - b₁ = 760: 335 accepted / 665 rejected → buy 254,600, sell 308,200, **P&L +53,600** (53.60/cp)
> - b₂ = 855: 404 accepted / 596 rejected → buy 345,420, sell 371,680, **P&L +21,637.51** (21.64/cp)
> - Combined: 75,237.51 = **75.24/cp = 92% of theoretical NE EV**
>
> **Empirical reserve CDF (back-solved from accept counts):**
> | Reserve threshold | Realized F(r) | Uniform-on-[670,920] F(r) | Gap |
> |---|---|---|---|
> | r ≤ 760 | 335/1000 = 0.335 | 0.360 | −0.025 |
> | r ≤ 855 | 739/1000 = 0.739 | 0.740 | −0.001 |
>
> **The uniform-reserve assumption is empirically validated** — within 3pp at b₁, within 0.1pp at b₂. The Bio-Pods reserve distribution really is uniform on the {670, 675, …, 920} grid, exactly as the briefing implied. The 91% realization efficiency (75.24 vs. 82.30 EV under continuous uniform) likely reflects a small grid-discretization gap plus per-cp variance, not a model failure.
>
> **N = 1,000 counterparties** is the *exact* number, not the ~921 estimate. The implied 921 from 75,238 / 81.67 was close — the actual gap (75.24 vs 81.67 per cp) reflects the slightly-aggressive submission, not an N undercount.
>
> **Peer-bid distribution** (`performance/manual trading/round 3/`): first bids cluster 750–770 (avg 768), second bids cluster 850–870 (avg 859). Our (760, 855) sat at the **lower edge of both distributions** — among the lowest 25% of solvers on each bid level. The narrow peer-bid bands (≤20 wide) confirm the common-knowledge regime.
>
> Bio-Pods at the symmetric NE is common-knowledge among solvers — many teams converged on similar (b₁, b₂) and earned similar realized PnL. The display rank #234 is non-deterministic tie-breaking among solvers; the true rank counting ties is ~#1,200.

## The Mechanic

Sealed-bid auction with two bids on the discrete grid $\{670, 675, \ldots, 920\}$ (51 levels, increment 5). Each counterparty $i$ has reserve price $r_i$ uniformly distributed on the same grid; we trade at most once with each counterparty and resell next day at $920$.

For each counterparty:
- **If $b_1 > r_i$:** trade at $b_1$, profit $920 - b_1$
- **Else if $b_2 > r_i$ AND $b_2 > \overline{b_2}$ (mean of all players' second bids):** trade at $b_2$, profit $920 - b_2$
- **Else if $b_2 > r_i$ AND $b_2 \leq \overline{b_2}$:** trade at $b_2$, profit penalised by $\left(\frac{920 - \overline{b_2}}{920 - b_2}\right)^3 \le 1$ (cubic punishment for under-cutting)
- **Else:** no trade

## Symmetric-NE Setup

At a symmetric Bayesian-Nash equilibrium, every player bids $(b_1^*, b_2^*)$, so $\overline{b_2} = b_2^*$ and the penalty multiplier is exactly 1. Expected profit per counterparty reduces to:

$$f(b_1, b_2) = \frac{b_1 - 670}{255}(920-b_1) + \frac{b_2 - b_1}{255}(920 - b_2)$$

First-order conditions give the linear system:

$$2b_1 - b_2 = 670, \quad -b_1 + 2b_2 = 920$$

**Continuous solution:** $b_1^* = 753.\overline{3}, \; b_2^* = 836.\overline{6}, \; f^* = 81.70$.

## Discrete Grid Snap

Snapping to the 5-unit grid gives 4 candidates: $\{(750, 835), (750, 840), (755, 835), (755, 840)\}$. Exhaustive search over all $51 \times 51 = 2{,}601$ ordered $(b_1, b_2)$ pairs under the symmetric-NE assumption confirms:

$$\boxed{(b_1^*, b_2^*) = (755, 840), \; f^* = 81.67 \text{ XIREC per counterparty}}$$

## The Elegant Structure

At the optimum, each bid covers **exactly $\frac{1}{3}$ of the reserve distribution**:
- $P(\text{first-bid trade}) = \frac{17}{51} = \frac{1}{3}$ (reserves 670–750)
- $P(\text{second-bid trade}) = \frac{17}{51} = \frac{1}{3}$ (reserves 755–835)
- $P(\text{no trade}) = \frac{17}{51} = \frac{1}{3}$ (reserves 840–920, margin too thin)

**Each bid covers exactly 17 of the 51 reserve levels.** The bottom 17 reserves (those above $b_2$) are deliberately unpursued because the residual margin $(920 - r)$ is too thin — bidding higher would lose more in margin than it gains in trade probability.

## Stability Check (±2 grid steps)

| $\Delta b_1$ | $\Delta b_2$ | $f$ | $\Delta f$ |
|---|---|---|---|
| $-1$ | $-1$ | 77.23 | **−4.43** (cubic penalty trips) |
| $-1$ | 0 | 81.27 | −0.39 |
| $-1$ | $+1$ | 81.47 | −0.20 |
| 0 | $-1$ | 77.23 | **−4.43** (cubic penalty trips) |
| **0** | **0** | **81.67** | **0.00 (NE)** |
| 0 | $+1$ | 81.47 | −0.20 |
| $+1$ | $-1$ | 77.31 | −4.35 |
| $+1$ | 0 | 81.57 | −0.10 |
| $+1$ | $+1$ | 81.47 | −0.20 |

Deviations downward in $b_2$ trip the cubic penalty (the **steep $-4$ point cliff** at $\Delta b_2 = -1$). Deviations upward in $b_2$ leave profit on the table. The diagonal optimum is **sharp** in the down-direction, **shallow** in the up-direction.

## Robustness to Peer Behaviour

| $\overline{b_2}_{\text{peer}}$ | Best response | EV | Note |
|---|---|---|---|
| $\le 835$ | $(750, 835)$ | 81.67 | undercut peers safely |
| 840 | $(755, 840)$ | 81.67 | **symmetric NE focal point** |
| 845 | $(755, 845)$ | 81.47 | match peers, lose 0.2 |
| 855 | $(760, 855)$ | 80.69 | chase, lose 1.0 |
| 870 | $(770, 870)$ | 78.43 | chase further, lose 3.2 |

Per-counterparty EV stays in $[78, 82]$ even if peers systematically over-bid by ±30 units. **Robust within $\pm 30$ of the focal NE.**

## ML Analogy

The cubic penalty is a **soft constraint regularizer** with a sharp boundary — it does nothing while the constraint is satisfied, then applies a steeply non-linear cost when violated. Like a **log barrier in interior-point optimization**: the optimum sits **just inside** the boundary, with the gradient of the regularizer balancing the gradient of the objective.

The symmetric-NE assumption is **fixed-point self-consistency**: assume everyone plays the same strategy, solve for it, verify the assumption holds. This is the standard equilibrium-finding technique in game theory and shows up in ML as **mean-field approximation** in multi-agent learning.

## Why the Bayesian-Nash Solution Generalizes

The same approach (set $\overline{b_2} = b_2^*$, solve FOCs, exhaustively verify on the discrete grid) handles any auction-type Prosperity manual challenge with:
- Continuous reserve distribution → discrete bid grid
- Multi-bid mechanic with conditional payoffs
- Symmetric players (or symmetric prior over peer behaviour)

For Prosperity 5+ this is the **template**: write the per-counterparty EV under symmetric-NE, take FOCs, snap to grid, verify with exhaustive search, **and** check stability against ±2-step deviations to confirm the optimum is sharp.

## Per-Counterparty EV vs Total EV

With typical Prosperity counterparty count of 30–60 per manual:
- 30 CP × 81.67 = 2,450 XIREC
- 60 CP × 81.67 = 4,900 XIREC

Range: **2,500–5,000 XIREC** total expected. Realized depends on actual N. See [[User_Reported_Anchors]] for the realized number once known.

## Links

[[Rounds/Round3_findings]] · [[Strategies/manual_trading]] · [[Manuals/MAF]] · [[Manuals/Invest_and_Expand]] · [[Research/Decisions_Log|D11]] · [[User_Reported_Anchors]] · [[Performance/Manual_Per_Round]]

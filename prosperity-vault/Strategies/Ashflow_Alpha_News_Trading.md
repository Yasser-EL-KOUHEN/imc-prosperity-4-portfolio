---
type: strategy
tags: [round5, manual, news, archetype-classification, quadratic-fee, submitted]
sources: [context/Round 5/Manual Trading Annex (Ashflow Alpha).txt, context/Round 5/Manual Trading Challenge.txt, context/Round 5/# Round 5 - The Final Stretch.txt]
updated: 2026-04-29
status: SUBMITTED
---

# Ashflow Alpha News-Driven Trading (Round 5 Manual)

> **Submitted: 85% budget allocated, 6 of 9 goods traded, 140,100 fees.**
> Model-implied net PnL = 140,100 (equals total fees by construction at optimum).
> See [Final Submission](#final-submission) below.

## Setup

**Market:** Ignith exchange — open for one day only.

**Budget:** 1,000,000 XIRECs. Distribute across up to 9 goods. Unused budget expires worthless.

**Fee per product (exact formula from competition spec):**
$$\text{fee}_i = \left(\frac{p_i}{100}\right)^2 \cdot B = 100 \cdot p_i^2 \;\text{(XIRECs)}$$
where $p_i$ is the percentage allocation and $B = 1{,}000{,}000$.

**Net PnL formula:**
$$\Pi_i = 100 \cdot p_i \cdot (s_i - p_i)$$
where $s_i$ is the **effective signed one-day move in %** (positive = your position profits by $s_i$%).

## This Is NOT a Gaussian Problem

An earlier draft of this strategy modelled each product as having a Gaussian return $(\mu_i, \sigma_i)$ and applied mean-variance shrinkage + conviction floors. **This was the wrong model.** Concretely:

- **Gaussian models daily market noise.** This challenge presents discrete, one-day, news-driven shocks. Normal daily return distributions are irrelevant.
- **Sentiment scores are noisy proxies.** Assigning a continuous $r_i = 0.44$ and shrinking it is fitting a noisy variable to a problem with discrete structure.
- **Archetype classification is the right tool.** Each article belongs to a category (recall, policy shock, index inclusion, fresh demand, stale hype, etc.). The archetype determines the effective move $s_i$.
- **The formula $p^* = s/2$ is exact.** There is no uncertainty to shrink; the risk is embedded in the $s_i$ estimate, not in a separate covariance matrix.
- **Conviction floors were wrong heuristics.** Volcanic incense was capped at 6% in the earlier draft. The correct answer is $s = 0$ (stale hype archetype) → $p^* = 0$ algebraically.

## The Optimization

Maximise $\Pi_i = 100\,p_i(s_i - p_i)$ per product:

$$\frac{\partial \Pi_i}{\partial p_i} = 100(s_i - 2p_i) = 0 \quad\Longrightarrow\quad \boxed{p_i^* = \frac{s_i}{2}}$$

**Optimal allocation is exactly half the effective signed move.** This is exact, not a heuristic.

At the optimum, model net PnL equals the fee paid (by construction):
$$\Pi_i^* = 100 \cdot p_i^{*2} = \text{fee}_i \quad \Longrightarrow \quad \Pi^* = \sum_i \text{fee}_i$$

Budget constraint $\sum_i p_i \leq 100$: not binding here ($\sum p_i^* = 85\%$), so no scaling needed.

## Article Archetype Classification

| Product | Archetype | $s_i$ % | Direction | Rationale |
|---|---|---|---|---|
| **Lava cake** | Mechanical recall | **50** | SELL | Actual lava confirmed by lab; sales halted; lawsuits filed; vendors returning stock. Structural, not reputational. |
| **Thermalite core** | Demand adoption report | **32** | BUY | Quantified 1.42M → 3.89M users; 16h42m avg daily usage. Hard numbers from a quarterly forecast. |
| **Ashes of the Phoenix** | Viral scandal | **28** | SELL | Resurfaced video of sourcing method. Immortal-bird disclaimer is weak counter. Viral outrage = structural reputational hit. |
| **Pyroflex cells** | Policy shock | **24** | SELL | Tax cut ending effective tomorrow; effective levy doubles overnight. Mechanical, not speculative. |
| **Magma ink** | Fresh scarcity demand | **24** | BUY | Hot drop + 6h+ queues = new demand spike. Merger-driven supply constraint. Fresh signal, not stale. |
| **Sulfur reactor** | Index inclusion | **12** | BUY | Elemental Index 118 rebalance. Funds tracking the index must buy. Mechanical, documented at +4–7% in real markets. |
| **Volcanic incense** | Late-stage stale hype | **0** | — | Whiff Nostralico publicly calling followers to "buy." Classic distribution signal. Market data already shows "accelerated buying concentrated in narrow time windows" — the rally is done. |
| **Obsidian cutlery** | Single production accident | **0** | — | One-off halt. Level-1 contamination events resolve quickly in real markets. Not structural. |
| **Scoria paste** | Low-quality forecast | **0** | — | Self-proclaimed market medium on streaming show. Staple good with low price elasticity. Weakest signal quality. |

## Volcanic Incense vs Magma Ink: The Key Distinction

Both are demand-side articles. The difference is **freshness and origin**:

- **Magma ink** (BUY, s=24%): The demand is *new* — triggered by the Lava Fountain Pen merger and hot-drop launch. Crowds queuing 6+ hours are evidence the market hasn't fully absorbed the shock yet. This is a fresh supply-demand imbalance.

- **Volcanic incense** (NO TRADE, s=0): Whiff Nostralico is *publicly calling for people to follow his lead and buy*. This is a pump-and-distribute signal — the influencer already bought, the price has already moved ("extended its rally this cycle"), and now he's inviting late buyers in while he exits. Entering now means paying the fee to be on the wrong side of the distribution.

## Final Submission

| Tradable Good | Side | $s_i$ % | $p_i$ % | Investment | Fee | Net PnL (model) |
|---|---|---|---|---|---|---|
| **Lava cake** | SELL | 50 | **25** | 250,000 | 62,500 | 62,500 |
| **Thermalite core** | BUY | 32 | **16** | 160,000 | 25,600 | 25,600 |
| **Ashes of the Phoenix** | SELL | 28 | **14** | 140,000 | 19,600 | 19,600 |
| **Pyroflex cells** | SELL | 24 | **12** | 120,000 | 14,400 | 14,400 |
| **Magma ink** | BUY | 24 | **12** | 120,000 | 14,400 | 14,400 |
| **Sulfur reactor** | BUY | 12 | **6** | 60,000 | 3,600 | 3,600 |
| Volcanic incense | — | 0 | 0 | 0 | 0 | 0 |
| Obsidian cutlery | — | 0 | 0 | 0 | 0 | 0 |
| Scoria paste | — | 0 | 0 | 0 | 0 | 0 |
| **TOTAL** | | | **85** | **850,000** | **140,100** | **140,100** |

**Fee verification:** $\sum_i p_i^2 / 100 = (625+256+196+144+144+36)/100 = 1401/100 \times 1000 = 140{,}100$ ✓

**Budget:** $25+16+14+12+12+6 = 85\%$ ✓ (budget constraint not binding)

### Rejected Alternatives

| Consideration | Rejected allocation | Why rejected |
|---|---|---|
| Thermalite | 17% | No basis for inflating beyond $s/2 = 16$; forecast not realized data |
| Pyroflex | 14% | "Abrupt" language suggests partial pricing-in; $p^* = 12$ is exact |
| Volcanic incense | 6% (earlier draft) | Late-stage stale hype; $s=0$ drops it algebraically, not via ad-hoc cap |
| Obsidian | 5% (Lagrangian would suggest) | One-off accident → $s=0$; no sustained structural damage |

### Model-Implied PnL

$$\Pi^* = \sum_i 100 \cdot p_i^{*2} = 140{,}100 \text{ XIRECs}$$

This is the ceiling under perfect archetype-to-move calibration. Actual realized PnL depends on how accurately the archetypes predicted next-day moves. The model says: if all six directional bets are correct, we capture 140,100 XIRECs net.

## ML Analogy

The quadratic fee is **L2 regularisation on portfolio weights** ($\lambda \|p\|^2$ with $\lambda = 100/\text{pct}^2$). The gross return is linear: $\Pi_{\text{gross}} = 100 \mathbf{s}^\top \mathbf{p}$. The optimum $p^* = s/2$ is the exact ridge solution $(\lambda I)^{-1} s$.

The zero allocations for Volcanic, Obsidian, and Scoria are **signal estimates, not regularisation artefacts** — $s_i = 0$ means the archetype predicts no net one-day move worth trading, so the L2 penalty suffices to drive $p_i^* = 0$ without any L0 component.

## Links

[[Rounds/Round5_Preview]] · [[Manuals/Ashflow_Alpha]] · [[Strategies/manual_trading]] · [[Concepts/fair_value]]

---
type: manual
tags: [round5, manual, news-trading, quadratic-fee, archetype-classification, ignith-exchange]
sources:
  - report/report.tex (§Manual Challenge — Ashflow Alpha (Ignith Exchange))
  - context/Round 5/# Round 5 - "Gloves Off 2".txt
updated: 2026-05-06
---

# Round 5 Manual — Ashflow Alpha (Ignith Exchange)

**Submitted:** 85% total allocation across 6 of 9 goods · **Model PnL:** 140,100 XIREC · **Realized: +95,214** · **Method:** Exact closed-form $p^* = s/2$ per product + archetype classification

> **Verified result (Prosperity result page, 2026-05-08):** **+95,214 realized**. End-of-R5 cumulative manual rank **#204** (final). Realization ratio: 95,214 / 140,100 = **0.679**.
>
> **Per-archetype scoreboard (4 of 6 correct):**
>
> | Archetype | Submitted | Realized P&L | Verdict |
> |---|---|---|---|
> | **Lava cake** | SELL 25% (s ≈ −50%) | **+95,884** | ✓ correct (single biggest contribution) |
> | Pyroflex cells | SELL 12% (s ≈ −12%) | +9,041 | ✓ correct |
> | Thermalite core | BUY 16% (s ≈ +16%) | +9,856 | ✓ correct |
> | Sulfur reactor | BUY 6% (s ≈ +6%) | +6,854 | ✓ correct |
> | **Magma ink** | BUY 12% (predicted up) | **−11,727** | ✗ wrong — went down or flat |
> | **Ashes of the Phoenix** | SELL 14% (predicted down) | **−14,694** | ✗ wrong — went up or flat |
> | Volcanic incense | 0% (skipped) | 0 | ✓ correct null |
> | Obsidian cutlery | 0% (skipped) | 0 | ✓ correct null |
> | Scoria paste | 0% (skipped) | 0 | ✓ correct null |
>
> **The misclassified archetypes were Magma ink and Ashes of the Phoenix** — earlier speculation about Lava cake or Pyroflex being off was wrong. Lava cake at SELL 25% delivered **+95,884** alone, more than the entire round's net PnL; without Lava cake, the manual would have netted near zero. Lava cake was the load-bearing call.
>
> The 4-of-6 archetype hit rate (67%) closely matches the 0.679 realization ratio — confirming that the optimization math ($p^* = s/2$) is correct and the failure was purely in archetype labeling, not in allocation sizing.
>
> **Back-solved realized $s_i$ (corrects the "misclassification" framing):** all 6 allocated archetypes were **directionally correct**; the failures were in *magnitude* prediction:
>
> | Archetype | Predicted s_i | Realized s_i (back-solved) | Gap |
> |---|---|---|---|
> | Lava cake | −50% | **−63.4%** | under-allocated |
> | Pyroflex cells | −24% | −19.5% | close |
> | Thermalite core | +32% | +22.2% | over-allocated |
> | Sulfur reactor | +12% | +17.4% | under-allocated |
> | **Magma ink** | +24% | **+2.2%** (essentially flat) | direction OK, magnitude wildly off |
> | **Ashes of the Phoenix** | −28% | **−3.5%** (essentially flat) | direction OK, magnitude wildly off |
>
> **Refined lesson:** when archetype-classification labels include both *direction* and *magnitude*, the magnitude is the harder estimation problem. Treat magnitude as a confidence interval and shrink p toward 0 when the interval is wide (James-Stein-style shrinkage). Magma ink and Ashes are the canonical failure modes — direction inferred from text-cycle archetype was correct; magnitude was wildly over-estimated. The optimal hindsight allocation would have shrunk both to ~1–2% (vs submitted 12% and 14%), saving ~$25K of fees that swamped the small directional gain.

## The Mechanic

One-day-only access to the Ignith exchange. 9 goods, budget $B = 1{,}000{,}000$ XIREC. Fee per product is quadratic in the percentage allocation $p_i \in [0, 100]$:

$$\text{fee}_i = \left(\frac{p_i}{100}\right)^2 \cdot B = 100 \cdot p_i^2 \quad \text{(XIREC)}$$

Net PnL from product $i$ with signed effective one-day move $s_i$ (%):

$$\Pi_i(p_i) = 100 \cdot p_i \cdot s_i - 100 \cdot p_i^2 = 100 \cdot p_i (s_i - p_i)$$

where $s_i > 0$ means a long position makes money (price moves up by $s_i$%).

## The 9 Articles: Archetype, Not Sentiment Score

This is **not a Gaussian return-estimation problem**. Each article describes a discrete headline shock with a near-deterministic directional outcome. The relevant question is: "which article archetype is this, and what effective one-day move does that archetype produce?"

| Product | Archetype | $s_i$ (%) | Direction | Notes |
|---|---|---|---|---|
| Lava cake | Mechanical recall | 50 | SELL | Sales halt + lawsuits + vendor returns |
| Thermalite core | Demand adoption report | 32 | BUY | $1.42\text{M} \to 3.89\text{M}$ quantified users |
| Ashes of the Phoenix | Viral scandal | 28 | SELL | Resurfaced sourcing video, viral outrage |
| Pyroflex cells | Policy shock | 24 | SELL | Tax cut ends; effective levy doubles |
| Magma ink | Fresh scarcity demand | 24 | BUY | Hot drop + 6h+ queues; merger-driven |
| Sulfur reactor | Index inclusion | 12 | BUY | Elemental Index 118; forced rebalancing |
| Volcanic incense | Late-stage stale hype | 0 | — | Already rallied; influencer distributing |
| Obsidian cutlery | Single production accident | 0 | — | One-off halt; level-1 contamination resolves |
| Scoria paste | Low-quality forecast | 0 | — | Self-proclaimed market medium; staple good |

## The Critical Distinction: Volcanic vs Magma

Both are demand-side articles. The key difference is **freshness and origin of the demand signal**:

- **Magma ink (BUY $s=24$%)**: fresh scarcity shock triggered by the Lava Fountain Pen merger and hot-drop launch. Large crowds queuing 6+ hours are concrete evidence of *new* demand before the market has fully priced it in.
- **Volcanic incense (NO TRADE, $s=0$)**: late-stage influencer hype. Whiff Nostralico is *publicly calling for followers to buy* — a classic pump signal where the rally has already happened and the influencer is distributing. Trading data confirms "accelerated buying concentrated within narrow time windows" around his appearances, meaning the market has already repriced. Entering now pays the fee with no remaining upside.

The distinguishing signal: **who is the source of the demand signal, and when did it originate?** Merger-driven real demand (Magma) vs. influencer distribution (Volcanic).

## Optimal Allocation Formula

For each product independently, maximize $\Pi_i(p_i) = 100 \cdot p_i(s_i - p_i)$ over $p_i \geq 0$:

$$\frac{\partial \Pi_i}{\partial p_i} = 100(s_i - 2p_i) = 0 \quad \Longrightarrow \quad \boxed{p_i^* = \frac{s_i}{2}}$$

**Optimal allocation is exactly half the effective signed move.** This is exact — not a heuristic.

The budget constraint $\sum_i p_i \leq 100$ is **not binding** here ($\sum p_i^* = 85\%$), so no scaling is needed. Each product's allocation is independent of the others.

## At the Optimum: Net PnL = Fee Paid

Substituting $p_i^* = s_i / 2$:

$$\Pi_i^* = 100 \cdot \frac{s_i}{2} \cdot \left(s_i - \frac{s_i}{2}\right) = 100 \cdot \left(\frac{s_i}{2}\right)^2 = \text{fee}_i$$

**Model-implied net PnL equals the fee paid — by algebraic construction.** The quadratic fee and linear gross return combine so that the net PnL at the peak is exactly the fee. This means every XIREC paid in fees corresponds to exactly one XIREC gained — the fee is the correct "price" for the access.

## Full Allocation Table

| Product | Direction | $s_i$ (%) | $p_i^*$ (%) | Gross (XIREC) | Fee | Net |
|---|---|---|---|---|---|---|
| Lava cake | SELL | 50 | 25 | 250,000 | 62,500 | **62,500** |
| Thermalite core | BUY | 32 | 16 | 160,000 | 25,600 | **25,600** |
| Ashes of the Phoenix | SELL | 28 | 14 | 140,000 | 19,600 | **19,600** |
| Pyroflex cells | SELL | 24 | 12 | 120,000 | 14,400 | **14,400** |
| Magma ink | BUY | 24 | 12 | 120,000 | 14,400 | **14,400** |
| Sulfur reactor | BUY | 12 | 6 | 60,000 | 3,600 | **3,600** |
| Volcanic incense | — | 0 | 0 | 0 | 0 | 0 |
| Obsidian cutlery | — | 0 | 0 | 0 | 0 | 0 |
| Scoria paste | — | 0 | 0 | 0 | 0 | 0 |
| **TOTAL** | | | **85** | **850,000** | **140,100** | **140,100** |

## ML Analogy — Exact Ridge Regression

The quadratic fee is structurally identical to **L2 regularisation**: $\text{fee} = \lambda \|p\|^2$ with $\lambda = 100$ per percentage-point squared. The gross return is linear: $\Pi_{\text{gross}} = 100 \cdot \mathbf{s}^\top \mathbf{p}$.

The optimum $p^* = s/2$ is the exact ridge solution $(\lambda I)^{-1} \cdot (\nabla \text{gross}) = s / (2 \cdot 1)$ with $\lambda = 1$ after appropriate scaling. The sparsity ($s_i = 0$ for Volcanic, Obsidian, Scoria) emerges from the signal estimation, not from an L0 penalty imposed post-hoc. **Zero allocation is a signal estimate, not a regularisation artefact.**

The archetype classification step is the **feature engineering** phase. A naïve model would try to estimate $s_i$ from raw sentiment; the correct model recognises that each article belongs to a discrete archetype with a known magnitude distribution. This is closer to **few-shot classification** than regression.

## Why Archetype Classification Beats Quantitative Estimation

For articles like Lava cake (mechanical recall), the effective move $s = 50$% is essentially deterministic — all comparable recalls produce large immediate drops. A quantitative model that tries to fit $s$ from the article text would have far more variance than the simple: "recall → 50%". The archetype table is the expert prior that dominates any data-sparse regression.

For Obsidian cutlery ("single production accident"), the key is the severity qualifier: "level-1 contamination resolves." A one-off, low-severity industrial event is fully hedged by existing safety buffers. Market repricing to a new structural level is not warranted. $s = 0$.

## Links

[[Rounds/Round5_findings]] · [[Strategies/Ashflow_Alpha_News_Trading]] · [[Manuals/Bio_Pods]] · [[Manuals/Invest_and_Expand]] · [[Manuals/AETHER_Crystal]] · [[User_Reported_Anchors]] · [[Research/Decisions_Log]] · [[Performance/Manual_Per_Round]]

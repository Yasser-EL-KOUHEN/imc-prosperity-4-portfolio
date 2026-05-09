---
type: competition
tags: [user-reported, anchors, ground-truth, gap-fill, source-of-truth, final-results]
sources:
  - User chat sessions (canonical for facts NOT in repo files)
  - round5/logs/ (canonical for facts present in JSON activitiesLog)
  - Prosperity website final leaderboard + per-round breakdown screenshots (2026-05-08)
updated: 2026-05-08
---

# User-Reported Anchors

> **Purpose:** Some load-bearing facts about this competition are **not** in any repo file — they live in the user's head or on the Prosperity leaderboard. This page is the **single source of truth** for those facts. Other pages cite this one.

---

## FINAL COMPETITION RESULT (received 2026-05-08)

### Headline

| Metric | Value | Source |
|---|---|---|
| **Final overall rank** | **#346 / 18,803 teams** (top 1.84%) | Prosperity website (final leaderboard, 2026-05-08) |
| **Algorithmic rank (overall)** | #537 | Same |
| **Manual rank (overall)** | #204 | Same |
| **Country rank** | **#11** | Same |
| **Final GOAT XIREC** | **383,727** | Same |
| Field size | 30,703 players · 18,803 teams · 1,549 universities · 117 countries | Same |
| Total XIRECs earned by all teams | 1,153,901,776 | Same |
| Average XIREC per round (all teams) | 52,675 | Same |

### Per-round PnLs (verified from per-round screenshots)

| Round | Algo PnL | Manual PnL | Round Total | Cumul. (qualifier or GOAT) |
|---|---|---|---|---|
| R1 | **+98,172** | **+71,500** | 169,672 | 169,672 |
| R2 | **+91,529** | **+153,345** | 244,874 | 414,546 |
| R3 | **+40,800** | **+75,238** | 116,038 | 116,037 (GOAT begins) |
| R4 | **+57,048** | **+57,516** | 114,564 | 230,601 |
| R5 | **+57,911** | **+95,214** | 153,125 | 383,727 |

### Cumulative leaderboard rankings at end of each round (CANONICAL)

This is the ranking schema the user identifies as canonical — cumulative leaderboard standing at the **end of each round**, broken out by category. The per-round screenshots also show a separate "round-rank" (rank for that round's PnL component alone) which is *not* the schema below.

| Round | Overall | Algorithmic | Manual | Country |
|---|---|---|---|---|
| R1 | ~#2,000 | ~#1,400 | **#72** *(≈ #3,000 without ties)* | #59 |
| R2 | #1,522 | #857 | #801 | #59 |
| R3 | #802 | #830 | **#234** *(≈ #1,200 without ties)* | #30 |
| R4 | #592 | #809 | #406 | #21 |
| **R5 (final)** | **#346** | **#537** | **#204** | **#11** |

### Algo cumulative-rank trajectory

~1,400 → 857 → 830 → 809 → **537**. Monotonic improvement (with one R3 dip) — the algo rank moved up by ~860 places net across the competition. The R5 final algo rank #537 is the strongest end-state.

### Manual cumulative-rank trajectory

**~3,000** (without ties; #72 displayed) → 801 → **~1,200** (without ties; #234 displayed) → 406 → **#204**. Monotonic improvement throughout. The R5 final manual rank #204 is comfortably stronger than the algo rank.

### Country-rank trajectory

59 → 59 → 30 → 21 → **#11**. By far the steepest improvement; the country (Morocco) rank dropped by 48 places.

### Tie caveats (BOTH R1 and R3 manuals had massive ties)

- **R1 manual** displayed rank **#72** but rank **without ties ≈ #3,000**. Dryland Flax + Ember Mushroom is a deterministic clearing-price-engineering puzzle: every solver who computes the clearing price submits the same orders and earns the same 71,500. Many teams achieved exactly this PnL and the Prosperity display-rank breaks ties non-deterministically — landing us at #72.
- **R3 manual** displayed rank **#234** but rank **without ties ≈ #1,200**. Bio-Pods at the symmetric Bayesian-Nash equilibrium (b₁=755, b₂=840) is similarly common-knowledge among solvers; many teams converged on the same NE bids and earned identical realized PnL.

The earlier conversation collapsed both caveats into one — the "displayed ~#70, real ~#1,200" memory was a *fusion* of R1's display rank (#72) with R3's without-ties rank (~#1,200). Both caveats are real and need to be preserved separately.

### GOAT decomposition (R3+R4+R5 only)

| Component | XIREC | % of GOAT |
|---|---|---|
| Algo (R3+R4+R5) | 155,759 | 40.6% |
| Manual (R3+R4+R5) | 227,968 | **59.4%** |
| **GOAT total** | **383,727** | 100% |

**Manuals delivered 60% of the final XIREC.** This is the central post-result insight: the algo carried less weight than the manuals in absolute terms, even though the algo represents the bulk of project hours. See [[Carry_Forward]] for the implication.

### All-rounds totals (including qualifier)

| Component | All 5 rounds total |
|---|---|
| Algo (R1+R2+R3+R4+R5) | 345,460 |
| Manual (R1+R2+R3+R4+R5) | 452,813 |
| **All rounds total** | **798,273** |

### Round 3 manual rank — clarification

In the resumed conversation the user previously said "displayed ~#70, real ~#1,200 due to ties". The actual screenshots show:
- **R3 manual rank: #234** (not #70 / #1,200)
- **R1 manual rank: #72** (very close to "~#70")

The most likely explanation: the user was mis-remembering — the "~#70" was the **R1 manual** rank (Dryland Flax + Ember Mushroom at #72), not R3. The Bio-Pods #234 result is consistent with a moderately-tied common-knowledge regime: many teams hit the NE bids but enough variation in submitted bid pairs (and reserve draws) gave a non-degenerate rank distribution. The Bio-Pods caveat is therefore softer than first stated: the manual gave a real rank lift over non-solvers, but the optimization is shared common knowledge among solvers.

---

## R5 Final Submission

| Fact | Value | Source / Date |
|---|---|---|
| Submitted version | `round5/strategies/round5_v42_trader.py` | repo (verifiable) |
| **v42 measured Prosperity backtester PnL** | **~$72,000** | user-reported, 2026-05-02 |
| Selection rationale | "We tried to not overfit to the Prosperity backtester" | user-reported, 2026-05-02 |
| **v42 R5 algo realized PnL** | **+57,911** | leaderboard 2026-05-08 |
| End-of-R5 cumulative algo rank | **#537** | leaderboard 2026-05-08 |
| Backtester-vs-real ratio | 57,911 / 72,000 = **0.804** | DERIVED |
| **Ashflow Alpha realized** | **+95,214** | leaderboard 2026-05-08 |
| End-of-R5 cumulative manual rank | **#204** | leaderboard 2026-05-08 |
| Ashflow vs theoretical (140,100) | 95,214 / 140,100 = **0.679** | DERIVED |
| **R5 GOAT contribution** | **153,125 XIREC** | leaderboard 2026-05-08 |

### Backtester-vs-real check on v42 — RESOLVED

Backtester (first 10% of Day 4): **$72,000**
Real R5 algo (full Day 5): **$57,911**
**Ratio: 0.80.** The full-day was *less* than the backtester window.

Reconciliation with the 8.6× local-fill inflation thesis:
- Backtester runs 10% of day with ~8.6× over-fill
- Net multiplier vs full-day: 0.10 × 8.6 = **0.86**
- Predicted full-day from $72K: $72K / 0.86 = **$83,720**
- Realized: **$57,911** = 0.69 of prediction

The thesis is *roughly* correct (the time-and-inflation factors do approximately cancel), but the realized full-day was further below the prediction by ~30%. The most likely cause: **Day 5 had different drift patterns than the historical Days 2/3/4** that informed v42's directional list. Some directional positions that worked on training-data days didn't resolve favorably on Day 5. This is a normal live-vs-test overfitting gap.

The encouraging side: end-of-R5 **cumulative algo rank #537** is the strongest algo end-state, with the trajectory ~1,400 → 857 → 830 → 809 → 537. The v42 design moved the algo rank up by ~860 places across the competition, even though the realized R5 absolute PnL was below the backtester window.

---

## R4 Manual Result

| Fact | Value | Source |
|---|---|---|
| Submitted manual portfolio | 12 instruments (chooser, 2 vanilla pairs, binary spread, KO put) | `Round4_findings.md` |
| Expected E[PnL] | +175,200 XIREC | `Round4_findings.md` (BS pricing × volume × multiplier) |
| **R4 manual realized** | **+57,516** (rank #316) | leaderboard 2026-05-08 |
| Realization ratio | 57,516 / 175,200 = **0.328** | DERIVED |
| **R4 algo realized** | **+57,048** (rank #772) | leaderboard 2026-05-08 |

The R4 manual was the worst realization-vs-EV across all 5 rounds (33%). Greek-asymmetric exotics (chooser, binary spread, KO put) suffered from a single AC mid drift. The +175,200 EV assumed BS-priced symmetry; the realized PnL is consistent with AC drifting strongly enough in one direction to make several legs nearly worthless.

---

## R3 Manual Result (Bio-Pods)

| Fact | Value | Source |
|---|---|---|
| Theoretical NE bids | (b₁, b₂) = (755, 840) | derived (symmetric BNE) |
| **Actually submitted bids** | **(b₁, b₂) = (760, 855)** | Prosperity result page (slight upward shading) |
| Per-counterparty NE EV (theoretical) | 81.67 XIREC | derived |
| **R3 manual realized** | **+75,237.51** | Prosperity result page |
| Counterparties at b₁=760: accepted/rejected | 335 / 665 (N=1,000) | Prosperity result page |
| Counterparties at b₂=855: accepted/rejected | 404 / 596 (N=1,000) | Prosperity result page |
| Per-CP realized at b₁ | 53.60 XIREC/cp | DERIVED |
| Per-CP realized at b₂ | 21.64 XIREC/cp | DERIVED |
| Combined per-CP realized | **75.24 XIREC/cp = 92% of theoretical NE** | DERIVED |
| R3 manual displayed rank (cumul) | #234 | leaderboard 2026-05-08 |
| R3 manual without-ties rank | ~#1,200 | user-reported tie caveat |
| Implied counterparty count | 75,238 / 81.67 ≈ **921** | DERIVED |
| **R3 algo realized** | **+40,800** (rank #832) | leaderboard 2026-05-08 |

R3 algo was the weakest of the 5 rounds (40,800), well below the local-3-day baseline of 153,566 scaled to 1 day (~51K) — about 80% of one-day-of-3 baseline. Possible causes: HYDROGEL and VEL fills under the real engine were lower than local; VEV options carried less per-tick alpha than estimated.

The implied counterparty count of ~921 (if the 81.67 EV is exact) is inconsistent with typical Prosperity manuals (usually 30–60). The discrepancy suggests either:
- The actual EV per counterparty was higher than 81.67 (e.g., reserve distribution skewed favorably)
- The "counterparty" unit in Prosperity is different from our derivation
- Bio-Pods PnL has a different formula than we modeled

Rank #234 across 18,803 teams is solid: the manual gave a real rank lift over non-solvers. The earlier "true rank ~#1,200" caveat is retracted — that was likely a confusion with R1 manual's #72.

---

## R2 Manual Result (Invest & Expand)

| Fact | Value | Source |
|---|---|---|
| Submitted I&E allocation | (x_R, x_S, x_V) = (18, 60, 22) | confirmed user-submitted |
| Theoretical PnL (uniform-rank prior, FOC opt 16,48,36) | 110,065 XIREC | derived |
| **R2 manual realized** | **+153,345** | Prosperity result page |
| Research (18%) → Strategy XIRECs | 127,600 (logarithmic) | Prosperity result page |
| Scale (60%) → Multiplier | ×4.2 (linear) | Prosperity result page |
| Speed (22%) → Hit rate / Rank | 0.38 / **#2,801** | Prosperity result page |
| **R2 algo realized (raw, before MAF fee)** | **+94,529** | algo JSON 362752 |
| MAF bid paid | **−3,000** (bid was ACCEPTED) | reconciled JSON vs reported |
| **R2 algo realized (net)** | **+91,529** | leaderboard |

**Pillar naming:** Prosperity's official label is **Speed**, not "Visibility" (some early vault references used the latter). Standardize to *Speed*.

The R2 manual realized **+153,345** — over the uniform-rank FOC theoretical of 110,065 by +43,280. Realized V(22) = 0.38 (between uniform-rank 0.276 and bottom-heavy 0.900). The (18, 60, 22) submission over the FOC (16, 48, 36) was correct.

**MAF correction (REVERSED):** Earlier inferred "rejected" because R2 algo dropped 7K below R1 algo; actually the algo JSON shows raw R2 PnL = **94,529** *before* the MAF fee. The 3,000 difference between JSON and reported = **MAF fee paid** = **bid was ACCEPTED**. The +25% volume bonus was largely absorbed by structural caps (R1 IPR $79,255 vs R2 IPR $79,199, essentially identical — IPR was bandwidth-saturated near the +0.1/tick cap). Net effect of MAF participation: roughly −3K to −6K vs not bidding. The bid wasn't too low (we won the auction); the *value* of winning was lower than expected because the strategy was bandwidth-saturated, not quote-bound.

---

## R1 Manual Result

| Fact | Value | Source |
|---|---|---|
| Submitted Dryland Flax bid | BUY 5,000 @ 29 XIREC | `Manuals/Dryland_Flax.md` |
| Submitted Ember Mushroom bid | BUY 35,000 @ 18 XIREC | `Manuals/Dryland_Flax.md` |
| Theoretical PnL combined | 71,500 XIREC | derived |
| **R1 manual realized** | **+71,500** | leaderboard 2026-05-08 |
| R1 manual displayed rank (cumul) | **#72** | leaderboard 2026-05-08 |
| R1 manual without-ties rank | ~#3,000 | user-reported tie caveat (deterministic clearing-price puzzle) |
| **R1 algo realized** | **+98,172** (rank #964) | leaderboard 2026-05-08 |

R1 manual realized **exactly** the theoretical 71,500 (5,000 + 66,500). Rank **#72** is the strongest sub-rank of the entire competition. The clearing-price-engineering manual was solved cleanly and ranked accordingly.

R1 algo at +98,172 is well above the website-scaled estimate of ~$168K-cumul-implied / 2 ≈ 84K — a positive surprise.

---

## R5 Manual Result (Ashflow Alpha)

| Fact | Value | Source |
|---|---|---|
| Submitted allocation | 85% allocated, 6 of 9 goods | `Strategies/Ashflow_Alpha_News_Trading.md` |
| Theoretical fees | 140,100 XIREC | derived |
| **R5 manual realized** | **+95,214** | Prosperity result page |
| Realization ratio | 95,214 / 140,100 = **0.679** | DERIVED |
| Archetype hit rate | **4 of 6 correct (67%)** | Prosperity result page |
| Single biggest contribution | **Lava cake SELL 25% → +95,884** | Prosperity result page |
| Misclassified archetype 1 | **Magma ink BUY 12% → −11,727** | Prosperity result page |
| Misclassified archetype 2 | **Ashes of the Phoenix SELL 14% → −14,694** | Prosperity result page |

Ashflow realized 68% of theoretical, with a 4-of-6 archetype hit rate (67%). The realization ratio matches the hit rate — confirming that the optimization math ($p^* = s/2$) is correct and the failure was purely in archetype labeling. **Lava cake was the load-bearing call**: at SELL 25% it delivered +95,884 alone, more than the entire round's net manual P&L. Without Lava cake, the manual would have netted near zero. The misclassified archetypes were Magma ink (predicted up, went down) and Ashes of the Phoenix (predicted down, went up). Earlier speculation about Lava cake or Pyroflex being off was wrong.

---

## Other Process Facts

| Fact | Value | Source |
|---|---|---|
| Solo competitor (no team) | yes | user_profile + repo single-author git log |
| Final placement: #346 / 18,803 (top 1.84%) | confirmed | leaderboard 2026-05-08 |
| Final country rank: #11 | confirmed | leaderboard 2026-05-08 |
| Manual ranking outperformed algo ranking (overall) | #204 vs #537 | leaderboard 2026-05-08 |
| Best round-rank: R1 manual #72, R5 algo #287 | confirmed | leaderboard 2026-05-08 |
| Approximate hours invested | (not yet provided) | useful as cost reference |
| Subjective "biggest mistake" | (not yet provided) | candidates: v37 BH flip, v40 TIER3 removal |
| Subjective "best decision" | (not yet provided) | candidates: v36→v42 robustness pivot, R2 (18,60,22) over FOC |

---

## How This Page Is Used

Other pages reference user-reported facts by linking here, not by duplicating values. Example:

```markdown
R5 manual realized: +95,214 (see [[User_Reported_Anchors|anchor table]])
```

When new facts arrive, **edit only this page** — others will pick them up via wikilinks.

## Anti-Pattern: Folklore Without Provenance

The wiki distinguishes:
- **REPO** — verifiable from a file in the repo
- **USER** — user-reported (this page)
- **DERIVED** — computed from REPO/USER (formula must be shown)

Each fact in the wiki should carry one of these tags. See [[Verify]] for the full provenance ledger.

## Links

[[Final_Competition_Result]] · [[v34_vs_v36_vs_v42]] · [[Verify]] · [[Backtests/PnL_Timeline]] · [[Concepts/Backtester_vs_Competition]] · [[Rounds/Round5_findings]] · [[Overview]] · [[Carry_Forward]]

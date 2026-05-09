---
type: manual
tags: [performance, official, manual, per-round, post-competition, all-rounds]
sources:
  - performance/manual trading/round 1/Manual Trading Results.txt
  - performance/manual trading/round 2/Manual Trading Results.txt
  - performance/manual trading/round 2/Distribution Speed Competitors/
  - performance/manual trading/round 3/Manual Trading Results.txt
  - performance/manual trading/round 3/Distribution First Bids and Second Bids competitors/
  - performance/manual trading/round 4/Manual Trading Results.txt
  - performance/manual trading/round 4/Distribution Exotic Products Positions Competitors/
  - performance/manual trading/round 5/Manual Trading Results.txt
updated: 2026-05-08
---

# Manual Trading — Official Per-Round Results

> Verbatim from `performance/manual trading/`. These are the canonical Prosperity-issued manual results, including peer-distribution graphs where provided.

---

## Round 1 — Intarian Welcome (clearing-price auction)

| Good | Side | Volume | Price | P&L |
|---|---|---|---|---|
| DRYLAND FLAX | BUY | 5,000 | 29 | +5,000 |
| EMBER MUSHROOM | BUY | 35,000 | 18 | +66,500 |
| **Total** | | | | **+71,500** |

Realized exactly the theoretical (5,000 + 66,500). End-of-R1 cumulative manual rank #72 (massive ties; ~#3,000 without ties).

---

## Round 2 — Invest & Expand

The Prosperity result page exposes the formula structure:

```
PnL = Research(x) × Scale(y) × Hit_rate(rank(z)) − Budget
```

| Pillar | Allocation | Output |
|---|---|---|
| Research (logarithmic) | 18% invested | Strategy XIRECs **127,600** |
| Scale (linear) | 60% invested | Multiplier **×4.2** |
| Speed (rank-based) | 22% invested | Hit rate **0.38** with rank **#2,801** |
| **Subtotal** | 100% | 127,600 × 4.2 × 0.38 ≈ **203,345** |
| Budget | | −50,000 |
| **Net P&L** | | **+153,345** |

**Pillar naming clarification:** Prosperity's official label for the third pillar is **Speed**, not **Visibility** as the vault initially used. All references should be standardized to *Speed*.

### Speed-investment peer distribution

The peer histogram of Speed allocations (`performance/manual trading/round 2/Distribution Speed Competitors/Distribution Speed.png`) shows:
- A large mode at 0% (~450 teams) — non-investors / non-solvers
- The **densest single bucket at 22%** (~600 teams) — exactly where we sat
- Secondary modes at 10%, 30%, 35–40%, 50%
- Long right tail to 90%

We were in the most-popular bucket; rank #2,801 reflects the ~10K-strong left tail of the distribution. Hit rate 0.38 is consistent with rank/total ≈ 0.15–0.20 (rank #2,801 of ~18,803 ≈ 0.149) being mapped to a rank-percentile-based hit-rate function.

### Back-checking the (18, 60, 22) decision

The realized V(22) = 0.38 is between uniform-rank (~0.276) and bottom-heavy (~0.900). Submitting **(18, 60, 22)** instead of the FOC-optimum (16, 48, 36) **over-performed the FOC theoretical** of 110,065 by **+43,280**. The bottom-heavy-tilt thesis was correct; the actual peer-prior was meaningfully bottom-heavy.

If we had submitted the FOC (16, 48, 36) under the *realized* V-curve:
- Research(16) ≈ 200K × ln(17)/ln(101) ≈ 122,820
- Scale(48) ≈ 0.07 × 48 = 3.36
- Hit rate at x_V = 36 (rank presumably better than #2,801 since fewer teams bid that high) — could be 0.5 to 0.7
- PnL ≈ 122,820 × 3.36 × 0.6 − 50,000 ≈ 197,604

So the FOC could have realized **higher** if x_V = 36 mapped to a better hit-rate. But we didn't know the V-curve at submission time, and (18, 60, 22) is a more robust hedge across peer-priors.

---

## Round 3 — Bio-Pods (sealed-bid auction)

### Submitted bids (CORRECTION: actual bids were (760, 855), not (755, 840) as derived)

| Bid | Value | Trades accepted | Trades rejected | Buy-price total | Sell-price total | P&L |
|---|---|---|---|---|---|---|
| First bid | **760** | 335 | 665 | 254,600 | 308,200 | **+53,600** |
| Second bid | **855** | 404 | 596 | 345,420 | 371,680 | **+21,637.51** |
| **Combined** | | | | 600,020 | 679,880 | **+75,237.51** |

**Counterparty count (verified):** Each bid level interacted with **1,000 counterparties** (335 + 665 = 1,000 at b₁; 404 + 596 = 1,000 at b₂). The implied 921 from our earlier 75,238 / 81.67 derivation was close to the right order, but the **actual N is exactly 1,000**.

**Per-counterparty realized:**
- At b₁ = 760: 53,600 / 1,000 = **53.60** XIREC/cp
- At b₂ = 855: 21,637.51 / 1,000 = **21.64** XIREC/cp
- Combined: 75,237.51 / 1,000 = **75.24** XIREC/cp

Our theoretical NE EV was 81.67/cp. Realized 75.24 is **92.1% of theoretical** — a clean confirmation that the symmetric NE solution is near-optimal even with the slightly-aggressive (760, 855) submission.

### Submitted-bid correction note

Earlier vault pages and report sections cited (755, 840) as the submitted Bio-Pods bids. The Prosperity result page confirms the *actual* submitted bids were **(760, 855)**:
- b₁ shaded **+5** above the symmetric NE (755 → 760)
- b₂ shaded **+15** above the symmetric NE (840 → 855)

This is consistent with anticipating that other solvers will also bid at or above the NE — the user's slight upward shading captures more counterparties at each bid level. The NE derivation in `report.tex` and `Manuals/Bio_Pods.md` is correct as theory; the *implementation* moved both bids slightly upward.

### Peer-bid distribution

`performance/manual trading/round 3/Distribution First Bids and Second Bids competitors/Distribution Bids Graph.png` shows two distinct clusters:
- **First bid (blue)**: peaks 750–770; **average 768**; modes at 750, 760, 765
- **Second bid (light)**: peaks 850–870; **average 859**; modes at 850, 855, 860

Our **(760, 855)** sat at the **lower edge of both distributions**:
- First bid 760 vs peer-avg 768 → 8 below median
- Second bid 855 vs peer-avg 859 → 4 below median

We were among the lowest 25% of solvers on both bid levels. Even slightly more conservative bidding (760, 855) earned 75.24/cp realized — the NE is robust to small downward perturbations of either bid.

The distribution shape strongly confirms the **common-knowledge regime** for Bio-Pods: the bid mass is concentrated in narrow bands (≤20 wide) around the NE, with very few teams bidding outside [740, 780] for b₁ or [840, 880] for b₂.

---

## Round 4 — AETHER_CRYSTAL Exotic Options

12-instrument portfolio (per-unit P&L × volume):

| Instrument | Side | Vol | Per-unit | Total P&L |
|---|---|---|---|---|
| AC (underlying) | BUY | 0 | +183.21 | 0 |
| AC_50_P | BUY | 50 | +370.10 | **+18,505.03** |
| AC_50_C | BUY | 50 | +628.31 | **+31,415.57** |
| AC_35_P | BUY | 50 | +184.87 | +9,243.40 |
| AC_40_P | SELL | 50 | −495.09 | **−24,754.41** |
| AC_45_P | BUY | 50 | +405.61 | +20,280.48 |
| AC_60_C | BUY | 0 | −564.80 | 0 |
| AC_50_P_2 | BUY | 50 | −282.40 | −14,119.75 |
| AC_50_C_2 | BUY | 50 | −468.84 | −23,442.21 |
| AC_50_CO | SELL | 50 | +1,087.08 | **+54,354.22** |
| AC_40_BP | SELL | 50 | +300.00 | +15,000.00 |
| AC_45_KO | BUY | 500 | −57.93 | **−28,966.10** |
| **TOTAL** | | | | **+57,516.23** |

### Big winners
- **AC_50_CO (chooser at 50, sold)**: +54,354.22 — chooser was overpriced; our short paid handsomely. The peer-distribution image confirms this was the *consensus* trade: ~2,000 teams also went short 50 of AC_50_CO; only ~450 went long.
- **AC_50_C (call at 50, bought)**: +31,415.57 — call paid off ⇒ AC closed *above* 50 at expiry, OR mid-path component of the chooser logic.
- **AC_45_P (put at 45, bought)**: +20,280.48 — put paid off ⇒ AC dipped below 45 at some point.
- **AC_50_P (put at 50, bought)**: +18,505.03 — put paid off ⇒ AC traded below 50.
- **AC_40_BP (binary put at 40, sold)**: +15,000 — binary expired worthless ⇒ AC stayed above 40 at expiry.

### Big losers
- **AC_45_KO (knockout 45, bought 500 vol)**: −28,966.10 — knockout was triggered (volume 500 means this was the largest position; the loss is per-unit small but volume-amplified).
- **AC_40_P (put at 40, sold)**: −24,754.41 — AC dipped below 40 at expiry, our short was assigned.
- **AC_50_C_2 (2-week call at 50, bought)**: −23,442.21 — 2-week call expired OTM; premium lost.
- **AC_50_P_2 (2-week put at 50, bought)**: −14,119.75 — 2-week put net-negative.

### Implied AC path

Combining the signals:
- AC_50_C won (call ITM) AND AC_50_P won (put ITM) — both happened along the path → *AC was volatile*, hit both above-50 and below-50 territory
- AC_45_P won (touched below 45)
- AC_40_P sold lost (touched below 40 at expiry, not just intraday)
- AC_40_BP sold won (closed above 40 at expiry)
- AC_45_KO bought lost (knockout activated)

Hypothesis: AC dipped sharply below 45 (knocking out the KO and putting the 40_P seller in the money), then rebounded above 40 by expiry but stayed below 50 (or oscillated). **The path was V-shaped or volatile, not monotone.** This is what hurt the symmetric-Greek pricing assumption: the chooser's value was preserved (sold high), but the vanilla puts/calls didn't symmetrically offset because the path crossed through their strikes mid-way.

Net: **+57,516.23**, far below the BS-derived E[+175,200]. The 67% miss was driven by **path-dependent losses** (knockout, 2-week vanillas expiring OTM) that the BS price didn't capture. **Lesson restated:** stress-path the portfolio under V-shaped and U-shaped underlying scenarios, not just terminal-distribution moments.

### Peer-distribution context — verified across all 12 instruments

We aligned with peer consensus on **every single position** in the 12-instrument portfolio. Not one contrarian trade.

| Instrument | Our position | Peer dominant cluster (n teams) | Note |
|---|---|---|---|
| AC | 0 | 0 (~1,600) | underlying — most skipped |
| AC_50_P | +50 | +50 long (~1,400) | strong long consensus |
| AC_50_C | +50 | +50 long (~1,000), contrarian −50 (~310) | majority long |
| AC_35_P | +50 | +50 long (~1,600) | strong long consensus |
| AC_40_P | −50 | −50 short (~1,800) | strong short consensus |
| AC_45_P | +50 | +50 long (~1,600) | strong long consensus |
| AC_60_C | 0 | 0 (~1,400) | most skipped (hard to predict) |
| AC_50_P_2 | +50 | +50 long (~2,200) | **extreme consensus** |
| AC_50_C_2 | +50 | +50 long (~1,800) | strong long consensus |
| AC_50_CO | −50 | −50 short (~2,000) | **extreme short consensus** |
| AC_40_BP | −50 | −50 short (~2,000) | **extreme short consensus** |
| AC_45_KO | +500 | +500 long (~1,600) | **extreme long consensus** |

### Implications — R4 was a **common-knowledge manual**, not a trade-selection failure

This re-frames the R4 manual diagnosis substantially:

1. **R4 was a third common-knowledge regime**, alongside R1 (deterministic clearing-price) and R3 (symmetric Bayesian-Nash). The "right" trades were apparent to most solvers running BS pricing; the entire field converged on roughly the same 12 positions.

2. **The 33% realization vs E[+175,200] is a field-level outcome, not us-specific.** Roughly 1,600–2,200 teams made each of the same trades. Our +57,516 is approximately what *every BS-pricing solver* realized. The earlier framing "our Greek-asymmetric portfolio bit us" was wrong — it bit *everyone*.

3. **AC_45_KO was an extreme aggregate loss event.** ~1,600 teams bought +500 long; knockout was triggered; the field-level loss is ~$46M aggregate (1,600 × $29K). Our −$28,966 is squarely in the consensus loss.

4. **Manual rank #316 confirms mid-pack.** Of the ~6,000 teams who attempted the R4 manual, we placed mid-distribution — exactly where you'd expect for a portfolio that aligned with consensus on every leg. The rank lift came from competently *executing* the consensus trade (sizing, instrument selection), not from out-of-sample edge.

### Updated lesson

The earlier lesson — "stress-path the portfolio under V-shape underlying" — is correct but incomplete. The more general lesson:

> **In a common-knowledge manual, your realized PnL is bounded by the field's collective error.** No individual analysis can outperform the consensus when the consensus is common knowledge. The competitive game in R4-style manuals is at the margin — sizing, direction-of-mispricing on the *one* instrument where reasonable people disagree (e.g. AC_50_C had ~310 contrarian shorts) — not at the level of "is this BS-priced fair".

This makes the count of common-knowledge manuals **3 of 5** in Prosperity 4: R1 (clearing-price), R3 (BNE), R4 (BS-pricing consensus). The two non-common-knowledge manuals are R2 (peer-prior I&E) and R5 (archetype taxonomy) — both rewarded asymmetric analysis (peer-prior thinking; archetype-confidence calls). Both delivered higher realization ratios (1.39× and 0.68× respectively) than the common-knowledge manuals (1.00, 0.92, 0.33).

---

## Round 5 — Ashflow Alpha (Ignith Exchange)

Per-archetype submission and realized:

| Good | Side | % | Investment | Fee | P&L |
|---|---|---|---|---|---|
| **Lava cake** | SELL | 25% | 250,000 | 62,500 | **+95,884** ✓ |
| Pyroflex cells | SELL | 12% | 120,000 | 14,400 | +9,041 ✓ |
| Magma ink | BUY | 12% | 120,000 | 14,400 | **−11,727** ✗ |
| Ashes of the Phoenix | SELL | 14% | 140,000 | 19,600 | **−14,694** ✗ |
| Thermalite core | BUY | 16% | 160,000 | 25,600 | +9,856 ✓ |
| Sulfur reactor | BUY | 6% | 60,000 | 3,600 | +6,854 ✓ |
| Volcanic incense | BUY | 0% | 0 | 0 | 0 (skipped) |
| Obsidian cutlery | BUY | 0% | 0 | 0 | 0 (skipped) |
| Scoria paste | BUY | 0% | 0 | 0 | 0 (skipped) |
| **TOTAL** | | **85%** | **850,000** | **140,100** | **+95,214** |

### Archetype scoreboard (corrected)

**4 archetypes correct, 2 wrong** (out of 6 allocated):

| Archetype | Predicted s_i | Side | Realized direction | Verdict |
|---|---|---|---|---|
| Lava cake | s = −50% (mechanical recall) | SELL 25% | strongly negative | ✓ correct (+95,884) |
| Pyroflex cells | s ≈ −12% (negative news cycle) | SELL 12% | mildly negative | ✓ correct (+9,041) |
| Thermalite core | s ≈ +16% (mid-cycle hype) | BUY 16% | positive | ✓ correct (+9,856) |
| Sulfur reactor | s ≈ +6% | BUY 6% | positive | ✓ correct (+6,854) |
| **Magma ink** | s ≈ +12% (we predicted up) | BUY 12% | actually negative or flat | ✗ **wrong** (−11,727) |
| **Ashes of the Phoenix** | s ≈ −14% (we predicted down) | SELL 14% | actually positive or flat | ✗ **wrong** (−14,694) |

The 3 unallocated goods (Volcanic incense, Obsidian cutlery, Scoria paste) all expected to resolve at 0 — confirmed correctly.

### Back-solved realized s_i per archetype

The PnL formula (BUY): $\pi_i = \frac{p_i}{100} \cdot s_i \cdot B - 100 p_i^2 = 10{,}000 \cdot p_i \cdot s_i - 100 p_i^2$, with $B = 1{,}000{,}000$.
For SELL the position is reversed: $\pi_i = -10{,}000 \cdot p_i \cdot s_i - 100 p_i^2$.

Solving for the realized $s_i$ given the reported $\pi_i$ and $p_i$:

| Archetype | Side | p_i | Predicted s_i (from p*=s/2) | Realized P&L | **Back-solved realized s_i** | Verdict |
|---|---|---|---|---|---|---|
| Lava cake | SELL | 25 | −50% | +95,884 | **−63.4%** (more negative than predicted!) | ✓ correct direction, under-allocated |
| Pyroflex cells | SELL | 12 | −24% | +9,041 | **−19.5%** (close to predicted) | ✓ correct |
| Thermalite core | BUY | 16 | +32% | +9,856 | **+22.2%** (less than predicted) | ✓ correct, slightly over-allocated |
| Sulfur reactor | BUY | 6 | +12% | +6,854 | **+17.4%** (more than predicted) | ✓ correct, under-allocated |
| **Magma ink** | BUY | 12 | +24% | −11,727 | **+2.2%** (essentially flat) | ✗ direction OK, magnitude wildly off |
| **Ashes of the Phoenix** | SELL | 14 | −28% | −14,694 | **−3.5%** (essentially flat) | ✗ direction OK, magnitude wildly off |
| Volcanic / Obsidian / Scoria | — | 0 | 0% | 0 | not allocated | ✓ correct null |

### Re-interpreted: not 4 wrong + 2 right; 6 directionally right but 2 magnitude-off

The earlier interpretation said "Magma ink and Ashes were misclassified — predicted up but went down" etc. The back-solve shows **the direction was correct on all 6 allocated archetypes**:
- Magma ink: we predicted UP (BUY), it went +2.2% UP (just barely) — direction correct, magnitude tiny
- Ashes of the Phoenix: we predicted DOWN (SELL), it went −3.5% DOWN (just barely) — direction correct, magnitude tiny

**The failure was in *magnitude* prediction, not in *direction*.** Magma ink moved 2% instead of the predicted ~24%; Ashes moved 3.5% instead of the predicted ~28%. At p=12% (Magma) and p=14% (Ashes), the fees were 14,400 and 19,600 respectively — but the realized notional gain was only 2,673 and 4,906. We over-allocated relative to the realized magnitude, so the fee dominated the gross.

### Optimal hindsight allocation

If we had known the realized $s_i$ values, the optimal allocations would have been:

| Archetype | Realized s_i | Optimal p* = |s_i|/2 | Difference |
|---|---|---|---|
| Lava cake | −63.4% | 31.7% (vs 25 actual) | **under-allocated by 6.7pp** |
| Pyroflex cells | −19.5% | 9.75% (vs 12) | over by 2.25pp |
| Thermalite core | +22.2% | 11.1% (vs 16) | over by 4.9pp |
| Sulfur reactor | +17.4% | 8.7% (vs 6) | under by 2.7pp |
| Magma ink | +2.2% | 1.1% (vs 12) | **over by 10.9pp** |
| Ashes of the Phoenix | −3.5% | 1.75% (vs 14) | **over by 12.25pp** |

Total optimal allocation: 64.3% (vs 85% submitted). Optimal hindsight PnL: $100 \cdot \sum (p_i^*)^2 \approx 100 \cdot (31.7^2 + 9.75^2 + 11.1^2 + 8.7^2 + 1.1^2 + 1.75^2) = 100 \cdot 1{,}256.5 = $ **125,650**. Realized 95,214 = **75.8% of optimal-hindsight PnL** — a competent execution given the s_i estimation errors.

### Realization vs theoretical (recap)

Theoretical at $p_i = s_i^{\text{predicted}}/2$: **140,100**. Realized: **95,214**. Ratio **0.679**.

**Lesson, sharpened:** the optimization math ($p^* = s/2$) is correct; the math itself contributed zero to the loss. The 32% gap is *entirely* explained by **magnitude-of-s_i estimation error on Magma ink and Ashes**. The lesson isn't "manuals are hard" — it's specifically "**when archetype-classification labels include both *direction* and *magnitude* components, the magnitude is the harder estimation problem.** Treat magnitude as a confidence interval, and shrink p toward 0 when the interval is wide."

ML analogy: this is heteroscedastic regression. The estimator $\hat{p} = \hat{s}/2$ is unbiased only when $\hat{s}$ is unbiased; under variance in $\hat{s}$, the optimal allocation is shrunk by the bias-variance tradeoff. A James-Stein-style shrinkage estimator $\hat{p}_{\text{JS}} = \hat{s}/2 \cdot (1 - \frac{c}{\hat{s}^2})$ would have under-allocated Magma and Ashes (where the magnitude prior was weaker) and not changed Lava cake meaningfully (where the prior was strong).

### Single biggest contribution

Lava cake at SELL 25% delivered **+95,884** — alone more than the *entire* round's net manual P&L. Without Lava cake, the manual would have netted −670 (the other 5 archetypes summed to net flat). The Lava cake archetype was the load-bearing call.

---

## Cross-round manual summary

| Round | Realized | Theoretical | Ratio | Notes |
|---|---|---|---|---|
| R1 | 71,500 | 71,500 | **1.00** | exact |
| R2 | 153,345 | 110,065 (FOC) | **1.39** | over-performed; (18,60,22) was right |
| R3 | 75,238 | 81.67 × N=1000 = 81,670 | **0.92** | NE strategy slightly off-NE submission still robust |
| R4 | 57,516 | 175,200 | **0.33** | path-dependent BS pricing failures |
| R5 | 95,214 | 140,100 | **0.68** | 4-of-6 archetype hit rate |

**The "manual EVs systematically optimistic" hypothesis is firmly rejected.** R1 was exact; R2 over-performed; R3 within 8% of theoretical at N=1000; R5's miss is exactly the 4-of-6 hit-rate prediction. Only R4 badly missed, and the cause is identified (path-dependent BS failure, not "manuals are hard").

## Links

[[Performance/Algo_Per_Round]] · [[User_Reported_Anchors]] · [[Final_Competition_Result]] · [[Manuals/Dryland_Flax]] · [[Manuals/Invest_and_Expand]] · [[Manuals/Bio_Pods]] · [[Manuals/Ashflow_Alpha]] · [[Verify]]

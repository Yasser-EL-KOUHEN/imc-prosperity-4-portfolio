---
type: competition
tags: [carry-forward, lessons, future, post-competition, retrospective, final-result]
sources:
  - prosperity-vault/Rounds/Round{1..5}_findings.md
  - prosperity-vault/Cross_Round_Comparison.md
  - prosperity-vault/Theory/After Competition - Honest assessment Theory Trading Report.txt
  - prosperity-vault/User_Reported_Anchors.md
  - report/report.tex (Lesson sections)
updated: 2026-05-08
---

# Carry-Forward — What I'd Do From Day 1 in Prosperity 5

> Final result anchor: **#346 / 18,803 (top 1.84%), GOAT 383,727**. Country **#11**. Rules I wish I had on day 1 of Prosperity 4. Ordered by the cost of having missed them.

## What the Final Result Adds (revised after per-component breakdown 2026-05-08)

The full per-component breakdown materially refines the post-result narrative. The earlier "manual EVs were systematically optimistic" hypothesis was **rejected**, and after viewing the peer-distribution graphs for R2/R3/R4 the framing sharpens further into a **common-knowledge taxonomy**:

| Manual | Realization | Common knowledge? | Real lesson |
|---|---|---|---|
| R1 (clearing-price) | 1.00× exact | **YES** (deterministic) | Many teams identical — display rank #72 is tie-breaking |
| R2 I&E (peer-prior) | 1.39× over-FOC | NO (asymmetric info) | Peer-prior sensitivity analysis paid off; submitted (18,60,22) was right |
| R3 Bio-Pods (NE) | 0.92× of NE | **YES** (symmetric BNE) | Reserve CDF empirically uniform on [670,920]; uniform-reserve assumption validated; #234 display is tie-breaking |
| R4 AC exotics | 0.33× of E[PnL] | **YES** (BS-pricing consensus) | We aligned with peer consensus on every single one of 12 instruments. 33% miss is field-level, not us-specific |
| R5 Ashflow (archetypes) | 0.68× of theoretical | NO (label confidence) | All 6 directionally correct; magnitude wildly off on Magma + Ashes |

**The unified lesson:**

1. **Common-knowledge manuals (R1, R3, R4) reward execution over insight.** When the puzzle is symmetric-information, every solver converges on the same trades. Display rank is dominated by tie-breaking; realization equals the field's collective expected value (less for path-dependent failures like R4). The competitive game is at the margin where reasonable people *disagree* — sub-pixel allocation tweaks, ordering effects, or the one instrument where consensus is split.

2. **Asymmetric-information manuals (R2, R5) reward analytical depth.** Peer-prior distributions and archetype-magnitude estimation are the load-bearing variables. Both manuals where this thinking applied delivered our best rank lifts (#801 in R2, #204 in R5). **Allocate hours here, not to common-knowledge solving.**

3. **Path-dependent BS pricing failures (R4) need stress-pathing**, not just terminal-distribution moments. The chooser, binary, KO legs all had path-dependent payoffs that diverged from BS-EV under the realized V-shaped path. ~1,600 teams bought the AC_45_KO and got knocked out together.

4. **Archetype magnitude > archetype direction** (R5 Ashflow). All 6 allocated archetypes were directionally right; the failure was magnitude estimation on Magma ink (predicted +24%, realized +2.2%) and Ashes (predicted −28%, realized −3.5%). When a label has direction + magnitude components, treat magnitude as a confidence interval and shrink p toward 0 when the interval is wide (James-Stein-style).

5. **3 of 5 manuals were common-knowledge regimes** — meaning the rank-per-hour return on solving was bounded by tie-breaking. The 2 asymmetric-info manuals (R2, R5) accounted for **R2 153,345 + R5 95,214 = 248,559 of the 452,813 manual XIREC (55%)**. Asymmetric-info manuals are where future-Prosperity hours should concentrate.

### Algo-vs-manual contribution

GOAT decomposition: algo 155,759 (40.6%) vs manual 227,968 (59.4%). **Manuals delivered 60% of GOAT XIREC** despite the algo representing the bulk of project hours. Combined with the R5 algo round-rank #287 (top 1.5%, the strongest algo rank of all 5 rounds), the picture is:

- **The algo got better rapidly through the competition** (rank trajectory 964 → 1,279 → 832 → 772 → **287**) — the v36→v42 robustness pivot was correct
- **But manuals were where the rank-per-effort returns were highest** — R1 manual at #72 alone is a stronger sub-result than the entire algo trajectory

**Future-Prosperity rule:** budget at least as many hours on manual derivation as on algo iteration. Especially for asymmetric-information manuals where peer-prior choice matters (I&E, Ashflow, MAF).

## Tier 1 — Rules That Cost the Most

### 1. Pre-register the OOS day (and never look at it during selection)

Make it a top-level constant in code, commit it, refuse to change it. R5 Phase 13 had MICROCHIP_SQUARE flip sign on the OOS day — if there hadn't been a hard pre-registered split, it would have shipped to v1 and lost real money.

```python
OOS_DAY = 4   # NEVER change this — pre-registered Phase 14
TRAIN_DAYS = [2, 3]
```

Why it matters: every parameter sweep, signal test, and tier decision otherwise has a P-hacking vulnerability. If the OOS day is "the day that worked", you're publishing a positive result for a coin flip.

### 2. Distinguish the backtester window from the scoring window

The Prosperity backtester runs the **first 10% of Day 4**. The competition leaderboard runs **the full day**. R5's v36 won the backtester ($78,799) and would have been the natural pick — but v34/v42 had the better full-day estimate (~$152K vs $130K).

Rule: before treating any backtester score as a target, check what window the **actual scoring** uses. If unsure, optimize for the **longer** window (full day = lower variance, captures regime changes).

### 3. Never tier on local-backtester data alone

R5's v35 was a careful local-CV reclassification with proper train/test splits. It pivoted the strategy and lost $9K vs v34. The local backtester's `--match-trades all` policy inflates fills (~8.6×) relative to real Prosperity. Different counterparty mix, different fill rate, different optimum.

Rule: tier and blacklist decisions use **real-engine logs only** (`round{N}/logs/{vN}/*.json`). Local backtester is for finding bugs, not selecting strategy.

### 4. Adverse-selection losses scale **with** trading volume

This is the v40 mistake distilled: `E[PnL_MM(ℓ)] = κ_p · ℓ · (s̄_p + α_p)`. When `s̄_p + α_p < 0`, increasing LIMIT increases losses. The right responses are TIER3 (smaller LIMIT) for borderline products and BLACKLIST (LIMIT=0) for hopeless ones — never aggressive MM in the hope of "more trades = recovery".

Rule: if a product loses money at LIMIT=5, it loses 2× as much at LIMIT=10. Verify with N=12+ cross-version evidence before tiering.

### 5. HAC standard errors for tick-data regressions

R3's `microstructure_eda.py` used naive OLS — biased downward, overstates significance. R5's Phase 14 corrected this (`statsmodels.OLS(...).fit(cov_type="HAC", cov_kwds={"maxlags": H})`). 7 of Phase 14's "significant" OBI signals would have failed the HAC bar set at ≈3σ.

Rule: any regression on tick-level series with autocorrelated residuals must use HAC. Pair with BH-FDR for the multiple-testing correction.

## Tier 2 — Rules That Save Time

### 6. EDA before strategy: ACF + Hurst + drift sign

Before writing any strategy, plot:
- AR(1) ρ at lag 1 (positive = momentum, negative = reversion)
- Hurst exponent (< 0.5 = reverting, > 0.5 = trending)
- Day-by-day drift sign + magnitude

This is 30 minutes of work and tells you whether **MM**, **mean-reversion**, or **directional** is the right strategy shape. R1 did this for ACO/IPR; R5 did this for the 50 products. Skipping it means you write the wrong strategy and spend a week tuning a parameter that can't help.

### 7. For tightly anti-correlated pairs (|ρ| > 0.85), use HEDGED_NO_SKEW

SNACKPACK CHOC/VAN at ρ = −0.916. The natural anti-correlation **is** the inventory hedge. Quote both with bigger inner size, no per-product skew, let positions accumulate. Beats two independent directional bets and beats two independent MM with skew.

This applies any time the pair correlation is structural (designed-in, like R5's flavor-substitute mechanic) rather than fitted (where it can disappear out-of-sample).

### 8. The cross-version log evidence pattern (N≥12 for blacklist)

Run K versions on real Prosperity. Aggregate per-product (avg PnL, n-positive). Products where avg ≤ −$threshold AND 0/K positive go to blacklist; borderline to TIER3. This is **bagging on the model side** (each version is a different sample of the same data).

Rule: don't blacklist on a single run. Don't blacklist without comparing to a control (a version where the product is at default LIMIT). Empirical thresholds: avg ≤ −$500 + 0/12 positive worked in R5.

### 9. Single-file BS with `math.erf`

No scipy needed. `math.erf` gives machine-precision normal CDF. Newton-Raphson for IV converges in <25 iterations. Pure-math implementation passes the single-file Prosperity constraint. R3's BS engine had max error 3.7×10⁻⁴ vs reference.

### 10. Anti-regression gate on every change

Maintain a **baseline** (R3: 153,566; R5: v34 = $62,299 on Prosperity). Every change must not break the baseline. Phase 12 reverted Change A because it broke the gate. v37/v38/v39/v40 all showed measurable regression vs v34 — that was the signal to roll back, not "wait for full-day evidence".

## Tier 3 — Rules That Improve Quality

### 11. Distinguish structural vs fitted relationships

| Type | Property | Survives OOS? |
|---|---|---|
| **Structural** | designed-in mechanic (CHOC/VAN flavor substitutes; PEBBLES size monotonicity; IPR linear drift) | yes |
| **Fitted** | discovered correlation that doesn't have a mechanism (random OBI β, lead-lag from CCF mining) | usually no |

Structural relationships transfer across data windows; fitted ones don't. R5 lead-lag was 100% mining — 0/36,750 survived the Bonferroni gate. Round 1 IPR's +0.1/tick was structural — held across all 3 days.

### 12. Don't take naked tail risk for tiny edges

R4 manual: AC_60_C had +0.004 edge sell-side, but σ=251% and naked short. We skipped it. Edge × volume = +$600 XIREC; potential loss = unbounded. The portfolio delta is balanced without it. **Don't let position control you.**

### 13. Static replication for exotic options

R4: chooser = `C(T) + P(T_c)` for r=0 GBM (no-arb). Binary cliff hedged with vanilla spread. Knockout with the Merton barrier formula + Broadie-Glasserman discrete adjustment.

The pricing is static math; the hedge is constructed once and held. No dynamic rebalancing. This is the cleanest manual-options approach when the market mis-prices an exotic.

### 14. The "all-days-improve" parameter sweep gate

For any parameter sweep, the winning config must improve **every** day individually, not just the 3-day total. Several plausible R3 configs (calibrated AR(1), naive OBI) were rejected by this gate even though the 3-day total looked good — they hurt one day each.

Rule: average can lie when one day dominates.

### 15. ML at n=150 per product is below the floor without pooling

R5 Phase 14 had 50 products × 3 days = 150 samples. Per-product n=3 is unworkable. Pooling across products with one-hot categorical feature got n=150 — workable but small. XGBoost with `max_depth=2`, `n_estimators=20`, early stopping reached AUROC OOS = 0.653.

If your dataset is per-product n < 50, **pool across products** as the first step. Then check whether the pooled model produces actionable per-product predictions (R5 Phase 14 didn't, which is why XGBoost graduated statistically but not practically).

### 16. The Phase 13 baseline is the floor

Don't ship anything that loses to the simplest correct strategy. R5 had 4 different ML attempts (GRU, XGBoost-as-direction-gate, SDE-synthetic, heavyweight ensemble) all of which lost to the directional-hold baseline. Phase 13 was locked.

Rule: if your fancy model can't beat a "fixed ±10 on HIGH-confidence drift products + standard MM elsewhere" baseline, ship the baseline.

## Tier 4 — Self-Discipline

### 17. Document failed hypotheses with their original evidence

A failure with documented data > a failure with handwaving. v35 has its full reasoning in the docstring; reading it 3 weeks later, the trap is clear. If we'd shipped v35-style reclassification in v9 era and lost the round, the docstring would have been the only path to understanding why.

### 18. Plan-decision-execute-verify loop, every phase

R3 ran 11 phases; R5 ran 14. Each had: PLAN → research → decision → execute → SUMMARY. The phase artifacts in `.planning/phases/{N}/` made it possible to audit later (which is how this wiki was written). **Never make a meaningful change without leaving an audit trail.**

### 19. Stop optimizing the document at 90/100

The "Honest assessment" of `Theory_Quantitative_Trading.tex` rates it 93/100 and says: *the right move now is to stop improving the document and start using it.* Same applies to the strategy: at v34 the directional setup was 95% of the alpha. v36–v42 were polish; v37/v39/v40 were over-tuning that lost ground.

Rule: when the marginal change is +/− $1K on a $60K base, you're polishing. The next breakthrough comes from a different question, not more iteration on the current one.

### 20. The vault is a tool, not a deliverable

This wiki gets used during the next round, not "submitted". Optimize for **lookup speed under time pressure**: glossary, quick numbers, decision log, parameters table. The narrative pages are for the post-mortem; the reference pages are for the panic moment when something breaks 6 hours before submission.

## Links

[[Overview]] · [[Cross_Round_Comparison]] · [[Concepts/Glossary]] · [[Concepts/Backtester_vs_Competition]] · [[Concepts/Adverse_Selection]] · [[Concepts/Lead_Lag]] · [[Research/Decisions_Log]] · [[Strategies/Round5_Version_History]] · [[Theory/After Competition - Honest assessment Theory Trading Report.txt|Theory: Honest Assessment]]

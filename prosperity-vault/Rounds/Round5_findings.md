---
type: round
tags: [round5, complete, post-mortem, directional, blacklist, hedged, ml-deadends, final-result]
sources:
  - round5/README.md
  - round5/strategies/round5_v42_trader.py
  - round5/research/full_day_optimal.py
  - round5/research/drift_audit.py
  - round5/research/lead_lag.py
  - round5/research/pairs_analysis.py
  - round5/research/analyze_prosperity_logs.py
  - round5/plots/full_day_optimal.csv
  - round5/plots/drift_audit.csv
  - round5/plots/lead_lag/lead_lag_pairs.csv
  - round5/plots/within_category_xcorr_summary.csv
  - .planning/phases/13-r5-directional-trading/
  - .planning/phases/14-r5-strategy-deepening/
  - log.md (2026-04-29 → 2026-04-30 entries)
  - prosperity-vault/User_Reported_Anchors.md (final leaderboard)
updated: 2026-05-08
---

# Round 5 — "The Final Stretch" (Post-Mortem)

**Status:** Complete · **Submitted version:** `round5/strategies/round5_v42_trader.py` · **Position limit:** ±10 (all 50 products) · **Days in data:** 2, 3, 4 (day 5 = competition)

## Final Result (received 2026-05-08)

| Metric | Value |
|---|---|
| **R5 GOAT contribution** | **153,125 XIREC** (algo + Ashflow Alpha manual combined) |
| Cumulative GOAT after R5 | 383,727 XIREC |
| **Final overall rank** | **#346 / 18,803** (top 1.84%) |
| Algorithmic / Manual / Country | #537 / #204 / #11 |

### Algo / manual breakdown (verified)

| Component | Realized PnL |
|---|---|
| **R5 algo (v42)** | **+57,911** |
| R5 manual (Ashflow Alpha) | +95,214 |
| R5 round total | 153,125 |

**End-of-R5 cumulative ranks (FINAL):** Overall **#346** · Algo **#537** · Manual **#204** · Country **#11**.

The R5 contribution (153,125) exceeded both R3 (116,038) and R4 (114,564), delivering the round's largest per-round increment. Cumulative algo rank moved from #809 (after R4) to **#537** — a single-round jump of 272 places, the strongest algo-rank delta of the competition. This vindicates the v36→v42 robustness pivot at the rank-against-the-field level even though absolute v42 algo PnL came in below the backtester window.

### v42 algo decomposition by strategy bucket

Cross-referencing the v42 trader's strategy lists against the JSON 50-product PnL:

| Bucket | n products | Net PnL | Notes |
|---|---|---|---|
| **DIRECTIONAL** (TARGETS_DIR ±10) | 13 | **+67,111** | dominant alpha source; carried the round |
| **HEDGED_NO_SKEW** (SNACKPACK CHOC/VAN) | 2 | **+9,858** | structural pair (ρ=−0.916) delivered as designed |
| **DEFAULT_MM** | 22 | **−16,294** | the only drag; dominated by single product (see below) |
| **TIER3** (LIMIT=5) | 2 | **−2,764** | small loss, manageable |
| **BLACKLIST** (LIMIT=0) | 11 | **0** | exactly zero — designed perfectly |
| **TOTAL** | 50 | **+57,911** | |

The strategy worked exactly as designed at the bucket level. BLACKLIST was perfectly disabled (every blacklisted product realized exactly $0). DIRECTIONAL was the dominant alpha source. HEDGED was a clean win. The −$16,294 DEFAULT_MM drag is **100% attributable to MICROCHIP_SQUARE alone** — without it, DEFAULT_MM would have netted +$2,342.

### MICROCHIP_SQUARE −$18,636 — narrative correction

Earlier vault narratives (and this page in earlier passes) framed MICROCHIP_SQUARE as "the canonical Phase-13 OOS-flip recurrence" — implying v42 had kept it directional and lost when it flipped again on Day 5. **That framing was wrong.** **MICROCHIP_SQUARE was NOT in v42's TARGETS_DIR**; it was in DEFAULT_MM. v42 had correctly excluded it from directional per the Phase 13 caution.

The −$18,636 loss came from **market-making MICROCHIP_SQUARE on a day with strong directional drift** — adverse selection picked off our quotes. The correct lesson: a drift-magnitude-based blacklist criterion would have caught it and added it to MM_BLACKLIST. The cross-version-log blacklist mechanism (N=12 logs) didn't flag MICROCHIP_SQUARE because its history was inconsistent enough to leave it in DEFAULT_MM. See [[Performance/Algo_Per_Round]] for the full bucket decomposition.

### PEBBLES basket realized

5 products in the directional basket. Net **+38,974**:
- PEBBLES_XL +10: +19,552 ✓
- PEBBLES_M (−10): +35,275 ✓ (M went down → short paid off)
- PEBBLES_L (−10): +12,441 ✓ (L went down → short paid off)
- PEBBLES_XS (−10): −3,443 ✗ (XS went up slightly)
- PEBBLES_S (−10): **−24,852** ✗ (S went up — biggest single-product loss in R5)

3 of 5 worked. The structural anti-correlation (PEBBLES_XL vs the smaller variants, ρ≈−0.5) held overall but PEBBLES_S reversed badly.

### GALAXY_SOUNDS_BLACK_HOLES (the v36/v42 disagreement product)

Realized: **−$4,914** at +10 directional. v36 had blacklisted BH (Prosperity-window drift was negative); v42 kept it directional (full-day drift was positive in `full_day_optimal.csv`). On the actual Day 5, BH drifted further negative — **v36's call would have been correct.** The $6,799 backtester gap that v42 accepted to keep BH did not pay off on Day 5 specifically. Verdict: rank-against-field still favored v42 (algo round-rank #287), but on this specific trade v36 was right.

### v42 backtester-vs-real — RESOLVED

- v42 backtester (first 10% of Day 4): **$72,000**
- v42 R5 algo realized (full Day 5): **$57,911**
- **Ratio: 0.80** — full-day was *less* than the backtester window

Reconciliation with the 8.6× inflation thesis: backtester runs 10% of day with 8.6× over-fill → net multiplier 0.86 vs full-day. Predicted full-day from $72K: $83.7K. Realized $57.9K = **69% of prediction**. The thesis is roughly correct (time × inflation factors approximately cancel), but Day 5 had different drift patterns than Days 2/3/4 — a normal live-vs-test gap of ~30%. Despite the absolute gap, **R5 algo round-rank #287 (top 1.5%)** is by far the strongest algo rank, vindicating the v36→v42 robustness pivot at the rank level.

### Ashflow Alpha realization

- Theoretical fees: 140,100
- Realized: **+95,214** (rank #310)
- Ratio: **0.679** — 32% of theoretical lost to archetype misclassification

Of the 6 allocated goods, 2–3 archetypes likely resolved against expectation. Candidates: Lava cake (assumed s=50%, may have been less), Pyroflex (assumed s=24%, news-cycle-dependent), or one of the "0%" goods unexpectedly moving. The optimization math (p*=s/2) is correct; the failure was archetype confidence.

> Companion page: [[Rounds/Round5_Preview]] (mid-round capture, written 2026-04-29). This page covers the full v1→v42 strategy evolution and the lessons that broke open during competition week.

---

## What Round 5 Actually Was

50 products in 10 categories of 5 each, all with mid-prices oscillating around ~10,000. Position limit ±10 across the board. **Old products no longer tradable.** Buyer/seller fields removed (no Mark counterparty signals like R4). One manual challenge ("Ashflow Alpha" — submitted at 85% / 140,100 fees, see [[Strategies/Ashflow_Alpha_News_Trading]]).

The 10 categories: GALAXY_SOUNDS, SLEEP_POD, MICROCHIP, PEBBLES, ROBOT, UV_VISOR, TRANSLATOR, PANEL, OXYGEN_SHAKE, SNACKPACK. Full breakdown with day-2 mid ranges in [[Products/Round5_Categories]].

The position limit collapse from 200 → 10 was the central structural change. **Per-tick alpha had to be high enough to make ±10 positions worthwhile.** This forced the strategy away from R3-style MM-and-scale toward **directional drift bets** (Phase 13) plus **selective MM with adverse-selection screening**.

---

## v42 — The Submission, and Why Not v36

**v42 measured Prosperity backtester PnL: ~$72,000.** v36 measured: $78,799. **v36 had the higher backtester score, but v42 was submitted.** The decision was deliberate and is the operationalization of the central R5 principle:

> The Prosperity backtester runs the first 10% of Day 4. The competition scores the full day. **Don't optimize for the dev-window metric when the test-window metric is what counts.**

What v42 keeps that v36 dropped (and why):
- **PANEL_2X4 +10 directional**: PW drift mixed/negative, FW drift +738 / +738 / +895 (HIGH-conf). v36 blacklisted; v42 keeps directional.
- **GALAXY_SOUNDS_BLACK_HOLES +10 directional**: PW drift consistently negative all 3 days; FW drift consistently positive +1,447 / +689 / +1,321. The canonical conflict product. v36 dropped from directional (treating it as a regular blacklist candidate); v42 keeps it.

The accepted cost: **−$6,799 backtester PnL** (= 78,799 − 72,000). The expected full-day return on that cost: **+$33K+** (PANEL_2X4 +$8,895 + BLACK_HOLES +$13,155 + secondary effects). Asymmetric upside, take it.

**ML analogy:** v42 is the **regularized best model**; v36 is the **dev-set local optimum**. When dev and test distributions differ, you don't pick the dev winner.

## Submitted Strategy (v42) at a Glance

```text
Layer 1 (Directional hold):  13 products at fixed ±10 — buy/sell ASAP, hold all day
Layer 2 (Per-product MM):    35 products at LIMIT=10 with inventory skew
                              + 2 TIER3 products at LIMIT=5  (small adverse-selection-prone)
                              + 8 BLACKLIST products skipped entirely (confirmed losers)
                              + 2 HEDGED_NO_SKEW: SNACKPACK CHOCOLATE+VANILLA
                                (ρ=−0.92, MM with bigger inner size and no skew)
```

Full v42 source: see [[Strategies/Round5_Version_History]].

### v42 Directional Targets (13)

| Product | Direction |
|---|---|
| MICROCHIP_OVAL | −10 |
| PEBBLES_XL, OXYGEN_SHAKE_GARLIC, GALAXY_SOUNDS_BLACK_HOLES, PANEL_2X4, UV_VISOR_RED, SNACKPACK_STRAWBERRY | +10 |
| PEBBLES_S, PEBBLES_XS, PEBBLES_M, PEBBLES_L, UV_VISOR_AMBER, SNACKPACK_PISTACHIO | −10 |

### v42 MM_BLACKLIST (8 confirmed losers + 3 zero-fill)

3 zero-fill from v34 evidence (skip-safe): TRANSLATOR_SPACE_GRAY, GALAXY_SOUNDS_PLANETARY_RINGS, ROBOT_DISHES.
8 confirmed cross-version losers: 7 ex-TIER3 (OXYGEN_SHAKE_MORNING_BREATH, GALAXY_SOUNDS_DARK_MATTER, PANEL_2X2, ROBOT_LAUNDRY, PANEL_1X2, PANEL_1X4, OXYGEN_SHAKE_MINT) + SLEEP_POD_LAMB_WOOL. See [[Strategies/Cross_Version_Blacklist]].

---

## The Three Big Insights

### Insight 1 — Backtester ≠ competition scoring (the central lesson)

Prosperity's local backtester runs the **first 10% of Day 4** (~100K of 1M timestamps). Competition scoring runs the **full day**. The two metrics can have different optimal strategies — and they did.

| Version | Backtester ($) | Estimated full-day ($) |
|---|---|---|
| v34 | 62,299 | **152,730** (best full-day) |
| v36 | **78,799** (backtester winner) | 130,680 |
| v37 (BH flip) | ~79,000 | 117,425 (catastrophic on full day) |
| v39 (PEBBLES_XL dropped) | 38,258 | 91,250 (lost +$40K alpha) |
| v40 (TIER3 removed) | 52,788 | ~$140K |
| v41 = v34 + STRAWBERRY | ~62,000 | ~$153K |
| **v42** | $72K (measured) | ~$163K pre-result est · **$57,911 realized Day-5 (SUPERSEDES estimate)** |

The N=12 cross-version Prosperity log evidence was telling us about **first-10% losses**, many of which **recover on the full day**. v36 blacklisted PANEL_2X4 (full-day +$8,895) and BLACK_HOLES (full-day +$13,155) — losing $22K of full-day directional alpha. v37 then **flipped BLACK_HOLES** to −10 trusting the Prosperity-window drift (which is consistently negative on the first 10%) — a $26K full-day swing the wrong way.

**The conflict products** (`drift_audit.csv` `conflict=True`): GALAXY_SOUNDS_BLACK_HOLES is the canonical example — Prosperity-window drift `−85.5 / −53.5 / −65.0` on days 2/3/4, but full-day drift `+1,446.5 / +688.5 / +1,320.5`. They literally point opposite directions. The full-day evidence won.

See [[Concepts/Backtester_vs_Competition]] for the full story.

### Insight 2 — Local-backtester inflation broke v35

`--match-trades all` in the local backtester gives **8.6× inflated fills** vs the real Prosperity matching engine. v35 was a careful "reliable BT" reclassification — train/test split, OOS gating, the works. It said: drop PEBBLES_M and PEBBLES_L (UNSTABLE/BLACKLIST in local BT), promote PANEL_1X4 to TIER1, etc. **All wrong** on real Prosperity.

The bug was upstream of the methodology: the local backtester was selling a different counterparty mix than real Prosperity, so signals that survived local OOS still didn't survive the real engine. v36's pivot was to **abandon local data entirely** for tier decisions and use only the N=12 Prosperity log set ([[Strategies/Cross_Version_Blacklist]]).

**ML analogy:** v35 vs v36 is dataset-shift in a nutshell. Local BT and Prosperity engine have different `P(counterparty | order_book)` distributions. Models trained on local-BT data with strict OOS still fail on Prosperity because the OOS held out timestamps, not distributions. The fix: train on data drawn from the deployment distribution.

### Insight 3 — TIER3 (reduced LIMIT) is the right answer for adverse selection

A subset of products consistently lose money to **MM-style quoting**. Not because of drift; because informed counterparties pick off our quotes (we buy as price falls, sell as price rises). The right response is **smaller exposure** — LIMIT=5 instead of 10 cuts the bleeding roughly in half.

v40's mistake was hypothesising "more trades on the full day = recovery" and removing TIER3 (LIMIT 5 → 10). **Wrong direction** — adverse-selection losses scale **with** trading volume, not against. v40 backtester regressed −$9,511 vs v34 with most of the loss attributable to un-TIER3'd products.

v42's final answer: blacklist 7 of the 9 ex-TIER3 products entirely (consistent losers across N=12 versions); keep 2 small-loss ones (MICROCHIP_RECTANGLE, OXYGEN_SHAKE_EVENING_BREATH) at LIMIT=5. See [[Concepts/Adverse_Selection]] · [[Strategies/TIER3_Market_Making]].

---

## Other Findings

### Lead-lag: confirmed null result

`round5/research/lead_lag.py` ran 36,750 lagged cross-correlation tests (1,225 product pairs × 5 lags × 3 days × 2 directions). Bonferroni α = 0.05 / 36,750 = **1.36e-6**. Required filters: |ρ| > 0.10 at best lag, same-direction lead on all 3 days, asymmetry score > 0.05.

**Zero pairs survived.** No tradable lead-lag in the R5 data. Documented as a **confirmed null**, not an inconclusive result. See [[Concepts/Lead_Lag]].

### Structural pairs

Within-category cross-correlation (`round5/research/pairs_analysis.py` → `plots/round5/within_category_xcorr_summary.csv`) found two real structural pairs:

| Pair | ρ | Strategy |
|---|---|---|
| SNACKPACK_CHOCOLATE / SNACKPACK_VANILLA | **−0.92** | HEDGED_NO_SKEW MM (bigger inner size, no inventory skew because the natural anti-correlation provides the hedge) |
| SNACKPACK_STRAWBERRY / SNACKPACK_RASPBERRY | −0.92 | (not exploited — STRAWBERRY became directional +10) |
| SNACKPACK_PISTACHIO / SNACKPACK_RASPBERRY | −0.83 | (PISTACHIO became directional −10) |
| PEBBLES sub-variants | ≈ −0.5 | Directional basket: XL +10, S/M/L/XS −10 |

The SNACKPACK CHOC/VAN pair is the one that's exploited as a pair (not as 2× directional). See [[Strategies/HEDGED_NO_SKEW]].

### XGBoost reached AUROC OOS = 0.653 — but didn't graduate

Phase 14's XGBoost depth-2 classifier on opening-window features (vol, OBI, depth ratio, drift, etc.) reached OOS AUROC 0.653 — clearly above the 0.55 escalation threshold. Logistic L1 was worse-than-chance OOS (0.441), exposing real non-linearity. But:
- It was a binary direction predictor; the actual decision is `±10 size + which products`, which the classifier didn't address
- Its 7 extra OBI-significant products overlapped Phase 13's set
- The Prosperity-window vs full-day distinction emerged as more important than in-sample signal quality

So Phase 14's signals sit in `round5/plots/eda2/` as a verified inventory but didn't change v34's strategy. See [[Backtests/Phase14_R5_EDA]].

### ML dead ends (Phase 15, Phase 16 — locked Phase 13)

| Approach | Outcome |
|---|---|
| GRU on tick sequences | Failed PnL gate |
| XGBoost as direction gate (production version) | Failed PnL gate |
| SDE-calibrated synthetic data augmentation (block bootstrap) | Failed PnL gate |
| Heavyweight GRU + synthetic ensemble (Phase 16) | Phase locked / not shipped |

The **Phase 13 baseline (v23-class strategy)** was the floor. Document these as honest dead ends — overfit was the universal failure mode at n ≈ 150 per product.

---

## v1 → v42 Evolution at a Glance

Full changelog: [[Strategies/Round5_Version_History]]. Key milestones:

| Version | Idea | Result |
|---|---|---|
| v1 | 7-product pure directional hold (no MM) | Phase 13 baseline: $261,461 over 3 local days |
| v9 | + MM layer on remaining products + skew | local 669K (inflated) |
| v14 | v9 + MM_BLACKLIST (local-BT-derived) | local-tuned, real-engine-uncertain |
| v21 | + 2-level depth (inner + outer quote) | local 699K |
| v23 | **Prosperity-informed redesign** — drop directional disasters (LAMB_WOOL), no local blacklist | Prosperity-validated |
| v26 | + per-product TIER1/TIER3/BLACKLIST from N=1 Prosperity log | +$10K vs v23 |
| v27 | best-of v9/v23/v26 synthesis | foundation for v34 |
| **v34** | + PEBBLES_M/L directional (basket completion) + HEDGED_NO_SKEW for SNACKPACK CHOC/VAN | **best full-day estimate $152K**; backtester $62K |
| v35 | local-CV reclassification | $53K (failed — local ≠ Prosperity) |
| v36 | cross-version N=12 blacklist (drop LAMB_WOOL, drop PANEL_2X4 directional) | **$78K backtester (winner)** but $130K full-day |
| v37 | v36 + BH flip to −10 (Prosperity-window drift) | catastrophic full-day (−$26K) |
| v38 | defensive — only 2 both-window-consistent dirs | $38K (low variance) |
| v39 | full-day bet — drop PEBBLES_XL | $38K (wrong window) |
| v40 | v34 + un-TIER3 + 2 new directional | worse than v34 (TIER3 removal mistake) |
| v41 | v34 + SNACKPACK_STRAWBERRY +10 only (TIER3 kept) | ~$62K |
| **v42** | v41 + 8 confirmed losers blacklisted (anti-overfit) | **$72K backtester · $57,911 REALIZED Day-5** (~$163K pre-result estimate was 3× over) |

---

## Carry-Forward Lessons

| Lesson | Source |
|---|---|
| Pre-register OOS day before any analysis runs | Phase 13 MICROCHIP_SQUARE flip; Phase 14 P-hacking pitfall |
| Distinguish backtester window from scoring window | v34/v36/v37/v40 cycle |
| `--match-trades all` inflates fills 8.6× — calibrate or drop | v35 failure |
| Adverse selection scales with volume — use TIER3 (smaller LIMIT) not blacklist for borderline | v40 mistake → v42 fix |
| For tightly anti-correlated pairs, MM with HEDGED_NO_SKEW > 2× directional | SNACKPACK CHOC/VAN |
| Lead-lag in tick data is mostly null at this size | `lead_lag.py` 0/36,750 survivors |
| HAC standard errors required for tick-data regressions | Phase 14 OBI methodology vs Round 3 naive OLS |
| ML at n ≈ 150 per product is below the floor without pooling | Phase 14 F (pooled to 150) |

## Hypothetical v43 — what the realized result tells us

After-the-fact, three load-bearing changes would have lifted v42's $57,911 algo realization:

| Change | Mechanism | Estimated lift |
|---|---|---|
| Drop **PEBBLES_S −10** from directional | Realized −$24,852 vs ~$0 if neutral. The cross-version log evidence had it consistently short, but on Day 5 the basket reversed asymmetrically. | **+$24,852** |
| Add **MICROCHIP_SQUARE** to MM_BLACKLIST | Realized −$18,636 in DEFAULT_MM. A drift-magnitude criterion (any product with >X bps cross-day drift) would have caught it. v42's blacklist mechanism was log-frequency-based and missed this. | **+$18,636** |
| v36's call on **PANEL_2X4** and **BLACK_HOLES** | Both realized negative on Day 5 (−$3,822 and −$4,914). v36 had blacklisted them; v42 kept them directional (+10 each). | **+$8,736** |

**Hypothetical v43: $57,911 + $52,224 = ~$110K full-day** — close to the local estimate. But this is hindsight: PEBBLES_S was correct under cross-version logs, MICROCHIP_SQUARE wasn't flagged by available signals at submission time, and the v42-vs-v36 trade-off was a forward-looking choice on the BLACK_HOLES Prosperity-window-vs-full-day conflict.

The realized rank #287 algo (top 1.5%) on this round suggests v42's *relative* design was solid even at $57K absolute. v43 hindsight gives a $50K lift that wasn't extractable in advance.

---

## Links

[[Rounds/Round5_Preview]] · [[Rounds/Round4_findings]] · [[Strategies/Directional_Holding]] · [[Strategies/TIER3_Market_Making]] · [[Strategies/HEDGED_NO_SKEW]] · [[Strategies/Cross_Version_Blacklist]] · [[Strategies/Round5_Version_History]] · [[Strategies/Ashflow_Alpha_News_Trading]] · [[Concepts/Backtester_vs_Competition]] · [[Concepts/Adverse_Selection]] · [[Concepts/Lead_Lag]] · [[Backtests/Phase13_R5_Directional]] · [[Backtests/Phase14_R5_EDA]] · [[Products/Round5_Categories]] · [[Research/Round5_Scripts]]

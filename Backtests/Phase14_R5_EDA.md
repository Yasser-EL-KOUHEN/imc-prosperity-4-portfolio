---
type: backtest
tags: [round5, phase14, eda, oos-validation, completed, signals]
sources:
  - round5/research/eda2/
  - round5/plots/eda2/
  - round5/backtests/Phase14_R5_EDA.md
  - .planning/phases/14-r5-strategy-deepening/14-RESEARCH.md
  - .planning/phases/14-r5-strategy-deepening/14-00-SUMMARY.md
  - .planning/phases/14-r5-strategy-deepening/14-01-SUMMARY.md
  - .planning/phases/14-r5-strategy-deepening/14-02-SUMMARY.md
  - .planning/phases/14-r5-strategy-deepening/14-03-SUMMARY.md
  - .planning/phases/14-r5-strategy-deepening/14-04-SUMMARY.md
updated: 2026-04-30
status: COMPLETE
---

# Phase 14 — R5 Strategy Deepening (Six-Analysis EDA)

> Six standard quant analyses run on R5 tick data with strict OOS discipline (train days 2+3, test day 4). Three signals survived their OOS gate; only one (XGBoost direction) clearly graduated.

> **Post-result validation (2026-05-08):** Phase 14's "no signal cleanly graduated to PnL" conclusion was correct. v42 shipped **without** any Phase-14-derived signal additions and realized $57,911 algo on Day 5. Phase 14's lead-lag null result (0/36,750 tests) and XGBoost AUROC=0.653 not graduating to PnL gate were both validated by the realized result — adding speculative signals would have introduced noise, not alpha. The decision to **not** ship Phase-14 signals was the right call.

## Setup Constraints

- **OOS_DAY = 4** pre-registered as a top-level constant in `eda2.py` and committed before any analysis ran (Pitfall-7 mitigation against P-hacking).
- HAC standard errors (Newey-West, `maxlags=H`) on every OBI/OFI regression — the Round 3 `microstructure_eda.py` had naive OLS, biased downward.
- BH-FDR within each analysis (`statsmodels.stats.multitest.multipletests("fdr_bh")`) — Bonferroni at α=0.05/1500 ≈ 3e-5 was too conservative; nothing would survive.
- Pooled cross-product training in F (per-product n=3 below the floor; pooled n=150 with product as one-hot feature).

## Six Analyses — Outcomes

| # | Analysis | OOS verdict | Phase 15 verdict |
|---|---|---|---|
| A | Multi-timescale ρ_H + Lo-MacKinlay variance ratio (50 prods × 5 horizons) | 0/250 PASS | SKIP |
| B | PCA factor model + residual mean-reversion (Horn's parallel analysis) | 31/200 PASS but \|ρ\|<0.08, half-life sub-tick | SKIP (gate artifact) |
| C | OBI predictive regression with HAC SEs (4 horizons × 50 products) | 8/200 OOS-significant + sign-stable | **IMPLEMENT** as entry-timing improver |
| D | Donchian box breakout (k × W × hold grid on 7 Phase-13 products) | 0/63 PASS | SKIP |
| E | Trajectory shape similarity (resampled 100-bin Pearson, day-vs-day) | 1/50 (PEBBLES_XS, already exploited) | SKIP |
| F | Logistic L1 → XGBoost → MLP escalation ladder | XGB AUROC OOS = **0.653** | **IMPLEMENT** as direction gate |

## F — XGBoost Direction Classifier (strongest survivor)

8 engineered opening-window features (vol, OBI moments, gap, depth ratio, drift, max DD, trade imbalance) + product as one-hot categorical. Pooled training: n=100 train, n=50 OOS.

| Model | AUROC train | AUROC OOS | Decision |
|---|---|---|---|
| Logistic L1 | 0.718 | **0.441** | escalate (worse than chance OOS — non-linear effects) |
| **XGBoost depth-2** | 0.778 | **0.653** | stop — passes 0.55 |
| Tiny MLP | — | — | not run |

XGBoost regularization for n=150: `max_depth=2`, `n_estimators=20` with early stopping, `reg_alpha=1.0`, `reg_lambda=1.0`, `min_child_weight=5`. Logistic underfitting OOS exposes non-linearity that XGBoost depth-2 captures cleanly.

**ML analogy:** Logistic L1 worse-than-chance OOS while XGBoost passes is the classic "linear model on a non-linear manifold" gap — the kind of gap that motivates ensembling/boosting in any tabular ML pipeline. With n=150 the early-stopping holdout is doing most of the regularizing.

## C — OBI Predictive Regression (8 day-4 OOS survivors)

Statistically significant on day 4 OOS with HAC errors (`maxlags=H`) and FDR correction:

| Product | Horizon | β_train | t_HAC OOS | Trade |
|---|---|---|---|---|
| GALAXY_SOUNDS_SOLAR_WINDS | 25 | −8.04 | −2.04 | SHORT |
| MICROCHIP_CIRCLE | 1 | +1.29 | +2.18 | LONG |
| PEBBLES_XL | 1 | +9.08 | +2.33 | LONG (already in Phase 13) |
| UV_VISOR_AMBER | 25 | +6.63 | +2.31 | LONG |
| UV_VISOR_ORANGE | 5 | +4.66 | +2.21 | LONG |
| OXYGEN_SHAKE_MINT | 1 | −1.65 | −2.06 | SHORT |
| OXYGEN_SHAKE_CHOCOLATE | 10 | +5.24 | +2.07 | LONG |
| SNACKPACK_VANILLA | 25 | +4.43 | +2.13 | LONG |

7 NEW directional candidates beyond Phase 13's 7 products.

> ⚠️ Note conflict with later v34→v42 evidence: UV_VISOR_AMBER ended up SHORT (−10) in the submitted v42 strategy because the **drift sign** was negative on real Prosperity, not the OBI sign. OBI gives the entry-timing edge; drift gives the directional bet. They can disagree, and when they did the drift evidence won.

## B — Why "31 passes" was a Gate Artifact (lesson)

The residual mean-reversion analysis flagged 31 products as having statistically significant |ρ_residual| ∈ [0.05, 0.08]. The **half-life** = `−log(2)/log(|ρ|)` works out to **0.26 ticks** — sub-tick. Faster than the simulator can act, regardless of how significant the t-stat is.

**Lesson learned:** the gate threshold should have been `|ρ| ≥ 0.20 AND half-life ≥ 5 ticks`. Phase 14 reports the 31 passes faithfully but does not recommend any of them. **Statistical significance ≠ economic tradability.** This was already the spirit of the Round 3 OBI threshold (`R² > 0.005 and |t| > 5`) but the new bar should have explicit half-life filtering.

## Why this didn't graduate to a Phase 15 strategy

After Phase 14, the team transitioned to **strategy iteration** (v23 → v42) directly using Prosperity log evidence (`round5/logs/`) instead of building on Phase 14's signal layer. Reasons:
- **F's classifier was binary directional (UP/DOWN);** the actual decision is **size×direction at fixed ±10**, which the classifier didn't address.
- **C's signals overlapped Phase 13's directional set** (PEBBLES_XL already there) and the 7 new ones were marginal (t_HAC ≈ 2.0–2.3).
- **The Prosperity-window vs full-day distinction** ([[Concepts/Backtester_vs_Competition]]) emerged as a more important factor than any in-sample signal quality. ML on the wrong data window doesn't help.

The Phase 14 outputs sit in `round5/plots/eda2/*.csv` as a verified signal inventory should future research (e.g. a Round 6) want to revisit them.

## Files

- Code: `round5/research/eda2/analysis_{a,b,c,d,e,f}.py`, `run_{abc,de,f}.py`, `synthesize.py`
- Outputs: `round5/plots/eda2/{A_autocorrelation, B_pca_loadings, B_pca_variance, B_residual_ou, C_obi_beta, D_box_breakout, E_trajectory_archetypes, E_trajectory_shape, F_features, F_auroc_report, synthesis}.csv`

## Links

[[Backtests/Phase14_R5_Setup]] · [[Backtests/Phase13_R5_Directional]] · [[Strategies/OBI_Signal]] · [[Concepts/Order_Book_Imbalance]] · [[Concepts/Backtester_vs_Competition]] · [[Research/Round5_Scripts]] · [[Rounds/Round5_findings]]

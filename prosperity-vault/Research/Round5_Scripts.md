---
type: research
tags: [round5, eda, scripts, research, lead-lag, drift-audit, pairs-analysis, ml-deadends]
sources:
  - round5/research/eda.py
  - round5/research/eda2/
  - round5/research/run_round5.py
  - round5/research/queue_priority_bt.py
  - round5/research/full_day_optimal.py
  - round5/research/drift_audit.py
  - round5/research/lead_lag.py
  - round5/research/lead_lag_within_cat.py
  - round5/research/pairs_analysis.py
  - round5/research/analyze_prosperity_logs.py
  - round5/research/_check_a.py
  - round5/research/_check_d.py
  - round5/research/competitor/
  - round5/plots/
updated: 2026-04-30
---

# Round 5 Research Scripts

All scripts live in `round5/research/`. R5 research broke into four phases:
1. **Phase 13 EDA** — find the directional bets (`eda.py`, `run_round5.py`)
2. **Phase 14 deepening** — six structured analyses (`eda2/*`)
3. **Strategy iteration helpers** — `queue_priority_bt.py`, `analyze_prosperity_logs.py`, `drift_audit.py`, `full_day_optimal.py`
4. **Cross-product investigations** — `lead_lag.py`, `lead_lag_within_cat.py`, `pairs_analysis.py`

---

## Phase 13 Pipeline (Directional Selection)

### `eda.py`

Core EDA for the 50 R5 products. Outputs in `round5/plots/`:
- `category_ranking.csv` — per-category mid-price stats (range, vol, drift)
- `cross_category_xcorr_{raw,summary}.csv` — between-category contemporaneous correlations
- `within_category_xcorr_{raw,summary}.csv` — within-category (the SNACKPACK CHOC/VAN ρ=−0.92 finding)
- `product_characterization.csv` — AR(1), spread, vol, drift per product per day
- `cointegration_tests.csv` — ADF on residuals after pair-fitting

The output that drove Phase 13 selection: per-product day-2/day-3/day-4 drift sign + magnitude. 7 products survived sign-stable + OOS day-4 positive: MICROCHIP_OVAL (−), PEBBLES_XL/S/XS, OXYGEN_SHAKE_GARLIC, GALAXY_SOUNDS_BLACK_HOLES, PANEL_2X4. See [[Backtests/Phase13_R5_Directional]].

**Key finding:** AR(1) ρ ≈ 0.999 across **all 50 products** → mean-reversion impossible at tick level. Designed alpha is multi-day **directional drift**.

### `run_round5.py`

Backtest harness. Modeled after `run_round4.py` with the TTE block removed (R5 has no options). Asserts `len(ROUND5_LIMITS) == 50` at module load.

CLI: `--day, --trader, --out, --no-out, --match-trades, --no-progress`. Output is per-product per-day PnL CSV.

---

## Phase 14 EDA Pipeline (`eda2/`)

Wave-0 setup phase shipped:
- `eda2/__init__.py` and `loaders.py` — re-export Phase 13 data pipeline + Phase 14 constants
- Pre-registered constants: `OOS_DAY=4`, `TRAIN_DAYS=[2,3]`, `PHASE13_TARGETS` (7-entry dict)

Six analyses (A–F) shipped, plus synthesis (G):

| Script | Analysis | Outputs |
|---|---|---|
| `eda2/analysis_a.py` | Multi-timescale ρ_H + Lo-MacKinlay variance ratio | `A_autocorrelation.csv` |
| `eda2/analysis_b.py` | PCA factor model + residual mean-reversion | `B_pca_loadings.csv`, `B_pca_variance.csv`, `B_residual_ou.csv` |
| `eda2/analysis_c.py` | OBI predictive regression with HAC SEs | `C_obi_beta.csv` |
| `eda2/analysis_d.py` | Donchian box breakout grid search (7 products) | `D_box_breakout.csv` |
| `eda2/analysis_e.py` | Trajectory shape similarity (Pearson on 100-bin resampled) | `E_trajectory_shape.csv`, `E_trajectory_archetypes.csv` |
| `eda2/analysis_f.py` | Logistic L1 → XGBoost → MLP escalation | `F_features.csv`, `F_auroc_report.csv` |
| `eda2/synthesize.py` | PASS/FAIL synthesis | `synthesis.csv` |
| `eda2/run_{abc,de,f}.py` | Orchestrators (parallel waves) | — |

**Outcome:** 3 of 6 analyses produced day-4 OOS-significant signals. Only **F (XGBoost AUROC OOS = 0.653)** clearly graduated. Implementation deferred — overshadowed by the backtester-vs-competition discovery. See [[Backtests/Phase14_R5_EDA]].

Methodological additions over Round 3:
- **HAC standard errors** (`statsmodels.OLS(...).fit(cov_type="HAC", cov_kwds={"maxlags": H})`) instead of Round 3's naive OLS — bias-corrects for tick-data autocorrelation
- **BH-FDR** (`statsmodels.stats.multitest.multipletests("fdr_bh")`) instead of Bonferroni — appropriate when many tests aren't independent
- **Lo-MacKinlay variance ratio** (`arch.unitroot.VarianceRatio(robust=True)`) for random-walk hypothesis testing
- **Horn's parallel analysis** for PCA k-selection (instead of Kaiser eigenvalue=1)

### `_check_a.py` / `_check_d.py`

Sanity checks for analyses A and D — verify computation matches expectations on synthetic data before running the real pass.

---

## Strategy Iteration Scripts

### `queue_priority_bt.py`

Local backtester variant with `--match-trades worse + 1/10 subsampling`. Used to build v35's "reliable BT" classification.

**This script's output ultimately misled v35.** The local-BT counterparty mix differs from real Prosperity. v35 pivoted away from this approach in favor of `analyze_prosperity_logs.py`. Document as an honest dead end.

### `analyze_prosperity_logs.py`

Aggregates per-product PnL across all real-Prosperity log files in `round5/logs/{v1, v9, v11, v14, v21, v23, v25, v26, v27, v31, v34, v35}/`. Outputs per-product (avg PnL, n-positive, n-runs) table.

This is the **N=12 cross-version evidence** that drove v36's blacklist. See [[Strategies/Cross_Version_Blacklist]].

### `drift_audit.py`

Compares per-product drift in **Prosperity window** (first 100,000 timestamps) vs **full day** (all 1,000,000 timestamps), days 2/3/4. Flags products with `pw_sign_consistent != fw_sign_consistent` — the **conflict products** where the two windows point opposite directions.

R5 result: **GALAXY_SOUNDS_BLACK_HOLES** is the canonical conflict product (PW: −85/−53/−65 vs FW: +1,446/+688/+1,320). v37's BH flip was based on PW evidence and lost $26K of full-day PnL. See [[Concepts/Backtester_vs_Competition]].

Output: `round5/plots/drift_audit.csv` (50 products × 11 columns).

### `full_day_optimal.py`

For each of the 50 products, computes day-2/day-3/day-4 full-day drift, classifies confidence (HIGH/MED/LOW based on sign-stability), recommends ±10/0 position. Estimates day-4 PnL at the recommended position with rough spread cost (10 ticks).

Output: `round5/plots/full_day_optimal.csv`. Top of the table sorted by `est_d4_pnl`:

```text
PEBBLES_XL                 +10  MED   est +$40,090
OXYGEN_SHAKE_GARLIC        +10  HIGH  est +$19,535
MICROCHIP_OVAL             -10  HIGH  est +$18,925
GALAXY_SOUNDS_BLACK_HOLES  +10  HIGH  est +$13,155
...
```

This file is the basis of the v34/v40/v41/v42 directional setups.

---

## Cross-Product Investigations

### `lead_lag.py`

Lagged cross-correlation function (CCF) across all 1,225 product pairs at lags ∈ {1, 2, 5, 10, 20}, days 2/3/4, both directions. **36,750 tests.** Bonferroni α = 1.36e-6.

**Result: 0 pairs survive.** Confirmed null result — no tradable lead-lag in R5 at the tested horizons. See [[Concepts/Lead_Lag]].

Outputs:
- `plots/round5/lead_lag/lead_lag_pairs.csv` (18,375 rows × 8 cols — every pair × lag × day with rho/p-value)
- `plots/round5/lead_lag/top_leaders.csv` (header only — no survivors)
- `plots/round5/lead_lag/asymmetry_scores.csv` (per-pair S(A→B) − S(B→A))

### `lead_lag_within_cat.py`

Same methodology restricted to within-category pairs (10 categories × 10 pairs each = 100 pairs). Bonferroni α = 1.67e-5. **Also 0 survivors.** Outputs in `plots/round5/lead_lag/within_cat_*.csv`.

### `pairs_analysis.py`

Within-category contemporaneous correlation matrices + cointegration tests + diverger identification (one product systematically opposing the basket).

**Key finding**: SNACKPACK CHOCOLATE/VANILLA ρ = −0.916 → exploited via [[Strategies/HEDGED_NO_SKEW]]. PEBBLES sub-variants ρ ≈ −0.5 → exploited via PEBBLES basket directional (XL +10 vs S/M/L/XS −10).

Outputs:
- `plots/round5/pairs/correlation_matrices.csv`
- `plots/round5/pairs/cointegration_tests.csv`
- `plots/round5/pairs/divergers.csv`

---

## ML Experiments (Phase 15+ — All Failed PnL Gate)

The `competitor/` directory holds GRU / XGBoost production trader experiments and synthetic-data augmentation pipelines. None passed the Phase 13 baseline gate. Document as dead ends, not silenced failures.

| Approach | Outcome |
|---|---|
| GRU on 100-tick windows | Failed PnL gate |
| XGBoost as production direction gate | Failed PnL gate |
| SDE-calibrated synthetic data + block bootstrap | Failed PnL gate |
| Heavyweight GRU + synthetic ensemble (Phase 16) | Phase locked / not shipped |

Phase 13's v23-class strategy held as the floor through every ML attempt. The XGBoost AUROC=0.653 in Phase 14 was the closest any ML approach got to actionable, but it never produced full-PnL improvement vs the directional+TIER3 hand-design.

---

## Data

`round5/data/`:
- `prices_round_5_day_{2,3,4}.csv` — 500K rows each, 50 products × 10K ticks. Schema: `day;timestamp;product;bid_price_{1,2,3};bid_volume_{1,2,3};ask_price_{1,2,3};ask_volume_{1,2,3};mid_price;profit_and_loss`
- `trades_round_5_day_{2,3,4}.csv` — 11–12K rows each. Schema: `timestamp;buyer;seller;symbol;currency;price;quantity` — **buyer and seller are empty strings** in all 35K+ trades (R5 removed counterparty disclosure vs R4)

---

## Links

[[Rounds/Round5_findings]] · [[Rounds/Round5_Preview]] · [[Backtests/Phase13_R5_Directional]] · [[Backtests/Phase14_R5_EDA]] · [[Backtests/Phase14_R5_Setup]] · [[Concepts/Lead_Lag]] · [[Concepts/Backtester_vs_Competition]] · [[Concepts/Adverse_Selection]] · [[Strategies/Directional_Holding]] · [[Strategies/Cross_Version_Blacklist]] · [[Strategies/HEDGED_NO_SKEW]] · [[Research/Round3_Scripts]]

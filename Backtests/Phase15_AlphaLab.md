---
type: backtest
tags: [round5, phase15, ml-deadend, alpha-lab, gru, xgboost, synthetic-data, null-result]
sources:
  - round5/research/competitor/alpha_lab.py
  - round5/runs/alpha_lab_step1_clean/
  - round5/runs/alpha_lab_step1_clean/metrics.json
  - round5/runs/alpha_lab_step1_clean/config.json
  - round5/plots/eda2/heavy/
  - .planning/phases/15-synthetic-augmented-sequential/  (empty — never executed)
  - .planning/phases/16-heavyweight-gru-synthetic/      (empty — never executed)
updated: 2026-05-01
status: NULL_RESULT
---

# Phase 15 — Alpha Lab (ML Production Trader Deadends)

> Phases 15 and 16 in the planning trail are documentation-empty (no SUMMARY.md was produced). The work happened in `round5/research/competitor/alpha_lab.py` and `round5/runs/alpha_lab_step1_clean/`. None of it shipped — Phase 13's directional baseline held as the floor through every ML attempt.

## What Was Tried

A "competitor's verbatim alpha trainer" (top-100 competitor's code) was run with `--no-leaky-features --overfit-level 1` to disable `leak_*` and `memorize_bucket_*` features and get an **honest** validation IC. The pipeline:

1. **Features (288 columns)**: per-product OBI, OFI, depth, spread, microstructure features at 4 snapshot windows; PCA + ICA decompositions; tree-based feature engineering (`use_tree_features=True`); target smoothing.
2. **Target**: 10-tick-forward return.
3. **Model**: PyTorch sequential network with weighted sampling + dropout + early stopping.
4. **Data**: all 1.5M rows across days 2/3/4. Train/valid split = 82/18 within-day.

## Honest Validation Metrics (with leak features disabled)

From `round5/runs/alpha_lab_step1_clean/metrics.json`:

```json
{
  "warning": "DANGEROUS_RESEARCH_ONLY__DO_NOT_ASSUME_OUT_OF_SAMPLE_ALPHA",
  "rows": 1498500,
  "train_rows": 1228650,
  "valid_rows":  269850,
  "n_features": 288,
  "n_products":  50,
  "horizon": 10,
  "valid_mse":  1.504e-05,
  "valid_mae":  3.016e-03,
  "valid_r2":  -0.169,
  "valid_ic":   0.025,
  "valid_rank_ic": 0.010,
  "sign_accuracy": 0.4915,
  "model_infos": [
    {"best_epoch": 9, "best_score": 0.0254, "feature_count": 288}
  ]
}
```

**The numbers are bad.**

| Metric | Value | What it means |
|---|---|---|
| `valid_r2` | **−0.169** | Worse than predicting the validation-set mean. Negative R² is the signature of an overfitting model that learned noise. |
| `valid_ic` | 0.025 | Information coefficient ≈ 0.025. For comparison: industrial-grade signals are 0.05–0.15; tradable threshold often 0.03+. |
| `valid_rank_ic` | 0.010 | Spearman rank correlation ≈ 0.01 — essentially zero predictive power in ordering. |
| `sign_accuracy` | **0.4915** | **Worse than a coin flip.** The model is anti-predictive on direction. |
| `best_epoch` | 9 | Early stopping kicked in fast → the loss flattened almost immediately. |

The pipeline's own embedded warning string is `DANGEROUS_RESEARCH_ONLY__DO_NOT_ASSUME_OUT_OF_SAMPLE_ALPHA` — i.e., even the source author acknowledges this is for research only.

## Why It Failed

1. **n=150 per product is below the ML floor**, even with pooled training. 288 features × negligible signal = the model overfits no matter how heavy the regularization.
2. **AR(1) ≈ 0.999 across all 50 products** means the next-tick return is dominated by the random component. There's no consistent signal at the 10-tick horizon for the model to learn.
3. **288 features is too many for n_train ≈ 1.2M** when most of the variance is microstructure noise. PCA + ICA + tree features just multiplied dimension without adding signal.
4. **Leak features are doing all the work in non-clean runs.** The pipeline has "memorize_bucket" and "leak_" features that explicitly violate temporal ordering. Disabling them collapses the IC from "looks tradable" to 0.025.

## What This Confirms

- **Phase 13 baseline is the floor.** Any production ML must beat the directional+TIER3 hand-design at the day-4-OOS PnL gate. None did.
- **The Phase 14 XGBoost AUROC=0.653 result was the highest any ML approach got** — and it was a **direction classifier on opening-window features**, much simpler than the Phase 15 alpha lab. The complexity-vs-signal curve flattens fast.
- **R5 alpha is structural, not learnable.** PEBBLES_XL +10, MICROCHIP_OVAL −10, UV_VISOR_RED +10 — these are visible from a 5-minute drift plot. They don't need a 288-feature neural net.

## ML Analogy

The valid_r2 = −0.169 with 288 features and n_train=1.2M is the textbook case of **the data not having enough signal at the chosen horizon**. The model bandwidth (288 features, deep PyTorch network) is large; the signal-to-noise ratio at h=10 ticks is small. Result: the model fits noise that doesn't generalize.

The right ML response is one of:
- **Lower-frequency target** (h=1000 ticks instead of 10) — but 100K-tick windows × 50 products = 50 samples per day, n=150 total; below floor again
- **Cross-product pooling** with simple model (Phase 14's logistic L1 was the right shape but found AUROC OOS = 0.441; XGBoost depth-2 squeezed out 0.653)
- **Structural features** (basket positions, regime indicators) instead of microstructure features

R5 chose option 3 implicitly — directional bets are basket/regime features in disguise. ML didn't add value because the structure was already exploitable without it.

## Phase 16 — Heavyweight GRU + Synthetic Ensemble

`.planning/phases/16-heavyweight-gru-synthetic/` is empty — the phase was scoped but never executed (or executed without producing a SUMMARY). The intent was to combine:
- A GRU on tick sequences for sequence modeling
- An SDE-calibrated synthetic-data generator for augmentation
- Block bootstrap on the synthetic samples
- Ensemble of 5+ such models

Per `Round5_findings.md` and `README.md`, this approach **failed the PnL gate**. No artifacts in the repo confirm specifically what happened — but the documented end-state is "Phase 13 locked as floor".

## Files

- `round5/research/competitor/alpha_lab.py` — the trainer (~3,000 lines, full PyTorch + sklearn pipeline)
- `round5/runs/alpha_lab_step1_clean/`
  - `config.json` — run config (no_leaky_features=true, overfit_level=1)
  - `metrics.json` — the bad numbers above
  - `feature_columns.json` — 288 feature names
  - `predictions.csv` — per-row predictions (validate independently)
  - `history.csv` — training loss trajectory
- `round5/plots/eda2/heavy/` — Phase 14 heavy-track outputs (separate from the alpha lab)

## Links

[[Backtests/Phase14_R5_EDA]] · [[Backtests/Phase13_R5_Directional]] · [[Rounds/Round5_findings]] · [[Concepts/Backtester_vs_Competition]] · [[Strategies/Directional_Holding]] · [[Research/Round5_Scripts]]

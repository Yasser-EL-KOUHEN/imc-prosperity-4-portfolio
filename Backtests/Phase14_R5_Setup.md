---
type: backtest
tags: [round5, phase14, eda, infrastructure, setup]
sources:
  - .planning/phases/14-r5-strategy-deepening/14-00-PLAN.md
  - .planning/phases/14-r5-strategy-deepening/14-00-SUMMARY.md
  - research/round5/eda2/__init__.py
  - research/round5/eda2/loaders.py
updated: 2026-04-29
---

# Phase 14 Plan 00 — Setup Wave (R5 Strategy Deepening)

> Wave-0 setup for the six-analysis Round 5 EDA push. No tradeable PnL change — pure infrastructure.

## What shipped

- Installed `xgboost==3.2.0` and `arch==8.0.0` (the two libraries flagged as missing in `14-RESEARCH.md`).
- Created Python package `research/round5/eda2/` with `__init__.py` and `loaders.py`.
- `loaders.py` re-exports the Phase 13 data pipeline from [[Research/Round5_Scripts|research/round5/eda.py]] and adds Phase 14-specific constants.
- Created output directory `plots/round5/eda2/` (with `.gitkeep`).
- [[Backtests/Phase13_R5_Directional|Phase 13 trader]] (`vault/round5_trader.py`) and `eda.py` are UNTOUCHED — verified via `git status`.

## `loaders.py` exports

| Constant | Value | Purpose |
|----------|-------|---------|
| `CATEGORIES` | dict (10 categories × 5 products) | Re-exported from `eda.py` |
| `ALL_PRODUCTS` | 50 product names | Re-exported from `eda.py` |
| `DAYS` | `[2, 3, 4]` | Re-exported from `eda.py` |
| `ROUND5_LIMITS` | `{p: 10 for p in ALL_PRODUCTS}` | All 50 products at limit 10 |
| `OOS_DAY` | `4` (NEVER change — pre-registered) | Pitfall-7 mitigation against P-hacking |
| `TRAIN_DAYS` | `[2, 3]` | Locked train split |
| `PHASE13_TARGETS` | 7-entry dict (MICROCHIP_OVAL=−10, PEBBLES_XL=+10, …) | From [[Backtests/Phase13_R5_Directional]] trader |
| `PLOTS_DIR` | `plots/round5/eda2/` (absolute) | Output dir for analyses A–F |

## Smoke test

```
loaded rows: 1,500,000
day-4 MICROCHIP_OVAL ticks: 10,000
smoke test OK
```

50 products × 3 days × 10,000 ticks = 1.5M rows, day-4 array length 10,000 (well above the ≥5,000 gate).

## Why a setup wave?

Six analyses (A multi-timescale ρ, B PCA factor, C OBI with HAC, D Donchian box breakout, E trajectory shape, F opening-window classifier) need to run in parallel without each one re-discovering pip dependencies and CSV paths. See [[Concepts/Order_Book_Imbalance]] for the OBI methodology, [[Strategies/Mean_Reversion]] for ρ vs random-walk null discussion.

The OOS pre-registration is the textbook anti-leakage move — analogue of \emph{not peeking at the test set} in ML. It is the lesson from [[Backtests/Phase11_Box_Signal|Phase 11's BNL-05/06 null result]].

## Library versions

| Library | Version | Used in plan |
|---------|---------|--------------|
| xgboost | 3.2.0 | 14-04 (escalation tier 2 of opening-window classifier) |
| arch | 8.0.0 | 14-01 (`arch.unitroot.VarianceRatio` Lo-MacKinlay test) |
| statsmodels | 0.14.6 | 14-01..14-03 (HAC SEs, BH-FDR, ADF) |
| scikit-learn | 1.8.0 | 14-02 (PCA), 14-04 (LogisticRegression) |
| torch | 2.10.0+cpu | 14-04 (escalation tier 3, tiny MLP) |

## Commits

- `d493271` — feat(14-00): add Phase 14 eda2 package skeleton + loaders + plots dir
- `e0699fd` — docs(14-00): complete Phase 14 setup plan — eda2 package + xgboost/arch installed

## What's next

Plans 14-01 through 14-04 (Wave 1) are unblocked and can run in parallel:

- **14-01** — Multi-timescale autocorrelation ρ_H + Lo-MacKinlay variance ratio test
- **14-02** — PCA factor model + residual mean-reversion (Horn's parallel analysis)
- **14-03** — OBI regression with HAC standard errors at horizons H ∈ {1, 5, 10, 25}
- **14-04** — Donchian breakout grid search on the 7 [[Backtests/Phase13_R5_Directional|Phase 13]] target products

Each will write CSVs into `plots/round5/eda2/`. Synthesis (R14-G) compiles a PASS/FAIL table — only hypotheses passing the day-4 OOS gate graduate to Phase 15 implementation.

## Cross-references

- [[Backtests/Phase13_R5_Directional]] — baseline this builds on (261,461 XIREC 3-day; 118,083 OOS day 4)
- [[Backtests/Phase11_Box_Signal]] — null-result discipline that motivates the OOS pre-registration
- [[Research/Round5_Scripts]] — the canonical Phase 13 `eda.py` that 14-00 re-exports
- [[Research/Decisions_Log]] — locked decisions feeding this phase

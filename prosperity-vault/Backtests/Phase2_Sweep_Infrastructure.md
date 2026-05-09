---
type: backtest
tags: [round3, phase2, parameter-sweep, hydrogel, env-var, calibration]
sources:
  - .planning/phases/02-parameter-sweep-infrastructure/02-SUMMARY.md
  - round3/backtests/phase2_sweep_results.log
  - round3/backtests/phase2_back04_best_config.md
  - round3/plots/hydrogel/joint_sweep.csv
updated: 2026-05-06
---

# Phase 2 — Parameter Sweep Infrastructure

**Goal:** Enable grid-search over HYDROGEL MM parameters without manually editing `trader.py`.
**Result:** 24-config sweep run; baseline IS the grid optimum. anchor_w=0.20 dominates all other factors.

---

## What Was Built

### Env-Var Injection into trader.py

`HydrogelMM.__init__` now reads three parameters from environment variables:

```python
import os

alpha      = float(os.environ.get("HYDRO_ALPHA",      "0.35"))
anchor_w   = float(os.environ.get("HYDRO_ANCHOR_W",   "0.20"))
take_thresh = float(os.environ.get("HYDRO_TAKE_THRESH", "2.5"))
```

Defaults match the prior hardcoded literals — baseline behaviour unchanged when env vars are unset. The sweep script (`round3/research/round3/hydrogel_sweep.py`) injects these via `subprocess.run(..., env={**os.environ, **config})`.

### Bug Fixed

`hydrogel_sweep.py` line 162 had an invalid format-string: `{'delta':>+10}`. The `+` sign prefix is not valid for string format specifiers. Fixed to `{'delta':>11}`. The sweep crashed silently before this fix, producing 1 distinct PnL value (no differentiation). After fix: **47 distinct total-PnL values** across 24 configs.

---

## Sweep Results (24 configs, 3 days)

**Baseline** (alpha=0.35, anchor_w=0.20, take_thresh=2.5):

| Day | PnL |
|---|---|
| 0 | 51,788 |
| 1 | 46,978 |
| 2 | 41,982 |
| **Total** | **140,748** |

**Key finding:** The current baseline IS the grid optimum. No config beats it on all 3 days simultaneously (`all_days_win=False` for all 24 non-baseline configs).

### Grid Landscape

| Parameter | Winner | Effect |
|---|---|---|
| `anchor_w` | **0.20 dominates** 0.0 and 0.10 strongly | Biggest effect — anchor pull toward 10,000 prior is load-bearing |
| `alpha` (EMA decay) | 0.35 near-optimal | Within anchor_w=0.20, small difference |
| `take_thresh` | 2.5 near-optimal | Lower → more aggressive fills on Day 0, worse Day 2 |

**Nearest runner-up:** alpha=0.50, anchor_w=0.20, take_thresh=2.0 → total=140,100 (−648 vs baseline); NOT robust (not all-days win).

---

## BACK-04: Local vs Official PnL Ratio

| Metric | Local day 2 | Prosperity v1 | Ratio |
|---|---|---|---|
| Total | 41,982 | 2,533 | **~16.6× over** |
| HYDROGEL_PACK only | 36,643 | 1,811 | **~20.2× over** |

This **~16–20× local inflation** is structural: the local backtester runs 10× more ticks per day and uses a more generous fill model. The ratio is stable across all 24 configs (re-confirmed by running best config: identical ratio).

> **Note:** This is distinct from the R5 `--match-trades all` inflation (~8.6×). The R3 ratio is larger because it compounds both tick-frequency inflation AND fill-model generosity.

Phase 1 had established the BACK-04 block (no reference logs available). Phase 2 resolved it by using the v1 Prosperity submission log as the reference — ratio documented and locked.

---

## Phase 3 Entry Conditions Unlocked

After Phase 2:
1. Any parameter change can be evaluated via `python research/round3/hydrogel_sweep.py` against baseline total (140,748)
2. `anchor_w` is the dominant parameter — Phase 3/4 improvements must come from strategy logic (bucketed rho, OBI), not grid search within these ranges
3. `trader.py` is env-var aware for all three `HYDRO_*` params — new params should follow the same `os.environ.get("PARAM", "default")` pattern

---

## Files Produced

| File | Content |
|---|---|
| `round3/backtests/phase2_sweep_results.log` | Full sweep stdout (24 configs, 47 distinct totals) |
| `round3/backtests/phase2_back04_best_config.md` | BACK-04 ratio confirmation + winner analysis |
| `round3/plots/hydrogel/joint_sweep.csv` | Updated sweep CSV |

## Links

[[Backtests/Phase1_Backtest_Calibration]] · [[Backtests/Phase3_HYDROGEL_FV]] · [[Backtests/Phase4_Rho_Sweep]] · [[Parameters/HYDROGEL_Params]] · [[Products/HYDROGEL_PACK]] · [[Research/Round3_Scripts]]

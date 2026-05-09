---
type: research
tags: [round3, scripts, research, microstructure, options, hydrogel]
sources: [research/round3/analyze_round3.py, research/round3/microstructure_eda.py, research/round3/iv_surface.py, research/round3/hydrogel_audit.py, research/round3/hydrogel_sweep.py, research/round3/obi_sweep.py, research/round3/rho_sweep.py, research/round3/skew_sweep.py, research/round3/vev_passive_comparison.py, research/round3/bs_verify.py, research/round3/safety_check.py, research/round3/box_signal_baseline.py, research/round3/box_sweep.py, research/round3/gamma_scalp.py, research/round3/options_quoting_verify.py, research/round3/run_round3.py, research/round3/extract_timeseries.py, research/round3/biopod_solver.py, research/round3/compare_to_competition.py]
updated: 2026-04-27
---

# Round 3 Research Scripts

## Overview

All scripts live in `research/round3/`. Shared utilities in `research/shared/`.

The Round 3 pipeline:
1. EDA → 2. Calibration → 3. Backtesting sweeps → 4. Verification → 5. Safety → 6. Box signal research

---

## Script Inventory

### Core EDA

#### `analyze_round3.py`
Primary EDA for Round 3 products. Analyzes:
- Price distributions for HYDROGEL_PACK, VELVETFRUIT_EXTRACT, and all option strikes
- ACF/PACF (stationarity confirmation)
- Spread patterns per product
- Flow direction statistics (bid-hit vs ask-hit rates)

**Key output:** Confirms HYDROGEL mean-reversion; identifies asymmetric flow on VEV_5000/5200.

#### `microstructure_eda.py`
Deep microstructure analysis:
- OBI beta calibration via OLS regression: `next_mid_change = β × OBI + ε`
- Results: HYDROGEL β=11.2 (R²=0.089, t=31); VEV_5300 β=0.65 (R²=0.125, t=38)
- Flow asymmetry: 94–98% of VEV_5000/5200 trades hit the bid
- Justification for bid-only quoting on ITM strikes

#### `extract_timeseries.py`
Extracts per-tick timeseries (position, PnL, mid-price) from backtest logs into `backtests/timeseries_day{D}.csv`. Used by Phase 3 fair value trace and Phase 4 position limit verification.

---

### Calibration Scripts

#### `hydrogel_audit.py`
AR(1) coefficient calibration from HYDROGEL price data:
- Segments moves by magnitude: [2,5) ticks and [5,10) ticks
- AR(1) coefficient for small moves: **−0.094**
- AR(1) coefficient for large moves: **−0.237**
- Source of the magnitude-bucketed design

#### `iv_surface.py`
Implied volatility surface computation:
- Per-strike IV from historical market prices using Newton-Raphson BS inversion
- Produces `plots/round3/round3_iv_surface.png` and `round3_strike_vols.csv`
- 3-day mean IV per strike → fed into `STRIKE_SIGMA` in trader.py
- Confirms vol smile: ATM (5400) has lowest IV (0.230), OTM/ITM higher

#### `bs_verify.py`
Black-Scholes price and delta verification:
- Computes BS prices for each strike at competition-specified params
- Compares to reference implementation
- Verifies all edge cases (T=0, σ≈0, S=0)

---

### Parameter Sweep Scripts

#### `hydrogel_sweep.py`
v6 joint grid search over `(alpha, anchor_w, take_threshold)`:
- Winner: alpha=0.35, anchor_w=0.20, take_thresh=2.5
- Key finding: doubling anchor_w from 0.10 to 0.20 is the dominant improvement
- +53,921 over v5b across 3 historical days (v6 basis)

#### `rho_sweep.py`
Fine grid over `(SMALL_RHO, LARGE_RHO)` — 49 configs:
- Winner: small=0.08, large=0.42 → 142,675 (Phase 4)
- Gate: all-days-win (beat Phase 3 baseline on every individual day)

#### `skew_sweep.py`
Grid over `HYDRO_INV_SKEW`:
- Winner: 0.03 (only value passing all-days gate + regression gate)

#### `obi_sweep.py`
OBI beta perturbation sweep (±20%) for options strikes:
- All 8 configs produce identical PnL (146,415)
- Finding: OBI sub-resolution vs passive edge constants in backtest

---

### Comparison and Verification

#### `vev_passive_comparison.py`
Compares VEV_PASSIVE_ONLY=0 vs =1:
- Passive-only wins: +839 over 3 days
- Gate: all-days-win → PASS

#### `options_quoting_verify.py`
Phase 7 gate verification:
- OPT-04: two-sided 5300/5400/5500 non-zero 3d sum → PASS
- OPT-05: bid_only=True static check for 5000/5200 → PASS
- OPTIONS-POSITIVE: agg PnL > 0 on ≥2 days → PASS

#### `compare_to_competition.py`
Compares local backtest PnL vs official sandbox logs:
- Local/official ratio: ~16.6x total, ~20.2x HYDROGEL
- Documents structural biases: tick frequency, fill model, MTM

#### `safety_check.py`
Phase 9 safety verification:
- AST scan for import violations
- Position limit structural verification
- 3 edge-case scenario tests

---

### Box Signal Research (Phase 11)

#### `box_signal_baseline.py`
Phase 11 Plan 01 research:
- Computes HYDROGEL and VEV lag-1 ACF (−0.1292, −0.1587)
- Sweeps box window N for range persistence
- Support/resistance bounce rate test vs null hypothesis
- OBI redundancy check (correlation < 0.7 → independent)

#### `box_sweep.py`
Phase 11 Plan 02 sweep:
- 9-config grid: N ∈ {100,200,500} × α ∈ {0.3,0.5,0.7}
- All fail 2/3-day anti-overfit gate
- BNL-05 REJECTED; BNL-06 SKIPPED

---

### Other Scripts

#### `run_round3.py`
Main backtest runner — wraps `prosperity3bt` with standard flags:
- `--merge-pnl` (always), `--match-trades all`, `--no-out`, `--no-progress`
- Passes `BT_INITIAL_TTE_DAYS` env var per day

#### `gamma_scalp.py`
Experimental gamma scalping research (v2 deferred idea):
- Tests gamma-based position sizing for options
- Result: not implemented in v3 (complexity vs benefit unfavorable)
- In v2 requirements backlog

#### `biopod_solver.py`
Research into BIOPOD product (Round 3 ancillary product):
- Mathematical solver for BIOPOD pricing
- Not integrated into main trader (out of scope for competition focus)

---

## Shared Utilities (`research/shared/`)

| File | Purpose |
|------|---------|
| `market_data.py` | Load and parse prices/trades CSVs into DataFrames |
| `options.py` | BS functions, IV computation (pre-trader.py versions) |
| `prosperity_bootstrap.py` | Wrapper for `prosperity3bt` CLI; handles env vars, log parsing |

---

## Data Files

| Location | Contents |
|----------|---------|
| `data/round3/prices_round_3_day_{0,1,2}.csv` | Tick-level prices per product |
| `data/round3/trades_round_3_day_{0,1,2}.csv` | Executed trades with timestamps |
| `plots/round3/` | IV surface, residuals, reversion buckets, trade-side rates |
| `backtests/timeseries_day{D}.csv` | Per-tick position + PnL from backtester |

---

## Links

[[Research/Round1_Scripts]] · [[Research/Decisions_Log]] · [[Products/HYDROGEL_PACK]] · [[Strategies/OBI_Signal]] · [[Concepts/Implied_Volatility]] · [[Backtests/Phase4_Rho_Sweep]]

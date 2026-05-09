---
type: research
tags: [round1, eda, scripts, research]
sources: [research/round1/eda.py, research/round1/edge_hunt.py, research/round1/edge_hunt2.py, research/round1/edge_hunt3.py, research/round1/edge_hunt4.py, research/round1/aco_opt_sweep.py, research/round1/aco_position_audit.py, research/round1/grid_rho_magnitude.py, research/round1/ipr_scalp_sweep.py, research/round1/run_jasper.py, research/round1/run_round1.py]
updated: 2026-04-27
---

# Round 1 Research Scripts

## Overview

All scripts live in `research/round1/`. Round 1 research focused on:
1. EDA of new products (RAINFOREST_RESIN, KELP, SQUID_INK)
2. Fair value model selection
3. Spread and rho parameter sweeps
4. Position management analysis

---

## Script Inventory

### `eda.py`
Core exploratory data analysis for Round 1 products.

**Outputs:** Plots in `plots/round1/` — for each product:
- `_01_price_overview.png` — mid-price time series, spread distribution
- `_02_acf_pacf.png` — autocorrelation / partial autocorrelation (stationarity test)
- `_03_order_book.png` — order book depth, volume distribution
- `_04_trade_flow.png` — trade direction, volume at different prices
- `_05_hurst.png` — Hurst exponent (H<0.5 = mean-reverting, H>0.5 = trending)

**Products analyzed:** RAINFOREST_RESIN, KELP, SQUID_INK, ASH_COATED_OSMIUM, INTARIAN_PEPPER_ROOT (Round 1 product set)

### `edge_hunt.py` / `edge_hunt2.py` / `edge_hunt3.py` / `edge_hunt4.py`
Sequential edge discovery scripts. Each iteration refined signal hypotheses for KELP and SQUID_INK:
- Edge_hunt: basic bid/ask imbalance signals
- Edge_hunt2: autocorrelation-based signals
- Edge_hunt3: volume-weighted signals
- Edge_hunt4: combination signals

**Key finding:** RAINFOREST_RESIN doesn't need signal — stable FV. SQUID_INK signals are too noisy for reliable quoting.

### `aco_opt_sweep.py`
Parameter sweep for ACO (ASH_COATED_OSMIUM) product — explored rho and alpha combinations.

### `aco_position_audit.py`
Audits position history for ACO trades — checks limit compliance and inventory tracking.

### `grid_rho_magnitude.py`
Grid search over magnitude-bucketed rho parameters — the precursor to Phase 4's fine grid in Round 3. Tests small_rho vs large_rho combinations for mean-reverting products.

### `ipr_scalp_sweep.py`
Parameter sweep for INTARIAN_PEPPER_ROOT (IPR) scalping strategy — quick in-out trades on short-lived price deviations.

### `run_jasper.py` / `run_round1.py`
Backtesting runners:
- `run_jasper.py`: test runner for a specific trader variant ("Jasper" — a v1 experimental version)
- `run_round1.py`: main Round 1 backtest runner; same structure as `run_round3.py`

---

## Key Findings from Round 1 Research

| Finding | Used In |
|---------|---------|
| RAINFOREST_RESIN FV ≈ 10,000 stable | Round 1 RESIN strategy |
| KELP needs dynamic FV estimate (VWAP/mid) | Round 1 KELP strategy |
| SQUID_INK: high volatility, low signal | Abandoned for aggressive quoting |
| Magnitude-bucketed rho idea first tested | Generalized to Round 3 HYDROGEL |
| Hurst exponent < 0.5 confirms mean-reversion | KELP, RESIN strategies |

---

## Data

Round 1 data in `data/round1/`:
- `prices_round_1_day_{-2,-1,0}.csv` — OHLCV per tick per product
- `trades_round_1_day_{-2,-1,0}.csv` — executed trades with timestamps

---

## Links

[[Rounds/Round1_findings]] · [[Research/Round3_Scripts]]

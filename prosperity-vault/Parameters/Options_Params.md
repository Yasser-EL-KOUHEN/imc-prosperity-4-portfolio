---
type: reference
tags: [options, parameters, iv-surface, obi, calibrated, round3, round4, post-r3]
sources: [round3/trader_final.py, round4/trader.py, performance/algorithmic trading/round 3/486282.py, backtests/phase6_bs_verify.md, backtests/phase6_sigma_verify.md, backtests/phase7_quoting_verify.md, backtests/phase8_obi_sweep.md, backtests/phase10_submission.md]
updated: 2026-05-08
---

# Options (VEV Vouchers) Parameters

> **Submission attribution (clarified 2026-05-08):** the parameter set below — including `initial_tte_days = 7.0` (Phase 10 Addendum 2 TTE recalibration) and per-strike σ values — describes the **post-R3 refinement** in `round3/trader_final.py` (the R4 basis). The **R3 submission `486282.py` used `initial_tte_days = 5.0`** and earlier per-strike σ values. The Phase 10 TTE recalibration was applied between R3 and R4 submissions.
>
> R3 realized VEV PnL across all 10 strikes: **−$8,466** (with un-refined params).
> R4 realized VEV PnL across all 10 strikes: **−$3,185** (with refined params + Mark signals).
> The +$5,281 R4-vs-R3 swing on the option book reflects the combined Phase 10 TTE recal + Phase 12 counterparty signals contribution. See [[Performance/Submission_Verification]] and [[Performance/Algo_Per_Round]].

All parameters from `round3/trader_final.py` (R4 basis) — `VoucherTrader` and `VoucherSurface` classes.

---

## Per-Strike Configuration (ACTIVE_CONFIG)

| Strike | two_sided | bid_only | sell_only | passive_size | obi_beta |
|--------|-----------|----------|-----------|--------------|----------|
| VEV_4000 | False | False | False | 6 | 0.30 |
| VEV_5000 | False | **True** | False | — | 0.30 |
| VEV_5100 | False | **True** | False | — | 0.30 |
| VEV_5200 | False | **True** | False | — | 0.30 |
| VEV_5300 | **True** | False | False | — | **0.65** |
| VEV_5400 | **True** | False | False | — | 0.46 |
| VEV_5500 | **True** | False | False | — | 0.49 |
| VEV_6000 | False | False | **True** | — | 0.30 |
| VEV_6500 | False | False | **True** | — | 0.30 |

---

## Per-Strike Implied Volatility (Calibrated)

From IV surface historical means + Phase 10 live calibration:

| Strike | Static σ | IV mean | |Diff| | Phase 10 live σ |
|--------|----------|---------|--------|---------|
| 5000 | 0.2420 | 0.2420 | 0.0000 | Live (day-specific) |
| 5100 | 0.2400 | — | — | Live |
| 5200 | 0.2440 | 0.2423 | 0.0017 | Live |
| 5300 | 0.2450 | 0.2450 | 0.0000 | Live |
| 5400 | **0.2300** | 0.2296 | 0.0004 | Live |
| 5500 | 0.2490 | 0.2491 | 0.0001 | Live |

ATM (5400) has the lowest vol — vol smile trough. See [[Concepts/Implied_Volatility]].

---

## TTE Schedule

From competition statement ("7 Solvenarian days, starting from day 1"):

| Backtest Day | TTE (days) | TTE (years) |
|-------------|-----------|-------------|
| 0 | 7.0 | 0.01918 |
| 1 | 6.0 | 0.01644 |
| 2 | 5.0 | 0.01370 |

TTE decays intraday: `T = max(initial_tte - timestamp/1_000_000, 1e-6) / 365`

Old approach (Phase 6-9): Binary-search TTE → estimated ~8.7d on day 0 (wrong!). Fixed in Phase 10 Addendum 2 (+265 PnL).

---

## OBI Betas (Per-Strike)

| Strike | β | R² | t-stat | Status |
|--------|---|----|----|------|
| 5300 | **0.65** | 0.125 | 38 | Active (sub-resolution in backtest) |
| 5400 | 0.46 | 0.075 | 28 | Active (sub-resolution in backtest) |
| 5500 | 0.49 | 0.081 | 30 | Active (sub-resolution in backtest) |
| 4000/5000/5100/5200/6000/6500 | 0.30 | — | — | Conservative (not in primary EDA) |

All 8 perturbation configs (±20% of calibrated betas) produced identical PnL (146,415) in Phase 8. OBI is structurally live but backtest-neutral.

---

## IV Monitor

| Parameter | Value |
|-----------|-------|
| Window | 500 ticks |
| Warmup | 250 ticks |
| Z-score usage | Passive sizing bias only (not aggressive) |

---

## Position Limit

| Parameter | Value |
|-----------|-------|
| `VoucherTrader.LIMIT` | **300** (all strikes) |

---

## Phase 10 VEV_4000 Addition

| Parameter | Value |
|-----------|-------|
| Strike | 4000 (deep ITM) |
| passive_size | 6 units |
| edges | passive: 9/5 ticks |
| 3d net contribution | **+6,887** (d0:+3000, d1:+2150, d2:-956) |

---

## Links

[[Products/Options/VEV_5300]] · [[Products/Options/VEV_5400]] · [[Products/Options/VEV_5000]] · [[Strategies/Options_Quoting]] · [[Concepts/Implied_Volatility]] · [[Concepts/Black_Scholes]] · [[Backtests/Phase6_BS_Verify]] · [[Backtests/Phase8_OBI_Sweep]]

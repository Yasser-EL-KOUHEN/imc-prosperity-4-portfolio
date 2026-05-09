---
type: backtest
tags: [phase6, options, black-scholes, verification]
sources: [backtests/phase6_bs_verify.md, backtests/phase6_sigma_verify.md]
updated: 2026-04-27
---

# Phase 6: Black-Scholes Verification

## OPT-01: BS Call Price Accuracy

**Params:** spot=5400, T=7/365

| Strike | σ | Trader Price | Reference | |Diff| | Pass |
|--------|---|-------------|-----------|--------|------|
| 5000 | 0.2420 | 400.644257 | 400.644232 | 2.50e-05 | ✅ |
| 5200 | 0.2440 | 211.880743 | 211.880687 | 5.63e-05 | ✅ |
| 5300 | 0.2450 | 133.130139 | 133.130228 | 8.91e-05 | ✅ |
| 5400 | 0.2300 | 68.614498 | 68.614869 | **3.70e-04** | ✅ |
| 5500 | 0.2490 | 35.339112 | 35.339209 | 9.71e-05 | ✅ |

Max |diff|: **3.70e-04** (threshold 5e-04 — PASS). Worst case at ATM (5400) — expected, as A&S CDF approximation error is largest near ATM. `math.erfc` implementation is accurate to machine precision.

---

## OPT-01: Edge Cases

| Case | Expected | Got | Pass |
|------|----------|-----|------|
| T=0: `bs_call(5400, 5300, 0.0, 0.245)` | 100.0000 | 100.000000 | ✅ |
| σ≈0: `bs_call(5400, 5300, 0.019, 1e-10)` | 100.0000 | 100.000000 | ✅ |
| S=0: `bs_call(0.0, 5300, 0.019, 0.245)` | 0.0000 | 0.000000 | ✅ |
| delta at expiry ITM: `bs_delta(5400, 5300, 0.0, 0.245)` | 1.0000 | 1.000000 | ✅ |

**OPT-01: PASS** ✅

---

## OPT-02: Per-Strike Sigma Calibration

**Source:** `plots/round3/iv_surface/per_strike_iv_summary.csv` (days 0, 1, 2 historical means)

| Strike | Trader σ | IV 3d mean | |Diff| | Pass |
|--------|----------|-----------|--------|------|
| 5000 | 0.2420 | 0.2420 | 0.0000 | ✅ |
| 5200 | 0.2440 | 0.2423 | **0.0017** | ✅ |
| 5300 | 0.2450 | 0.2450 | 0.0000 | ✅ |
| 5400 | 0.2300 | 0.2296 | 0.0004 | ✅ |
| 5500 | 0.2490 | 0.2491 | 0.0001 | ✅ |

Worst |diff|: **0.0017** (threshold 0.002 — PASS).

**OPT-02: PASS** ✅

---

## Delta Flow Confirmed

Delta output from BS engine flows correctly into the `GreeksLedger` → `VEVUnderlying` hedge target computation. Verified via code inspection.

---

## Links

[[Concepts/Black_Scholes]] · [[Concepts/Implied_Volatility]] · [[Parameters/Options_Params]] · [[Backtests/Phase7_Options_Quoting]] · [[Backtests/PnL_Timeline]]

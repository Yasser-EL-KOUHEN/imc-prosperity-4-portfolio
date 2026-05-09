---
type: backtest
tags: [phase4, hydrogel, rho-sweep, parameter-tuning, post-r3]
sources: [backtests/phase4_rho_sweep.md, backtests/phase4_bucketed_vs_flat.md, backtests/phase4_inv_skew_sweep.md, backtests/phase4_position_limit.md]
updated: 2026-05-08
---

# Phase 4: HYDROGEL Parameter Sweep

> **Submission attribution (clarified 2026-05-08):** the Phase 4 winner (`small_rho=0.08, large_rho=0.42`) is the *post-R3 refinement* parameter set used in `round3/trader_final.py` and inherited by `round4/trader.py`. **It was NOT the parameter set submitted to R3.** The R3 submission `486282.py` used `small_rho=0.12, large_rho=0.48` — pre-Phase-4-refinement values. The R3 algo PnL of $40,800 reflects the earlier params; the R4 algo PnL of $57,048 is what the Phase 4 winner produced on the real engine. See [[Performance/Submission_Verification]].

## 1. Fine Rho Grid (49 configs)

**Grid:** SMALL_RHO ∈ {0.06,0.08,0.10,0.12,0.14,0.16,0.18} × LARGE_RHO ∈ {0.24,0.30,0.36,0.42,0.48,0.54,0.60}

**Gate:** Beat Phase 3 reference on ALL 3 days individually (d0>51,788, d1>46,978, d2>41,982)

### Top 10 Results

| rank | small_rho | large_rho | d0 | d1 | d2 | total | delta | all_days_win |
|------|-----------|-----------|----|----|-----|-------|-------|-------------|
| **1** | **0.08** | **0.42** | 52,941 | 47,432 | 42,302 | **142,675** | **+1,927** | **YES** |
| 2 | 0.10 | 0.48 | 53,516 | 46,974 | 41,744 | 142,234 | +1,486 | NO (d2) |
| 3 | 0.06 | 0.24 | 55,138 | 47,087 | 39,552 | 141,777 | +1,029 | NO (d2) |
| 6 | 0.06 | 0.42 | 52,009 | 47,070 | 42,302 | 141,381 | +633 | YES |
| 7 | 0.12 | 0.42 | 52,197 | 47,052 | 42,052 | 141,301 | +553 | YES |

**Winner: small_rho=0.08, large_rho=0.42** — highest total that also passes all-days gate.

Key pattern: large_rho=0.42 dominates the all-days-win configs. Higher rho on large moves captures more reversion profit. small_rho=0.08 (just below the calibrated AR(1) value of 0.094) is slightly more conservative on small moves.

---

## 2. Bucketed vs Flat Comparison

Phase 3 reference: d0=51,788, d1=46,978, d2=41,982 (total 140,748)

| Config | d0 | d1 | d2 | Total | Beats flat-low all-days |
|--------|----|----|-----|-------|------------------------|
| flat-low (0.12/0.12) | 53,832 | 46,925 | 39,816 | 140,573 | N/A |
| flat-mid (0.30/0.30) | 53,412 | 45,689 | 40,488 | 139,589 | N/A |
| bucketed (0.12/0.48) | 51,788 | 46,978 | 41,982 | 140,748 | NO |

Bucketed (Phase 3 default) beats flat-low only in total; it doesn't win all 3 days over either baseline. The fine grid (Phase 4) finds the true optimum.

---

## 3. Inventory Skew Sweep

**Grid:** HYDRO_INV_SKEW ∈ {0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08}

**Gate:** 3d total ≥ 140,748 AND max single-day regression ≤ 2.0%

| skew | d0 | d1 | d2 | total | max_regression | passes |
|------|----|----|-----|-------|----------------|--------|
| 0.00 | 67,476 | 30,985 | 32,594 | 131,055 | 34.0% | ❌ |
| 0.01 | 59,846 | 35,751 | 36,660 | 132,257 | 23.9% | ❌ |
| 0.02 | 56,181 | 42,629 | 41,354 | 140,164 | 9.3% | ❌ |
| **0.03** | **52,941** | **47,432** | **42,302** | **142,675** | **-0.8%** | **✅** |
| 0.04 | 49,393 | 49,545 | 40,774 | 139,712 | 4.6% | ❌ |
| 0.05 | 43,804 | 47,831 | 40,492 | 132,127 | 15.4% | ❌ |

**Winner: inv_skew=0.03** — the only value that passes both gates. Too low → day 1/2 collapse (inventory builds up). Too high → day 0 collapses (over-corrects).

Note: with skew=0.03, max_regression = -0.8% (negative = improvement vs baseline).

---

## 4. Position Limit Verification

HYDROGEL 3d total at Phase 4 winner config (small=0.08, large=0.42, skew=0.03):

| Day | Total PnL | HYDROGEL PnL |
|-----|-----------|-------------|
| 0 | 52,941 | 50,942 |
| 1 | 47,432 | 43,735 |
| 2 | 42,302 | 36,963 |
| **Total** | **142,675** | **131,640** |

Max |position| across all days: 0 (settlement artifact — position closes end-of-day in --merge-pnl mode). Position limit enforcement confirmed structurally via buy_cap/sell_cap pattern.

---

## Links

[[Products/HYDROGEL_PACK]] · [[Parameters/HYDROGEL_Params]] · [[Strategies/Mean_Reversion]] · [[Concepts/inventory_risk]] · [[Backtests/PnL_Timeline]]

---
type: backtest
tags: [phase11, box-signal, support-resistance, null-result, rejected, post-r3]
sources: [backtests/phase11_baseline_parity.md, backtests/phase11_box_sweep.md, .planning/STATE.md]
updated: 2026-05-08
---

# Phase 11: Box-and-Lines Signal Research

> **Submission attribution (clarified 2026-05-08):** Phase 11 is post-R3 — its REJECTED null-result conclusion ("box signal doesn't add value") informed the R4 trader (`round4/trader.py`) by *not* adding the box signal. Both R3 and R4 submissions correctly omit the box signal; Phase 11 confirmed the omission was right. See [[Performance/Submission_Verification]].

## Hypothesis

A **support/resistance box signal** — tracking N-period min/max to detect trading ranges — could improve HYDROGEL quoting size and VEV hedge direction, beating the 153,566/567 baseline on ≥2/3 training days (anti-overfit gate).

---

## Plan 01: BNL-01..04 Research Dossier

### BNL-01: HYDROGEL Autocorrelation

From `research/round3/box_signal_baseline.py`:

| Metric | HYDROGEL_PACK | VEV |
|--------|--------------|-----|
| Lag-1 ACF | **−0.1292** | −0.1587 |
| Negative lags in 1–50 | 28/50 | 20/50 |
| Regime | Mean-reverting | Mildly mean-reverting |

Confirmed: both HYDROGEL and VEV are mean-reverting (negative lag-1 ACF). This is consistent with the AR(1) model used by HydrogelMM.

### BNL-02: Box Detection Window Validation

N ∈ {50, 100, 200, 500, 1000} swept for range persistence duration:

**Median persistence = 0 for ALL N** — HYDROGEL price rarely maintains a box for sustained periods. The market is continuously mean-reverting (returning to 10,000), so price "boxes" form and break immediately.

**N=200 chosen** as the compromise between:
- Too small (N=50): box forms/breaks every few ticks → noisy signal
- Too large (N=1000): 1,000-tick warm-up before first signal; misses early-day structure

### BNL-03: Support/Resistance Bounce Rate

**Finding (counterintuitive):** Near resistance, price shows **momentum** (not reversal):
- Near resistance z-score: −6.99 to −13.66 (strongly negative → price keeps rising)
- The signal is momentum at extremes, not mean-reversion

**Decision:** If box signal used, apply to support side only for VEV hedge bias (where momentum does not dominate), not symmetrically.

### BNL-04: OBI Redundancy Check

Pearson correlation between box-position signal and OBI signal: **< 0.7**

Box state adds independent information vs OBI — signals are not redundant. This cleared the redundancy gate for BNL-05 sweep.

### BNL-01..04 Summary

All four research requirements PASS — the infrastructure is sound. Proceed to BNL-05 (HYDRO sweep).

---

## Plan 02: BNL-05/06 — HYDRO Box Signal Sweep

**Baseline:** 153,566 (d0=58,678 | d1=51,088 | d2=43,800)

**Gate:** 2/3 days improved AND 3d total > 153,566

### Grid (9 configs): N ∈ {100, 200, 500} × α ∈ {0.3, 0.5, 0.7}

| N | α | d0 | d1 | d2 | total | days improved | gate |
|---|---|----|----|-----|-------|---------------|------|
| 100 | 0.7 | 58,678 | 51,090 | 43,800 | 153,568 | **1/3** | ❌ FAIL |
| 100 | 0.3 | 58,678 | 51,088 | 43,800 | 153,566 | 0/3 | ❌ FAIL |
| 200 | 0.3 | 58,678 | 51,088 | 43,800 | 153,566 | 0/3 | ❌ FAIL |
| 500 | 0.3 | 58,678 | 51,088 | 43,800 | 153,566 | 0/3 | ❌ FAIL |
| 200 | 0.5 | 58,678 | 51,082 | 43,800 | 153,560 | 0/3 | ❌ FAIL |
| 100 | 0.5 | 58,678 | 51,052 | 43,800 | 153,530 | 0/3 | ❌ FAIL |
| 500 | 0.5 | 58,678 | 51,022 | 43,800 | 153,500 | 0/3 | ❌ FAIL |
| 200 | 0.7 | 58,678 | 51,008 | 43,768 | 153,454 | 0/3 | ❌ FAIL |
| 500 | 0.7 | 58,678 | 50,922 | 43,768 | 153,368 | 0/3 | ❌ FAIL |

**Best result:** N=100, α=0.7 → 153,568 — only +2 above baseline, only 1/3 days improved.

**BNL-05: REJECTED** — no config passes the 2/3-day anti-overfit gate.

### BNL-06: SKIPPED

VEV box beta sweep not run — no HYDRO winner to build on. Per research §8: "no compounding of untested changes."

---

## Final State

- `HYDRO_BOX_ALPHA=0.0` default — box state wired but disabled
- `VEV_BOX_BETA=0.0` default — signal not tested
- Baseline **153,566 preserved** (1-unit rounding from plan's cited 153,567)

---

## Lessons

1. **Box signal ≠ useful for pure mean-reverting products.** HYDROGEL's mean-reversion already exploits price deviations optimally; scaling quote size by position-in-box adds noise.
2. **Anti-overfit gates matter.** The best config (153,568) looks like +2 improvement but fails on 2/3 days — likely noise.
3. **Research §8 cascade rule:** No compounding untested changes. If HYDRO fails, don't run VEV sweep on untested HYDRO change.

---

## Links

[[Products/HYDROGEL_PACK]] · [[Strategies/OBI_Signal]] · [[Backtests/PnL_Timeline]] · [[Research/Round3_Scripts]]

---
type: backtest
tags: [phase8, obi, options, sweep, sub-resolution]
sources: [backtests/phase8_obi_sweep.md]
updated: 2026-04-27
---

# Phase 8: OBI Beta Sweep

## Setup

**Script:** `research/round3/obi_sweep.py`

**Phase 7 baseline:** 143,514 (d0=53,780 | d1=47,432 | d2=42,302)

8 configs tested: CALIBRATED (0.65/0.46/0.49) + BASELINE (same as calibrated) + 6 ±20% perturbations.

---

## Gate Results

| Gate | Condition | Result |
|------|-----------|--------|
| NO-REGRESS | calibrated 3d total ≥ 143,514 | ✅ PASS (146,415 > 143,514) |
| OBI-IMPROVEMENT | calibrated options agg > baseline on ≥2 days | ❌ FAIL (0/3 days) |
| CALIBRATED-OPTIMAL | calibrated 3d total ≥ all 6 perturbations | ✅ PASS (all tied) |
| **OVERALL** | all three gates | ❌ **FAIL** |

> Per CONTEXT.md, OBI-IMPROVEMENT is a stretch goal; NO-REGRESS is the hard gate. Phase 9 is unblocked.

---

## All 8 Config Results

| Config | 3d Total | d0 | d1 | d2 | opts_agg |
|--------|----------|----|----|----|----------|
| BASELINE | 146,415 | 53,780 | 48,115 | 44,520 | 7,325 |
| **CALIBRATED** | **146,415** | **53,780** | **48,115** | **44,520** | **7,325** |
| PERTURB_5300_HI (0.78) | 146,415 | 53,780 | 48,115 | 44,520 | 7,325 |
| PERTURB_5300_LO (0.52) | 146,415 | 53,780 | 48,115 | 44,520 | 7,325 |
| PERTURB_5400_HI (0.552) | 146,415 | 53,780 | 48,115 | 44,520 | 7,325 |
| PERTURB_5400_LO (0.368) | 146,415 | 53,780 | 48,115 | 44,520 | 7,325 |
| PERTURB_5500_HI (0.588) | 146,415 | 53,780 | 48,115 | 44,520 | 7,325 |
| PERTURB_5500_LO (0.392) | 146,415 | 53,780 | 48,115 | 44,520 | 7,325 |

**All 8 configs produce identical PnL (146,415).** The OBI signal is sub-resolution on this dataset.

---

## Why OBI is Sub-Resolution

The OBI term is `β × OBI ∈ [-0.65, +0.65]` for VEV_5300 at calibrated beta. The passive quoting edge constants are 0.35–1.3 ticks. The discrete order-book structure means:

```
quoted_price = round(fair + OBI_adjustment)
```

A 0.65-tick OBI adjustment rounds to the same integer price as a 0.52-tick or 0.78-tick adjustment. Hence all beta values (within the ±20% range) land at the same price levels, generating identical fills.

**The +2,901 improvement (146,415 vs Phase 7's 143,514)** is NOT from OBI. It comes from Phase 7 quoting logic changes (two-sided 5300/5500, bid-only 5000/5200) compounding over all 3 days.

---

## Decisions

- **NO-REGRESS PASS → no rollback:** Calibrated OBI config is retained in ACTIVE_CONFIG
- **OBI-IMPROVEMENT FAIL (stretch goal) → no action:** Consistent with the Phase 3 HYDROGEL OBI finding — OBI is statistically significant but sub-resolution in the fill model
- **CALIBRATED-OPTIMAL PASS → no beta adjustment:** Calibrated values are tied-optimal; no perturbation wins

---

## Links

[[Strategies/OBI_Signal]] · [[Concepts/Order_Book_Imbalance]] · [[Parameters/Options_Params]] · [[Backtests/Phase7_Options_Quoting]] · [[Backtests/Phase9_Safety]] · [[Backtests/PnL_Timeline]]

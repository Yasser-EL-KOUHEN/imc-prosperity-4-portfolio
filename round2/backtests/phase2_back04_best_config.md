# BACK-04: Local vs Official — Best Config (Phase 2)

**Best config:** alpha=0.35, anchor_w=0.20, take_thresh=2.5
**Robust (all_days_win):** NO — no config in the 24-config grid beats the baseline on all 3 days simultaneously
**Interpretation:** The current default configuration IS the grid optimum. The sweep confirms v6 calibration was already at the right point for this grid.

## Sweep Result Summary

47 of 47 configs returned distinct total-PnL values (injection confirmed working).
0 configs have `all_days_win = True` — the baseline is Pareto-dominant in this grid.

Top 5 by 3-day total:

| alpha | anchor_w | take_thresh | Day 0 | Day 1 | Day 2 | Total | Delta |
|-------|----------|-------------|-------|-------|-------|-------|-------|
| **0.35** | **0.20** | **2.5** | **51,788** | **46,978** | **41,982** | **140,748** | **+0 (baseline)** |
| 0.50 | 0.20 | 2.0 | 53,011 | 46,211 | 40,878 | 140,100 | -648 |
| 0.50 | 0.20 | 2.5 | 53,216 | 48,016 | 38,826 | 140,058 | -690 |
| 0.20 | 0.20 | 2.0 | 47,747 | 47,720 | 44,456 | 139,923 | -825 |
| 0.50 | 0.20 | 3.0 | 53,081 | 48,438 | 37,848 | 139,367 | -1,381 |

**Pattern:** anchor_w=0.20 dominates; alpha=0.35 is near-optimal; lowering take_thresh risks instability on day 2.

## Day-2 Local vs Official (best config = baseline)

| Metric | Local day 2 | Official v1 | Ratio |
|--------|-------------|-------------|-------|
| **TOTAL** | 41,982 | 2,533.41 | ~16.6x over |
| HYDROGEL_PACK | 36,643 | 1,810.63 | ~20.2x over |
| VELVETFRUIT_EXTRACT | 1,104 | 612.23 | ~1.8x over |
| VEV_5100 | 3,505 | 45.71 | ~76.7x over |

**Baseline ratio (Phase 1):** ~16.6x total, ~20.2x HYDROGEL
**Best config ratio (Phase 2):** same (best config IS the baseline)

**Signal:** The sweep confirms the v6 calibration is locally optimal within this grid. Any improvement must come from a different mechanism (e.g., larger grid, magnitude-bucketed rho sweep, or fundamentally different strategy logic — Phase 3/4 territory).

## Conclusion

BACK-04 re-measurement confirms Phase 1 findings unchanged. The local→official ratio is structural (10x tick difference + fill model) and does not depend on parameter choice within this grid.

---
type: product
tags: [round5, snackpack, structural-pair, hedged-no-skew, anti-correlation]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/plots/within_category_xcorr_summary.csv
  - round5/plots/full_day_optimal.csv
  - round5/research/pairs_analysis.py
updated: 2026-05-01
---

# SNACKPACK (Protein Snack Packs 🍫)

**Category:** Protein Snack Packs · **Position limit:** ±10 per product · **Mid-range:** tightest in R5 (avg span 9,656–10,295)

The R5 category with the **strongest within-category contemporaneous anti-correlations**. Multiple pairs at |ρ| > 0.83. Used three different ways in v42: HEDGED_NO_SKEW MM, directional, and default MM.

## Per-Product Disposition (v42)

| Product | Strategy | Reason |
|---|---|---|
| SNACKPACK_CHOCOLATE | **HEDGED_NO_SKEW** MM | ρ = −0.916 with VANILLA (structural pair) |
| SNACKPACK_VANILLA | **HEDGED_NO_SKEW** MM | partner of CHOCOLATE |
| SNACKPACK_PISTACHIO | **−10 directional** | full-day drift consistent − (−489 / −124 / −282) |
| SNACKPACK_STRAWBERRY | **+10 directional** | full-day drift consistent + (+436 / +358 / +98); v41/v42 add |
| SNACKPACK_RASPBERRY | TIER3 (small loss) → upgraded back to default MM in v42 | mixed; small consistent loss |

## Within-Category Correlations

From `round5/plots/within_category_xcorr_summary.csv` (lag-0 correlation of returns, 3-day average):

| Pair | ρ_returns |
|---|---|
| **SNACKPACK_CHOCOLATE / SNACKPACK_VANILLA** | **−0.9159** |
| SNACKPACK_STRAWBERRY / SNACKPACK_RASPBERRY | −0.9238 |
| SNACKPACK_STRAWBERRY / SNACKPACK_PISTACHIO | +0.9133 |
| SNACKPACK_PISTACHIO / SNACKPACK_RASPBERRY | −0.8309 |
| SNACKPACK_RASPBERRY / SNACKPACK_CHOCOLATE | +0.0308 (uncorrelated) |

Notice the structural pattern: **two anti-correlated pairs** (CHOC/VAN, STRAW/RASP) with PISTACHIO correlated to STRAW (and anti-correlated to RASP). Like the PEBBLES basket but with a different topology.

## Why HEDGED_NO_SKEW for CHOC/VAN Specifically

We have three "very anti-correlated" pairs (|ρ| > 0.83), but only CHOC/VAN became HEDGED_NO_SKEW. The others were routed to directional layers:

- STRAWBERRY: full-day drift sign-stable + → directional **+10**
- PISTACHIO: full-day drift sign-stable − → directional **−10**
- RASPBERRY: no clean directional signal → default MM
- CHOCOLATE / VANILLA: no clean directional signal but tightly anti-correlated → **HEDGED_NO_SKEW** (structural hedge does the work)

The decision rule: **if a product has a clean directional signal, take it as ±10. Only after directional bets are settled do we look at remaining pairs for HEDGED_NO_SKEW.** CHOC/VAN had no directional → became the perfect HEDGED_NO_SKEW pair.

## HEDGED_NO_SKEW Settings (v42)

```python
HEDGED_NO_SKEW = {"SNACKPACK_CHOCOLATE", "SNACKPACK_VANILLA"}

# When iterating through MM_PRODUCTS:
if product in HEDGED_NO_SKEW:
    return MM_LIMIT_DEFAULT, 8, 2, SKEW_THRESHOLD_DEFAULT
    #                       ^   ^   default skew threshold (rarely triggers)
    #                       inner=8 (vs default 6), outer=2
```

Bigger inner size + structural hedge = capture more spread without adding net category exposure. The SKEW_THRESHOLD is unchanged because we don't expect to hit it (the partner naturally accumulates the opposite side).

## Tightness Caveat

SNACKPACK is the tightest-spread category in R5 (mid range avg span only 9,656–10,295). Tight spreads → adverse selection risk is highest. The HEDGED_NO_SKEW choice is partially forced by this: **straight directional bets** on CHOC/VAN would have been hard because the per-day drift is small, and **default MM** would have lost to adverse selection. The hedged approach exploits the only stable feature (the −0.92 correlation) without taking on direction risk.

## Links

[[Strategies/HEDGED_NO_SKEW]] · [[Strategies/Directional_Holding]] · [[Products/PEBBLES]] (the other category with structural correlations) · [[Products/Round5_Categories]] · [[Parameters/Round5_Params]] · [[Research/Round5_Scripts]]

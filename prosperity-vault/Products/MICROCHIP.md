---
type: product
tags: [round5, microchip, directional, oos-failure-microchip-square]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/plots/full_day_optimal.csv
  - round5/plots/drift_audit.csv
updated: 2026-05-02
---

# MICROCHIP (Organic Microchips 💾)

**Category:** Organic Microchips · **Position limit:** ±10 per product · **Mid-range:** wide (avg span 9,190 to 11,268) — MICROCHIP_SQUARE is a 22% outlier

The category that taught the team the value of **strict OOS gating**. Phase 13's MICROCHIP_SQUARE flip is the canonical R5 lesson on why "average across days" can lie.

## Per-Product Disposition (v42)

| Product | v42 strategy | Reason |
|---|---|---|
| MICROCHIP_CIRCLE | default MM | mixed drift; no clean directional; reasonable MM |
| **MICROCHIP_OVAL** | **−10 directional** | sign-stable across **all 3 days** in BOTH windows: −744 / −1,824 / −1,898 |
| MICROCHIP_SQUARE | default MM (kept after Phase 13 rejection) | **train-OOS sign flip** in Phase 13; not safe directional |
| MICROCHIP_RECTANGLE | TIER3 (LIMIT=5) | small loss (−$128 v34); kept at TIER3 not blacklist |
| MICROCHIP_TRIANGLE | TIER1 default MM | top earner +$2,801 in v9; decent earner across versions |

## MICROCHIP_OVAL — The R5 Workhorse

The most reliable directional product across all v1→v42:

```text
day-2 drift: −744       both windows: DOWN
day-3 drift: −1,824     both windows: DOWN
day-4 drift: −1,897.5   both windows: DOWN
sign_stable: True
both-window-consistent: True
```

Real Prosperity v34 PnL contribution: **+$4,518**. v36 same. v40 same. Across all 16+ measured versions, MICROCHIP_OVAL never lost money on Prosperity at −10. **The single most reliable bet in R5.**

It's also one of only 2 products that survived v38's defensive both-window-consistent filter — MICROCHIP_OVAL and UV_VISOR_AMBER, both at −10. If you had to ship one trader with two trades, it would be these two.

## MICROCHIP_SQUARE — The Cautionary Tale

`full_day_optimal.csv`:
```text
MICROCHIP_SQUARE: d2=−186, d3=+432, d4=−479, sign_stable=False, recommend_pos=0, confidence=LOW
```

But Phase 13's earlier EDA (training-only) showed:
```text
day-2: +2,456     day-3: +3,438     day-4: −2,278     <-- OOS REVERSAL
```

A signal that scored +5,894 on the training average was **−2,278** on the OOS day. Without a hard OOS gate this would have shipped to v1 as another directional bet — and lost money. Phase 13 rejected it; v42 keeps it at default MM where it neither wins nor loses much.

This is the page-by-page reason `OOS_DAY = 4` is a top-level constant ([[Research/Decisions_Log|D19]]).

## MICROCHIP_RECTANGLE — Why TIER3, not Blacklist

v34 PnL: −$128. v40 PnL: similar small loss. The TIER3 vs blacklist threshold is "small enough to keep capacity for upside" — RECTANGLE is at the boundary.

```python
TIER3_PRODUCTS = {
    "MICROCHIP_RECTANGLE",          # v34 −$128 (tiny)
    "OXYGEN_SHAKE_EVENING_BREATH",  # v34 −$30 (basically zero)
}
```

If RECTANGLE turns into a $-500-per-run pattern in future data, it should be promoted to BLACKLIST. The decision is data-driven and will be revisited if more Prosperity logs are run.

## Within-Category Structure

MICROCHIP doesn't have the strong basket structure of PEBBLES (no monotone size-mid-price pattern: shapes don't have a natural ordering). The within-category correlations are mostly noise (|ρ_returns| < 0.2 except for SQUARE-vs-others which is OUTSIDE the basket).

So MICROCHIP is treated **product-by-product** rather than as a basket.

## Links

[[Products/Round5_Categories]] · [[Strategies/Directional_Holding]] · [[Strategies/TIER3_Market_Making]] · [[Backtests/Phase13_R5_Directional]] · [[Concepts/Backtester_vs_Competition]] · [[Research/Decisions_Log]] · [[Parameters/Round5_Params]]

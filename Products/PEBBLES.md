---
type: product
tags: [round5, pebbles, basket, directional, structural-correlation]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/plots/full_day_optimal.csv
  - round5/plots/within_category_xcorr_summary.csv
  - round5/plots/drift_audit.csv
  - round5/research/pairs_analysis.py
updated: 2026-05-01
---

# PEBBLES (Purification Pebbles 💎)

**Category:** Purification Pebbles · **Position limit:** ±10 per product · **Within-category structure:** size-monotonic mid-prices, anti-correlated returns

The most structurally exploitable R5 category. Mid-prices are **monotone in size** (XS < S < M < L < XL with day-2 averages 9,189 / 9,650 / 9,747 / 9,863 / 11,550) and **returns are anti-correlated** between XL and the smaller variants (ρ ≈ −0.5). This is the cleanest "designed pattern" in R5.

## Per-Product Day-2/3/4 Drift (`full_day_optimal.csv`)

| Product | d2 drift | d3 drift | d4 drift | Sign-stable? | v42 disposition |
|---|---|---|---|---|---|
| PEBBLES_XS | −1,952 | −1,204 | −824 | HIGH (all −) | **−10 directional** |
| PEBBLES_S | −840 | −177 | −937 | HIGH (all −) | **−10 directional** |
| PEBBLES_M | −986 | +2,039 | −364 | mixed | **−10 directional** (basket completion) |
| PEBBLES_L | (variable) | (variable) | −1,888 | mixed but −0.5 corr to XL | **−10 directional** (basket completion) |
| PEBBLES_XL | +3,675 | −1,553 | +4,014 | MED (day-3 dip) | **+10 directional** |

## The Basket Bet

PEBBLES_XL **+10** + PEBBLES_S/M/L/XS **−10** each = a structural basket trade. When the category aggregates upward (e.g., XL goes up), the smaller pebbles tend down via the −0.5 anti-correlation. The basket captures both sides instead of just betting on XL.

This was the **"Edge 1"** introduced in v34. Phase 13 had only XL/S/XS as directional; v34 added M/L for completion. Verified Prosperity gain in v34: PEBBLES_M +$1,487, PEBBLES_L +$512.

## Day-4 PnL at v42 Position Sizes

Per `full_day_optimal.csv`'s `est_d4_pnl` column at recommended position:

| Product | Position | Day-4 drift | Est day-4 PnL |
|---|---|---|---|
| PEBBLES_XL | +10 | +4,014 | +$40,090 |
| PEBBLES_L | −10 | −1,888 | +$18,835 |
| PEBBLES_XS | −10 | −824 | +$8,185 |
| PEBBLES_S | −10 | −937 | +$9,320 |
| PEBBLES_M | −10 | −364 | +$3,590 |
| **Total** | | | **+$80,020** |

This is the largest single-category contribution to v42's full-day estimate.

## v39's Mistake (the cautionary tale)

v39 **dropped PEBBLES_XL/M/L** because their full-day drifts were "mixed" (PEBBLES_XL: +3,675 / −1,553 / +4,014). The day-3 dip is real but days 2 and 4 each have +$36K+ of PnL at +10 position. Net 3-day +$61,130, OOS day-4 +$40,060.

**v39 backtester PnL: $38,258** vs v34's $62,299. The PEBBLES drop alone cost ~$40K of single-day alpha. **Don't drop a HIGH-confidence directional after one bad day.**

## Why the Pattern Is Real

`round5/plots/within_category_xcorr_summary.csv` shows **negative lag-0 correlations** between XL and the smaller variants. This is consistent with a "category total demand is fixed, larger pebbles substitute for smaller ones" mechanic. Whether IMC designed it this way or it's emergent from the simulator's bot logic, it transfers across days — making it a structural relationship, not a fitted one.

## Links

[[Products/Round5_Categories]] · [[Strategies/Directional_Holding]] · [[Strategies/HEDGED_NO_SKEW]] (for the SNACKPACK analog) · [[Concepts/Backtester_vs_Competition]] · [[Parameters/Round5_Params]] · [[Rounds/Round5_findings]] · [[Backtests/Phase13_R5_Directional]]

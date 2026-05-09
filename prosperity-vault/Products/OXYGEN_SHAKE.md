---
type: product
tags: [round5, oxygen-shake, directional, garlic-outlier, blacklist-heavy]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/plots/full_day_optimal.csv
updated: 2026-05-02
---

# OXYGEN_SHAKE (Liquid Breath Oxygen Shakes 🥤)

**Category:** Oxygen Shakes · **Position limit:** ±10 per product · **Outlier:** OXYGEN_SHAKE_GARLIC (counterintuitive — taste suggests low demand, mid says high demand)

The category with **the single biggest directional winner** (GARLIC +10) plus **multiple consistent MM losers** (MORNING_BREATH, MINT). Three of five sub-products are blacklisted in v42.

## Per-Product Disposition (v42)

| Product | Day-2 mid avg | v42 strategy | Reason |
|---|---|---|---|
| **OXYGEN_SHAKE_GARLIC** | 11,058 (highest) | **+10 directional** | full-day +1,829 / +111 / +1,959 (HIGH-conf) |
| OXYGEN_SHAKE_CHOCOLATE | 9,356 | default MM | Phase 14 OBI flag (t_HAC OOS +2.07 at H=10) |
| OXYGEN_SHAKE_EVENING_BREATH | 9,185 | TIER3 (LIMIT=5) | small loss −$30 v34; kept |
| OXYGEN_SHAKE_MINT | 9,894 | **BLACKLIST** | v34 −$969, v40 −$1,384 |
| OXYGEN_SHAKE_MORNING_BREATH | 10,584 | **BLACKLIST** | v34 −$1,258, v40 −$2,410 (worst in category) |

## OXYGEN_SHAKE_GARLIC — Top Single-Product Contributor

`full_day_optimal.csv`:
```text
GARLIC: d2=+1,829, d3=+111, d4=+1,959, sign_stable=True, recommend_pos=+10
        est_d4_pnl=+$19,535 (3rd-highest single-product estimate after PEBBLES_XL and BH)
```

Real Prosperity contribution: **+$19,510 day-4 measured** (Phase 13 SUMMARY). The day-3 small drift (+111) is noise on a small magnitude; the day-2 and day-4 drifts are decisively bullish.

The "GARLIC outlier" question — why is the (presumably) least-appetizing flavor the most expensive? Probably an IMC-designed contrarian pattern, but the wiki doesn't try to explain the narrative. The data says +10 directional, the data wins.

## The Blacklisted Pair (MINT, MORNING_BREATH)

Both are tight-spread products with mixed-drift day-by-day patterns and consistent multi-version losses. Textbook adverse-selection-prone:

```text
v34 (LIMIT=5 in TIER3):    MINT −$969    MORNING_BREATH −$1,258
v40 (LIMIT=10 default):    MINT −$1,384  MORNING_BREATH −$2,410
                                ↑ ~1.4×        ↑ ~1.9×
```

Doubling LIMIT roughly doubles the loss — the volume-scaling adverse-selection signature. v42 promotes both to BLACKLIST (LIMIT=0).

## EVENING_BREATH — Why TIER3, Not Blacklist

v34 PnL: −$30 (basically zero). The bracket `s̄ + α` is right at zero — quoting captures the spread approximately equal to adverse-selection cost. Keeping it at TIER3 (LIMIT=5) preserves capacity for any upside scenario without significant downside.

If a future version showed the loss growing (e.g. v40 with LIMIT=10 → meaningful loss), we'd promote it to BLACKLIST. The data hasn't shown that yet.

## CHOCOLATE — Phase 14 OBI Signal

Phase 14 flagged OXYGEN_SHAKE_CHOCOLATE at horizon H=10 with **t_HAC OOS = +2.07** and β_train = +5.24 (LONG signal). This was one of the 8 day-4-OOS-significant OBI signals. It didn't graduate to a v42 directional or directional+OBI-tilt because:
- The Phase 14 → Phase 15 graduation didn't happen (Phase 15 went to ML deadends)
- CHOCOLATE doesn't have HIGH-confidence drift (mixed full-day signs)
- Default MM works for this product

Future research could add OBI tilt to CHOCOLATE's MM quotes ("β_train > 0 → tilt bid up") but it wasn't shipped in v42.

## Links

[[Products/Round5_Categories]] · [[Strategies/Directional_Holding]] · [[Strategies/TIER3_Market_Making]] · [[Strategies/Cross_Version_Blacklist]] · [[Backtests/Phase14_R5_EDA]] · [[Concepts/Adverse_Selection]] · [[Parameters/Round5_Params]]

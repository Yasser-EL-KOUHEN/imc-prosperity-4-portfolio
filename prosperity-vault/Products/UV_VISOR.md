---
type: product
tags: [round5, uv-visor, directional, both-window-consistent]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/plots/full_day_optimal.csv
updated: 2026-05-02
---

# UV_VISOR (UV-Visors 🕶️)

**Category:** UV-Visors · **Position limit:** ±10 per product · **Pattern:** color-spectrum-like ordering (AMBER lowest, YELLOW/RED highest)

A category with **two clean directional bets** (AMBER −10, RED +10), both surviving the strictest "both-window-consistent" filter. AMBER is one of only 2 products in v38's defensive minimal portfolio.

## Per-Product Disposition (v42)

| Product | Day-2 mid avg | v42 strategy |
|---|---|---|
| UV_VISOR_YELLOW | 10,790 | default MM |
| **UV_VISOR_AMBER** | 9,177 (lowest) | **−10 directional** |
| UV_VISOR_ORANGE | 9,877 | default MM (TIER1 v26 era — top earner +$3,203 in v9) |
| **UV_VISOR_RED** | 10,778 | **+10 directional** |
| UV_VISOR_MAGENTA | 10,399 | default MM (was on local-BT blacklist; removed) |

## UV_VISOR_AMBER — Twin of MICROCHIP_OVAL

Both-window-consistent DOWN across all 3 days. Together with MICROCHIP_OVAL, these are the only two products that survived v38's defensive minimal-portfolio filter (only HIGH-confidence sign-stable in BOTH the Prosperity window AND the full day).

`full_day_optimal.csv`:
```text
UV_VISOR_AMBER: full-day drifts consistent − across days 2/3/4
                Prosperity-window drifts also consistent −
```

Real Prosperity v34 PnL: **+$4,164**. v9 (first MM-era version): **+$4,164** also. v36 (with cross-version blacklist): kept directional, +$4,164. **The single most stable directional bet alongside MICROCHIP_OVAL.**

## UV_VISOR_RED

Sign-stable + across all 3 days at full-day window. v34 PnL **+$5,856** (verified). v36 same. The 2nd-highest single-product contribution after PEBBLES_XL (+$9,561) in v34's Prosperity log.

## UV_VISOR_ORANGE — The TIER1 Default-MM Earner

ORANGE was a TIER1 product in v26 (MM_LIMIT bumped to 10) based on +$3,203 earnings in v9's Prosperity log. Phase 14 OBI analysis flagged ORANGE at horizon 5 with t_HAC OOS = +2.21 (LONG signal). It's a strong candidate for directional add but never quite met the HIGH-confidence sign-stable bar — it stayed at default MM.

If you ran more versions and confirmed the OBI signal, ORANGE could move to directional +10 in a future iteration.

## UV_VISOR_MAGENTA — Removed from Local-BT Blacklist

MAGENTA was in v14's local-BT-derived blacklist. The Prosperity log evidence (v23+) showed MM works fine on it. v23 removed the local-BT blacklist entirely; subsequent versions left MAGENTA at default MM. This is a small case study in why **local-BT blacklists don't transfer** ([[Research/Decisions_Log|D20]]).

## Within-Category Structure

The mid-price ordering loosely tracks color-spectrum brightness/wavelength but not cleanly enough to drive a basket trade. Returns correlations are mostly noise; the within-category correlation summary doesn't show |ρ| > 0.5 for any UV_VISOR pair.

## Links

[[Products/Round5_Categories]] · [[Products/MICROCHIP]] (other both-window-consistent) · [[Strategies/Directional_Holding]] · [[Backtests/Phase14_R5_EDA]] (OBI on ORANGE) · [[Parameters/Round5_Params]] · [[Research/Decisions_Log]]

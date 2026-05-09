---
type: product
tags: [round5, panel, conflict-product, panel-2x4, blacklist]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/plots/full_day_optimal.csv
  - round5/plots/drift_audit.csv
updated: 2026-05-01
---

# PANEL (Construction Panels 🪟)

**Category:** Construction Panels · **Position limit:** ±10 per product · **Mid-price ordering:** roughly increasing with panel area (1×2 < 2×2 < 1×4 < 2×4 ≈ 4×4)

A category with **one strong directional winner** (PANEL_2X4) and **multiple confirmed adverse-selection losers** (1×2, 1×4, 2×2). The decision tree:
- 1 directional +10 (PANEL_2X4 — full-day +)
- 4 of 5 sub-products MM-blacklisted in v42

## Per-Product Disposition (v42)

| Product | Day-2 mid avg | v42 strategy | Reason |
|---|---|---|---|
| PANEL_1X2 | 9,232 | **BLACKLIST** | v34 −$929, v40 −$1,654 (un-TIER3 disaster) |
| PANEL_2X2 | 9,807 | **BLACKLIST** | v34 −$1,464, v40 −$2,180 |
| PANEL_1X4 | 10,022 | **BLACKLIST** | v34 −$1,007, v40 −$1,626 |
| **PANEL_2X4** | 10,714 | **+10 directional** | full-day drift +738 / +738 / +895 (HIGH-conf) |
| PANEL_4X4 | 10,040 | default MM | top earner historically (+$4,370 in v34); KEEP |

## PANEL_2X4 — The Only Sign-Stable Directional

`full_day_optimal.csv`:

```text
PANEL_2X4: d2=+738, d3=+738, d4=+894.5, sign_stable=True, recommend_pos=+10, est_d4_pnl=+$8,895
```

The day-2 and day-3 drifts are **literally identical** (+738 / +738) — almost suspiciously deterministic. Day-4 +895 confirms the trend.

## v36's Mistake (and v34/v42's correction)

v36 blacklisted PANEL_2X4 because the cross-version Prosperity log evidence showed avg PnL = −$3,452 (deterministic per-run loss in the **first 10% window**). But:

```text
drift_audit.csv  PANEL_2X4:
  pw_d2=+100,    pw_d3=+84,    pw_d4=−341     pw_sign_consistent=0 (mixed)
  fw_d2=+738,    fw_d3=+738,   fw_d4=+894.5   fw_sign_consistent=+1
```

The Prosperity window has the day-4 piece **negative** (−341) — first 10% of the day catches a dip. The full day recovers strongly (+894.5). Blacklisting on Prosperity-window evidence sacrifices the full-day +$8,895.

v42 keeps PANEL_2X4 directional **despite** the cross-version Prosperity loss because the full-day evidence dominates. This is a different rule from the BLACK_HOLES case (which is also conflict but with stronger PW negativity all 3 days, hence v37's flip-and-fail).

## The 3 Blacklisted PANELs

PANEL_1X2, PANEL_2X2, PANEL_1X4 are textbook adverse-selection-prone products:
- Tight spreads (1–4 ticks)
- Mixed full-day drifts (no clean directional)
- Consistent multi-version losses at LIMIT=5 (TIER3) and 2× the loss at LIMIT=10 (v40 evidence)

The bracket `s̄ + α < 0` is decisively negative. v42 blacklists them entirely.

## PANEL_4X4 — The Surprise Top Earner

PANEL_4X4 was a TIER1 product in v26 (top earner > $2K Prosperity) with v34 +$4,370. Despite the mixed-drift profile (`d2=−322, d3=+574, d4=−1,127`), MM at default LIMIT works because:
- Spread is wide enough for spread capture (largest panel = highest absolute price → wider absolute spread)
- No structural anti-correlation to exploit (the 1×4/2×2 substitutes are blacklisted)
- Inventory builds and unwinds within the day at the default skew threshold

This is the case where **default MM** wins: not flashy, just consistent.

## Links

[[Products/Round5_Categories]] · [[Strategies/Cross_Version_Blacklist]] · [[Strategies/TIER3_Market_Making]] · [[Strategies/Directional_Holding]] · [[Concepts/Backtester_vs_Competition]] · [[Concepts/Adverse_Selection]] · [[Parameters/Round5_Params]]

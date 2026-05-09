---
type: product
tags: [round5, robot, blacklist-heavy, zero-fill]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/plots/full_day_optimal.csv
updated: 2026-05-02
---

# ROBOT (Domestic Robots 🤖)

**Category:** Domestic Robots · **Position limit:** ±10 per product · **Pattern:** mixed within-category; 2 of 5 blacklisted

A category with **no directional bets** and **two BLACKLIST entries** (DISHES, LAUNDRY). The remaining three are at default MM with one (IRONING) being a top earner.

## Per-Product Disposition (v42)

| Product | Day-2 mid avg | v42 strategy | Reason |
|---|---|---|---|
| ROBOT_VACUUMING | 9,747 | default MM | mixed; manageable v34 PnL |
| ROBOT_MOPPING | 10,539 | default MM | wide-spread; sufficient earnings |
| **ROBOT_DISHES** | 9,473 | **BLACKLIST** (zero-fill) | earns $0 in any version |
| **ROBOT_LAUNDRY** | 10,274 | **BLACKLIST** | v34 −$1,000, v40 −$1,782 (un-TIER3 disaster) |
| ROBOT_IRONING | 9,354 (lowest in cat) | default MM (TIER1 v26 era) | top earner +$2,408 in v9 |

## ROBOT_DISHES — Zero-Fill

Like GALAXY_SOUNDS_PLANETARY_RINGS and TRANSLATOR_SPACE_GRAY, ROBOT_DISHES is a **zero-fill product**: our MM quotes don't get filled in any version (probably the bot doesn't quote two-sided enough, or our MM gets priced out by the bot's tighter quotes). Earnings = $0 across all measured versions.

Blacklisting is **costless** for these zero-fill products — saves no losses but also costs no upside. Kept on the blacklist for clarity (so the iteration code doesn't spend cycles on them).

## ROBOT_LAUNDRY — The TIER3-Removal Casualty

LAUNDRY was at TIER3 (LIMIT=5) in v26 onward with v34 PnL **−$1,000**. v40 promoted it to LIMIT=10 default MM under the "more trading = recovery" hypothesis. Result: **−$1,782** (1.78× loss = textbook adverse-selection volume scaling).

v42 BLACKLISTED it. The bracket `s̄ + α` is decisively negative on Prosperity at LIMIT=10; even at LIMIT=5 (TIER3) it loses $1K/run. Stop trading it.

## ROBOT_IRONING — Surprise Top Earner

IRONING has the **lowest mid avg** in the category (9,354) and was promoted to TIER1 in v26 based on **+$2,408 v9 Prosperity earnings**. v34 confirmed: **+$2,408**. The MM strategy works because:
- Spread is reasonable (typical 2–3 ticks)
- Bot is quoting both sides actively
- No structural anti-correlation to fight

This is a case where **default MM at top tier (LIMIT=10)** quietly accumulates without needing any clever logic.

## ROBOT_MOPPING — Phase 14 Volatility-Adjusted

Phase 14's analyses didn't flag MOPPING as significant. It's at default MM. v9 had it earning +$2,352 day-3 alone. Mixed across days, but within v34's evidence it's a manageable earner.

## ROBOT_VACUUMING — Removed from v14 Local-BT Blacklist

VACUUMING was on v14's local-BT blacklist along with PEBBLES_M, MOPPING, SOLAR_FLAMES, MAGENTA, TRANSLATOR_SPACE_GRAY, PANEL_1X2, PANEL_4X4. **All but TRANSLATOR_SPACE_GRAY were wrong** (too aggressive blacklisting on local-BT data). v23 onwards: VACUUMING runs at default MM successfully.

## Pattern Across the Category

ROBOT is the category with **no clean within-category structure** (no monotone mid ordering, no strong correlations). Each product is treated independently. This is the **default case** in R5: no basket, no pair, no directional — just per-product MM with blacklisting where the data demands.

## Links

[[Products/Round5_Categories]] · [[Strategies/Cross_Version_Blacklist]] · [[Strategies/TIER3_Market_Making]] · [[Concepts/Adverse_Selection]] · [[Parameters/Round5_Params]]

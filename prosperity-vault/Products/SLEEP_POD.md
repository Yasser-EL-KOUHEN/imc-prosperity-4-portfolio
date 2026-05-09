---
type: product
tags: [round5, sleep-pod, lamb-wool-disaster, blacklist]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/plots/full_day_optimal.csv
updated: 2026-05-02
---

# SLEEP_POD (Vertical Sleeping Pods 🛏️)

**Category:** Vertical Sleeping Pods · **Position limit:** ±10 per product · **Notable:** SLEEP_POD_LAMB_WOOL is the most-blacklisted product in R5 history

A category with **no clean directional bets** and **one consistent loser** (LAMB_WOOL). Mostly default MM with one BLACKLIST.

## Per-Product Disposition (v42)

| Product | Day-2 mid avg | v42 strategy | Notes |
|---|---|---|---|
| SLEEP_POD_SUEDE | 10,255 | default MM (TIER1 v9 era) | top earner +$5,016 train avg in v35 BT |
| **SLEEP_POD_LAMB_WOOL** | 10,769 | **BLACKLIST** | tried directional +10 (v9, v40) and default MM (v34); both failed |
| SLEEP_POD_POLYESTER | 10,697 | default MM | UNSTABLE classification but acceptable Prosperity result |
| SLEEP_POD_NYLON | 9,511 (only sub-9,500 in cat) | default MM (TIER1 v9 era) | +$2,212 in v9 |
| SLEEP_POD_COTTON | 10,738 | default MM | top earner v34 +$5,133 |

## SLEEP_POD_LAMB_WOOL — The Most-Blacklisted Product in R5

LAMB_WOOL has been tried in **every possible MM configuration** across v1→v42:

| Version | LAMB_WOOL configuration | Result |
|---|---|---|
| v9 | Directional +10 | **−$5,978** |
| v23 | Removed from directional, default MM | **−$2,525** (v23 was first PnL-improvement re-design) |
| v34 | Default MM (no directional, no blacklist) | **−$4,284** |
| v40 | Directional +10 again (full-day-bet hypothesis) | **−$5,978** (worst tested) |
| **v42** | **BLACKLIST** | $0 (saved) |

The cross-version Prosperity log evidence (`avg PnL = −$3,905, 0/12 positive`) was the v36 signal. v40 ignored it (full-day hypothesis: small +$16 day-4 drift might recover) and got the same −$5,978. v42 stops trying.

**This is the textbook example of a product where the data tells you "stop trading me" and the strategy needs to listen.**

## Why Default MMs Win on the Other 4

SUEDE (+$5,016 train avg in v35 BT), COTTON (+$5,133 v34 Prosperity), NYLON (+$2,212 v9), POLYESTER (+$2,158 v9) — these are top earners under simple default MM at LIMIT=10:

- Wider absolute spreads (high-mid products → wider bid-ask in absolute terms)
- Adequate liquidity (the bot quotes both sides regularly)
- No structural anti-correlation to exploit (within-category correlations are noise)

Default MM **just works** — no skew tuning needed beyond the standard SKEW_THRESHOLD=6, no directional bet needed. The category contributes most of its profit through SUEDE/COTTON/NYLON/POLYESTER's MM operations while LAMB_WOOL is excluded.

## NYLON — The Sub-9,500 Outlier

NYLON is the only SLEEP_POD with day-2 mid avg under 9,500 (avg 9,511 vs 10,000 for the other 4). It was hypothesised early on as a potential structural undervaluation — possible mean-reversion target. But:
- AR(1) ρ ≈ 0.999 (no mean reversion at tick level)
- No clean drift sign across days
- MM works fine at default settings

So it stays at default MM. The "structural undervaluation" hypothesis didn't translate to a tradable signal.

## Phase 14 — No SLEEP_POD Signals Survived

Phase 14's analyses (autocorrelation, OBI, Donchian, trajectory shape, XGBoost) didn't flag any SLEEP_POD product as a day-4-OOS-significant signal. The category is profitable through default MM and not through ML or microstructure signals.

## Links

[[Products/Round5_Categories]] · [[Strategies/Cross_Version_Blacklist]] · [[Concepts/Adverse_Selection]] · [[Strategies/Round5_Version_History]] (LAMB_WOOL appears in v9, v23, v34, v36, v40, v42 entries) · [[Parameters/Round5_Params]]

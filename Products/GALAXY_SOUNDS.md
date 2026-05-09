---
type: product
tags: [round5, galaxy-sounds, conflict-product, black-holes, zero-fill]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/plots/full_day_optimal.csv
  - round5/plots/drift_audit.csv
updated: 2026-05-02
---

# GALAXY_SOUNDS (Galaxy Sounds Recorders 🎙️)

**Category:** Galaxy Sounds Recorders · **Position limit:** ±10 per product · **Includes the canonical R5 conflict product** (BLACK_HOLES)

The category that produced the most painful R5 lesson: **GALAXY_SOUNDS_BLACK_HOLES is the only conflict product** in `drift_audit.csv` — Prosperity-window drift and full-day drift point in **opposite directions** every day. v37 trusted the Prosperity-window evidence and lost $26K.

## Per-Product Disposition (v42)

| Product | Day-2 mid avg | v42 strategy | Reason |
|---|---|---|---|
| GALAXY_SOUNDS_DARK_MATTER | 10,112 | **BLACKLIST** | v34 −$938, v40 −$2,384 |
| **GALAXY_SOUNDS_BLACK_HOLES** | 10,680 | **+10 directional (conflict product)** | full-day + (+1,447 / +689 / +1,321), Prosperity-window − |
| GALAXY_SOUNDS_PLANETARY_RINGS | 10,013 | **BLACKLIST** (zero-fill) | earns $0 in any window |
| GALAXY_SOUNDS_SOLAR_WINDS | 10,067 | TIER3 (kept from v36) | small mixed loss; Phase 14 OBI flag (SHORT) |
| GALAXY_SOUNDS_SOLAR_FLAMES | 11,096 | default MM (returned from v14 local-BT blacklist) | mixed; manageable |

## BLACK_HOLES — The Conflict Product

`drift_audit.csv`:
```text
                pw_d2     pw_d3     pw_d4     |  fw_d2     fw_d3     fw_d4
BLACK_HOLES   −85.5     −53.5     −65.0     |  +1,446.5   +688.5    +1,320.5
              ↓          ↓          ↓             ↑          ↑          ↑
              all 3 days NEGATIVE in Prosperity window
              all 3 days POSITIVE in full day
```

**This is the only product in R5 with `conflict=True`** in `drift_audit.csv` (windows sign-consistent in opposite directions). Every other "conflict" is just one window mixed and the other consistent.

## v37's Mistake (the most expensive single decision)

v37 changed exactly one thing vs v36: flipped GALAXY_SOUNDS_BLACK_HOLES from "removed from directional" to **directional −10** (using the Prosperity-window evidence).

Estimated Prosperity-window gain: ~+$1,324 (the deterministic per-run negative drift would now flip to positive at −10 position).

**Estimated full-day cost: −$26,310** (BH +10 → +$13,155 becomes BH −10 → −$13,155, swing of $26,310).

This is the single most expensive R5 decision in the v1→v42 evolution. Documented as a load-bearing lesson in [[Concepts/Backtester_vs_Competition]] and [[Strategies/Round5_Version_History|v37 entry]].

## v42's Choice: Trust the Full Day

v42 keeps BLACK_HOLES at **+10 directional** (the v34 setup, NOT v36's removal or v37's flip). Rationale:
- Full-day drift is sign-stable + on **all 3 days**
- The drift magnitude is significant (+$13K full-day at +10)
- Cross-version Prosperity log loss (avg −$732/run) is real but small relative to the full-day gain
- The conflict has a clear interpretation: BLACK_HOLES sells off in the morning then recovers strongly through the day

If competition scoring is full-day → +$13K/run. If competition scoring is first-10% → −$732/run. Asymmetric upside; take it.

## DARK_MATTER — Why Blacklisted

```text
DARK_MATTER  v34: −$938   v40: −$2,384 (LIMIT=10 doubled the loss)
             cross-version avg: −$1,503
             0/12 positive runs
```

Textbook adverse-selection pattern with no offsetting drift signal. v42 BLACKLIST.

## PLANETARY_RINGS — Zero-Fill

`PLANETARY_RINGS earns $0 across all measured Prosperity runs.` Either the bot doesn't quote two-sided enough for our MM to fill, or our MM quotes get systematically priced out. Either way, blacklisting is **costless** — we save no losses but also lose no gains. Kept on the blacklist for clarity.

## SOLAR_WINDS — Phase 14 OBI SHORT Signal

Phase 14 flagged SOLAR_WINDS at horizon H=25 with **t_HAC OOS = −2.04** and β_train = −8.04 (SHORT signal). It also has small consistent multi-version losses (−$370 in v36). Kept at **TIER3** in v42 — small enough to preserve capacity for the OBI signal if future research wants to act on it.

## SOLAR_FLAMES — Returned from v14 Blacklist

SOLAR_FLAMES was in v14's local-BT-derived blacklist along with PEBBLES_M (which we now know is a positive contributor). v23 removed the local-BT blacklist; SOLAR_FLAMES has been at default MM since. Real-Prosperity evidence shows it's manageable — neither blacklist nor TIER3 needed.

## Links

[[Products/Round5_Categories]] · [[Concepts/Backtester_vs_Competition]] (canonical conflict-product example) · [[Strategies/Round5_Version_History]] (v37 cautionary tale) · [[Strategies/Cross_Version_Blacklist]] · [[Backtests/Phase14_R5_EDA]] · [[Parameters/Round5_Params]]

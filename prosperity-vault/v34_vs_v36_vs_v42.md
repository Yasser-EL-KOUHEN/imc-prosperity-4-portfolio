---
type: competition
tags: [round5, comparison, v34, v36, v42, decision-page]
sources:
  - round5/strategies/round5_v34_trader.py
  - round5/strategies/round5_v36_trader.py
  - round5/strategies/round5_v42_trader.py
  - round5/logs/v34/575850.json (verified)
  - round5/logs/v36/578532.json (verified)
  - round5/logs/v40/579308.json (verified, used for delta-from-v34 baseline)
  - User_Reported_Anchors (v42 backtester = $72K)
updated: 2026-05-02
---

# v34 vs v36 vs v42 — Side-by-Side Decision Page

> The single page to read when you need to understand why **v42** was submitted, not v36 (the backtester champion) or v34 (the v34-era best directional setup).

## Headline Numbers

| Metric | v34 | v36 | **v42 (SUBMITTED)** |
|---|---|---|---|
| Backtester PnL (real Prosperity, first 10% of Day 4) | $62,299 | **$78,799** ⭐ | **$72,000** |
| Estimated full-day PnL (pre-result) | **$152,730** ⭐ | $130,680 | ~$163,000 *(SUPERSEDED)* |
| **Realized full-day PnL (Day 5 competition)** | not run | not submitted | **$57,911** |
| Backtester rank | 4th | 1st | 2nd |
| Status | superseded | not submitted | **SUBMITTED** |

⭐ = winner on that metric. v36 is the backtester local-optimum; v42 is the chosen-for-robustness submission.

## Configuration Differences

### Directional positions (Layer 1)

| Product | v34 | v36 | v42 |
|---|---|---|---|
| MICROCHIP_OVAL | −10 | −10 | −10 |
| PEBBLES_XL | +10 | +10 | +10 |
| OXYGEN_SHAKE_GARLIC | +10 | +10 | +10 |
| **GALAXY_SOUNDS_BLACK_HOLES** | **+10** | _(removed → MM blacklist)_ | **+10** |
| PEBBLES_S | −10 | −10 | −10 |
| PEBBLES_XS | −10 | −10 | −10 |
| **PANEL_2X4** | **+10** | _(removed → MM blacklist)_ | **+10** |
| UV_VISOR_AMBER | −10 | −10 | −10 |
| UV_VISOR_RED | +10 | +10 | +10 |
| SNACKPACK_PISTACHIO | −10 | −10 | −10 |
| PEBBLES_M | −10 | −10 | −10 |
| PEBBLES_L | −10 | −10 | −10 |
| **SNACKPACK_STRAWBERRY** | _(not directional)_ | _(not directional)_ | **+10** (v41/v42 add) |
| **# directional products** | 12 | 10 | **13** |

### MM_BLACKLIST (Layer 2 — products excluded from MM)

| Product | v34 | v36 | v42 | Reason |
|---|---|---|---|---|
| TRANSLATOR_SPACE_GRAY | yes | yes | yes | zero-fill (earns $0) |
| GALAXY_SOUNDS_PLANETARY_RINGS | yes | yes | yes | zero-fill |
| ROBOT_DISHES | yes | yes | yes | zero-fill |
| SLEEP_POD_LAMB_WOOL | _no (default MM −$4,284)_ | **YES** (avg cross-version −$3,905) | **YES** | confirmed loser every config |
| PANEL_2X4 | _no (kept directional +10)_ | **YES** ⚠ | _no (kept directional +10)_ | **PW −$3,452 BUT FW +$8,895 → conflict** |
| GALAXY_SOUNDS_BLACK_HOLES | _no (kept directional +10)_ | **YES** ⚠ | _no (kept directional +10)_ | **PW −$732 BUT FW +$13,155 → conflict** |
| GALAXY_SOUNDS_DARK_MATTER | TIER3 (−$938) | yes | **YES** | confirmed loser, scale w/ vol |
| OXYGEN_SHAKE_MORNING_BREATH | TIER3 (−$1,258) | yes | **YES** | confirmed loser |
| PANEL_2X2 | TIER3 (−$1,464) | yes | **YES** | confirmed loser |
| ROBOT_LAUNDRY | TIER3 (−$1,000) | yes | **YES** | confirmed loser |
| PANEL_1X2 | TIER3 (−$929) | yes | **YES** | confirmed loser |
| PANEL_1X4 | TIER3 (−$1,007) | yes | **YES** | confirmed loser |
| OXYGEN_SHAKE_MINT | TIER3 (−$969) | yes | **YES** | confirmed loser |
| **# blacklist entries** | **3** | **11** | **11** (different mix) |

⚠ = the two products v36 incorrectly blacklisted. v42 corrects this.

### TIER3 (LIMIT=5)

| Product | v34 | v36 | v42 |
|---|---|---|---|
| 7 ex-TIER3 (later promoted to v42 BLACKLIST) | yes | _(blacklist)_ | _(blacklist)_ |
| MICROCHIP_RECTANGLE | yes | TIER3 (−$128) | **TIER3** |
| OXYGEN_SHAKE_EVENING_BREATH | yes | TIER3 (−$30) | **TIER3** |
| **# TIER3 entries** | **9** | **2** | **2** |

### HEDGED_NO_SKEW

| Product | v34 | v36 | v42 |
|---|---|---|---|
| SNACKPACK_CHOCOLATE | HEDGED | HEDGED | HEDGED |
| SNACKPACK_VANILLA | HEDGED | HEDGED | HEDGED |

Unchanged across all three. Structural ρ = −0.916 anti-correlation; HEDGED_NO_SKEW preserved everywhere.

## Why v42 Over v36 ($6,799 Backtester Gap)

The decision rule: **the backtester is a regression-detection gate, not an optimization target.** v36 won the backtester by *over-fitting to the first-10%-of-day window*: it blacklisted PANEL_2X4 (PW: −$3,452) and BLACK_HOLES (PW: −$732), which earn **+$8,895** and **+$13,155** respectively on the **full day**. This is the canonical signature of distribution mismatch.

Calculation:

```text
v36 vs v42 backtester delta:        +$78,799 − $72,000  = +$6,799 (v36 better)
v42 keeps that v36 dropped:
  PANEL_2X4 +10 directional (FW)    +$8,895   (v36 loses this; v42 captures)
  BLACK_HOLES +10 directional (FW)  +$13,155  (v36 loses this; v42 captures)
v36 vs v42 full-day delta:          +$8,895 + $13,155 − $6,799  =  +$15,251 (v42 better)

Plus the v42 STRAWBERRY +10 add (+~$925 full-day, net of −$199 backtester loss):
  v42 net advantage on full day:   ~$15,977
```

**Cost of robustness: $6,799 of backtester. Expected return on robustness: ~$16K of full day.** 2.4× return on the gap.

## ML Analogy

This decision is exactly the **train-loss-vs-test-loss tradeoff** in any ML pipeline where the training distribution is a biased prefix of the test distribution. The v36 selection rule is "max train metric"; the v42 selection rule is "max test estimate subject to no-regression on train". When prefix and full data disagree (as in `drift_audit.csv` for PANEL_2X4 and BLACK_HOLES), the test-distribution-aware rule wins.

The Round 5 chapter is, in compressed form, **a practical demonstration of the dangers of selecting on the wrong validation split**. v37, v39, v40 are all variants of the same mistake from different angles. v42 is the version that learned the lesson.

## What v42 Is NOT

To prevent confusion when reading other pages:

- **Not the backtester champion** — v36 is.
- **Not the directional-only baseline** — v1 is (Phase 13's $19,995 baseline).
- **Not the highest-trader-PnL on local backtester** — v9/v21 are (inflated locally).
- **Not the version with the most directional positions** — v9/v14 had 13–14, v42 has 13.
- **Not "v34 + STRAWBERRY"** — that's v41. v42 = v41 + 8-product blacklist.
- **Not the "full-day-bet" version** — that's v39 (which lost the PEBBLES_XL alpha).
- **Not the "defensive" version** — that's v38 (only 2 directional bets).

## Links

[[Strategies/Round5_Version_History]] · [[Concepts/Backtester_vs_Competition]] · [[Strategies/Cross_Version_Blacklist]] · [[Backtests/PnL_Timeline]] · [[Final_Competition_Result]] · [[Parameters/Round5_Params]] · [[User_Reported_Anchors]] · [[Rounds/Round5_findings]]

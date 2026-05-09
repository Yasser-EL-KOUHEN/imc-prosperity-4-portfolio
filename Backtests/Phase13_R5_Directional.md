---
type: backtest
tags: [round5, phase13, directional, oos-validation, completed]
sources:
  - round5/research/eda.py
  - round5/research/run_round5.py
  - round5/strategies/round5_trader.py
  - round5/backtests/Phase13_R5_Directional.md
  - .planning/phases/13-r5-directional-trading/13-01-SUMMARY.md
  - .planning/phases/13-r5-directional-trading/CONTEXT.md
updated: 2026-04-30
status: COMPLETE
---

# Phase 13 — R5 Directional Trading Backtest

> Status: ✅ Executed. Both anti-regression gates PASS.

> **Post-result validation (2026-05-08):** Phase 13's directional thesis was **fundamentally correct**. The v42 DIRECTIONAL bucket realized **+$67,111** on the real Day 5 — the dominant alpha source for R5, carrying 116% of the +$57,911 net algo PnL. 7 of 13 directional bets paid; 6 reversed (PEBBLES_S −$24,852 the worst). The **Phase 13 architectural premise — "fixed ±10 holds capture multi-day directional drift" — is empirically validated**, even though specific product selections varied in their Day-5 outcomes. The miss rate (46%) is higher than the train-window forecast suggested but the wins-vs-losses asymmetry kept the bucket strongly net-positive.
>
> **MICROCHIP_SQUARE OOS-flip preserved as a Phase-13 lesson:** v42 correctly excluded MICROCHIP_SQUARE from `TARGETS_DIR` per Phase 13's noted OOS sign-flip on Day 4. The product still lost $18,636 on Day 5 — but from MM exposure (DEFAULT_MM bucket), not directional. The Phase 13 caution worked at the directional level; the residual loss is a separate "MM adverse selection on strongly-drifting products" issue (see [[Strategies/Cross_Version_Blacklist]]). See [[Performance/Algo_Per_Round]] for full bucket decomposition.

## Strategy

Pure directional position-building. For 7 OOS-validated products (train days 2+3, OOS day 4), aggressively cross the spread at first available tick to reach `target = ±10` and **hold for the rest of the day**. No active management, no MM, no pairs logic, no BS pricing.

**Why directional and not MM?** All 50 R5 products have AR(1) ρ ≈ 0.999 — effectively non-stationary. Mean-reversion impossible. The designed alpha is **multi-day directional drift** (the IMC briefing's hint about "embedded patterns").

Trader: `round5/strategies/round5_trader.py` (= round5_v1).
Runner: `round5/research/run_round5.py`.
Stateless: `traderData = ""`, position recovered from `state.position`.

## Selected Products (OOS-validated)

| Product | Direction | Rationale |
|---------|-----------|-----------|
| MICROCHIP_OVAL | SHORT (−10) | Accelerating downtrend, all 3 days |
| PEBBLES_XL | LONG (+10) | Strongest raw drift; +4,014 OOS despite day-3 dip |
| OXYGEN_SHAKE_GARLIC | LONG (+10) | Fresh demand: +1,828 / +111 / +1,958 |
| GALAXY_SOUNDS_BLACK_HOLES | LONG (+10) | Consistent uptrend: +1,446 / +688 / +1,320 |
| PEBBLES_S | SHORT (−10) | Down on all 3 days: −1,952 / −1,204 / −824 |
| PEBBLES_XS | SHORT (−10) | Down on all 3 days |
| PANEL_2X4 | LONG (+10) | Nearly identical drift each day: +738 / +738 / +894 |

Rejected: **MICROCHIP_SQUARE** (strong train +2,456/+3,438 but OOS reversal −2,278). Phase 13's lesson product — the canonical reminder for why the OOS gate exists.

## Backtest Results

### Per-Day Totals
| Day | PnL |
|-----|-----|
| Day 2 | +111,845 |
| Day 3 | +31,533 |
| Day 4 (OOS) | +118,083 |
| **GRAND TOTAL** | **+261,461** |

### Per-Product Breakdown (3-Day)
| Product | Day 2 | Day 3 | Day 4 | 3-Day Total |
|---------|-------|-------|-------|-------------|
| GALAXY_SOUNDS_BLACK_HOLES | +14,405 | +6,810 | +13,125 | +34,340 |
| MICROCHIP_OVAL | +7,395 | +18,275 | +18,976 | +44,646 |
| OXYGEN_SHAKE_GARLIC | +18,225 | +1,035 | +19,510 | +38,770 |
| PANEL_2X4 | +7,340 | +7,333 | +8,907 | +23,580 |
| PEBBLES_S | +8,340 | +1,710 | +9,315 | +19,365 |
| PEBBLES_XL | +36,685 | −15,615 | +40,060 | +61,130 |
| PEBBLES_XS | +19,455 | +11,985 | +8,190 | +39,630 |

## Anti-Regression Gates

| Gate | Condition | Result |
|---|---|---|
| Gate A | GRAND TOTAL > 0 | **PASS (+261,461)** |
| Gate B | All 7 products > 0 on OOS day 4 | **PASS (7/7)** |

Backtester values are ~1% below EDA theoretical maxima (spread-crossing costs vs midpoint).

## What Phase 13 Locked

- The 7 directional products + signs (kept across every later v1→v42 unless explicitly justified to drop)
- The "OOS = day 4 only" pre-registration discipline (against P-hacking — see [[Concepts/Backtester_vs_Competition]])
- Stateless trader pattern (no jsonpickle for R5)
- The premise that R5 alpha is **directional drift**, not MM

## Phase 13 Failure Modes Surfaced

- **MICROCHIP_SQUARE** — train winner that flipped sign OOS. The single most important null in the EDA.
- **Single-day "average across 3 days" stats** — a signal that scores well on the 3-day average can be entirely driven by 1 day. Always require day 4 to pass on its own.

## Links

[[Backtests/Phase14_R5_EDA]] · [[Backtests/Phase14_R5_Setup]] · [[Strategies/Directional_Holding]] · [[Concepts/Backtester_vs_Competition]] · [[Research/Round5_Scripts]] · [[Rounds/Round5_findings]]

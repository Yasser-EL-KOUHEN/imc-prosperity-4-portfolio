---
type: backtest
tags: [phase5, velvetfruit, passive, delta-hedge, post-r3]
sources: [backtests/phase5_vev_passive_comparison.md, backtests/phase5_delta_hedge.md]
updated: 2026-05-08
---

# Phase 5: VELVETFRUIT Passive-Only Comparison

> **Submission attribution (clarified 2026-05-08):** Phase 5's passive-only-flag refinement is in `trader_final.py` (R4 basis), not in the R3 submission `486282.py`. The realized R3 VEL PnL was −$5,834 (without the refinement); the realized R4 VEL PnL was +$4,033 (with the Phase 5 refinement plus Mark-counterparty signals). The +$9,866 swing demonstrates the Phase 5 + Phase 12 combined value. See [[Performance/Submission_Verification]].

## Experiment Setup

**Script:** `research/round3/vev_passive_comparison.py`

Two configs:
- **Baseline** (`VEV_PASSIVE_ONLY=0`): aggressive hedge sections + standalone alpha allowed
- **Passive-only** (`VEV_PASSIVE_ONLY=1`): only passive joins at best_bid/best_ask

**Gate:** all-days-win (passive ≥ baseline on every individual day)

---

## Results

### Per-Day Total PnL

| Day | Baseline Total | Passive-Only Total | Delta | Wins |
|-----|---------------|-------------------|-------|------|
| 0 | 52,941 | **53,780** | **+839** | YES |
| 1 | 47,432 | 47,432 | 0 | YES (tie) |
| 2 | 42,302 | 42,302 | 0 | YES (tie) |
| **Total** | **142,675** | **143,514** | **+839** | **PASS** |

### VEV Standalone PnL

| Day | Baseline VEV | Passive-Only VEV | Delta |
|-----|-------------|-----------------|-------|
| 0 | 3,937 | **4,518** | **+581** |
| 1 | 1,990 | 1,990 | 0 |
| 2 | 1,104 | 1,104 | 0 |
| **Total** | **7,031** | **7,612** | **+581** |

**WINNER: Passive-only (+839 total, +581 VEV standalone)**

---

## Analysis

The +839 gain comes entirely from **day 0**:
- Day 0: +839 total (+581 VEV standalone + remaining from better HYDROGEL execution without competing limit usage)
- Days 1/2: exact ties — the aggressive sections never fired (delta stayed below `DELTA_CAP_HARD` and mean-reversion edge never reached 2.0)

**Implication:** The -90K day 2 loss from v2's aggressive hedger was a v1/v2-specific bug (the spread-crossing was uncontrolled in those versions). The current codebase's aggressive sections were already tightly guarded enough that they had zero impact on days 1/2.

**v2 lesson reinforced:** Even tightly guarded spread-crossing left money on the table on day 0. Disabling it entirely improved d0 PnL by 839.

---

## New Phase 5 Baseline

| Metric | Value |
|--------|-------|
| d0 | 53,780 |
| d1 | 47,432 |
| d2 | 42,302 |
| 3d total | **143,514** |
| vs Phase 4 | **+839** |

---

## Links

[[Products/VELVETFRUIT_EXTRACT]] · [[Strategies/Delta_Hedging]] · [[Parameters/VELVETFRUIT_Params]] · [[Backtests/PnL_Timeline]]

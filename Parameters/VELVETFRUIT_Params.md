---
type: reference
tags: [velvetfruit, parameters, hedge, passive, round3, round4, post-r3]
sources: [round3/trader_final.py, round4/trader.py, performance/algorithmic trading/round 3/486282.py, backtests/phase5_vev_passive_comparison.md, backtests/phase5_delta_hedge.md]
updated: 2026-05-08
---

# VELVETFRUIT_EXTRACT Parameters

> **Submission attribution (clarified 2026-05-08):** the parameter set below describes the **post-R3 refinement** in `trader_final.py` (the R4 basis). Phase 5's "passive-only-flag" refinement is in this file but was *not* in the R3 submission `486282.py` (which used the v3 hedger logic without the passive-only flag). VEL realized PnL: R3 **−$5,834** (un-refined), R4 **+$4,033** (refined + Mark signals). See [[Performance/Submission_Verification]].

All parameters from `round3/trader_final.py` (R4 basis) — `VEVUnderlying` class.

---

## Core Parameters

| Parameter | Value | Env var | Source |
|-----------|-------|---------|--------|
| `LIMIT` | **200** | — | Fixed |
| `VEV_PASSIVE_ONLY` | **True (1)** | `VEV_PASSIVE_ONLY` | Phase 5 experiment (+839 over baseline) |

---

## Passive-Only Mode

When `VEV_PASSIVE_ONLY=True` (default):
- **Allowed:** Join at `best_bid` (passive buy for positive hedge)
- **Allowed:** Join at `best_ask` (passive sell for negative hedge)
- **Forbidden:** Cross the spread (no aggressive hedging)
- **Removed:** Sections 1 (aggressive hedge) and 2 (standalone alpha) — both gated off

**Gate result (Phase 5):**

| Day | Baseline | Passive-only | Delta |
|-----|----------|-------------|-------|
| 0 | 52,941 | 53,780 | +839 |
| 1 | 47,432 | 47,432 | 0 |
| 2 | 42,302 | 42,302 | 0 |

All-days-win gate: **PASS**. Days 1/2 tied because aggressive sections never fired (delta stayed below cap).

---

## Delta Hedge Target

The hedge target is computed from the `GreeksLedger`:

```python
target_pos = -aggregate_delta * spot_fair
hedge_needed = target_pos - current_pos
```

The `GreeksLedger` accumulates per-fill deltas from all options trades across all strikes.

---

## Env-Var Override Hook

`VEV_PASSIVE_ONLY` defaults to `"1"` (true) in `VEVUnderlying.__init__`. Override with:
```bash
VEV_PASSIVE_ONLY=0 python run_round3.py  # re-enable aggressive mode for testing
```

---

## Historical Context

| Version | VEV Mode | Day 2 Result |
|---------|----------|-------------|
| v1 | Aggressive spread-crossing | -90,000 loss |
| v2 | Controlled aggressive | Better, but still spread-crossing |
| v3 | Passive-only (current) | +4,154 / +1,044 / +138 per day |

---

## Links

[[Products/VELVETFRUIT_EXTRACT]] · [[Strategies/Delta_Hedging]] · [[Backtests/Phase5_VEV_Passive]] · [[Parameters/Options_Params]]

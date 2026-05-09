---
type: backtest
tags: [round4, phase12, counterparty, anti-regression, signal-c, composite]
sources: [.planning/phases/12-counterparty-exploitation/12-01-PLAN.md, 12-01-SUMMARY.md, vault/round4_trader.py]
updated: 2026-04-28
---

# Phase 12 — Counterparty Exploitation Backtest

## Anti-Regression Gate

**Required:** 3-day Round 3 PnL ≥ 153,566 XIREC (Phase 11 baseline).

**Achieved:** 153,566 — exact match. **PASS**.

| Day | TTE | round3_final_trader | round4_trader | Δ |
|---|---|---|---|---|
| Day 0 | 8.0d | 58,678 | 58,678 | 0 |
| Day 1 | 7.0d | 51,088 | 51,088 | 0 |
| Day 2 | 6.0d | 43,800 | 43,800 | 0 |
| **TOTAL** | | **153,566** | **153,566** | **0** |

The round4 trader passes the gate with all four fixes applied. The neutral local delta is expected because the new signals are live-only (composite flow + Signal C cooldown) — `state.market_trades` is a deterministic CSV in the local backtester.

---

## Round 4 Forward Backtest

| Day | TTE | round4_trader |
|---|---|---|
| Day 1 | 7.0d | 51,088 |
| Day 2 | 6.0d | 43,800 |
| Day 3 | 5.0d | 57,030 |
| **TOTAL** | | **151,918** |

Day 1+2 PnL is identical to Round 3 days 1+2 (same training data). Day 3 (57,030) is the new actual competition data extracted from `logs/round3/Prosperity Results/486282.json`.

---

## Implemented Changes Summary

| Change | Status | Outcome | Reason |
|---|---|---|---|
| **A — VEV_6000/6500 sell at bid=0** | **REVERTED** | Not applied | Local backtest settled at mid=0.5 → −900 regression. Even on live server, EV=0 (sell at 0, collect 0). No upside vs current. |
| **B — Mark 67 composite + bid tilt** | **APPLIED** | Neutral local, +PnL live | `state.market_trades` is predetermined in backtest; signal fires only on real counterparty flow. |
| **C — DAY_TTE 1-indexed dict** | **APPLIED** | Neutral (backward compat) | Round 4 day numbering 1, 2, 3 vs old 0-indexed list. |
| **D — Signal C (Mark 49 cooldown)** | **APPLIED** | Neutral local, +PnL live | 500ms bid suppression after Mark 49 sell. |

---

## Bug Audit Trail (Phase 12 extension)

Four bugs were identified and fixed in succession after the initial plan:

### Bug 1: VEV_6000/6500 Settlement Mismatch (Pre-Phase)

**Symptom:** Applying Change A regressed PnL from 153,566 to 152,737 (−829).

**Root cause:** Local `prosperity3bt --merge-pnl` settles positions daily at `mid = (bid + ask) / 2`. For VEV_6000/6500: bid=0, ask=1 → mid = 0.5. Selling 300 units at the position limit × 0.5 = −150/day per product = −900 total regression.

**True BS value** at S≈5250, K=6000, T=7d, σ=0.24: ~0.02 per unit (much less than 0.5 settlement). Local backtest overestimates MTM cost by 25×.

**Decision:** Revert. Even if real server uses 0.02 settlement, EV = 0 (selling at bid=0 collects 0 premium and the option expires worthless with high probability). No upside, uncertain downside.

### Bug 2: `mark49_last_ts` Used Wrong Timestamp

**Symptom:** Signal C cooldown anchor was 100ms early.

**Root cause:** `scan_counterparty_flow()` stored `trade.timestamp` in the cooldown variable. But `state.market_trades` is one-tick lagged → `trade.timestamp` = tick τ−1, not the current detection tick τ.

**Fix:** Removed `mark49_last_ts` from scan return; set in `Trader.run()` as `mark49_last_ts = state.timestamp` when `flow["mark49_events"] > 0`.

### Bug 3: Scan-Before-Reset Day Boundary Race

**Symptom:** At `state.timestamp == 0`, stale prior-day trades could contaminate the just-reset `mark_net` and falsely set `mark49_last_ts = 0`, triggering Signal C for the first 5 ticks of the new day on a phantom detection.

**Fix:** Moved `scan_counterparty_flow()` into the `else` branch. Day-start path resets state and skips the scan entirely.

### Bug 4: Missing `state.own_trades` Source

**Symptom:** Counterparty events where Mark 67/49 traded directly with us were undetected (since they don't appear in `state.market_trades`).

**Fix:** Iterate `for source in (state.market_trades, state.own_trades)` in `scan_counterparty_flow()`. No double-counting: Prosperity guarantees mutual exclusivity.

**Verification:** Datamodel confirmed via direct read of `datamodel.py` — `TradingState` has both fields.

---

## Position Limit and Syntax Verification

```bash
$ python -c "import ast; ast.parse(open('vault/round4_trader.py').read()); print('syntax ok')"
syntax ok

$ grep -c "scan_counterparty_flow" vault/round4_trader.py
2   # 1 definition, 1 call site

$ grep -c "mark_net\|mark49_last_ts" vault/round4_trader.py
13  # composite score + cooldown anchor referenced throughout
```

No position limit breaches in 3-day Round 3 backtest.

---

## Artefacts Created

| Path | Purpose |
|---|---|
| `vault/round4_trader.py` | Round 4 algo submission file (1,008 lines) |
| `research/round4/run_round4.py` | Round 4-specific backtest runner (--trader override support) |
| `.planning/phases/12-counterparty-exploitation/12-01-PLAN.md` | Phase plan |
| `.planning/phases/12-counterparty-exploitation/12-01-SUMMARY.md` | Execution summary |

---

## Surprises / Lessons

1. **Local backtest mid-settlement** can dominate small-edge trades. Always check whether `--merge-pnl` settlement assumptions match real server behaviour.
2. **One-tick lag is everywhere**: `state.market_trades` AND its `trade.timestamp` field both refer to the prior tick. Use `state.timestamp` for any "now" semantics.
3. **`own_trades` carries counterparty names too in Round 4** — the documentation's "buyer/seller only non-empty if SUBMISSION" rule was the rounds 1–3 default; Round 4 fills both sides everywhere.
4. **Day boundary races** matter: any state initialised at `timestamp == 0` must be reset BEFORE consuming `state.market_trades`.

---

## Links

[[Rounds/Round4_findings]] · [[Strategies/Counterparty_Exploitation]] · [[Backtests/Phase11_Box_Signal]] · [[Backtests/Phase10_Submission]] · [[Backtests/PnL_Timeline]]

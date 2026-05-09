---
type: backtest
tags: [phase9, safety, imports, edge-cases, verification]
sources: [backtests/phase9_safety.md]
updated: 2026-04-27
---

# Phase 9: Safety Hardening Gate Results

## Summary

**Date:** 2026-04-27 | **Script:** `research/round3/safety_check.py`

**Phase 8 baseline:** 146,415 (d0=53,780 | d1=48,115 | d2=44,520)

All 4 gates PASS. Trader is ready for Phase 10 submission.

---

## Gate Results

| Gate | Condition | Result |
|------|-----------|--------|
| SAFE-01 | Position limits enforced structurally in all classes | ✅ PASS |
| SAFE-02 | 0 import violations in AST scan of 5,956 nodes | ✅ PASS |
| SAFE-03 | 3 edge case scenarios pass without exception | ✅ PASS |
| NO-REGRESS | 3d total ≥ 146,415 | ✅ PASS |

---

## SAFE-01: Position Limits

Verified via direct class attribute inspection:
- `HydrogelMM.LIMIT = 200` ✅
- `VEVUnderlying.LIMIT = 200` ✅
- `VoucherTrader.LIMIT = 300` ✅

Pattern regex `buy_cap = self.LIMIT - pos` and `sell_cap = self.LIMIT + pos` each matched **3 occurrences** (one per class). All order quantities use `min(qty, cap, ...)` before emission.

---

## SAFE-02: Import Compliance

AST walk of `trader.py` (5,956 nodes) found **0 import violations**.

Allowed set: `{datamodel, jsonpickle, math, typing, collections, os, __future__}`

All imports confirmed clean:
- `datamodel` — IMC competition module
- `typing`, `collections`, `math`, `os` — Python stdlib
- `jsonpickle` — competition-allowed serialization
- `__future__` — stdlib annotations

---

## SAFE-03: Edge Cases

Three synthetic `TradingState` objects tested:

| Scenario | Description | Result |
|----------|-------------|--------|
| A | `order_depths={}` (no products at all) | ✅ No crash |
| B | Empty buy/sell dicts per product | ✅ No crash |
| C | All products: bid=ask (zero spread) | ✅ No crash |

Guards confirmed active:
- `best_bid_ask()` returns None on empty sides
- `top_obi()` returns 0.0 on empty volume
- Each strategy class checks for None before proceeding
- `Trader.run()` wraps `jsonpickle.decode` in try/except

---

## No-Regression PnL

| Day | PnL |
|-----|-----|
| 0 | 53,780 |
| 1 | 48,115 |
| 2 | 44,520 |
| **Total** | **146,415** |

Matches Phase 8 baseline exactly (delta = 0). No safety fixes were needed — all guards were already in place.

---

## Fixes Applied

**None.** All requirements satisfied by existing code. Phase 9 was a pure verification phase.

---

## Links

[[Concepts/Position_Limits]] · [[Backtests/Phase8_OBI_Sweep]] · [[Backtests/PnL_Timeline]]

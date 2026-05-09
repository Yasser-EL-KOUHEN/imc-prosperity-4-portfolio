---
type: counterparty
tags: [round4, mark, local-high-seller, bearish-signal, passive-seller]
sources:
  - .planning/phases/12-counterparty-exploitation/RESEARCH.md
  - vault/round4_trader.py
updated: 2026-05-02
---

# Mark 49 — The Local-High Seller

**Role:** Large directional VEL seller. Net short across all 3 R4 days. **Sells passively** (posts asks, waits to be hit). The bearish counterpart to [[Marks/Mark_67]].

## Behavioral Profile

| Metric | Day 1 | Day 2 | Day 3 |
|---|---|---|---|
| Trades | 40 | 43 | 39 |
| Buy quantity | 38 | 40 | 37 |
| Sell quantity | 342 | 400 | 329 |
| Net | −304 | −360 | −292 |

**3-day net: −956 VEL.** Same net-seller profile every day.

## How Mark 49 Trades

- **Passive seller** (99% of sell trades happen at the existing `ask₁`): posts asks, waits for an aggressive buyer to hit them
- **Avg sell price: +0.67 vs mid** — captures roughly half-spread plus a small premium
- **Sparse, irregular intervals**: median gap **17,800–21,750 ms** (much wider than Mark 67's ~10–15 sec)
- **Concentrated in early/mid-day**, no strict periodicity

## The Local-High Pattern

Mark 49 sells **local highs**. The counterpart to Mark 67's local-low buying.

The combination of these two:
- Mark 67 buys local lows aggressively (ripples bounce up after)
- Mark 49 posts asks at local highs and waits

…defines the **day's volatility regime**. When both are active, VEL is range-bound and the directional flow is **net bullish** (Mark 67 buys ~503/day vs Mark 49 sells ~340/day).

## Signal C — Mark 49 Cooldown

After a Mark 49 detection, the algo **halves VEL passive bid size for 500ms (5 ticks)**. The reasoning: if Mark 49 just sold at the local high, we don't want to pay up for the next available bid (which might be the **start of a reversal toward Mark 67's dip-buy zone**).

```python
if state.timestamp - mark49_last_ts < 500:
    bid_size = bid_size // 2
```

**Critical:** the cooldown anchor is `state.timestamp` (the current tick), **not** `trade.timestamp` (which is the prior tick due to one-tick lag in the Prosperity datamodel). See [[Research/Decisions_Log|D13]] for the bug and fix.

## Composite Flow Score Component

Each Mark 49 sell event contributes **−1** to `mark_net`. When `mark_net ≤ −3`, the algo trims the VEL bid extra by 2 (bearish regime).

Note the **asymmetric thresholds**: +5 to trigger bullish tilt, −3 to trigger bearish trim. This is by design — Mark 67's events are more numerous (50/day vs Mark 49's 36/day), so the bullish trigger is set higher to require stronger evidence.

## Counterparty Topology

- **Mark 67 buys 963 of Mark 49's sells** (63.8% of all Mark 49 outflow)
- **Mark 22 buys 89 units from Mark 49**
- **Mark 55 buys 54 units from Mark 49; sells 26 to Mark 49** (near-symmetric arbitrage)

The Mark 49 → Mark 67 transfer is the dominant flow. They are functionally **the two endpoints of VEL price discovery in R4**.

## ML Analogy

Mark 49 detection is a **non-maximum suppression** (NMS) event in object-detection terminology: after spotting a peak, suppress further detections in a temporal neighborhood (the 500ms cooldown). The composite flow score using both Mark 67 (+) and Mark 49 (−) is a **two-class evidence accumulator** for regime classification.

## Why We Don't Use Mark 49 As Take-Side

A naive interpretation — "Mark 49 just sold, hit Mark 49's ask" — would mean **buying right after a local high**, the opposite of what we want. Mark 49 sells **into** the high, then the price typically reverts toward the mid; chasing Mark 49's ask is buying the top.

The cooldown is the right exploitation: **don't quote into the next available bid** while Mark 49's sell is still working through the order book.

## Links

[[Strategies/Counterparty_Exploitation]] · [[Marks/Mark_67]] · [[Marks/Mark_22]] · [[Rounds/Round4_findings]] · [[Backtests/Phase12_Counterparty]] · [[Research/Decisions_Log]] · [[Products/VELVETFRUIT_EXTRACT]]

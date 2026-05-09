---
type: counterparty
tags: [round4, mark, dip-buyer, bullish-signal, directional-counterparty]
sources:
  - .planning/phases/12-counterparty-exploitation/RESEARCH.md
  - round4/research/run_round4.py
  - vault/round4_trader.py
updated: 2026-05-02
---

# Mark 67 — The Dip Buyer

**Role:** Aggressive long-VEL buyer. Pure-buyer across all 3 R4 days. **Never sells.** The single most exploitable directional signal in R4.

## Behavioral Profile

| Metric | Day 1 | Day 2 | Day 3 |
|---|---|---|---|
| Trades | 58 | 61 | 46 |
| Buy quantity | 519 | 567 | 424 |
| Sell quantity | 0 | 0 | 0 |
| Net | +519 | +567 | +424 |

**3-day net: +1,510 VEL.** Same buy-only profile every day — perfect cross-day consistency.

## How Mark 67 Trades

- **Aggressive taker** (99.4% of buys at `ask₁`): hits existing asks, doesn't post passive bids
- **Avg buy price: +0.80 vs mid** — pays the half-spread + a bit more
- **Wide irregular intervals**: median inter-trade ≈ 10–15 sec
- **Active throughout the day**: first ~10K ms, last ~986K ms

## The Dip-Buyer Pattern

Mark 67 buys **systematically at local lows**:
- 92.7% of buys (153/165 total) happen when price is **below the 5-tick moving average**
- 100ms BEFORE the buy: mid drops avg **−1.78** (97.6% are drops)
- 100ms AFTER the buy: mid rises avg **+1.97** (95.8% are rises)

This is the textbook **mean-reversion dip-buy**: Mark 67 lurks for local dips, fills aggressively, and the price bounces because Mark 67's own demand creates the bounce.

## Cannot Be Used for Momentum Chasing

A naive interpretation — "Mark 67 just bought, follow Mark 67" — **fails empirically**. The price bounce from Mark 67's tick-T buy is already in the mid by tick T+100 (the next tick we can act on). Mean PnL of "buy VEL after seeing Mark 67 in market_trades" = **−5.02 per unit** (165 instances).

The signal is **session-level**, not tick-level. Mark 67's presence indicates a **regime** (someone with deep pockets has decided VEL belongs higher); we ride the regime by tilting our passive bid up, **not** by chasing individual fills.

## Composite Flow Score (`mark_net`)

The Phase 12 R4 algo uses Mark 67 as the **bullish input** to a composite flow accumulator:

```python
mark_net = 0
for trade in (state.market_trades, state.own_trades):    # both collections
    for t in trade.get("VELVETFRUIT_EXTRACT", []):
        if t.buyer == "Mark 67":
            mark_net += 1                                # bullish signal
        if t.seller == "Mark 49":
            mark_net -= 1                                # bearish signal
```

Tilt rule: when `mark_net ≥ 5`, increase VEL passive bid by `+3`. ~50 Mark 67 events vs ~36 Mark 49 events per day → expected end-of-day `mark_net ≈ +14` (bullish bias on net).

## Direct Trades With Us

Critical implementation detail: when Mark 67 takes our passive ask, the trade goes to `state.own_trades`, **not** `state.market_trades`. Pre-fix, the scanner missed every direct fill, undercounting Mark 67 events by potentially 100% on ticks where Mark 67 traded only with us. See [[Research/Decisions_Log|D14]] for the both-collections fix.

## ML Analogy

Mark 67 is a **conditional regime indicator**: P(VEL up | Mark 67 active) > P(VEL up). The composite flow score is a **streaming Bayesian evidence accumulator** (SPRT-style); the signal is the cumulative count, not the per-tick observation.

## Counterparty Topology

- **Buys 963 units from Mark 49** (63.8% of all Mark 49 sells go to Mark 67) — Mark 49 posts asks, Mark 67 hits them
- **Shared timestamps with Mark 49**: 26 / 35 / 28 per day → frequently same-tick counterparties

This topology hint is what allowed the team to build the composite flow score: Mark 49 sells local highs, Mark 67 buys local lows, both at the same time → they define the day's regime.

## Links

[[Strategies/Counterparty_Exploitation]] · [[Marks/Mark_49]] · [[Marks/Mark_22]] · [[Rounds/Round4_findings]] · [[Backtests/Phase12_Counterparty]] · [[Research/Decisions_Log]] · [[Products/VELVETFRUIT_EXTRACT]]

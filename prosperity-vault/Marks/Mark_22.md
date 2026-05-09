---
type: counterparty
tags: [round4, mark, otm-call-seller, vel-taker, structured-short]
sources:
  - .planning/phases/12-counterparty-exploitation/RESEARCH.md
  - vault/round4_trader.py (Change A revert)
updated: 2026-05-02
---

# Mark 22 — Systematic OTM Call Short-Seller + VEL Taker

**Role:** Mostly an options seller (structured short on VEV_5300–6500). Also takes VEL as a seller. **Excluded from the composite flow score** despite being net-short VEL — frequency mismatch with Mark 67/49 would distort the signal.

## Behavioral Profile

**VEL:** Net −551 over 3 days. ~184 trades/day (large compared to Mark 67's ~55 or Mark 49's ~40).

**Options:** Pure seller of VEV_5300, 5400, 5500, 6000, 6500. **Counterparty for Mark 01's option buys.** 100% of Mark 01's option buys come from Mark 22 — counterparty is locked.

| Symbol | Mark 22 sell trades (total over 3 days) | Avg price |
|---|---|---|
| VEV_5300 | 132 | 35.9 |
| VEV_5400 | 263 | 11.1 |
| VEV_5500 | 299 | 3.8 |
| VEV_6000 | 317 | **0.0** |
| VEV_6500 | 317 | **0.0** |

## The "Sell at Bid=0" Pattern

For VEV_6000 and VEV_6500, **the order book has bid₁ = 0, ask₁ = 1**. Mark 22 doesn't post asks — Mark 22 **hits Mark 01's bid of 0**. Mark 22 is *giving the options away for free*.

Why? These are far OTM with strike 6000/6500 vs underlying ~5250. They expire worthless with near certainty. Mark 22's collected premium = $0 either way; settling the position cleanly at $0 saves margin/inventory cost.

## Why We Don't Match This (Phase 12 Change A — REVERTED)

The original Phase 12 RESEARCH proposed: **mirror Mark 22, sell VEV_6000/6500 at bid=0**. Logic: collect 0 premium, options expire worthless, EV = 0. But:

- **Local backtester** marks the trade at `mid = (bid+ask)/2 = 0.5`, then settles at fair value ≈ 0.02 → recorded loss = −0.48 per unit
- Across 317 trades/product/day → **−150/day per product mark-to-market loss**
- On the **live server**, EV is genuinely 0 (collect 0, expire at ~0)
- But the **anti-regression gate** (153,566 baseline) breaks in the local backtest

**Decision:** Revert. Don't sell at bid=0. Accept that our `ask=1` orders never fill (Mark 22 supplies at 0, undercuts us). EV is 0 either way; the local-BT pseudo-loss kills the regression gate.

This is the **canonical "local-BT pricing artifact ≠ live PnL"** lesson — the same theme as v35's local-CV reclassification failure later, but in a different form.

## Why Mark 22 Is Excluded From `mark_net`

| Mark | VEL events/day | Direction |
|---|---|---|
| Mark 67 | ~55 | bullish (+1) |
| Mark 49 | ~36 | bearish (−1) |
| **Mark 22** | **~184** | bearish (would be −1) |

If Mark 22 events were added to `mark_net` at −1 each, they would **dominate** the score (3.4× as frequent as Mark 67 + Mark 49 combined). The signal would degrade into "is Mark 22 active today" rather than "is the day net bullish." So Mark 22 is **tracked separately** for future research but excluded from the regime-detection composite.

## What Mark 22 Tells Us

Mark 22's behavior is consistent with a **structured short-call program**: systematically sell OTM call premium across multiple strikes, deliver at expiry. The buy-side counterparty (Mark 01) is the structured-long-call counterpart — they together form a **paired institutional trade**, not a price discovery duo.

For us: Mark 22's existence means we **don't need to short OTM calls** — Mark 22 already covers that flow with structurally-correct pricing. Our edge is elsewhere (HYDROGEL MM, VEL passive, options near-the-money quoting).

## Cross-Day Consistency

**MEDIUM** — vol regime shifts change whether Mark 22's option prices are above or below BS fair. The structural fact (Mark 22 = seller, Mark 01 = buyer, locked counterparty) is consistent; the prices vary with the day's IV regime.

## Links

[[Strategies/Counterparty_Exploitation]] · [[Marks/Mark_67]] · [[Marks/Mark_49]] · [[Marks/Mark_01]] · [[Backtests/Phase12_Counterparty]] · [[Products/Options/VEV_6000]] · [[Products/Options/VEV_6500]] · [[Research/Decisions_Log]]

---
type: counterparty
tags: [round4, mark, market-maker, hydrogel, mirror-mark14]
sources:
  - .planning/phases/12-counterparty-exploitation/RESEARCH.md
updated: 2026-05-02
---

# Mark 38 — Mirror Market Maker (Mark 14's Bilateral Partner)

**Role:** Mark 14's complementary maker. Pure HYDROGEL + VEV_4000 bilateral counterparty.

## Behavioral Profile

| Product | Trades | Net | Pattern |
|---|---|---|---|
| HYDROGEL | 1,022 | **+34** | 100% with Mark 14 |
| VEV_4000 | 442 | **−46** | Mirrors Mark 14 here too |

## The "Apparent Contradiction" Resolution

When you query "Mark 14 takes / Mark 14 makes" and "Mark 38 takes / Mark 38 makes," both Mark 14 and Mark 38 appear to take from each other. This is resolved by **tick-by-tick role alternation**:

```text
T   :  Mark 14 posts bid₁ → Mark 38 hits it (Mark 38 = taker)
T+1 :  Mark 38 posts bid₁ → Mark 14 hits it (Mark 14 = taker)
T+2 :  Mark 14 posts ask₁ → Mark 38 hits it ...
```

The aggregate bilateral is net-zero by construction — Mark 14 net −44, Mark 38 net +34, sum ≈ −10 over 3 days × 1,000+ trades = **noise around zero**.

## Why Both Marks Exist

In algo-trading terms, this is a **multi-bot bilateral spread-capture loop**: two cooperating algorithms quote both sides of a market, alternate roles, and capture the spread between them indefinitely. The Prosperity simulator likely seeds this pair to provide background liquidity in HYDROGEL and VEV_4000 without committing to a directional view.

For us, Mark 14 + Mark 38 ≡ **the existing top-of-book**. We out-quote both by posting at `best_bid+1 / best_ask-1`.

## No Exploitable Signal

Same as Mark 14: symmetric maker, no directional info. Cross-day consistency: **PERFECT**.

## What Mark 38 Tells Us About VEV_4000

Mark 38 trades VEV_4000 (442 times, net −46) — confirming that **VEV_4000 has a non-trivial maker presence**. This was one of the inputs to the Phase 10 decision to add VEV_4000 as a passive-MM target with size=6 (the +$6,887 PnL win). Mark 38's presence on this strike means the bot maintains a real bid-ask there; our passive MM has fillable counterparties.

## Links

[[Strategies/Counterparty_Exploitation]] · [[Marks/Mark_14]] · [[Strategies/market_making]] · [[Products/HYDROGEL_PACK]] · [[Products/Options/VEV_4000]] · [[Backtests/Phase10_Submission]]

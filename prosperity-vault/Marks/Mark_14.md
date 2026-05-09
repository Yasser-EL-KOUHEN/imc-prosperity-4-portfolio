---
type: counterparty
tags: [round4, mark, market-maker, hydrogel, primary-mm-competition]
sources:
  - .planning/phases/12-counterparty-exploitation/RESEARCH.md
updated: 2026-05-02
---

# Mark 14 — Primary Market Maker (HYDROGEL + VEL + VEV_4000)

**Role:** Algorithmic two-sided market maker. **Our primary competition** in HYDROGEL passive quoting. Tightly bilateral with [[Marks/Mark_38]].

## Behavioral Profile

| Product | Trades | Net | Pattern |
|---|---|---|---|
| HYDROGEL | 1,003 | **−44** | 100% with Mark 38 as counterparty |
| VEL | 647 | **−2** | Bid₁ + ask₁ maker, near-neutral |
| VEV_4000 | (subset of options) | mixed | Maker on this strike |

## How Mark 14 Trades

- **Pure passive maker**: bids at `bid₁`, sells at `ask₁` — never aggressive
- **Avg HYDROGEL bid: −7.98 vs mid · Avg ask: +7.94 vs mid** → captures ~16-tick spread
- **All trade timestamps are multiples of 100ms** → purely algorithmic, no human input
- **Median interval: 900–1,100 ms** (almost periodic)

## The Mark 14 ↔ Mark 38 Bilateral

100% of Mark 14's HYD trades are with Mark 38 as counterparty. They alternate maker/taker roles tick by tick:

```text
tick T:   Mark 14 posts bid → Mark 38 takes
tick T+1: Mark 38 posts bid → Mark 14 takes
```

This **net-zero bilateral** churns spread without moving the underlying price. From our perspective, Mark 14 + Mark 38 together act as a **liquidity surface** at the existing book that we have to price-improve to fill against.

## Implications for Our HYDROGEL MM

When our HYDROGEL passive quote is **inside the spread** (`best_bid+1 / best_ask-1`), we **front-run Mark 14** in price priority and fill first. When we are not competitive (our quote at or below `best_bid`), Mark 14 fills first.

This is the operational reason for the R3 Phase 4 quote-anchor decision: **always post at `best_bid+1 / best_ask-1`**, never at `FV ± offset` (the latter sometimes lands at `best_bid` and gets queued behind Mark 14). See [[Strategies/Mean_Reversion]] · [[Research/Decisions_Log|D6 anchor_w]].

## No Exploitable Alpha Beyond OBI

Unlike Mark 67 / Mark 49, Mark 14 carries **no directional information** — it's a symmetric maker. The only thing we can do with Mark 14 is:
1. **Out-quote it** (price-improve to fill ahead)
2. **Use the bilateral to estimate top-of-book stability** (when both Mark 14 and Mark 38 are present, the spread is wide and stable; when only one is, the spread is tighter)

Neither yields a separate trading signal beyond what OBI/spread analysis already captures.

## Cross-Day Consistency

**PERFECT.** Identical algorithmic pattern all 3 days. This is the kind of counterparty whose behavior we can rely on as background structure (vs. Mark 67 whose **schedule** is variable but whose **role** is consistent).

## Links

[[Strategies/Counterparty_Exploitation]] · [[Marks/Mark_38]] · [[Strategies/market_making]] · [[Strategies/Mean_Reversion]] · [[Products/HYDROGEL_PACK]] · [[Backtests/Phase12_Counterparty]]

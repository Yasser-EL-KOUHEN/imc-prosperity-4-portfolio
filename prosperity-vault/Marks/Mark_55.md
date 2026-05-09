---
type: counterparty
tags: [round4, mark, vel-taker, arbitrageur, symmetric-flow]
sources:
  - .planning/phases/12-counterparty-exploitation/RESEARCH.md
updated: 2026-05-02
---

# Mark 55 — High-Frequency VEL Taker (Likely Arbitrageur)

**Role:** Symmetric two-sided VEL taker. Hits both bids and asks across the day. Net ≈ 0 over 3 days.

## Behavioral Profile

| Day-aggregate | Buy qty | Sell qty | Net |
|---|---|---|---|
| 3-day VEL totals | 3,254 | 3,297 | **−43** |

Total trades: **1,198** over 3 days (≈ 400/day — high frequency).

## How Mark 55 Trades

- **Avg trade size: 5.5 units** (small relative to Mark 67's avg ~9 or Mark 49's larger sells)
- **Median inter-trade interval: 1,750–2,000 ms** (much faster than Mark 67/49)
- **Active all day, every day** — no concentration in a particular window

**Counterparties:** Trades with Mark 01, Mark 14, Mark 22, Mark 49, Mark 67. Takes both Mark 01's and Mark 14's passive quotes — i.e., hits the **existing maker quotes** symmetrically rather than running a directional strategy.

## Why "Likely Arbitrageur"

Net flat (−43 over 6,500+ traded units = 0.7% of volume) + symmetric in direction + high frequency + diverse counterparties = the signature of a **mid-arb or cross-product arb**. Possibilities:

- **VEL vs implied-VEL-from-options** arbitrage (sells VEL when implied VEL from option chain says it's high)
- **Cross-VEV-strike basket arbitrage** (VEL = function of options portfolio at expiry)
- **External-market arbitrage** (Mark 55 is reconciling Prosperity-VEL with another reference price)

We can't see the other leg, so we can't replicate the strategy. But we can **infer market efficiency**: the presence of an active arbitrageur means VEL is reasonably well-priced relative to its information set; large pricing errors won't persist.

## No Exploitable Direct Signal

Mark 55's net ≈ 0 means **no directional information**. The signal value is in **what Mark 55's presence tells us about the market**, not in following Mark 55 directly.

## Frequency Mismatch with Composite Flow

Like Mark 22, Mark 55 is **excluded from `mark_net`** despite being a taker — its frequency (~400 events/day) would dominate Mark 67 (~55) + Mark 49 (~36) and degrade the regime signal.

## Cross-Day Consistency

**HIGH.** Same volume and pattern every day — confirming the algorithmic-arbitrageur classification.

## Links

[[Strategies/Counterparty_Exploitation]] · [[Marks/Mark_67]] · [[Marks/Mark_49]] · [[Marks/Mark_22]] · [[Marks/Mark_01]] · [[Products/VELVETFRUIT_EXTRACT]] · [[Backtests/Phase12_Counterparty]]

---
type: counterparty
tags: [round4, mark, vel-mm, otm-call-buyer, mark-22-counterpart]
sources:
  - .planning/phases/12-counterparty-exploitation/RESEARCH.md
updated: 2026-05-02
---

# Mark 01 — Dual-Role: VEL Market Maker + Long OTM Call Accumulator

**Role:** Two-sided MM in VEL (near-neutral). Systematic OTM call **buyer** across all VEV strikes ≥ 5300 — the buy-side counterpart to [[Marks/Mark_22]].

## Behavioral Profile

**VEL** (1,843 role appearances, 3 days):
- Buys at `bid₁` (passive maker, avg −2.60 vs mid)
- Sells at `ask₁` (passive maker, avg +2.69 vs mid)
- Earns ~5.3 spread per round-trip
- **Net +42 over 3 days = effectively neutral**
- Active all 3 days, same-tick bursts common (median inter-trade ~0)

**Options** — pure long-side accumulator, **buys ONLY from Mark 22**:

| Strike | Trades | Buy qty | Avg price | Days |
|---|---|---|---|---|
| VEV_5200 | 11 | 34 | 65.4 | Day 3 only |
| VEV_5300 | 132 | 439 | 35.9 | All 3 |
| VEV_5400 | 263 | 911 | 11.1 | All 3 |
| VEV_5500 | 299 | 1,042 | 3.8 | All 3 |
| VEV_6000 | 317 | 1,105 | **0.0** | All 3 |
| VEV_6500 | 317 | 1,105 | **0.0** | All 3 |

100% of Mark 01's option fills are sourced from Mark 22. Counterparty is **locked**.

## How Mark 01 Trades Options

Mark 01 **posts the bids**; Mark 22 hits them. For VEV_6000/6500:
- Mark 01 posts `bid = 0`
- Mark 22 hits at price 0 (gives the option away)
- Mark 01 accumulates inventory at zero cost, expects worthless expiry, **collects $0 either way**

Why post bid=0 if the option is going to expire worthless? Because the **portfolio constraint** matters: Mark 01 might be running a **vol-arbitrage strategy** that requires the options as accounting positions, even when their EV is zero.

## Why We Don't Exploit This

Mark 01 is a **market maker for us, not against us**. When we want to:
- Sell VEL at the ask: Mark 01 sometimes buys at ours bid (helps us close)
- Buy VEL at the bid: Mark 01 sometimes sells at our ask
- Sell OTM calls: Mark 01 buys (Phase 12's "Change A" — proposed selling VEV_6000/6500 at bid=0 to mirror Mark 22, **reverted** because of local-BT pricing artifact at mid=0.5)

The "Change A revert" decision means we **don't compete with Mark 22** for selling OTM calls to Mark 01. The local-BT EV is −150/day per product (mark-to-market loss); the live EV is 0. Anti-regression gate fails locally → reverted.

## Cross-Day Consistency

**HIGH.** Same MM-VEL-plus-buy-OTM behavior every day. Mark 01 is the longest-tenured stable counterparty alongside Mark 14/Mark 38.

## What Mark 01 Tells Us About OTM Strikes 5300–6500

Mark 01 + Mark 22 together form **the entire flow** for OTM call strikes in VEV. Without their bilateral, those strikes wouldn't have liquidity. Our R3 strategy **doesn't quote these strikes two-sided** (D3/D4 in the Decisions Log: 5300 two-sided, 5400/5500 two-sided, but 5000–5200 bid-only and 6000/6500 sell-only). The Mark 01 / Mark 22 bilateral explains why this segmentation works: **the maker flow we'd target is already saturated** by their pair.

## Links

[[Strategies/Counterparty_Exploitation]] · [[Marks/Mark_22]] · [[Marks/Mark_14]] · [[Marks/Mark_67]] · [[Strategies/Options_Quoting]] · [[Products/Options/VEV_6000]] · [[Products/Options/VEV_6500]] · [[Backtests/Phase12_Counterparty]] · [[Research/Decisions_Log]]

---
type: product
tags: [round1, round2, trend-following, long-accumulation]
sources: [rounds/round1/trader.py, rounds/round2/trader.py, report/report.tex]
updated: 2026-04-27
---

# INTARIAN_PEPPER_ROOT (IPR)

**Rounds:** 1, 2 | **Position limit:** ±80 | **Type:** Linearly trending commodity

## Market Characteristics

- **Price trend:** +0.1 XIREC per tick = +1,000 XIREC per day (deterministic linear growth)
- **Regime:** Trending (positive momentum; opposite of mean-reversion)
- **Strategy implication:** Accumulate max-long position; NEVER sell

## Theoretical Ceiling

```
80 units × 3,000 XIREC gain/unit/day × 3 days = 240,000 XIREC
```

Achieved: **238,054 XIREC** (99.2% of ceiling).

Gap of ~1,946 XIREC due to spread costs (filling at ask) early in day 0 before reaching the position limit. Spread cost total (3-day): **794 XIREC**.

## Strategy

```python
# Reach +80 position as fast as possible, then hold
1. Aggressively take all available asks each tick (up to buy_cap)
2. Post passive buy at best_bid+1 for any remaining buy_cap
3. NEVER post passive sells — hold the long for the entire 3 days
```

The strategy has no sell logic at all; it is purely a long-accumulation machine.

## Performance

| Metric | Value |
|--------|-------|
| Real exchange Day 0 | 7,286 XIREC |
| 3-day total (v3 backtest) | 238,054 XIREC |
| Theoretical ceiling | 240,000 XIREC |
| Efficiency | 99.2% |

IPR is the **dominant earner** in Round 1 by total PnL — the pure trend signal is far stronger than any MM edge on ACO.

## Intarian Welcome Auction (Round 1 Manual)

Round 1 included a one-time manual trading event: **Dryland Flax** auction.

- **Action taken:** BUY 5,000 units @ 29 XIREC
- **Profit:** 5,000 XIREC (asset settled above purchase price)

This auction result adds directly to Round 1 manual PnL.

## ML Analogy

A classification problem where the signal is always "BUY." The optimal policy is degenerate — always hold maximum long. The only "model" needed is recognizing the trend regime from EDA. In contrast to ACO (mean-reverting = AR(1) ρ < 0), IPR has positive momentum (Hurst > 0.5 would confirm this). The two products sit at opposite ends of the autocorrelation spectrum.

## Lessons Carried Forward

The IPR experience reinforced that **regime identification** must precede strategy selection. HYDROGEL (Round 3) is the mean-reverting counterpart — uses AR(1) with ρ₁=−0.094/−0.237 (magnitude-bucketed). IPR taught: when the regime is clear, maximize exposure without hedging.

## Links

[[Products/ASH_COATED_OSMIUM]] · [[Strategies/market_making]] · [[Rounds/Round1_findings]] · [[Research/Round1_Scripts]]

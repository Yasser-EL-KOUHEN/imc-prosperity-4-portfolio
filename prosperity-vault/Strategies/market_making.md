---
type: strategy
tags: [core, round1, round2, round3, passive]
sources: [rounds/round1/trader.py, rounds/round3/trader.py, context/Trading glossary.txt]
updated: 2026-04-27
---

# Market Making

## Core Idea

A market maker simultaneously posts a **bid** (buy limit order) below and an **ask** (sell limit order) above the fair value of an asset. When both sides fill, the spread is captured as profit.

**ML analogy:** Market making is like a regression model that bids/asks around `ŷ` (the fair value prediction), with the spread acting as a confidence interval around the prediction. The wider the interval, the safer (fewer fills but less risk). The tighter the interval, the more fills but more adverse selection risk.

```
PnL per round-trip = ask_fill_price - bid_fill_price = spread_captured
```

## The Airport Currency Exchange Analogy

A currency exchange at an airport buys USD at 0.95 EUR and sells at 1.05 EUR. They profit 10 cents on each buy-sell pair, regardless of whether EUR/USD moves. IMC's business (and ours in the competition) is the same structure, just faster and more precise.

## Key Parameters

| Parameter | Effect | Too tight | Too wide |
|-----------|--------|-----------|----------|
| Spread | Main profit lever | Adverse selection dominates | No fills |
| Passive edge | Min distance from fair to quote | Miss good quotes | Too conservative |
| Take threshold | Min edge to cross the spread aggressively | Miss free money | Pay spread for nothing |
| Quote size | Volume per side | Underutilizes position | Hits limit fast |

## Passive vs Aggressive Orders

- **Passive (resting):** bid < best_ask, ask > best_bid → waits in queue → earns spread
- **Aggressive (crossing):** bid ≥ best_ask → executes immediately → pays spread

Our default is passive. Aggressive orders are placed only when the edge exceeds a threshold:

```python
# From HydrogelMM
if adjusted_fair - ask_price >= take_threshold:  # take_threshold = 2.5
    take_qty = min(book_size, buy_cap, 30)       # aggressive buy
```

## Inventory Management

Without inventory control, a market maker who fills one side more than the other will accumulate a directional position — increasing risk. Two mechanisms:

1. **Inventory skew:** Shift `adjusted_fair = fair - alpha × pos`. When long, bias fair value down → our ask moves lower (more attractive to sellers) and our bid moves lower (less attractive to buyers) → inventory mean-reverts
2. **Position limits:** Hard cap enforced per tick: `buy_cap = LIMIT - pos`

See [[Concepts/inventory_risk]].

## When It Works vs When It Fails

| Condition | Works? | Why |
|-----------|--------|-----|
| Stable price (RAINFOREST_RESIN) | ✅ Very well | Mean-reversion keeps inventory safe |
| Mean-reverting price (HYDROGEL_PACK) | ✅ Well | Price comes back; inventory self-corrects |
| Trending price | ❌ Dangerous | One side fills continuously; inventory grows against trend |
| High volatility (SQUID_INK) | ❌ Dangerous | Adverse selection; fills are against informed flow |

## Our Implementations

| Product | Version | Key Tweak |
|---------|---------|-----------|
| RAINFOREST_RESIN | Pure symmetric MM | Fixed FV=10,000; no signal needed |
| KELP | Dynamic FV MM | VWAP/mid estimate |
| HYDROGEL_PACK | AR(1) reversion MM | EMA + magnitude-bucketed rho; inventory skew |
| VEV options | Options MM | BS fair value; OBI signal; flow-asymmetry aware |

## Links

[[Concepts/fair_value]] · [[Concepts/inventory_risk]] · [[Concepts/Spread_Dynamics]] · [[Strategies/Mean_Reversion]] · [[Products/HYDROGEL_PACK]]

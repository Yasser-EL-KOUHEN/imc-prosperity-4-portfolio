---
type: concept
tags: [spread, passive, aggressive, market-making, microstructure]
sources: [context/Trading glossary.txt, rounds/round3/trader.py, backtests/phase4_rho_sweep.md]
updated: 2026-04-27
---

# Spread Dynamics

## What the Spread Is

The **bid-ask spread** is the gap between the best bid (highest buy offer) and best ask (lowest sell offer):

```
spread = best_ask - best_bid
```

For a market maker:
- Posting a bid at `best_bid + 1` and ask at `best_ask - 1` captures `spread - 2` per round-trip
- The spread is the raw profit margin per filled pair of orders

## Spread as Profit Margin

```
gross_spread_capture = ask_fill - bid_fill ≥ 0 (when we fill both sides)
net_PnL_per_roundtrip ≈ spread_captured - adverse_selection_cost
```

**Adverse selection:** If the market moves against us *between* our bid fill and ask fill, we're left with inventory in the wrong direction. The spread must be wide enough to compensate for this risk.

## Our Passive Quoting Threshold (HYDROGEL)

The HYDROGEL strategy only places passive quotes when the spread is wide enough:

```python
if spread >= 16:   # only quote passively when spread ≥ 16 ticks
    passive_bid = best_bid + 1
    passive_ask = best_ask - 1
```

Why 16 ticks? The passive edge check (`adjusted_fair - passive_bid >= 1.2`) ensures we only quote when our fair value gives us at least 1.2 ticks of edge from our quote price. With a 16-tick spread, quoting at (best_bid+1, best_ask-1) gives us ~7 ticks from mid — well above our edge requirement.

## Aggressive vs Passive Orders

| Type | When | Cost | Benefit |
|------|------|------|---------|
| Passive | Always (wait for fills) | None (earn spread) | Efficient execution |
| Aggressive | When edge ≥ 2.5 ticks | Pays spread | Immediate execution |

Aggressive orders in HydrogelMM:
```python
if adjusted_fair - ask_price >= take_threshold:   # take_threshold = 2.5
    take(ask_price, qty)   # buy at ask → pay spread
```

Big edge (≥5.0 ticks) allows larger aggressive orders (60 vs 30 units).

## Spread Regimes in Round 3

| Product | Typical Spread | Strategy |
|---------|---------------|---------|
| HYDROGEL_PACK | 16+ ticks | Passive quote when ≥16 ticks |
| VEV options | Variable (0–wide) | Passive quote always; warns on 0-spread days |
| VELVETFRUIT_EXTRACT | Market-determined | Passive join only |

### Why HYDROGEL Spread ≥ 16 Matters

The v6 dominant improvement was `anchor_w` increase to 0.20. This generated more passive quote fires *inside* the 16-wide spread. The 16-tick threshold captures the regime where spreads are wide enough to quote profitably.

## Spread and Fill Rate

- Wider spread → higher gross profit per fill, lower fill rate (fewer counterparties at our price)
- Tighter spread → lower gross profit per fill, higher fill rate

HYDROGEL passive quoting at (best_bid+1, best_ask-1) places us *inside* the market maker quotes, giving us fill priority over anyone quoting at best_bid or best_ask.

## Links

[[Strategies/market_making]] · [[Concepts/fair_value]] · [[Concepts/inventory_risk]] · [[Products/HYDROGEL_PACK]]

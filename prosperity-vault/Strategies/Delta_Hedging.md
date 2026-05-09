---
type: strategy
tags: [round3, options, velvetfruit, passive, hedge]
sources: [rounds/round3/trader.py, backtests/phase5_vev_passive_comparison.md, backtests/phase5_delta_hedge.md]
updated: 2026-04-27
---

# Delta Hedging

## What Delta Is

In options theory, **delta** (Δ) measures how much the option price changes per unit change in the underlying:

```
Δ = ∂C/∂S    (partial derivative of call price wrt spot)
```

For a European call:
```python
d1 = (log(S/K) + 0.5 * σ² * T) / (σ * sqrt(T))
Δ = N(d1)      # standard normal CDF of d1
```

Delta ranges from 0 (far OTM) to 1 (far ITM), reflecting the probability that the call expires in the money.

**ML analogy:** Delta is the gradient of the option price with respect to the input feature (spot price). Hedging away delta is like removing the first-order linear dependence of your portfolio on the underlying — you're left holding only the "residual" (gamma, vega, etc.).

## Why We Hedge Delta

When we sell options, we collect premium but take on directional exposure. If we sold a call with Δ=0.5 and the spot rises, our short call loses money. The hedge: **buy 0.5 shares of the underlying** to offset.

In Prosperity terms: our `VoucherTrader` sells (or buys) VEV call options, accumulating a net delta. We use `VELVETFRUIT_EXTRACT` to neutralize that exposure.

```python
target_vev_pos = -aggregate_options_delta * spot_fair
hedge_needed = target_vev_pos - current_vev_pos
```

## Passive-Only Constraint

**Critical design decision:** We hedge passively — only joining at best_bid or best_ask, never crossing the spread.

**Why:** Spread-crossing for aggressive hedging cost **−90K XIREC on day 2** in v2. The execution cost of crossing the spread outweighed the delta hedge benefit when the options book was small.

```python
if VEV_PASSIVE_ONLY:
    # Only place orders inside the spread
    if hedge_needed > 0:
        bid = Order(UNDERLYING, best_bid, min(hedge_needed, buy_cap))
    elif hedge_needed < 0:
        ask = Order(UNDERLYING, best_ask, -min(-hedge_needed, sell_cap))
    # Never: bid at best_ask or ask at best_bid
```

## Hedge Accuracy vs Cost

| Hedging style | Accuracy | Cost |
|--------------|----------|------|
| Aggressive (cross spread) | High (fills immediately) | High (always pays spread) |
| Passive (join queue) | Lower (fill not guaranteed) | Low (earns or pays nothing extra) |

We accept lower hedge accuracy to eliminate execution cost. The residual delta exposure is small because:
1. Options positions are moderate (LIMIT=300 per strike)
2. Spot moves slowly (passive hedge catches up over multiple ticks)

## Phase 5 Result

Passive-only vs allowing aggressive sections:

| Config | 3d Total | VEV 3d |
|--------|----------|--------|
| Baseline (aggressive allowed) | 142,675 | 7,031 |
| Passive-only | **143,514** | **7,612** |
| Delta | **+839** | **+581** |

Gate: all-days-win → **PASS** (passive ≥ baseline every individual day).

## Greeks Ledger

The trader maintains a `GreeksLedger` that tracks per-strike delta from filled options positions. This accumulates across ticks and drives the `VEVUnderlying` hedge target.

## Links

[[Products/VELVETFRUIT_EXTRACT]] · [[Strategies/Options_Quoting]] · [[Concepts/Black_Scholes]] · [[Concepts/Implied_Volatility]] · [[Backtests/Phase5_VEV_Passive]] · [[Parameters/VELVETFRUIT_Params]]

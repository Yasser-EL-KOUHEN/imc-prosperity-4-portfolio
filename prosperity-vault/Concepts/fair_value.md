---
type: concept
tags: [core, fair-value, pricing]
sources: [context/Trading glossary.txt, rounds/round3/trader.py, research/round3/hydrogel_audit.py]
updated: 2026-04-27
---

# Fair Value

## What It Is

Fair value is our best estimate of what an asset is *actually* worth, as opposed to what it happens to be trading for right now.

**ML analogy:** Fair value is `ŷ` — the predicted label from a regression model. The market price is a noisy observation around `ŷ`. Our job is to estimate `ŷ` well and trade around it: buy when market price is below ŷ, sell when above.

## Estimation Methods

### 1. Fixed Anchor (RAINFOREST_RESIN)

When the true value is known or extremely stable:

```
fair = 10000  (constant)
```

Works when there's an external anchor — like a peg, a mathematical formula, or a competition-provided constant. Best signal-to-noise.

### 2. Mid-Price (Simple)

```
fair = (best_bid + best_ask) / 2
```

Fast and simple. Works when the spread is symmetric and there's no systematic bias. Implicit assumption: market makers are symmetric.

### 3. VWAP (Volume-Weighted Average Price)

```
fair = Σ(price_i × volume_i) / Σ(volume_i)
```

Better for liquid markets with varying depth at different levels. Weights prices by executed volume → more robust to thin levels.

### 4. EMA (Exponential Moving Average) — HYDROGEL

```
ema = alpha * mid + (1 - alpha) * ema    # alpha = 0.35
```

Smoothed mid-price. For mean-reverting products, EMA tracks the "center of gravity" the price oscillates around. We then apply the anchor pull:

```
fair = (1 - anchor_w) * ema + anchor_w * anchor_price  # anchor_w = 0.20
```

### 5. Black-Scholes (Options)

```
fair = BS(spot, strike, T, sigma)
```

Theoretical formula from no-arbitrage option pricing. Requires: spot, strike, time to expiry, implied volatility. See [[Concepts/Black_Scholes]].

## Adjusting Fair Value

After estimating the base fair value, we adjust for:

1. **Reversion signals:** `fair -= rho * (mid - last_mid)` — expect price to revert
2. **OBI signal:** `fair += beta * OBI` — lean with order flow pressure
3. **Inventory skew:** `adjusted_fair = fair - alpha * pos` — not a signal; risk management

## Fair Value Quality vs PnL

The better our fair value estimate, the better our quoting. Key insight: **fair value doesn't need to be exact** — it just needs to be better than the market at the times we fill. A 1% better estimate can generate substantial spread capture.

## In Our Trader

| Product | Method | Quality |
|---------|--------|---------|
| RAINFOREST_RESIN | Fixed 10,000 | ✅ Excellent |
| KELP | Dynamic mid/VWAP | ✅ Good |
| HYDROGEL_PACK | EMA + anchor + reversion | ✅ Good (corr=0.96 with cumPnL) |
| Options | Black-Scholes + live σ | ✅ Good |

## Links

[[Strategies/market_making]] · [[Strategies/Mean_Reversion]] · [[Concepts/Black_Scholes]] · [[Concepts/Order_Book_Imbalance]] · [[Products/HYDROGEL_PACK]] 
---
type: concept
tags: [options, iv-surface, sigma, round3, calibration]
sources: [rounds/round3/trader.py, backtests/phase6_sigma_verify.md, research/round3/iv_surface.py, plots/round3/round3_iv_surface.png]
updated: 2026-04-27
---

# Implied Volatility

## What It Is

**Implied volatility (IV)** is the value of σ that, when plugged into the Black-Scholes formula, gives the current market price of an option:

```
market_price = BS(S, K, T, σ_implied)
Solve for σ_implied → IV
```

IV is "what the market thinks volatility is" — it's not historical vol measured from realized prices, but the forward-looking vol priced into options by market participants.

**ML analogy:** IV is like reverse-engineering a model's learned weight from its output. We know the input (market price) and the model (BS), and we solve for the hidden parameter (σ). This inverse problem is solved numerically (Newton-Raphson).

## The Volatility Smile / Skew

In theory (pure BS), all strikes should have the same IV for the same maturity. In practice they don't — this is the **volatility smile**:

| Strike | IV (Round 3) |
|--------|--------------|
| 5000 (ITM) | 0.242 |
| 5200 (near-ITM) | 0.244 |
| 5300 (slightly ITM) | 0.245 |
| 5400 (ATM) | **0.230 ← lowest** |
| 5500 (OTM) | 0.249 |

The ATM option has the **lowest** implied vol — classic vol smile trough. OTM and ITM options have higher IV, pricing in tail risk that BS underestimates.

## IV Surface (3-Day Historical Means)

Research from `research/round3/iv_surface.py` computed per-strike IV from historical market prices across days 0, 1, 2. Per-strike means match our static calibration within 0.0017 (threshold 0.002) — confirming the sigmas are stable.

## Live Sigma Calibration (Phase 10 Addendum 2)

Old approach: use fixed static STRIKE_SIGMA lookup. Problem: TTE was wrong (~8.7d estimated vs 7.0d from competition statement).

New approach (in production):
1. At start of each day, read market mid-prices for all active strikes
2. Binary-search σ per strike: find σ such that `BS(spot, K, T, σ) = market_mid`
3. Store `_live_sigma` dict in trader_data (persists across ticks)
4. Fall back to static STRIKE_SIGMA if calibration fails

This gives us day-specific implied vols that account for actual market conditions.

**Gain from recalibration:** +265 over 3 days (153,302 → 153,567)

## IV Z-Score Signal

The `IVMonitor` tracks rolling IV history per strike:

```python
window = 500 ticks
warmup = 250 ticks
z_score = (current_IV - rolling_mean) / rolling_std
```

**Usage:** Passive sizing bias only (not aggressive taking):
- High z-score (IV expensive) → lean toward larger ask size
- Low z-score (IV cheap) → lean toward larger bid size

**Why not aggressive:** v2 tried z-take (market-order when IV was extreme) → net-negative after delta hedge slippage was paid.

## IV vs Realized Vol

| Metric | Round 3 |
|--------|---------|
| Realized vol (HYDROGEL, day 1) | stdev=37.61 on ~10,000 mid-price range |
| Implied vol (VEV_5400 ATM) | 0.230 annualized |
| Relationship | IV prices in expected future vol; realized vol is historical |

## Links

[[Concepts/Black_Scholes]] · [[Strategies/Options_Quoting]] · [[Products/Options/VEV_5400]] · [[Parameters/Options_Params]] · [[Backtests/Phase6_BS_Verify]]

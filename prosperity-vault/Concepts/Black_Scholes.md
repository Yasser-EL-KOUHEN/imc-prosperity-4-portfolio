---
type: concept
tags: [options, black-scholes, pricing, greeks, round3]
sources: [rounds/round3/trader.py, backtests/phase6_bs_verify.md, research/round3/bs_verify.py]
updated: 2026-04-27
---

# Black-Scholes Options Pricing

## What It Is

The **Black-Scholes model** prices European options under the assumption of:
- Geometric Brownian Motion for the underlying price
- Constant volatility σ (the "flat vol" assumption — often violated)
- No dividends, continuous trading, no transaction costs

**ML analogy:** BS is a closed-form prediction function — like a regression model with known weights. The inputs are (S, K, T, σ) and the output is the call price. Unlike a learned model, the formula is derived from first principles (no-arbitrage arguments). But σ is learned from market prices (implied volatility calibration).

## The Formula

For a **European call option:**

```
d1 = [ln(S/K) + (0.5 × σ² × T)] / (σ × √T)
d2 = d1 - σ × √T

C = S × N(d1) - K × N(d2)
```

Where:
- `S` = spot price of underlying
- `K` = strike price
- `T` = time to expiry (in years)
- `σ` = implied volatility (annual)
- `N(x)` = cumulative standard normal distribution

## Implementation (No scipy)

```python
def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def black_scholes_call(spot, strike, T, sigma):
    if T <= 0 or sigma < 1e-9:
        return max(spot - strike, 0.0)  # intrinsic value
    sigma_root_t = sigma * math.sqrt(T)
    d1 = (math.log(spot / strike) + 0.5 * sigma**2 * T) / sigma_root_t
    d2 = d1 - sigma_root_t
    return spot * normal_cdf(d1) - strike * normal_cdf(d2)
```

`math.erfc` achieves machine precision for the CDF. Maximum error vs reference: **3.70e-04** (well under 5e-04 threshold).

## The Greeks

### Delta (Δ) — Price sensitivity to spot
```python
def black_scholes_delta(spot, strike, T, sigma):
    d1 = ...
    return normal_cdf(d1)    # ∈ [0, 1] for calls
```

Used for: delta hedging via VELVETFRUIT_EXTRACT

### Vega (ν) — Price sensitivity to volatility
```python
def black_scholes_vega(spot, strike, T, sigma):
    d1 = ...
    return spot * math.sqrt(T) * normal_pdf(d1)
```

Used for: Newton-Raphson IV solver (implied volatility extraction)

### Gamma (Γ) — Rate of delta change
```python
def black_scholes_gamma(spot, strike, T, sigma):
    d1 = ...
    return normal_pdf(d1) / (spot * sigma * math.sqrt(T))
```

Currently wired but not actively used in trading logic.

## Verification Results (Phase 6)

All 5 active strikes verified within tolerance at spot=5400, T=7/365:

| Strike | σ | BS Price | Reference | |Diff| | Pass |
|--------|---|----------|-----------|--------|------|
| 5000 | 0.242 | 400.644 | 400.644 | 2.5e-05 | ✅ |
| 5200 | 0.244 | 211.881 | 211.881 | 5.6e-05 | ✅ |
| 5300 | 0.245 | 133.130 | 133.130 | 8.9e-05 | ✅ |
| 5400 | 0.230 | 68.614 | 68.615 | 3.7e-04 | ✅ |
| 5500 | 0.249 | 35.339 | 35.339 | 9.7e-05 | ✅ |

Edge cases: T=0 → intrinsic, σ≈0 → intrinsic, S=0 → 0. All PASS.

## Implied Volatility (Inverse Problem)

To find σ from market price: Newton-Raphson solver (convergence in <25 iterations):

```python
def implied_vol_newton(price, spot, strike, T, sigma_init=0.24):
    sigma = sigma_init
    for _ in range(25):
        c = black_scholes_call(spot, strike, T, sigma)
        v = black_scholes_vega(spot, strike, T, sigma)
        sigma_new = sigma - (c - price) / v   # Newton step
        if abs(sigma_new - sigma) < 1e-5:
            return sigma_new
        sigma = sigma_new
    return sigma
```

## Edge Cases Handled

| Case | Condition | Return |
|------|-----------|--------|
| At expiry | T ≤ 0 | `max(S - K, 0)` |
| Zero vol | σ < 1e-9 | `max(S - K, 0)` |
| Zero spot | S ≤ 0 | 0.0 |
| Near-zero σ√T | σ√T < 1e-12 | `max(S - K, 0)` |

## Links

[[Concepts/Implied_Volatility]] · [[Strategies/Options_Quoting]] · [[Strategies/Delta_Hedging]] · [[Products/Options/VEV_5400]] · [[Backtests/Phase6_BS_Verify]]

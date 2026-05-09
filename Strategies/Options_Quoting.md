---
type: strategy
tags: [round3, options, black-scholes, iv-surface, two-sided, bid-only]
sources: [rounds/round3/trader.py, backtests/phase6_bs_verify.md, backtests/phase6_sigma_verify.md, backtests/phase7_quoting_verify.md, backtests/phase10_submission.md]
updated: 2026-04-27
---

# Options Quoting Strategy

## Overview

Our options quoting consists of three layers:
1. **Fair value computation:** Black-Scholes call price using per-strike live sigma
2. **OBI adjustment:** Order book imbalance shifts the fair value
3. **Quoting logic:** Two-sided (5300/5400/5500) or bid-only (4000/5000/5100/5200)

## Layer 1: Black-Scholes Fair Value

No scipy available — pure math implementation:

```python
def black_scholes_call(spot, strike, T, sigma):
    if T <= 0 or sigma < 1e-9:
        return max(spot - strike, 0.0)   # intrinsic value at expiry
    sigma_root_t = sigma * sqrt(T)
    d1 = (log(spot/strike) + 0.5 * sigma**2 * T) / sigma_root_t
    d2 = d1 - sigma_root_t
    return spot * N(d1) - strike * N(d2)   # N = normal_cdf via math.erf
```

**Edge cases handled:** T=0 (intrinsic), sigma≈0 (intrinsic), spot=0 (zero). All verified in Phase 6.

## Layer 2: Per-Strike Sigma (IV Surface)

Each strike has its own implied volatility (the "smile"):

| Strike | σ (calibrated) | σ (IV mean) | |Diff| | Status |
|--------|---------------|------------|--------|--------|
| 5000 | 0.242 | 0.2420 | 0.0000 | PASS |
| 5200 | 0.244 | 0.2423 | 0.0017 | PASS |
| 5300 | 0.245 | 0.2450 | 0.0000 | PASS |
| 5400 | 0.230 | 0.2296 | 0.0004 | PASS |
| 5500 | 0.249 | 0.2491 | 0.0001 | PASS |

**Phase 10 improvement (Addendum 2):** Live sigma calibration — at the start of each day, binary-search per-strike sigma from market prices so BS(spot, K, T, σ) = market_mid. TTE also corrected from binary-search estimate (~8.7d) to competition-specified values [7.0, 6.0, 5.0].

## Layer 3: TTE (Time to Expiry)

| Day | TTE (days) | TTE (years) |
|-----|-----------|-------------|
| 0 | 7.0 | 7/365 |
| 1 | 6.0 | 6/365 |
| 2 | 5.0 | 5/365 |

TTE decreases intraday: `T = max(initial_tte - timestamp/1_000_000, 1e-6) / 365`

## Layer 4: Quoting by Flow Asymmetry

Research finding from `research/round3/microstructure_eda.py`:

| Strike | Flow Pattern | Quoting Mode |
|--------|-------------|-------------|
| VEV_4000 | Deep ITM; passive MM | bid+ask passive |
| VEV_5000 | 94–98% bid-hit | bid-only |
| VEV_5100 | Mostly bid-hit | bid-only |
| VEV_5200 | Mostly bid-hit | bid-only |
| VEV_5300 | Symmetric | two-sided |
| VEV_5400 | Symmetric | two-sided |
| VEV_5500 | Symmetric | two-sided |
| VEV_6000 | OTM; sell_only infrastructure | ask-only (0 fills) |
| VEV_6500 | OTM; sell_only infrastructure | ask-only (0 fills) |

**Bid-only implementation:** `bid_only=True` in ACTIVE_CONFIG. Multiple guards in code prevent any ask orders from being generated (delta bypass, should_quote_ask, allow_sell).

## IV Z-Score as Passive Sizing Bias

The `IVMonitor` tracks rolling implied vol per strike:

```python
window = 500 ticks, warmup = 250 ticks
iv_zscore = (current_iv - rolling_mean) / rolling_std
```

High IV z-score → options are "expensive" relative to recent history. This biases **passive quote size** (not aggressive takes):
- High z-score → larger ask size (sell more when IV is elevated)
- Low z-score → larger bid size (buy more when IV is depressed)

**Why not aggressive:** v2 aggressive z-takes were net-negative once delta-hedge slippage was paid.

## Phase 10 Additions: VEV_4000 and Recalibration

Phase 10 Addendum 1 added VEV_4000 (deep ITM call) with passive MM (size=6, edges 9/5):
- Net contribution: **+6,887** over 3 days (d0:3000, d1:2150, d2:-956)
- Deep ITM options have high intrinsic value; spread capture from passive MM is reliable

Phase 10 Addendum 2 (TTE/σ recalibration): **+265** from correcting TTE from 8.7→7.0 on day 0.

## Gate Results (Phase 7)

| Gate | Condition | Result |
|------|-----------|--------|
| OPT-04 | 5300/5400/5500 non-zero 3-day PnL | PASS |
| OPT-05 | 5000/5200 bid_only static check | PASS |
| OPTIONS-POSITIVE | aggregate PnL > 0 on ≥2 days | PASS |
| NO-REGRESS | 3d total ≥ 143,514 | PASS |

## Links

[[Concepts/Black_Scholes]] · [[Concepts/Implied_Volatility]] · [[Strategies/Delta_Hedging]] · [[Strategies/OBI_Signal]] · [[Products/Options/VEV_5300]] · [[Products/Options/VEV_5000]] · [[Backtests/Phase6_BS_Verify]] · [[Backtests/Phase7_Options_Quoting]] · [[Parameters/Options_Params]]

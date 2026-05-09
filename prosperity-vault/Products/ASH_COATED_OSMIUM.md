---
type: product
tags: [round1, round2, market-making, mean-reversion, stable]
sources: [rounds/round1/trader.py, rounds/round2/trader.py, report/report.tex]
updated: 2026-04-27
---

# ASH_COATED_OSMIUM (ACO)

**Rounds:** 1, 2 | **Position limit:** ±80 | **Type:** Stable commodity with AR(1) mean-reversion

## Market Characteristics

- **Fair value:** ≈ 10,000 (very stable; EDA: mean=10,000, std≈5/day)
- **AR(1) coefficient:** ρ₁ = −0.495 (strong mean-reversion on mid-price changes)
- **Bot spread:** 16 ticks (bot posts near 9992/10008)
- **Regime:** Mean-reverting; Hurst < 0.5

## Strategy (v3 — FV anchor blend)

### Fair Value Formula

```
FV_base = 0.85 × EMA(mid, α=0.50) + 0.15 × 10,000
FV      = FV_base − ρ(|Δmid|) × Δmid
```

**Magnitude-bucketed reversion coefficients:**

| |Δmid| range | ρ    | Interpretation |
|-------------|------|----------------|
| < 2 ticks   | 0.25 | Small noise; weak pull back |
| 2–5 ticks   | 0.60 | Medium move; moderate pull back |
| ≥ 5 ticks   | 0.74 | Large move; strong pull back |

### Quote Placement

- **Passive:** `best_bid + 1` / `best_ask − 1` — 1 tick inside bot's spread (price priority over bot)
- **Aggressive:** Take any ask < FV or bid > FV (free edge from bot mispricing)

## Version History

### v1 (bug — never use)
Passive quotes computed as `FV ± QUOTE_OFFSET`. These quotes are typically outside the bot's spread → never fill. The Jasper backtest inflated PnL by ignoring time priority, giving a misleadingly high ~263K score.

### v2 (fix)
Anchored passive quotes to the order book: `best_bid+1 / best_ask-1`. Guarantees price priority over the bot. Backtest (3-day): 289,094 XIREC.

### v3 (improvement — deployed)
Added FV anchor blend: 85% fast-EMA + 15% known prior (10,000). Justified by EDA — FV is stationary with a very strong prior.

ACO improvement: 51,040 → 53,116 (+4.1%, +2,076 XIREC over 3 days); robust across ALL days (passes anti-overfit gate).

## Performance

| Version | ACO 3-Day | Total 3-Day | vs v2 |
|---------|-----------|-------------|-------|
| v2 | 51,040 | 289,094 | — |
| v3 | 53,116 | 291,170 | +2,076 |

**Real exchange (Day 0):** 2,668 XIREC

## Rejected Alternatives (all fail per-day gate)

- **Inventory skew** (`k × pos` shift on FV) — loses passive-fill edge
- **Inventory gate** (rho downscale when loaded) — AR(1) is still predictive under load
- **Slow-EMA anchor** — injects noise; FV is stationary, so slow EMA adds noise not signal

## ML Analogy

Bayesian shrinkage toward a known constant. Instead of trusting the noisy EMA fully, we shrink 15% toward the known FV prior (10,000). Equivalent to a ridge penalty pulling the estimate toward the prior mean. The 0.85/0.15 blend was chosen by sweep, not by hand.

## Links

[[Products/INTARIAN_PEPPER_ROOT]] · [[Strategies/market_making]] · [[Strategies/Mean_Reversion]] · [[Concepts/fair_value]] · [[Rounds/Round1_findings]]

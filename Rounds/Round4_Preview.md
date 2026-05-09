---
type: round
tags: [round4, upcoming, counterparty, aether-crystal, exotic-options]
sources: [context/Round 4/# Round 4 - The More The Merrier.txt, context/Round 4/Manual Challenge.txt, data/round4/]
updated: 2026-04-27
---

# Round 4 — "The More The Merrier" (Pre-work Preview)

> **SUPERSEDED.** This page is the pre-Phase-12 scoping doc dated 2026-04-27. For the active Round 4 state, see [[Rounds/Round4_findings]].

## Status

**Pre-work scoping** — captured the round announcement before any analysis was done

---

## Round Context

**Key change:** Counterparty information is now available. The `Trade.buyer` and `Trade.seller` fields (previously `None`) now contain participant IDs. Each counterparty's trading behavior can be studied and exploited.

**Products:** Same as Round 3 — `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, 10 `VELVETFRUIT_EXTRACT_VOUCHER` — but TTE is now 4 days (one round closer to expiry).

**TTE at Round 4 start:** VEV_5000 example: TTE = 4 days.

**Position limits:** Same as Round 3.

| Product | Limit |
|---------|-------|
| HYDROGEL_PACK | 200 |
| VELVETFRUIT_EXTRACT | 200 |
| Each VEV_XXXX | 300 |

---

## Algorithmic Challenge — "Hello, I'm Mark"

### Counterparty Information

The `Trade` class now exposes `buyer` and `seller` names:

```python
class Trade:
    def __init__(self, symbol, price, quantity, buyer=None, seller=None, timestamp=0):
        self.buyer = buyer    # Now populated with participant ID
        self.seller = seller  # Now populated with participant ID
```

**Strategy implication:** Identify which counterparties are liquidity-takers vs providers, which are directional vs mean-reverting, and exploit predictable behavior patterns.

**Research workflow for counterparty data:**
1. Parse `trades_round_4_day_*.csv` — extract buyer/seller names per trade
2. Cluster counterparties by: trade frequency, typical trade size, directional bias
3. Identify "mark" counterparties (uninformed flow) vs "informed" counterparties to fade
4. Condition quoting: tighten spreads when interacting with known uninformed flow; widen when interacting with potentially informed participants

---

## Manual Challenge — "Vanilla Just Isn't Exotic Enough"

**Underlying:** `AETHER_CRYSTAL` — simulated via GBM with:
- Zero risk-neutral drift
- Annualized volatility σ = **251%**
- 4 steps per trading day, 252 trading days per year
- **No continuous monitoring** — knock-out checks only at discrete steps

**Contract size:** 3,000 (PnL multiplier on individual option prices)

**PnL settlement:** Mark-to-fair-value at expiry across 100 simulations. Hold positions to expiry (no intra-round trading across days).

### Time conventions

```python
TRADING_DAYS_PER_YEAR = 252
STEPS_PER_DAY = 4
def weeks_to_years(weeks): return (weeks * 5) / 252  # 5 business days/week
```

- "2 weeks" = 10 trading days = 40 steps
- "3 weeks" = 15 trading days = 60 steps

### Available Contracts

| Contract | Type | Expiry | Strike | Notes |
|----------|------|--------|--------|-------|
| AETHER_CRYSTAL | Spot | — | — | Underlying; bid 49.975, ask 50.025 |
| AC_50_P | Vanilla Put | T+21 | 50 | Standard put; bid 12, ask 12.05 |
| AC_50_C | Vanilla Call | T+21 | 50 | Standard call; bid 12, ask 12.05 |
| AC_35_P | Vanilla Put | T+21 | 35 | OTM put; bid 4.33, ask 4.35 |
| AC_40_P | Vanilla Put | T+21 | 40 | OTM put; bid 6.5, ask 6.55 |
| AC_45_P | Vanilla Put | T+21 | 45 | OTM put; bid 9.05, ask 9.1 |
| AC_60_C | Vanilla Call | T+21 | 60 | OTM call; bid 8.8, ask 8.85 |
| AC_50_P_2 | Vanilla Put | T+14 | 50 | 2-week put; bid 9.7, ask 9.75 |
| AC_50_C_2 | Vanilla Call | T+14 | 50 | 2-week call; bid 9.7, ask 9.75 |
| AC_50_CO | Chooser | T+21, choose at T+14 | 50 | Converts to ITM side after 2 weeks |
| AC_40_BP | Binary Put | T+21 | 40 | Pays 10 if spot < 40 at expiry |
| AC_45_KO | Knock-Out Put | T+21 | 45, barrier 35 | Worthless if spot ever < 35 |

### Pricing Framework (GBM with σ = 251%)

With such extreme volatility, deep OTM options carry substantial probability of finishing ITM. Key insight: at σ=251%, put-call parity and near-ATM options are heavily influenced by vol.

**Chooser option:** After T+14, buyer picks the side (put or call) that's in-the-money. Value ≥ max(call, put) for same strike/expiry → always worth at least as much as either vanilla alone.

**Binary put:** Pays fixed 10 if S_T < 40. Value = 10 × N(−d₂) in BS framework. Not path-dependent (discrete grid check only at expiry).

**Knock-Out put:** Standard put until barrier breach. Since σ=251% and barrier=35 is 30% below spot=50, the probability of touching 35 in 60 discrete steps is non-trivial. Options analysis required.

### Strategy Approach

1. Calculate BS prices for vanilla options at σ=251%, S=50, r=0
2. Compare to market mid-prices — buy underpriced, sell overpriced
3. Chooser: price as max(put, call) + time-value-of-choice
4. Binary put: price as N(−d₂) × 10
5. Knock-out put: price as put price × (1 − P(barrier breach))
6. Delta-hedge the underlying via AETHER_CRYSTAL spot if net delta exposure is large

---

## Available Data

| File | Contents |
|------|---------|
| `data/round4/prices_round_4_day_1.csv` | Tick-level prices (day 1) |
| `data/round4/prices_round_4_day_2.csv` | Tick-level prices (day 2) |
| `data/round4/prices_round_4_day_3.csv` | Tick-level prices (day 3) |
| `data/round4/trades_round_4_day_1.csv` | Executed trades with buyer/seller IDs (day 1) |
| `data/round4/trades_round_4_day_2.csv` | Executed trades with buyer/seller IDs (day 2) |
| `data/round4/trades_round_4_day_3.csv` | Executed trades with buyer/seller IDs (day 3) |

---

## Research Workflow for Round 4

1. **Counterparty clustering:** Parse trades CSVs, group by buyer/seller, measure directional bias and trade timing patterns
2. **HYDROGEL/VEV dynamics:** Same products — check if parameters drift vs Round 3 with extra TTE day consumed
3. **Aether Crystal analysis:** Parse prices for AETHER_CRYSTAL if present; compute realized vol to verify σ=251% assumption
4. **Options valuation:** Implement chooser, binary put, and knock-out put pricing in pure Python

---

## Links

[[Competition/Round_Schedule]] · [[Rounds/Round3_findings]] · [[Research/Round3_Scripts]] · [[Strategies/market_making]] · [[Strategies/Mean_Reversion]] · [[Concepts/Black_Scholes]] · [[Concepts/Implied_Volatility]]

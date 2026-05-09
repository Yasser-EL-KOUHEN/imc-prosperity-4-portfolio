---
type: concept
tags: [round5, market-making, adverse-selection, informed-traders, position-sizing]
sources:
  - round5/strategies/round5_v34_trader.py
  - round5/strategies/round5_v40_trader.py
  - round5/strategies/round5_v42_trader.py
  - round5/logs/
updated: 2026-04-30
---

# Adverse Selection

## What It Is

When you post a passive quote (bid or ask), other traders choose whether to hit it. **Informed** traders — those with a better estimate of the next mid-price — preferentially hit your quote when it's mispriced **against you**. Result: you systematically buy as price falls and sell as price rises, accumulating losing inventory.

This is **selection bias on order flow.** You don't see all possible counterparties uniformly; you see counterparties who chose to trade with you because your quote was favorable to them.

**ML analogy:** Adverse selection is the **label noise asymmetry** of MM — your "Y" (next price) and your "X" (decision to fill at this quote) are not independent. The fills you observe are a biased sample (positive selection on the counterparty side). It's the trading equivalent of training on review data where reviews are written by users who self-select into either love-it or hate-it categories.

## Symptoms

A product suffering adverse selection in MM has this signature:
- Quote both bid and ask, get filled on both sides
- Mid-price moves **against the side you just filled** more often than chance
- Cumulative MM PnL bleeds linearly in the number of trades
- Spread captured per trade < expected, even before inventory cost

In R5 logs, this looked like products with **avg PnL ≤ −$500 across N=12 versions, 0/N positive**. The bleeding scales with trading volume, not against it.

## Why It Hits R5 Harder Than R3

R3 HYDROGEL had:
- Wide spread (≥16 ticks)
- Strong mean-reversion (ρ_AR1 = −0.13 at lag 1)
- Slow counterparty mix (Mark 14 / Mark 38 bilateral)

So MM at LIMIT=200 captured most of the spread, with reversion paying off the residual inventory. Low adverse selection.

R5 50-product universe had:
- Tight spreads (typically 1–4 ticks)
- AR(1) ≈ 0.999 → effectively a random walk with drift (no reversion to harvest)
- Unknown / informed counterparty mix (no Mark IDs to taxonomize)

So **MM-spread capture is the only edge** when drift is small — and that edge is weakest in tight-spread markets where adverse selection is strongest. Some R5 products had **negative expected MM PnL even at LIMIT=10**.

## Identifying Adverse-Selection-Prone Products

The R5 v34→v42 process identified them by **direct PnL evidence** across versions:

```text
1. Run K versions on real Prosperity (K=12 by v36)
2. Aggregate per-product PnL across runs
3. Products with avg ≤ -$500 AND 0/K positive = candidates
4. Confirm: smaller-LIMIT version (TIER3 = LIMIT 5) bleeds at half the rate of LIMIT 10
   → adverse-selection (volume-scaling) loss, not random
5. Action: blacklist (LIMIT 0) for the worst, TIER3 (LIMIT 5) for borderline
```

This is purely empirical — no theoretical model of who the informed counterparty is. The data tells you which products bleed and you respect the data.

## Position-Sizing Response (Volume = Loss Multiplier)

The key insight: **adverse-selection losses scale linearly with traded volume.** If you double your LIMIT, you trade ~2× more, and you lose ~2× more.

Concrete in v40 backtest evidence: 9 ex-TIER3 products promoted from LIMIT=5 to LIMIT=10 lost an additional **$6,536** in the backtester (first 10% of day 4). Per-product, the loss roughly doubled.

| LIMIT | Trading volume | Spread captured | Adverse-selection cost | Net |
|---|---|---|---|---|
| 0 (blacklist) | 0 | 0 | 0 | **0** ← ideal for hopeless products |
| 5 (TIER3) | half | half | half | **−$X** |
| 10 (default) | full | full | full | **−$2X** |

The right answer for an adverse-selection-prone product is to **stop trading it** (blacklist) or trade it minimally (TIER3) — never more aggressively. v40's mistake was conflating "more trades" with "more upside" without accounting for the sign of expected per-trade PnL.

## Mitigations (and Why They Failed for R5)

| Mitigation | Why it didn't help R5 |
|---|---|
| Wider spread quotes (skip MIN_SPREAD < 2 ticks) | Already on; tight-spread products often have spread = 1, so we just don't quote them |
| Larger inventory skew | Helps unwind toxic inventory but doesn't prevent the next adverse fill |
| Inventory limits (LIMIT=10) | Capacity bound, not an edge |
| Two-level quoting (inner + outer) | Outer quotes capture sweeps but also get adverse-selected |
| OBI tilt (β > 0) | Phase 14 found 8/200 OBI signals OOS-significant; small effect, hard to combine with directional bets |

The structural fix (blacklist) outperforms every active-management trick for the worst-case products. Sometimes the right strategy is **not to play**.

## When NOT to Use Blacklist

A product with:
- Mixed positivity (e.g. 4/12 positive runs, avg = −$200)
- Genuine drift on full day (the conflict products from drift_audit.csv)
- Recoverable behavior (e.g. zero-fill products which earn $0 = neither lose nor win)

Blacklist would forfeit the upside without saving meaningful losses. R5 used these criteria:

```text
BLACKLIST:  consistent loss, near-zero positivity, no full-day recovery
TIER3:      small loss (−$30 to −$200), kept for upside potential
DEFAULT MM: avg ≥ $0 OR mixed positivity with drift recovery
```

## Links

[[Rounds/Round5_findings]] · [[Strategies/TIER3_Market_Making]] · [[Strategies/Cross_Version_Blacklist]] · [[Strategies/market_making]] · [[Concepts/inventory_risk]] · [[Concepts/Backtester_vs_Competition]] · [[Strategies/Counterparty_Exploitation]] (R4 — opposite case where counterparties were known)

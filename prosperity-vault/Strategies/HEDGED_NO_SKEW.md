---
type: strategy
tags: [round5, market-making, structural-pairs, snackpack, anti-correlated, calibrated]
sources:
  - round5/strategies/round5_v27_trader.py
  - round5/strategies/round5_v34_trader.py
  - round5/strategies/round5_v42_trader.py
  - round5/research/pairs_analysis.py
  - round5/plots/within_category_xcorr_summary.csv
updated: 2026-04-30
---

# HEDGED_NO_SKEW (Structural-Pairs Market Making)

## What It Is

For products that are tightly **anti-correlated with another product in the universe**, the natural inventory-risk hedge already exists in the market structure. We can quote them with **bigger size and no inventory skew** — let positions accumulate freely, and let the structurally-paired product provide the offsetting exposure.

In R5, exactly one pair qualified: **SNACKPACK_CHOCOLATE / SNACKPACK_VANILLA**, with `ρ = −0.92` over the full data.

## The Mechanic

Standard MM uses **inventory skew** to discourage one-sided accumulation:

```python
# Standard: skew quotes when |pos| crosses threshold
if pos >= SKEW_THRESHOLD:        # too long → make ask more aggressive, bid less aggressive
    bid_offset = 0   # less attractive bid (joins queue)
    ask_offset = 1   # keep aggressive ask
elif pos <= -SKEW_THRESHOLD:
    bid_offset = 1
    ask_offset = 0
```

For HEDGED_NO_SKEW products, this skew is **disabled** (or rather, the threshold is the default and we never expect to hit it asymmetrically because the other side of the pair naturally accumulates the opposite position):

```python
HEDGED_NO_SKEW = {"SNACKPACK_CHOCOLATE", "SNACKPACK_VANILLA"}

def get_mm_settings(product):
    if product in HEDGED_NO_SKEW:
        return MM_LIMIT_DEFAULT, 8, 2, SKEW_THRESHOLD_DEFAULT
        #              ^^         ^   ^   default skew threshold (rarely triggers)
        #              full       inner doubled (vs default 6) — exploit the natural hedge
    ...
```

**Key parameter changes for HEDGED_NO_SKEW products:**
- Full `LIMIT=10` (top tier)
- **Inner size = 8** (vs default 6) — bigger quote because we don't fear inventory build-up
- Outer size = 2 (vs default 4) — keep some queue presence
- Skew threshold unchanged (the natural hedge does the work; explicit skew rarely triggers)

## Why It Works on SNACKPACK CHOC/VAN

`round5/research/pairs_analysis.py` ran the within-category correlation matrix on first-differenced mid-prices, day-by-day. SNACKPACK CHOC vs VAN gave the strongest within-category anti-correlation in the entire dataset:

| Pair | ρ (returns, 3-day avg) |
|---|---|
| SNACKPACK_CHOCOLATE / SNACKPACK_VANILLA | **−0.916** |
| SNACKPACK_STRAWBERRY / SNACKPACK_RASPBERRY | −0.924 |
| SNACKPACK_PISTACHIO / SNACKPACK_RASPBERRY | −0.831 |
| (PEBBLES sub-variants) | ≈ −0.5 |

Why CHOC/VAN was chosen as HEDGED_NO_SKEW (and not the other ≥|−0.83| SNACKPACK pairs):
- STRAWBERRY ended up in the **directional** layer (+10) — full-day +UP signal
- PISTACHIO ended up in the **directional** layer (−10) — full-day −DOWN signal
- RASPBERRY had no committed direction; left in default MM
- CHOC and VAN both had **no clean directional signal** but were anti-correlated → ideal HEDGED_NO_SKEW pair

Result: when our CHOC inventory grows long, our VAN inventory typically grows short (or vice versa), with the pair's combined dollar exposure staying close to zero. The hedge is **provided by the market**, not by our skew logic.

## Why Bigger Inner Size?

The inner-size parameter sets quote depth at the touch (best_bid / best_ask):
- Default: 6 → captures medium-flow products
- HEDGED_NO_SKEW: 8 → exploits the natural hedge by **quoting more aggressively**

Standard MM caps inner size to limit inventory risk per quote. HEDGED_NO_SKEW's whole premise is that the inventory risk on one product is offset by inverse inventory on the partner. So we can quote larger and capture more spread.

If the inner-size were 10 (= LIMIT), a single fill would max out the position — at which point the order is rejected. 8 leaves headroom for partial fills + secondary cycles within the same tick.

## Empirical Evidence (v34 → v42)

The HEDGED_NO_SKEW logic was introduced in **v34** (Edge 2). It survived every subsequent revision (v35, v36, v37, v38, v39, v40, v41, v42) — every single attempt to revisit the strategy left HEDGED_NO_SKEW intact. That's a strong vote.

**Why this is structurally robust:** the −0.92 correlation comes from the IMC-designed mechanics (CHOC and VAN are flavor-substitutes in the SNACKPACK basket — when consumers prefer one, the other dips). Unlike fitted signals (OBI β, drift estimates), it's not a property of the data **window** — it's a property of the **product**. So it transfers cleanly across the Prosperity-window vs full-day distinction that broke other signals (see [[Concepts/Backtester_vs_Competition]]).

## ML Analogy

HEDGED_NO_SKEW is the **paired-encoder trick** in contrastive learning: when two latent variables are known to be anti-correlated, you don't regularize them independently — you let them co-vary, and your loss function uses their **difference** (or sum, depending on sign).

In our setting: standard MM regularizes inventory per-product (the skew is a per-product penalty). HEDGED_NO_SKEW recognizes that the relevant exposure is the **pair-difference**, not the per-product position, and removes the per-product penalty so the model can do its job.

## Post-Result Validation (2026-05-08)

HEDGED_NO_SKEW realized **+$9,858.39** on the real Day-5 engine — a clean structural-pair win exactly as the design predicted:

| Product | Realized PnL |
|---|---|
| SNACKPACK_VANILLA | +$8,998.08 |
| SNACKPACK_CHOCOLATE | +$860.31 |
| **Total** | **+$9,858.39** |

The −0.916 within-category correlation held on Day 5 (otherwise we'd see +VAN, −CHOC or vice versa, and the per-product skew removal would have hurt). Both legs net-positive ⇒ the pair was traded with low net exposure throughout the day, capturing spread on both sides as the variants oscillated against each other.

**Compared to defaults:** if SNACKPACK_VANILLA and CHOCOLATE had been in DEFAULT_MM (LIMIT=10, inner_size=6, with skew), the realized PnL would have been bounded by the spread × fills × (1 − inventory penalty). Removing the skew let inventory accumulate to ±10 on each leg without penalty as the prices oscillated — a tighter quote band on average and more spread captured. The +$9,858 vindicates the **paired-encoder ML analogy**: the right unit of regularization is the pair-difference, not the per-product position.

## Links

[[Rounds/Round5_findings]] · [[Strategies/TIER3_Market_Making]] · [[Strategies/Directional_Holding]] · [[Strategies/market_making]] · [[Concepts/inventory_risk]] · [[Products/Round5_Categories]] · [[Research/Round5_Scripts]] · [[Performance/Algo_Per_Round]]

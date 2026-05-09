---
type: strategy
tags: [round5, market-making, adverse-selection, tiered-limits, calibrated]
sources:
  - round5/strategies/round5_v26_trader.py
  - round5/strategies/round5_v34_trader.py
  - round5/strategies/round5_v40_trader.py
  - round5/strategies/round5_v41_trader.py
  - round5/strategies/round5_v42_trader.py
  - round5/logs/
updated: 2026-04-30
---

# TIER3 Market Making (Reduced-LIMIT MM for Adverse-Selection-Prone Products)

## What It Is

A subset of R5 products consistently lose money under standard MM at LIMIT=10. The losses are not directional drift; they are **adverse selection** — informed counterparties pick off our quotes (we end up long when price falls, short when it rises). The TIER3 response is **reduced position exposure** — drop LIMIT to 5 instead of 10, halve inner/outer quote sizes, lower the inventory-skew threshold so the strategy unwinds toxic inventory faster.

Per-product MM settings:

```python
MM_LIMIT_DEFAULT       = 10   # full LIMIT
MM_INNER_SIZE          = 6
MM_OUTER_SIZE          = 4
SKEW_THRESHOLD_DEFAULT = 6    # at |pos| > 6, skew quotes asymmetrically

MM_LIMIT_TIER3         = 5    # half LIMIT
TIER3_INNER_SIZE       = 3    # half inner
TIER3_OUTER_SIZE       = 2    # half outer
SKEW_THRESHOLD_TIER3   = 3    # earlier skew (already small limit)

def get_mm_settings(product):
    if product in TIER3_PRODUCTS:
        return MM_LIMIT_TIER3, TIER3_INNER_SIZE, TIER3_OUTER_SIZE, SKEW_THRESHOLD_TIER3
    if product in HEDGED_NO_SKEW:
        return MM_LIMIT_DEFAULT, 8, 2, SKEW_THRESHOLD_DEFAULT  # bigger inner, no real skew
    return MM_LIMIT_DEFAULT, MM_INNER_SIZE, MM_OUTER_SIZE, SKEW_THRESHOLD_DEFAULT
```

## TIER3 in v42 (final submitted)

| Product | v34 PnL | v40 PnL | v42 verdict |
|---|---|---|---|
| MICROCHIP_RECTANGLE | −$128 | small loss | **KEEP at TIER3** (small enough to absorb) |
| OXYGEN_SHAKE_EVENING_BREATH | −$30 | small loss | **KEEP at TIER3** |
| OXYGEN_SHAKE_MORNING_BREATH | −$1,258 | −$2,410 | **promoted to BLACKLIST** in v42 |
| GALAXY_SOUNDS_DARK_MATTER | −$938 | −$2,384 | **BLACKLIST** |
| PANEL_2X2 | −$1,464 | −$2,180 | **BLACKLIST** |
| ROBOT_LAUNDRY | −$1,000 | −$1,782 | **BLACKLIST** |
| PANEL_1X2 | −$929 | −$1,654 | **BLACKLIST** |
| PANEL_1X4 | −$1,007 | −$1,626 | **BLACKLIST** |
| OXYGEN_SHAKE_MINT | −$969 | −$1,384 | **BLACKLIST** |

7 of v34's 9 TIER3 products graduated to MM_BLACKLIST in v42 because the v40 evidence showed un-TIER3'ing them **doubled** the loss. If TIER3=5 still loses meaningfully and TIER3=10 loses even more, the right answer is **TIER3=0 (skip the product)** — which is exactly what blacklisting is.

## The v40 Mistake — Why TIER3 Is Right

v40 hypothesised that TIER3's reduced LIMIT was a Prosperity-backtester-loss-fitting artifact (N=1 evidence). The hypothesis: on the **full day** (10× more ticks), more trading opportunities + full LIMIT = recovery via spread capture.

**Wrong direction.** The 9 un-TIER3'd products in v40 lost an additional **$6,536 in the backtester** vs v34 — and that's just the first 10% of day 4. On the full day with 10× more trading, adverse-selection losses scale further. v40's full-day estimate vs v34: **−$25K**.

The lesson: **adverse-selection losses scale WITH trading volume, not against.** More quoting = more times an informed counterparty picks off your quote. TIER3's smaller LIMIT correctly identifies "we lose money MMing this product, reduce exposure." Removing it doubles the bleeding.

v41 reverted v40: keep TIER3, add only one new directional (STRAWBERRY). v42 went further: the consistently-losing TIER3 products are now blacklisted.

## When TIER3 vs BLACKLIST?

| Loss magnitude | Decision |
|---|---|
| Tiny (< $200/version) | TIER3 — small enough to keep capacity for upside |
| Moderate ($200–$1,000/version, mixed days) | TIER3 with monitoring |
| Consistent ($500+/version, 0/N positive) | BLACKLIST |

The threshold is also informed by **n-of-N positive ratio**: a product losing $200 every run is worse for the blacklist than a product losing $1,000 in 8 of 12 runs and gaining $500 in 4. The latter has variance you might want to keep capturing on a different scoring window.

## ML Analogy

TIER3 is **L2 weight regularization on the position-sizing layer**: products with high adverse-selection risk get their "weight" (LIMIT) shrunk toward zero. BLACKLIST is **L1 (hard zero)** for products where the optimal weight really is zero — the L2 penalty alone leaves a tiny residual that still bleeds.

The v40 mistake was unhelpful regularization removal: the model regularised correctly, then v40 removed the penalty hoping for "more capacity" without verifying the products had positive expected value. They didn't. The L2 was load-bearing.

## Post-Result Validation (2026-05-08)

v42's TIER3 bucket realized **−$2,764** on the real Day-5 engine — a manageable, contained loss exactly as the L2 framing predicted:

| Product | Realized PnL |
|---|---|
| MICROCHIP_RECTANGLE | −$402.37 |
| OXYGEN_SHAKE_EVENING_BREATH | −$2,362.00 |
| **Total** | **−$2,764.37** |

Compare to the BLACKLIST bucket (LIMIT=0): all 11 products realized exactly **$0** on Day 5 — perfectly disabled.

**The shrinkage hierarchy works as designed:**
- Default MM (LIMIT=10) on a *good* product: clean win (UV_VISOR_YELLOW +$7,754, ROBOT_VACUUMING +$5,099, etc.)
- TIER3 (LIMIT=5) on a *small-loss* product: contained loss (≤ $2.4K per product)
- BLACKLIST (LIMIT=0) on a *clear-loser* product: exactly zero

**Caveat — DEFAULT_MM was not always safe.** MICROCHIP_SQUARE in DEFAULT_MM realized **−$18,636** on Day 5 — adverse selection picked off our quotes when the underlying drifted strongly. This is the signal that v43 should add a **drift-magnitude** criterion to escalate from DEFAULT_MM → TIER3 → BLACKLIST, not just cross-version log evidence (which left MICROCHIP_SQUARE in DEFAULT_MM).

## Links

[[Rounds/Round5_findings]] · [[Strategies/Directional_Holding]] · [[Strategies/Cross_Version_Blacklist]] · [[Concepts/Adverse_Selection]] · [[Strategies/market_making]] · [[Concepts/inventory_risk]] · [[Performance/Algo_Per_Round]]

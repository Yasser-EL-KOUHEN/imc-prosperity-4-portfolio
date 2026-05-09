---
type: product
tags: [round5, translator, tightest-category, zero-fill]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/plots/full_day_optimal.csv
updated: 2026-05-02
---

# TRANSLATOR (Instant Translators 🗣️)

**Category:** Instant Translators · **Position limit:** ±10 per product · **Spread regime:** tightest in R5 (avg span 9,637–10,188; only ~5%)

The **tightest mid-price range** of any R5 category. No directional bets, one BLACKLIST (zero-fill), and the rest at default MM. **Low alpha potential by design.**

## Per-Product Disposition (v42)

| Product | Day-2 mid avg | v42 strategy | Reason |
|---|---|---|---|
| **TRANSLATOR_SPACE_GRAY** | 9,707 | **BLACKLIST** (zero-fill) | earns $0 in every version since v1 |
| TRANSLATOR_ASTRO_BLACK | 9,938 | default MM (TIER1 v26 era) | +$2,316 in v9 |
| TRANSLATOR_ECLIPSE_CHARCOAL | 9,637 | default MM (TIER1 v26) | +$2,884 in v9 |
| TRANSLATOR_GRAPHITE_MIST | 9,788 | default MM (TIER1 v26) | +$3,676 in v9 (top earner in cat) |
| TRANSLATOR_VOID_BLUE | 10,188 | default MM | mixed; earnings stable |

## TRANSLATOR_SPACE_GRAY — The Zero-Fill

The longest-tenured BLACKLIST entry. Has been blacklisted since **v14** and never produced a single non-zero PnL on any measured Prosperity run. Reasons (inferred):
- Lowest-spread / tightest-quote product in the category
- Bot quotes are aggressive enough that our default MM can't get inside the spread
- When we do post inside, the quote is immediately picked off by an informed counterparty

Either way: **$0 in every measured version → keep blacklisted**. Like ROBOT_DISHES and GALAXY_SOUNDS_PLANETARY_RINGS, this is a **costless blacklist**.

## The Tightness Problem

TRANSLATOR has the smallest mid-price range of any R5 category:

```text
Cat-avg range (5 products):  9,637 – 10,188     range = 551 ticks
PEBBLES range (for comparison): 9,189 – 11,550   range = 2,361 ticks  (4.3× wider)
```

Tight ranges → tight spreads → small per-fill spread capture → low alpha for MM. The category contributes modest earnings (a few thousand per top-earner), nothing dramatic.

## Phase 14 — No TRANSLATOR Signals Survived

None of Phase 14's six analyses (autocorrelation, OBI, Donchian, trajectory, XGBoost) flagged any TRANSLATOR product as a day-4-OOS-significant signal. Consistent with the "low-alpha competitive MM" classification from initial EDA.

## Within-Category Structure

The TRANSLATOR variants are all **dark color names** (GRAPHITE, ECLIPSE, VOID, ASTRO, SPACE) — possibly suggesting a brightness/luminosity ordering that maps to mid-price. But the data doesn't support a strong basket trade (within-category correlations are mostly noise).

## v34 Per-Product Prosperity Contribution (verified)

```text
TRANSLATOR_GRAPHITE_MIST    +$3,676   (TIER1 boost helps capture more spread)
TRANSLATOR_ECLIPSE_CHARCOAL +$2,884
TRANSLATOR_ASTRO_BLACK      +$2,316
TRANSLATOR_VOID_BLUE        +$2,084 (estimate; not in TIER1)
TRANSLATOR_SPACE_GRAY        $0     (BLACKLIST)
```

Sum across 4 active TRANSLATORs ≈ **+$11K** — meaningful but well below PEBBLES (+$80K estimated full-day) or the per-product top earners.

## Links

[[Products/Round5_Categories]] · [[Strategies/market_making]] · [[Strategies/Cross_Version_Blacklist]] · [[Concepts/Adverse_Selection]] · [[Parameters/Round5_Params]]

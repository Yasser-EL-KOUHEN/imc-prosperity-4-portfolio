---
type: product
tags: [round5, capture, 50-products, 10-categories, placeholders]
sources: [context/Round 5/# Round 5 - The Final Stretch.txt, data/round5/prices_round_5_day_*.csv]
updated: 2026-04-29
---

# Round 5 — 50 Products in 10 Categories

> Capture-only page. Per-product analysis deferred — see [[Rounds/Round5_Preview]] for status.

**All products:** position limit ±10. Mid prices oscillate around ~10,000 (universal across categories).

## Category 1: Galaxy Sounds Recorders 🎙️

| Product | Day-2 mid range | Day-2 mid avg |
|---|---|---|
| GALAXY_SOUNDS_DARK_MATTER | 9,614 – 10,695 | 10,112 |
| GALAXY_SOUNDS_BLACK_HOLES | 9,608 – 11,792 | 10,680 |
| GALAXY_SOUNDS_PLANETARY_RINGS | 9,253 – 11,279 | 10,013 |
| GALAXY_SOUNDS_SOLAR_WINDS | 9,320 – 10,992 | 10,067 |
| **GALAXY_SOUNDS_SOLAR_FLAMES** | 9,838 – **11,970** | **11,096** |

SOLAR_FLAMES has the widest range and highest avg → most volatile in this category. Worth investigating for trend.

## Category 2: Vertical Sleeping Pods 🛏️

| Product | Day-2 mid range | Day-2 mid avg |
|---|---|---|
| SLEEP_POD_SUEDE | 9,596 – 11,368 | 10,255 |
| SLEEP_POD_LAMB_WOOL | 9,880 – 12,036 | 10,769 |
| SLEEP_POD_POLYESTER | 9,686 – 11,870 | 10,697 |
| SLEEP_POD_NYLON | 8,829 – 10,096 | 9,511 |
| SLEEP_POD_COTTON | 9,838 – 11,738 | 10,738 |

NYLON is the only one with avg < 10,000 — possible structural undervaluation or mean-reversion target.

## Category 3: Organic Microchips 💾

| Product | Day-2 mid range | Day-2 mid avg |
|---|---|---|
| MICROCHIP_CIRCLE | 8,572 – 10,082 | 9,190 |
| MICROCHIP_OVAL | 9,015 – 10,433 | 9,766 |
| **MICROCHIP_SQUARE** | 9,756 – **12,508** | **11,268** |
| MICROCHIP_RECTANGLE | 8,948 – 10,442 | 9,597 |
| MICROCHIP_TRIANGLE | 9,478 – 10,826 | 10,216 |

**SQUARE is a clear outlier** (22% above category mean). Possible deliberate "winner" product per the announcement's hint about embedded patterns.

## Category 4: Purification Pebbles 💎

| Product | Day-2 mid range | Day-2 mid avg |
|---|---|---|
| PEBBLES_XS | 7,849 – 10,496 | 9,189 |
| PEBBLES_S | 8,815 – 10,687 | 9,650 |
| PEBBLES_M | 8,918 – 10,390 | 9,747 |
| PEBBLES_L | 8,632 – 10,822 | 9,863 |
| **PEBBLES_XL** | 9,188 – **14,155** | **11,550** |

Monotonic increase by size: XS < S < M < L < XL. **XL is a 4,000-point outlier** — strongest within-category trend in the entire dataset. Likely a designed pattern.

## Category 5: Domestic Robots 🤖

| Product | Day-2 mid range | Day-2 mid avg |
|---|---|---|
| ROBOT_VACUUMING | 9,136 – 10,303 | 9,747 |
| ROBOT_MOPPING | 9,802 – 11,340 | 10,539 |
| ROBOT_DISHES | 8,855 – 10,178 | 9,473 |
| ROBOT_LAUNDRY | 9,742 – 10,859 | 10,274 |
| ROBOT_IRONING | 8,630 – 10,102 | 9,354 |

Mixed; no obvious within-category trend.

## Category 6: UV-Visors 🕶️

| Product | Day-2 mid range | Day-2 mid avg |
|---|---|---|
| UV_VISOR_YELLOW | 9,734 – 11,830 | 10,790 |
| UV_VISOR_AMBER | 8,440 – 10,036 | 9,177 |
| UV_VISOR_ORANGE | 9,374 – 10,336 | 9,877 |
| UV_VISOR_RED | 9,916 – 11,370 | 10,778 |
| UV_VISOR_MAGENTA | 9,726 – 11,340 | 10,399 |

AMBER lowest, YELLOW/RED highest. Possible color-spectrum ordering effect to investigate.

## Category 7: Instant Translators 🗣️

| Product | Day-2 mid range | Day-2 mid avg |
|---|---|---|
| TRANSLATOR_SPACE_GRAY | 9,134 – 10,278 | 9,707 |
| TRANSLATOR_ASTRO_BLACK | 9,484 – 10,520 | 9,938 |
| TRANSLATOR_ECLIPSE_CHARCOAL | 8,931 – 10,597 | 9,637 |
| TRANSLATOR_GRAPHITE_MIST | 9,168 – 10,388 | 9,788 |
| TRANSLATOR_VOID_BLUE | 9,467 – 11,346 | 10,188 |

**Tightest category** — averages span only 9,637–10,188. Suggests low alpha potential; likely competitive MM only.

## Category 8: Construction Panels 🪟

| Product | Day-2 mid range | Day-2 mid avg |
|---|---|---|
| PANEL_1X2 | 8,412 – 10,203 | 9,232 |
| PANEL_2X2 | 9,201 – 10,326 | 9,807 |
| PANEL_1X4 | 9,196 – 11,226 | 10,022 |
| **PANEL_2X4** | 9,982 – 11,806 | **10,714** |
| PANEL_4X4 | 9,528 – 10,548 | 10,040 |

Roughly increasing with panel area (1×2 < 2×2 < 1×4 < 2×4 ≈ 4×4) — basic supply/demand by raw material? PANEL_2X4 stands out as highest avg.

## Category 9: Liquid Breath Oxygen Shakes 🥤

| Product | Day-2 mid range | Day-2 mid avg |
|---|---|---|
| OXYGEN_SHAKE_MORNING_BREATH | 9,930 – 11,228 | 10,584 |
| OXYGEN_SHAKE_EVENING_BREATH | 8,278 – 10,300 | 9,185 |
| OXYGEN_SHAKE_MINT | 9,465 – 10,451 | 9,894 |
| OXYGEN_SHAKE_CHOCOLATE | 8,760 – 10,104 | 9,356 |
| **OXYGEN_SHAKE_GARLIC** | 9,616 – 11,874 | **11,058** |

GARLIC the outlier — counterintuitive (taste suggests low demand). Possible designed contrarian pattern.

## Category 10: Protein Snack Packs 🍫

| Product | Day-2 mid range | Day-2 mid avg |
|---|---|---|
| SNACKPACK_CHOCOLATE | 9,560 – 10,280 | 9,961 |
| SNACKPACK_VANILLA | 9,676 – 10,516 | 10,064 |
| SNACKPACK_PISTACHIO | 9,417 – 10,106 | 9,656 |
| SNACKPACK_STRAWBERRY | 9,554 – 10,776 | 10,295 |
| SNACKPACK_RASPBERRY | 9,707 – 10,647 | 10,065 |

**Tightest range overall** (avg span 9,656–10,295). Likely market-making category with very tight spreads.

## Initial Observations

1. **Outliers per category (potential designed "winners")**:
   - SOLAR_FLAMES, MICROCHIP_SQUARE, PEBBLES_XL, OXYGEN_SHAKE_GARLIC, PANEL_2X4
   - PEBBLES shows a monotonic XS→XL pattern — strongest deliberate-design signal
2. **Tight categories (low-alpha MM only)**: TRANSLATORS, SNACK_PACKS
3. **Sub-9,500 averages (potential undervaluation or asymmetric distribution)**: NYLON sleep pod, AMBER visor, EVENING_BREATH/CHOCOLATE oxygen, all microchips except SQUARE/TRIANGLE, several pebble sizes, several panels
4. **Position limit 10** drastically reduces dollar exposure per trade — strategy quality must be high; size optimization is secondary

## Deferred Analysis

Per-product investigation needed:
- Realized vol and AR(1) coefficients
- Spread distribution (is mid - bid₁ uniform across products, or wider on outliers?)
- OBI signal strength
- Cross-product correlations (within-category trading?)
- Time-of-day patterns

## Links

[[Rounds/Round5_Preview]] · [[Strategies/Ashflow_Alpha_News_Trading]] · [[Strategies/market_making]] · [[Strategies/Mean_Reversion]]

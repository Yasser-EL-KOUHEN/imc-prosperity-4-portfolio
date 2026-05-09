---
type: round
tags: [round5, upcoming, capture, 50-products, 10-categories, ashflow-alpha, ignith]
sources: [context/Round 5/# Round 5 - The Final Stretch.txt, context/Round 5/Manual Trading Challenge.txt, context/Round 5/Manual Trading Annex (Ashflow Alpha).txt, data/round5/]
updated: 2026-04-29
---

# Round 5 — "The Final Stretch"

## Status

**Captured (no analysis yet)** — context and data ingested 2026-04-29. Round 4 submission still in progress.

## What's New vs Round 4

| Dimension | Round 4 | Round 5 |
|---|---|---|
| Tradable products | HYDROGEL + VEL + 10 VEV vouchers (12) | **50 NEW products** in 10 categories (5 each) |
| Old products | Active | **No longer tradable** |
| Position limit | HYDROGEL 200 / VEL 200 / VEV 300 | **All 10** (very tight) |
| Counterparty info | Buyer/seller named (Marks 01/14/22/38/49/55/67) | **Removed** — buyer/seller fields empty in `trades_round_5_*.csv` |
| Manual challenge | AETHER_CRYSTAL exotic options | **Ignith exchange** (one-day) with news-driven goods |
| Days in data | 1, 2, 3 (1-indexed) | **2, 3, 4** — implies Round 5 = day 5 (3 historical + 1 competition) |

The position limit collapse from hundreds → **10** is a fundamental structural change. Per-tick alpha needs to be much higher to make sweeps meaningful. Strategy must lean on **price-prediction quality**, not size.

---

## Algorithmic Challenge — "Cherry Picking Winners"

50 products, 10 categories of 5 each. Each category has its own story; some have embedded patterns "waiting to be discovered". Position limit ±10 across all.

### The 10 Categories

| # | Category | 5 Products |
|---|---|---|
| 1 | **Galaxy Sounds Recorders** | DARK_MATTER, BLACK_HOLES, PLANETARY_RINGS, SOLAR_WINDS, SOLAR_FLAMES |
| 2 | **Vertical Sleeping Pods** | SUEDE, LAMB_WOOL, POLYESTER, NYLON, COTTON |
| 3 | **Organic Microchips** | CIRCLE, OVAL, SQUARE, RECTANGLE, TRIANGLE |
| 4 | **Purification Pebbles** | XS, S, M, L, XL |
| 5 | **Domestic Robots** | VACUUMING, MOPPING, DISHES, LAUNDRY, IRONING |
| 6 | **UV-Visors** | YELLOW, AMBER, ORANGE, RED, MAGENTA |
| 7 | **Instant Translators** | SPACE_GRAY, ASTRO_BLACK, ECLIPSE_CHARCOAL, GRAPHITE_MIST, VOID_BLUE |
| 8 | **Construction Panels** | 1X2, 2X2, 1X4, 2X4, 4X4 |
| 9 | **Liquid Breath Oxygen Shakes** | MORNING_BREATH, EVENING_BREATH, MINT, CHOCOLATE, GARLIC |
| 10 | **Protein Snack Packs** | CHOCOLATE, VANILLA, PISTACHIO, STRAWBERRY, RASPBERRY |

### Initial Price-Range Snapshot (Day 2 mid-prices)

| Category | Mid-price range (avg across 5) | Typical ±range/avg |
|---|---|---|
| Galaxy Sounds | 10,013 – 11,096 | ~5–10% |
| Sleep Pods | 9,511 – 10,769 | ~5–10% |
| Microchips | 9,190 – 11,268 | ~5–15% |
| Pebbles | 9,189 – 11,550 | ~5–25% (XL widest) |
| Robots | 9,354 – 10,539 | ~5–10% |
| UV-Visors | 9,177 – 10,790 | ~5–15% |
| Translators | 9,637 – 10,188 | ~5% (tightest) |
| Panels | 9,232 – 10,714 | ~5–10% |
| Oxygen Shakes | 9,185 – 11,058 | ~5–15% |
| Snack Packs | 9,656 – 10,295 | ~3–7% (very tight) |

All products oscillate around ~10,000 like ASH_COATED_OSMIUM in Round 1, but with variable trend/range character per product. **Within-category dispersion** is interesting (e.g., MICROCHIP_CIRCLE avg 9,190 vs MICROCHIP_SQUARE avg 11,268 — a 22% spread within a 5-product category).

### Hypothesis Buckets (For Future Analysis)

The phrase "some offer more market inefficiencies than others" + "strong patterns are embedded in the price movements" suggests a tiered structure:
- **Pattern-rich products**: clear mean-reversion or trend, suitable for aggressive strategies (analogue to ACO, IPR, HYDROGEL)
- **Noisy products**: competitive market making, modest passive edge (analogue to standard MM)
- **Within-category relationships**: pairs trading or basket arbitrage if a category index is meaningful

To investigate: realized vol per product, AR(1) coefficients, OBI quality, cross-product correlations within and across categories.

---

## Manual Challenge — "Extra! Extra! Read all about it!" ✓ SUBMITTED

One-shot trade on the **Ignith exchange** for one day only. Budget **1,000,000 XIRECs**.
**Final submission: 85% allocated, 6 of 9 goods, 140,100 fees, model net PnL = 140,100.**

### Fee and Optimisation

$$\text{fee}_i = \left(\frac{p_i}{100}\right)^2 \cdot B = 100\,p_i^2 \quad\text{(XIRECs)}$$
$$\text{Net PnL}_i = 100\,p_i(s_i - p_i) \quad\Longrightarrow\quad p_i^* = \frac{s_i}{2}$$

where $s_i$ = effective signed one-day move in %. At the optimum, net PnL equals the fee paid (by algebraic construction). **This is NOT a Gaussian/sentiment-score problem** — it is a discrete headline-shock problem solved via archetype classification.

### Article Archetypes and Effective Moves

| Good | Archetype | $s_i$ % | Direction | $p_i^*$ % |
|---|---|---|---|---|
| Lava cake | Mechanical recall | 50 | SELL | **25** |
| Thermalite core | Demand adoption report | 32 | BUY | **16** |
| Ashes of the Phoenix | Viral scandal | 28 | SELL | **14** |
| Pyroflex cells | Policy shock | 24 | SELL | **12** |
| Magma ink | Fresh scarcity demand | 24 | BUY | **12** |
| Sulfur reactor | Index inclusion | 12 | BUY | **6** |
| Volcanic incense | Late-stage stale hype | 0 | — | 0 |
| Obsidian cutlery | Single production accident | 0 | — | 0 |
| Scoria paste | Low-quality forecast | 0 | — | 0 |

**Volcanic incense vs Magma ink:** Both are demand articles. Magma ink = fresh crowd demand (new product, scarcity, queues). Volcanic incense = Nostralico calling followers to "follow my lead and buy" — a distribution signal, not a new demand signal. Late-stage hype → $s = 0$.

Full analysis: [[Strategies/Ashflow_Alpha_News_Trading]]

---

## Available Data

| File | Rows | Contents |
|---|---|---|
| `data/round5/prices_round_5_day_2.csv` | 500K | All 50 products, 10K ticks/day each, 3-level book + mid + PnL |
| `data/round5/prices_round_5_day_3.csv` | 500K | Same |
| `data/round5/prices_round_5_day_4.csv` | 500K | Same |
| `data/round5/trades_round_5_day_2.csv` | 11K | Executed trades; **buyer/seller fields empty** |
| `data/round5/trades_round_5_day_3.csv` | 12K | Same |
| `data/round5/trades_round_5_day_4.csv` | 12K | Same |

Schema (prices): `day;timestamp;product;bid_price_{1,2,3};bid_volume_{1,2,3};ask_price_{1,2,3};ask_volume_{1,2,3};mid_price;profit_and_loss`

Schema (trades): `timestamp;buyer;seller;symbol;currency;price;quantity` — buyer and seller are empty strings in all 35K+ trades observed.

---

## Next Steps (algorithmic side — deferred per user)

- [x] Manual challenge: SUBMITTED 2026-04-29 (85% / 140,100 fees / 6 goods)
- [ ] Per-product EDA: realized vol, AR(1), spread distribution, OBI quality
- [ ] Cross-product correlations within and across categories
- [ ] Identify "pattern-rich" vs "competitive MM" products (ACO/IPR/HYDROGEL classification)
- [ ] Cherry-pick 10–20 products for trading; ignore the rest (alpha-per-product effort tradeoff at limit=10)
- [ ] Algorithmic implementation, backtesting, iteration

---

## Links

[[Rounds/Round4_findings]] · [[Strategies/Counterparty_Exploitation]] (no longer applies in R5) · [[Concepts/fair_value]] · [[Concepts/Order_Book_Imbalance]] · [[Strategies/market_making]]

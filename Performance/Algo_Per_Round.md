---
type: backtest
tags: [performance, official, real-engine, per-product, post-competition, all-rounds]
sources:
  - performance/algorithmic trading/round 1/272592.json
  - performance/algorithmic trading/round 2/362752.json
  - performance/algorithmic trading/round 3/486282.json
  - performance/algorithmic trading/round 4/544306.json
  - performance/algorithmic trading/round 5/581865.json
updated: 2026-05-08
---

# Algorithmic Trading — Official Per-Product Real-Engine PnL

> Parsed from Prosperity-issued submission JSONs in `performance/algorithmic trading/`. Per-product `profit_and_loss` at the last timestamp of `activitiesLog`. These are the **canonical real-engine numbers** for what the competition actually paid us.

## Per-round totals (verified)

| Round | Submission ID | JSON total | User-reported algo | Difference | Notes |
|---|---|---|---|---|---|
| R1 | 272592 | **98,172.12** | 98,172 | 0 | exact match |
| R2 | 362752 | **94,529.00** | 91,529 | **−3,000** | **MAF bid was ACCEPTED** — fee deducted from reported total |
| R3 | 486282 | **40,799.58** | 40,800 | 0 (rounding) | exact match |
| R4 | 544306 | **57,047.69** | 57,048 | 0 (rounding) | exact match |
| R5 | 581865 | **57,911.39** | 57,911 | 0 (rounding) | exact match |

### MAF correction (REVERSED from earlier inference)

The R2 algo JSON shows raw PnL **94,529** before the MAF fee. The user-reported R2 algo of **91,529** = JSON total − **3,000**. The 3,000 is exactly the submitted MAF bid. **The bid was accepted; we paid the fee in exchange for the +25% quote-flow bonus.** The earlier inference that "the bid was rejected because R2 algo dropped 7K below R1 algo" is **wrong** — the actual gap was only −3,643 (94,529 − 98,172) before the fee, which is normal day-to-day variance, and the fee accounted for the rest.

**Implication for MAF lesson:** The +25% volume bonus did *not* lift the algo by the expected $5–7K — IPR was ceiling-bound near +0.1/tick capacity (R1 IPR $79,255 vs R2 IPR $79,199, essentially identical), and ACO didn't gain proportionally to quote count (R1 ACO $18,917 vs R2 ACO $15,330). The bid was paid but the volume bump was largely absorbed by structural caps. Net effect of MAF participation: roughly −$3K to −$6K vs not bidding. The bid wasn't *too low* (we won the auction); the *value* of winning was lower than the BS-implied $5–7K because the strategy was bandwidth-saturated.

---

## Round 1 — ACO + IPR (2 products)

| Product | Real-engine PnL |
|---|---|
| INTARIAN_PEPPER_ROOT | **+79,255.00** |
| ASH_COATED_OSMIUM | +18,917.12 |
| **Total** | **98,172.12** |

IPR dominated as expected — greedy long accumulation against the +0.1/tick trend. ACO contribution lower than the local-3-day estimate (~53K) but consistent with single-day → 18.9 ≈ 53K/3 × 1.07, well within fill-variance.

---

## Round 2 — ACO + IPR + MAF bid (2 products + fee)

| Product | Real-engine PnL |
|---|---|
| INTARIAN_PEPPER_ROOT | +79,199.00 |
| ASH_COATED_OSMIUM | +15,330.00 |
| **Subtotal** | 94,529.00 |
| MAF fee | −3,000.00 |
| **Net (user-reported)** | **91,529.00** |

R2 IPR (+79,199) ≈ R1 IPR (+79,255) — IPR was bandwidth-saturated; MAF +25% quotes didn't lift it. ACO −3,587 vs R1 — within normal variance.

---

## Round 3 — HYDROGEL + VEL + 10 VEV (12 products, exact)

| Product | Real-engine PnL |
|---|---|
| HYDROGEL_PACK | **+55,100.50** |
| VEV_4000 | 0.00 (no trades) |
| VEV_4500 | 0.00 (no trades) |
| VEV_5400 | 0.00 (no trades) |
| VEV_6000 | 0.00 (no trades) |
| VEV_6500 | 0.00 (no trades) |
| VEV_5500 | −51.88 |
| VEV_5300 | −241.84 |
| VEV_5000 | −449.17 |
| VEV_5100 | −1,598.18 |
| VELVETFRUIT_EXTRACT | **−5,834.75** |
| VEV_5200 | **−6,125.11** |
| **Total** | **+40,799.58** |

HYDROGEL real-engine: +55,100 (one day). Local-3-day baseline was 153,566 / 3 = 51,189/day → real-engine 55,100 = **108% of local per-day**. HYDROGEL actually *over*-performed local on day-1 of R3.

But VELVETFRUIT_EXTRACT (delta-hedged passive) lost −5,834 and VEV_5200 lost −6,125 — these two products account for the entire $14K drag against HYDROGEL's win. The other 8 VEV strikes either traded zero (5 strikes, deep ITM/OTM) or contributed small losses (3 strikes, total −2,341).

**Net non-HYDROGEL contribution: −14,301.** Removing VEL passive and consolidating to 1–2 active VEV strikes would have cleaned up the round.

---

## Round 4 — Same product set + counterparty signals (12 products, exact)

| Product | Real-engine PnL |
|---|---|
| HYDROGEL_PACK | **+56,200.25** |
| VELVETFRUIT_EXTRACT | +4,032.55 |
| VEV_4000 | +2,875.66 |
| VEV_4500 | 0.00 (no trades) |
| VEV_6000 | 0.00 (no trades) |
| VEV_6500 | 0.00 (no trades) |
| VEV_5400 | −7.79 |
| VEV_5500 | −14.92 |
| VEV_5100 | −584.30 |
| VEV_5000 | −1,102.04 |
| VEV_5200 | −1,638.35 |
| VEV_5300 | **−2,713.37** |
| **Total** | **+57,047.69** |

HYDROGEL again the dominant winner: +56,200 (vs +55,100 in R3 — 1.99% variance, the strategy is calibrated). The Mark-counterparty signals (composite flow tilt + Mark 49 cooldown) and the 4 Phase-12 fixes lifted the round by ~$6.2K vs R3 — concentrated entirely in VELVETFRUIT_EXTRACT flipping from −5,834 (R3) to +4,033 (R4), a +9,866 swing. The live-only mark signals appear to have specifically helped VEL execution.

VEV options on R4: net **−3,185** (vs R3's −8,466) — improvement driven by VEV_4000 swinging from 0 to +2,875. Other 9 strikes substantially smaller than R3 across the board. The Mark signals also benefited the option book modestly.

---

## Round 5 — 50 products (v42)

### Decomposition by strategy bucket (v42 lists × JSON 50-product PnL)

| Bucket | n | Net PnL | % of total |
|---|---|---|---|
| **DIRECTIONAL** (TARGETS_DIR ±10) | 13 | **+67,110.92** | 116% (carried the round) |
| **HEDGED_NO_SKEW** (SNACKPACK CHOC/VAN) | 2 | **+9,858.39** | 17% |
| **DEFAULT_MM** (22 products) | 22 | **−16,293.55** | −28% (dominated by MICROCHIP_SQUARE) |
| **TIER3** (LIMIT=5) | 2 | **−2,764.37** | −5% (small loss, manageable) |
| **BLACKLIST** (LIMIT=0) | 11 | **0.00** | 0% (designed exactly) |
| **TOTAL** | 50 | **+57,911.39** | 100% |

The strategy worked exactly as designed at the bucket level: DIRECTIONAL was the dominant alpha source, BLACKLIST was perfectly disabled (zero PnL on every blacklisted product), HEDGED_NO_SKEW was a small clean win, TIER3 lost a manageable amount. DEFAULT_MM was the *only* drag — and it was dominated by a single product (see below).

### DIRECTIONAL bucket (n=13, +67,110.92 net)

| Product | Side | PnL | Outcome |
|---|---|---|---|
| PEBBLES_M | −10 | +35,275.81 | M went down → short paid off |
| PEBBLES_XL | +10 | +19,552.34 | XL went up → long paid off |
| OXYGEN_SHAKE_GARLIC | +10 | +14,692.50 | up |
| UV_VISOR_RED | +10 | +13,743.70 | up |
| PEBBLES_L | −10 | +12,441.80 | L went down → short paid off |
| UV_VISOR_AMBER | −10 | +6,235.31 | down |
| SNACKPACK_STRAWBERRY | +10 | +5,975.43 | up |
| SNACKPACK_PISTACHIO | −10 | −1,125.45 | mild reversal |
| MICROCHIP_OVAL | −10 | −2,649.41 | reversal |
| PEBBLES_XS | −10 | −3,443.12 | XS went up — short hurt |
| PANEL_2X4 | +10 | −3,822.22 | down — long hurt |
| GALAXY_SOUNDS_BLACK_HOLES | +10 | −4,913.63 | down — long hurt (BH was the contested R5 directional) |
| PEBBLES_S | −10 | **−24,852.15** | S went up — short hurt badly |

**PEBBLES basket net: +38,973.68** (5 products: XL +19,552, M +35,275, L +12,441, XS −3,443, S −24,852). 3 of 5 worked; PEBBLES_S reversed badly. The structural anti-correlation thesis held overall but with one large outlier.

**GALAXY_SOUNDS_BLACK_HOLES at −4,913** is notable: this is the v36/v42 disagreement product (v36 dropped it; v42 kept it because Prosperity-window drift was negative but full-day drift was positive). On Day 5, it drifted further down — v36's call would have been correct. The $6,799 backtester gap that v42 accepted to keep BLACK_HOLES did *not* pay off on Day 5 specifically. Verdict on v42 vs v36: rank-against-the-field still favored v42 (#287 algo round-rank), but the specific directional bet was wrong.

### DEFAULT_MM bucket (n=22, −16,293.55 net)

| Product | PnL | Note |
|---|---|---|
| UV_VISOR_YELLOW | +7,754.37 | top MM winner |
| ROBOT_VACUUMING | +5,099.71 | |
| TRANSLATOR_ASTRO_BLACK | +2,872.10 | |
| UV_VISOR_ORANGE | +2,663.24 | |
| PANEL_4X4 | +2,223.32 | |
| ROBOT_IRONING | +2,200.00 | |
| TRANSLATOR_ECLIPSE_CHARCOAL | +1,707.21 | |
| OXYGEN_SHAKE_CHOCOLATE | +1,037.00 | |
| GALAXY_SOUNDS_SOLAR_FLAMES | +894.86 | |
| UV_VISOR_MAGENTA | +621.23 | |
| MICROCHIP_CIRCLE | +578.00 | |
| SLEEP_POD_COTTON | +303.22 | |
| TRANSLATOR_GRAPHITE_MIST | −399.40 | |
| SNACKPACK_RASPBERRY | −883.37 | |
| GALAXY_SOUNDS_SOLAR_WINDS | −1,251.35 | |
| SLEEP_POD_POLYESTER | −1,433.96 | |
| TRANSLATOR_VOID_BLUE | −1,946.92 | |
| SLEEP_POD_SUEDE | −2,370.70 | |
| MICROCHIP_TRIANGLE | −3,471.00 | |
| SLEEP_POD_NYLON | −5,205.74 | |
| ROBOT_MOPPING | −8,649.38 | |
| **MICROCHIP_SQUARE** | **−18,636.00** | **single-product MM disaster** |

**Without MICROCHIP_SQUARE, DEFAULT_MM net = +2,342.45** (slightly positive). The bucket's net loss is 100% attributable to one product.

### CORRECTION: MICROCHIP_SQUARE was NOT in the directional list

Earlier vault narratives ("MICROCHIP_SQUARE flip recurrence" — the canonical Phase-13 OOS-flip in directional) were **wrong** about v42's structure. **MICROCHIP_SQUARE was in DEFAULT_MM, not in TARGETS_DIR.** v42 had correctly excluded it from directional (per Phase 13's noted OOS-flip bug). The −18,636 loss came from **market-making MICROCHIP_SQUARE on a day with strong directional drift** — adverse selection picked off our quotes. The lesson is different than originally documented:

- **Old (wrong) lesson:** "MICROCHIP_SQUARE flipped again on Day 5; we should have removed it from directional"
- **New (correct) lesson:** "MICROCHIP_SQUARE was already excluded from directional. The loss came from MM exposure to a strongly-drifting product. The fix would have been to **add it to MM_BLACKLIST** when its drift signal exceeds the adverse-selection threshold, not to remove it from directional (where it already wasn't)."

This is a more nuanced bug: v42's filter-into-blacklist logic was based on cross-version log evidence (N=12), but MICROCHIP_SQUARE's logs were inconsistent enough that it stayed in DEFAULT_MM. A drift-magnitude-based blacklist criterion would have caught it.

### HEDGED_NO_SKEW (n=2, +9,858.39 net)

| Product | PnL |
|---|---|
| SNACKPACK_VANILLA | +8,998.08 |
| SNACKPACK_CHOCOLATE | +860.31 |

The structural pair (ρ = −0.916 from `within_category_xcorr_summary.csv`) delivered as expected. Bigger inner size 8 + no inventory skew = clean spread capture. ML analogy: anti-correlated dual hedge is a low-variance estimator.

### TIER3 (n=2, −2,764.37 net)

| Product | PnL |
|---|---|
| MICROCHIP_RECTANGLE | −402.37 |
| OXYGEN_SHAKE_EVENING_BREATH | −2,362.00 |

LIMIT=5 worked: total bleed was contained. Compared to v40's TIER3-removal mistake (which doubled losses by un-tiering 9 products to LIMIT=10), keeping LIMIT=5 saved meaningful capital.

### BLACKLIST (n=11, 0.00 net)

All 11 products: **exactly 0.00 PnL** — no trades placed, no PnL accumulated. The blacklist worked perfectly.

| Product | PnL |
|---|---|
| TRANSLATOR_SPACE_GRAY, GALAXY_SOUNDS_PLANETARY_RINGS, ROBOT_DISHES, OXYGEN_SHAKE_MORNING_BREATH, GALAXY_SOUNDS_DARK_MATTER, PANEL_2X2, ROBOT_LAUNDRY, PANEL_1X2, PANEL_1X4, OXYGEN_SHAKE_MINT, SLEEP_POD_LAMB_WOOL | 0.00 each |

### Full 50-product table (sorted by PnL desc)

| Rank | Product | Bucket | PnL |
|---|---|---|---|
| 1 | PEBBLES_M | DIRECTIONAL | +35,275.81 |
| 2 | PEBBLES_XL | DIRECTIONAL | +19,552.34 |
| 3 | OXYGEN_SHAKE_GARLIC | DIRECTIONAL | +14,692.50 |
| 4 | UV_VISOR_RED | DIRECTIONAL | +13,743.70 |
| 5 | PEBBLES_L | DIRECTIONAL | +12,441.80 |
| 6 | SNACKPACK_VANILLA | HEDGED | +8,998.08 |
| 7 | UV_VISOR_YELLOW | DEFAULT_MM | +7,754.37 |
| 8 | UV_VISOR_AMBER | DIRECTIONAL | +6,235.31 |
| 9 | SNACKPACK_STRAWBERRY | DIRECTIONAL | +5,975.43 |
| 10 | ROBOT_VACUUMING | DEFAULT_MM | +5,099.71 |
| 11 | TRANSLATOR_ASTRO_BLACK | DEFAULT_MM | +2,872.10 |
| 12 | UV_VISOR_ORANGE | DEFAULT_MM | +2,663.24 |
| 13 | PANEL_4X4 | DEFAULT_MM | +2,223.32 |
| 14 | ROBOT_IRONING | DEFAULT_MM | +2,200.00 |
| 15 | TRANSLATOR_ECLIPSE_CHARCOAL | DEFAULT_MM | +1,707.21 |
| 16 | OXYGEN_SHAKE_CHOCOLATE | DEFAULT_MM | +1,037.00 |
| 17 | GALAXY_SOUNDS_SOLAR_FLAMES | DEFAULT_MM | +894.86 |
| 18 | SNACKPACK_CHOCOLATE | HEDGED | +860.31 |
| 19 | UV_VISOR_MAGENTA | DEFAULT_MM | +621.23 |
| 20 | MICROCHIP_CIRCLE | DEFAULT_MM | +578.00 |
| 21 | SLEEP_POD_COTTON | DEFAULT_MM | +303.22 |
| 22–32 | (11 BLACKLIST products) | BLACKLIST | 0.00 each |
| 33 | TRANSLATOR_GRAPHITE_MIST | DEFAULT_MM | −399.40 |
| 34 | MICROCHIP_RECTANGLE | TIER3 | −402.37 |
| 35 | SNACKPACK_RASPBERRY | DEFAULT_MM | −883.37 |
| 36 | SNACKPACK_PISTACHIO | DIRECTIONAL | −1,125.45 |
| 37 | GALAXY_SOUNDS_SOLAR_WINDS | DEFAULT_MM | −1,251.35 |
| 38 | SLEEP_POD_POLYESTER | DEFAULT_MM | −1,433.96 |
| 39 | TRANSLATOR_VOID_BLUE | DEFAULT_MM | −1,946.92 |
| 40 | OXYGEN_SHAKE_EVENING_BREATH | TIER3 | −2,362.00 |
| 41 | SLEEP_POD_SUEDE | DEFAULT_MM | −2,370.70 |
| 42 | MICROCHIP_OVAL | DIRECTIONAL | −2,649.41 |
| 43 | PEBBLES_XS | DIRECTIONAL | −3,443.12 |
| 44 | MICROCHIP_TRIANGLE | DEFAULT_MM | −3,471.00 |
| 45 | PANEL_2X4 | DIRECTIONAL | −3,822.22 |
| 46 | GALAXY_SOUNDS_BLACK_HOLES | DIRECTIONAL | −4,913.63 |
| 47 | SLEEP_POD_NYLON | DEFAULT_MM | −5,205.74 |
| 48 | ROBOT_MOPPING | DEFAULT_MM | −8,649.38 |
| 49 | **MICROCHIP_SQUARE** | DEFAULT_MM | **−18,636.00** |
| 50 | **PEBBLES_S** | DIRECTIONAL | **−24,852.15** |
| | **Total** | | **+57,911.39** |

---

## Cross-round consistency

HYDROGEL real-engine PnL is **remarkably stable**: R3 day 55,100 vs R4 day 56,200 — 1.99% variance. The strategy is calibrated and the underlying alpha is real. VEV options were a steady drag in R3/R4. R5's PEBBLES basket and OS_GARLIC / UV_VISOR_RED directional bets were the strongest single-round contributions of any algo across the competition.

## Links

[[Performance/Manual_Per_Round]] · [[User_Reported_Anchors]] · [[Final_Competition_Result]] · [[Verify]] · [[Backtests/PnL_Timeline]] · [[Manuals/MAF]] · [[Strategies/Round5_Version_History]] · [[Concepts/Backtester_vs_Competition]]

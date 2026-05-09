---
type: backtest
tags: [calibration, tolerance, round3, day3, hydrogel, options, synthetic-fills]
sources: [backtests/phase1_back04_tolerance.md, research/round3/compare_to_competition.py, research/round3/options_fill_model.py, logs/round3/Prosperity Results/486282.json]
updated: 2026-04-27
---

# Phase 1 BACK-04: Local vs Official Backtest Calibration

> **Verdict: PASS at 10% tolerance.** Local overestimates by +7.2%. Apply ×0.93 to total local PnL for an unbiased point estimate.

---

## Log Type Clarification

| Log | Ticks | Coverage | Use |
|-----|-------|----------|-----|
| **Prosperity Results** (486282.json) | 10,000/day | Full day — ground truth | This report |
| **Prosperity Backtest** (466298.json) | 1,000/day | 10% preview only | NOT used for calibration |

> **Previous error:** BACK-04 had compared local full-day (10,000 ticks) against the Backtest preview (1,000 ticks = 10% of day, 2,533 XIREC), reporting a misleading **1,557% error**. Correct comparison against the full Results log gives **7.2% error**.

---

## Official Day 3 Results

| Product | Server PnL (XIREC) |
|---------|-------------------|
| HYDROGEL_PACK | +55,100.50 |
| VELVETFRUIT_EXTRACT | −5,834.75 |
| VEV_5000 | −449.17 |
| VEV_5100 | −1,598.18 |
| VEV_5200 | −6,125.11 |
| VEV_5300 | −241.84 |
| VEV_5500 | −51.88 |
| **TOTAL** | **40,799.58** |

---

## Local vs Server: Day 3

Local uses `data/round3/prices_round_3_day_3.csv` (extracted from 486282.json activitiesLog). No trades CSV — day 3 server trades are unavailable from competition data.

| Metric | Local (no trades) | Server | Rel Error |
|--------|------------------|--------|-----------|
| **TOTAL** | 43,749 | 40,799.58 | **+7.2%** |

### Per-product breakdown

| Product | Local | Server | Rel Error | Note |
|---------|-------|--------|-----------|------|
| HYDROGEL_PACK | 46,156 | 55,100.50 | **−16.2%** | Misses ~1,130 passive fills (training CSVs: ~324/day) |
| VELVETFRUIT_EXTRACT | 0 | −5,834.75 | +100% | No trades CSV → delta-hedge passive fills missing |
| VEV_5000 | 0 | −449.17 | +100% | |
| VEV_5100 | 0 | −1,598.18 | +100% | Passive bid fill build-up not captured |
| VEV_5200 | −2,407 | −6,125.11 | +60.7% | Partially captured via aggressive OB fills |
| VEV_5300 | 0 | −241.84 | +100% | |
| VEV_5500 | 0 | −51.88 | +100% | |

> **Net cancellation:** HYDROGEL is underestimated by 16.2% locally; options are over-estimated (zero vs negative). These biases partially cancel, leaving only +7.2% at the portfolio level.

---

## Known Divergence Sources

| Factor | Finding |
|--------|---------|
| Tick resolution | Both local and server sample every 100 units; 10,000 ticks/day. **No frequency gap.** |
| Passive fill model | Local fills passively only from trades CSV (~324 HYDROGEL events/day in training data). Server day 3 had ~1,130 HYDROGEL trades (3.5× more competition bot activity). |
| End-of-day MTM | Server settles at hidden fair value; local uses mid_price from CSV. Gap <0.5% for HYDROGEL; larger for options with wide bid-ask. |
| Options position build-up | Server passive option bids fill more often → larger long positions in VEV_5100/5200 → MTM loss vs near-zero locally. |
| --match-trades flag | No effect: all three modes (all/worse/none) give identical results with empty/sparse trades CSV. Not a root cause. |

---

## Proxy Trades Experiment

To bound the HYDROGEL passive fill gap, training-day trades CSVs were used as proxy for missing day 3 trades.  
(HYDROGEL price range is nearly identical across all days: 9,891–10,081.)

| Proxy | Local Total | vs Server | Notes |
|-------|-------------|-----------|-------|
| No trades (baseline) | 43,749 | +7.2% | All fills from OB only |
| Day 0 trades | 37,628 | −7.8% | HYDROGEL 44K; VEV −3,329 |
| Day 1 trades | 44,280 | +8.6% | HYDROGEL 48K; VEV −574 |
| Day 2 trades | 36,138 | −11.4% | HYDROGEL 41K; VEV −1,649 |
| **Average of proxies** | **39,349** | **−3.5%** | Best aggregate estimate |

**Conclusion:** Proxies are directionally unstable (±11%) because passive fills are directional — a trade from a different day can be profitable or loss-making depending on subsequent price movements. The average (39,349 = −3.5%) is the best point estimate but the no-trades run (43,749 = +7.2%) is simpler and within tolerance.

---

## Structural Limitation

Training data contains **~324 HYDROGEL trade events/day** (days 0–2). Back-engineering from the PnL gap implies **~1,130 events on competition day 3** (3.5× more bot activity from other teams crossing our spread). This is not reproducible from historical training data.

**Implication:**
- Local backtest is a reliable **directional signal** — a consistent improvement across days 0–2 is likely real.
- HYDROGEL PnL is ~7% under-estimated locally.
- Options PnL is over-estimated (negative server MTM vs near-zero locally).
- These biases partially cancel, yielding a +7.2% total overestimate.
- **Calibration factor:** multiply local total PnL by **×0.93** for an unbiased competition-day estimate.

---

## Infrastructure Built

| Artifact | Purpose |
|---------|---------|
| `data/round3/prices_round_3_day_3.csv` | 120,000 rows of market data extracted from 486282.json |
| `data/round3/trades_round_3_day_3.csv` | Empty (day 3 trades unavailable from logs) |
| `research/shared/infer_trades.py` | Synthetic trade inference from OB volume changes (tested, rejected — 174× overcounting from bot cancellations) |
| `research/round3/run_round3.py` | Added day 3 support (TTE=5.0d) to the backtest wrapper |
| `research/round3/compare_to_competition.py` | Full comparison pipeline: parse official JSON, run local backtests, generate tolerance report |
| `research/round3/options_fill_model.py` | Synthetic passive fill model: Bernoulli per eligible tick, per-strike calibration, simulate/calibrate modes |

---

## Options Backtest Blind Spot

Options PnL IS captured on training days 0–2 (trade CSVs exist). The problem is structural and specific to competition day:

- Local options (day 3): −0 to −2,407 XIREC
- Server options (day 3): −14,301 XIREC total

The same 3.5× bot-activity multiplier that drove the HYDROGEL passive fill gap also inflated options passive fills. Our passive VEV_5100/5200 bids were filled far more often, building large long positions that bled MTM as VELVETFRUIT moved.

**Consequence:** Options parameters (sizing, strike selection, bid-only vs two-sided) were tuned in Phases 6–8 on a model that cannot see competition-day fill rates. A larger passive bid size always looks better locally (more spread captured) but increases inventory risk on the server proportionally.

### Sizing Constraint for Round 4

Let $q$ = passive bid size, $N$ = training-day fill events, $λ$ = server/training fill-rate ratio (≈3.5). Expected server inventory:

$\text{Pos}_{\text{server}} \approx \lambda \cdot q \cdot N$

Set $q$ so MTM drawdown budget (e.g. 2,000 XIREC/strike/day) is not exceeded at $λ=3.5$:

$q \leq \frac{\text{Budget}}{\lambda \cdot N \cdot \Delta \cdot \sigma \cdot \sqrt{\Delta t}}$

### Design Rules for Round 4

1. **Budget-constrained sizing** — size passively so competition-day MTM stays within declared budget
2. **Prefer two-sided quoting** at symmetric strikes — fills partially self-hedge vs naked bid-only accumulation
3. **Do not optimise options sizing on 3-day local PnL** — reflects training fill rates, not competition fill rates
4. **Day 3 as calibration constraint** — 6× loss amplification (local −2,407 → server −14,301) bounds the fill-rate multiplier any Round 4 options model must account for

---

## Synthetic Fill Model Calibration

Built `research/round3/options_fill_model.py` to close the measurement gap using the exchange mechanism directly.

### Model

For each tick where:
- VEV option spread ≥ 3 (so VoucherTrader places a passive bid at `best_bid+1`)
- BS fair value − passive_bid ≥ edge threshold `ε_k`

Draw Bernoulli(p_k). If hit, inject a synthetic trade at `best_bid+1` with size `q_k` into the day-3 trades CSV. The standard backtest pipeline then picks it up via `--match-trades all`.

### Per-Strike Calibration Results

| Strike | p_fill | Local PnL | Server Target | Error |
|--------|--------|-----------|---------------|-------|
| 4000 | 0.000 | 0 | 0 | 0 |
| 5000 | 0.000 | 0 | −449 | +449 (saturation) |
| 5100 | 0.000 | 0 | −1,598 | +1,598 (saturation) |
| **5200** | **0.050** | **−6,266** | **−6,125** | **−141 (2.3%)** |
| 5300 | 0.000 | 0 | −242 | +242 (only 46 eligible ticks) |
| 5400 | 0.000 | 0 | 0 | 0 |
| 5500 | 0.000 | 0 | −52 | +52 |

`CALIBRATED_P_FILL = {5200: 0.05, all others: 0.00}`

Deep-ITM strikes (5000/5100): position limit (LIMIT=300) and DELTA_CAP_HARD=120 bind quickly, saturating PnL curve before server target is reached.

### Calibrated Simulation: Full Breakdown (day 3)

| Product | Local (calibrated) | Server | Gap |
|---------|-------------------|--------|-----|
| HYDROGEL_PACK | 46,156 | 55,100 | −8,944 |
| VELVETFRUIT_EXTRACT | 0 | −5,835 | +5,835 (unmodelled) |
| VEV_5000 | 0 | −449 | +449 |
| VEV_5100 | 0 | −1,598 | +1,598 |
| **VEV_5200** | **−6,266** | **−6,125** | **−141** |
| VEV_5300 | 0 | −242 | +242 |
| VEV_5500 | 0 | −52 | +52 |
| **GRAND TOTAL** | **39,890** | **40,799** | **−909 (−2.2%)** |

Generated: 223 synthetic VEV_5200 fill events at p_fill=0.05.

### Calibration Summary

| Scenario | Local total | vs Server |
|---------|------------|-----------|
| No fills (baseline) | 43,749 | +7.2% |
| VEV_5200 synthetic fills (p*=0.05) | 39,890 | **−2.2%** |

The calibrated model reduces total bias from +7.2% to −2.2%. Remaining gaps:
- **VELVETFRUIT_EXTRACT (−5,835):** second-layer step-4 on the underlying — passive VEV sell orders filled by competing bots. Not modelled; requires a separate Bernoulli process for VEV spot.
- **VEV_5000/5100:** likely 2–5 server fills total; position limits prevent faithful reproduction at per-tick resolution.

**Key insight:** Near-ATM VEV_5200 was the primary source of competition-day options losses. Approximately 1 passive fill per 45 eligible ticks on competition day vs 0 in training data.

---

## Why Most Strikes Produce Zero Local Transactions

This is expected and structurally inevitable. `VoucherTrader` has exactly two fill paths:

### Path 1: Aggressive take (step 3)

```python
edge = fair - ask_price   # BS_FV minus bot's ask
if edge < config["take_buy_edge"]:
    break
```

Since sigma was calibrated to historical option prices, `BS_FV ≈ option mid` by construction. At spread=2, `ask = mid + 1`, so `edge ≈ -1`. Structurally negative — **the take condition can never fire at spread=2**.

The only way it fires: VELVETFRUIT moves fast enough between ticks that BS_FV jumps above the stale option ask by more than `take_buy_edge`. This is a gamma event. Highest gamma = VEV_5200 (near-ATM). That's where the −2,407 local PnL comes from — rare aggressive buys during underlying spikes.

### Path 2: Passive quote fill (step 4)

The algo posts a passive bid only when spread ≥ 3 (`can_join = passive_bid < passive_ask`). For the bid to fill, a bot trade must arrive from the trades CSV crossing it.

Problem: In training data, options bot trades almost exclusively occur when spread = 2 (bots trade when the market is tight). So:
- Spread ≥ 3 → algo places passive bid → no CSV trade exists to fill it
- Spread = 2 → CSV trade might exist → can_join=False, no passive bid placed

The two conditions are nearly mutually exclusive in training data.

### Per-Strike Breakdown

| Strike | Why zero locally |
|--------|-----------------|
| VEV_4000 | `take_buy_edge=14.0` unreachable (BS_FV ≈ ask − 10). Passive bids placed inside 21-wide spread but no VEV_4000 bot trades in training CSV |
| VEV_5000/5100 | Low-liquidity OB — sell orders frequently absent (nothing to take aggressively). Passive bids placed but never crossed by CSV trades |
| **VEV_5200** | **Near-ATM, highest gamma → aggressive takes fire during underlying spikes → −2,407 local** |
| VEV_5300/5400/5500 | Spread = 2 nearly always in training data → can_join=False → passive path dead. Gamma too low for aggressive path |

### Implication

The local backtest is **useless for sizing** options positions (always too few fills) and only **marginally useful for directionality** (direction correct but magnitude ~3× compressed). The synthetic fill model is the only way to evaluate options under realistic competition-day fill rates.

---

## Links

[[Backtests/PnL_Timeline]] · [[Products/HYDROGEL_PACK]] · [[Products/VELVETFRUIT_EXTRACT]] · [[Strategies/Options_Quoting]] · [[Rounds/Round3_findings]]

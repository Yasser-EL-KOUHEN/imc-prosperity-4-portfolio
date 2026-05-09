---
type: concept
tags: [glossary, terminology, all-rounds, reference]
sources:
  - context/Game Mechanics Overview.txt
  - context/Trading glossary.txt
  - context/What is Prosperity.txt
  - vault canonical usage across pages
updated: 2026-05-01
---

# Glossary — IMC Prosperity 4 Terms

## Competition / Platform

| Term | Definition |
|---|---|
| **XIREC** | Synthetic profit unit. The leaderboard currency. Sometimes appears as "SEASHELLS" inside the matching engine logs (interchangeable). |
| **Prosperity** | The IMC trading simulator. Reads/writes order books per tick; matches our orders against bot orders. |
| **Prosperity backtester** | The dev-iteration tool. Runs the **first 10% of Day 4** (~100K of 1M ticks). Different scoring window from competition leaderboard. See [[Concepts/Backtester_vs_Competition]]. |
| **Local backtester** | Hand-rolled Python harness in `round{N}/research/run_round{N}.py`. Runs against CSV data with `--match-trades` policy. With `--match-trades all` it inflates fills relative to real Prosperity (documented as ~8.6× from v34/v35 comparison in `README.md`). |
| **GOAT** | "Great Orbital Ascension Trials" — the Round 3+ leaderboard reset. R3 starts the cumulative-PnL phase that runs through R5. |
| **Round 0** | Tutorial round (EMERALDS, TOMATOES). Simulator practice; no scoring weight. |
| **trader.py** | Single-file Python algorithm submitted to the platform. Allowed imports: `datamodel`, `jsonpickle`, standard library. |
| **TradingState** | The per-tick context object passed to `Trader.run()`. Contains `order_depths`, `position`, `market_trades`, `own_trades`, `timestamp`, `traderData`. |

## Order Book / Trading

| Term | Definition |
|---|---|
| **OBI** | Order Book Imbalance: `(bid_volume_1 - ask_volume_1) / (bid_volume_1 + ask_volume_1)` at top-of-book. Predictive of next-tick mid in some products. See [[Concepts/Order_Book_Imbalance]]. |
| **Spread** | `best_ask - best_bid`. Tight spreads (1–4 ticks) are R5-typical; wide (≥16) is R3 HYDROGEL-typical. |
| **Mid-price** | `(best_bid + best_ask) / 2`. The fair-value reference. |
| **Spread-cross / Aggressive take** | Buy at `best_ask` or sell at `best_bid` — pay the spread for guaranteed fill. |
| **Passive quote / Join queue** | Post bid at `best_bid` or `best_bid+1` (inside spread). Earn the spread on fill but no guarantee of fill. |
| **Adverse selection** | Informed counterparties hit your quote when price is moving against you. The reason MM bleeds on tight-spread products. See [[Concepts/Adverse_Selection]]. |

## Strategy Vocabulary

| Term | Definition |
|---|---|
| **MM (Market Making)** | Two-sided passive quoting; profit from spread × fills, minus inventory cost. The R3 HYDROGEL strategy. See [[Strategies/market_making]]. |
| **AR(1) mean reversion** | First-order autoregressive model; price reverts to mean with strength ρ. R3 HYDROGEL: ρ ≈ −0.13 (clean reversion). R5: ρ ≈ +0.999 (random walk with drift, no reversion). See [[Strategies/Mean_Reversion]]. |
| **Anchor blend** | Fair-value model: `fair = (1 - w)·EMA + w·anchor`. R3 HYDROGEL: anchor = 10,000, w = 0.20. R1 ACO: anchor = 10,000, w = 0.15. Bayesian shrinkage toward known prior. |
| **Magnitude-bucketed ρ** | Reversion coefficient depends on move size: small_rho if `|dmid| ∈ [2, 5)`, large_rho if `≥ 5`. R3 HYDROGEL: 0.08 / 0.42 (Phase 4 grid winner). |
| **Inventory skew** | Shift fair value against current position to encourage rebalancing: `adjusted_fair = fair − k·position`. R3: k=0.03 continuous. R5: step at \|pos\| > 6. |
| **Directional holding** | Build to fixed ±LIMIT at first tick, hold all day. R5 strategy for products with multi-day drift. See [[Strategies/Directional_Holding]]. |
| **TIER3** | R5-specific: products MM'd at reduced LIMIT=5 (vs default 10) due to adverse-selection risk. See [[Strategies/TIER3_Market_Making]]. |
| **HEDGED_NO_SKEW** | R5: structurally-paired products MM'd with bigger inner size and no inventory skew because the pair anti-correlation provides the hedge. SNACKPACK CHOC/VAN at ρ = −0.916. See [[Strategies/HEDGED_NO_SKEW]]. |
| **MM_BLACKLIST** | Products where MM is unconditionally skipped (LIMIT=0). R5: 11 products in v42 (3 zero-fill + 8 cross-version losers). |
| **OOS / OOS_DAY** | Out-of-sample validation. R5: `OOS_DAY = 4` pre-registered as a top-level constant; train days 2+3 only. |
| **HAC** | Heteroskedasticity- and Autocorrelation-Consistent standard errors (Newey-West). Required for tick-data regressions; naive OLS overstates significance. Used in Phase 14. |
| **BH-FDR** | Benjamini-Hochberg False Discovery Rate. Multiple-testing correction less conservative than Bonferroni. Used in Phase 14 (50 products × multiple horizons → many tests). |
| **Bonferroni** | Multiple-testing correction: α / n_tests. Used for the lead-lag null result (α = 0.05/36750 ≈ 1.36e-6). See [[Concepts/Lead_Lag]]. |

## R4 Counterparty Vocabulary

| Term | Definition |
|---|---|
| **Mark** | A bot counterparty in R4 with disclosed name (`Mark 67`, `Mark 49`, etc.). R5 removed disclosure (buyer/seller fields are empty strings). |
| **Mark 67** | The "dip buyer" — never sells, takes ask₁ at local lows (92.7% buys at below-5-MA). Bullish signal. |
| **Mark 49** | The "local-high seller" — passive ask poster, hit at local peaks. Bearish signal. |
| **Mark 22** | Aggressive VEL seller (184/day). Excluded from composite (frequency mismatch). |
| **Composite flow / `mark_net`** | `(Mark 67 buy events) − (Mark 49 sell events)` per tick, accumulated over the day. Used as VEL passive bid tilt at thresholds ±5/−3. |
| **own_trades vs market_trades** | The Prosperity datamodel splits trades into two non-overlapping collections: `own_trades` (we were a counterparty), `market_trades` (we were not). Both must be scanned to see all Mark activity. See [[Research/Decisions_Log|D14]]. |

## Options / R3-R4 Specific

| Term | Definition |
|---|---|
| **VEV** | VELVETFRUIT_EXTRACT_VOUCHER — call options on VELVETFRUIT_EXTRACT in R3. 10 strikes from 4000 to 6500. |
| **AC** | AETHER_CRYSTAL options in R4 manual — 11 vanillas + 1 chooser + 1 binary put + 1 knockout put. |
| **TTE** | Time to expiry, in days. R3 schedule: Day 1 → 7d, Day 2 → 6d, Day 3 → 5d (encoded as a dict). |
| **IV (Implied Volatility)** | The σ that makes the BS price equal to the market price. Per-strike σ varies (smile). R3 ATM strike (5400) had lowest σ = 0.230 (smile trough). |
| **IV z-score** | `(realized_IV - strike_IV) / strike_IV_std`. Used as passive sizing bias only — never aggressive taking ([[Research/Decisions_Log|D2]]). |
| **Chooser option** | Owner picks between call and put at a future date T_c < T. Static-replicable for r=0 GBM as `C(T) + P(T_c)`. See [[Concepts/Chooser_Option]]. |
| **Binary / Digital option** | Pays a fixed amount if S exceeds (or is below) a strike; zero otherwise. Cliff payoff at strike. Fair value = `N(±d₂) × payout`. See [[Concepts/Binary_Option]]. |
| **Knockout option** | Standard option that becomes worthless if S crosses a barrier B. Merton barrier formula + Broadie-Glasserman discrete adjustment. See [[Concepts/Knockout_Option]]. |
| **Delta-1 (instrument)** | An instrument that moves 1:1 with the underlying. HYDROGEL_PACK is a delta-1 commodity in R3. Options are delta < 1. |

## Phase Numbering (which round?)

| Phase range | Round | Topic |
|---|---|---|
| 1–2 | R3 prep | Backtest engine, parameter sweep infrastructure |
| 3–4 | R3 | HYDROGEL signal core + tuning |
| 5 | R3 | VELVETFRUIT hedge validation |
| 6–8 | R3 | Options BS + quoting + OBI |
| 9 | R3 | Safety hardening |
| 10–11 | R3 | Submission pipeline + box-and-lines null |
| 12 | R4 | Counterparty exploitation |
| 13–14 | R5 | Directional trading + 6-analysis EDA |
| 15–16 | R5 | ML deadends (alpha_lab, GRU, synthetic) — empty `.planning/` dirs |
| 17 | R5 | (informal in v23 docstring; no planning artifact) |

## Confidence Levels (used in `full_day_optimal.csv`)

| Level | Criterion |
|---|---|
| HIGH | Drift sign-stable on **all 3** days (2/3/4) |
| MED | Drift sign agrees on 2/3 days, day-4 sign matches |
| LOW | Mixed across days (don't trade directional; default to MM) |

## Quick Numbers Reference

| Number | Where it comes from |
|---|---|
| 263K | R1 final XIREC (algo) |
| 153,566 | R3 final local-baseline 3-day PnL |
| 175,200 | R4 manual portfolio expected value (E[+58.4 × 3000 mul]) |
| 261,461 | R5 Phase 13 v1 GRAND TOTAL (3-day local, 7-product directional only) |
| 78,799 | R5 v36 measured Prosperity backtester PnL (local-optimum, NOT submitted) |
| 72,000 | R5 v42 measured Prosperity backtester PnL (user-reported; **submitted**, deliberately lower than v36 to avoid overfitting) |
| 62,299 | R5 v34 measured Prosperity backtester PnL (full-day champion baseline) |
| 152,730 | R5 v34 estimated full-day PnL (from `full_day_optimal.csv` × position) |
| 163,000 | R5 v42 estimated full-day PnL (v34 setup + STRAWBERRY + 8-loser blacklist) |
| 36,750 | R5 lead-lag tests run (1,225 pairs × 5 lags × 3 days × 2 directions) |
| 1.36e-6 | R5 lead-lag Bonferroni α (0.05/36,750) |
| 0/36,750 | R5 lead-lag tests surviving filter (confirmed null) |
| −0.916 | R5 SNACKPACK CHOC/VAN return correlation (canonical structural pair) |
| ≈0.999 | R5 AR(1) ρ across all 50 products (mean-reversion impossible) |

## Links

[[Overview]] · [[Cross_Round_Comparison]] · [[Concepts/Backtester_vs_Competition]] · [[Concepts/Adverse_Selection]] · [[Concepts/Lead_Lag]] · [[Research/Decisions_Log]] · [[Strategies/Round5_Version_History]]

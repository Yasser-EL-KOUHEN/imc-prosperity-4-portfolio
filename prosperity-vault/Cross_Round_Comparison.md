---
type: competition
tags: [cross-round, comparison, evolution, all-rounds, post-competition]
sources:
  - round{0..5}/README.md
  - prosperity-vault/Rounds/
  - prosperity-vault/Performance/
  - report/report.tex
updated: 2026-05-08
---

# Cross-Round Comparison

> One page that tracks what stayed the same and what changed, round by round.

## Realized Per-Round Results (verified 2026-05-08)

| Round | Algo PnL | Manual PnL | Cumul. rank (overall) |
|---|---|---|---|
| R1 | +98,172 (v2 — book-anchored) | +71,500 | ~#2,000 |
| R2 | +91,529 (v3 + MAF, ACCEPTED) | +153,345 | #1,522 |
| R3 | +40,800 (v3 stripped) | +75,238 (Bio-Pods (760, 855)) | #802 |
| R4 | +57,048 (v3 + Mark signals) | +57,516 (AC exotics) | #592 |
| R5 | +57,911 (v42) | +95,214 (Ashflow Alpha) | **#346** |

**GOAT total (R3+R4+R5):** algo 155,759 + manual 227,968 = **383,727 XIREC**, **#346 / 18,803 (top 1.84%)**.

**Manuals carried 60% of GOAT XIREC** despite the algo dominating project hours.

## Manual Common-Knowledge Index

| Round | Manual | Common knowledge? | Realization ratio | Rank lift available? |
|---|---|---|---|---|
| R1 | Dryland Flax + Ember Mushroom | YES (deterministic clearing-price) | 1.00 | no — display rank is tie-breaking |
| R2 | I&E (Research/Scale/Speed) | NO (peer-prior matters) | 1.39 | YES (rank #801) |
| R3 | Bio-Pods (sealed-bid NE) | YES (symmetric BNE) | 0.92 | minimal — display rank is tie-breaking |
| R4 | AC exotic options (12 instruments) | YES (BS-pricing consensus) | 0.33 | minimal — we aligned with field on every leg |
| R5 | Ashflow Alpha (archetype taxonomy) | NO (archetype confidence matters) | 0.68 | YES (rank #204) |

**3 of 5 manuals were common-knowledge regimes.** The two non-common-knowledge manuals (R2, R5) outperformed on rank-per-effort. Carry-forward: invest more time on asymmetric-information manuals where peer-prior choice or label confidence drives rank lift.

## Product / Universe

| Round | # products | Position limit | Spread regime | Counterparty info |
|---|---|---|---|---|
| 0 | 2 (EMERALDS, TOMATOES) | 80 | medium | none |
| 1 | 3 (EMERALDS, ACO, IPR) | 20 | wide on ACO (~16t) | none |
| 2 | same as R1 | 20 | same | none |
| 3 | 12 (HYDROGEL + VEL + 10 VEV) | 200 / 200 / 300 | wide on HYDROGEL (≥16t) | none |
| 4 | same 12 as R3 | same | same | **Mark IDs disclosed** (Mark 01–67) |
| 5 | 50 new (10 categories × 5) | **±10 universal** | tight (1–4t typical) | **Mark IDs removed** (empty fields) |

**The structural inflection:** R5's position-limit collapse from 200 → 10 forced a complete strategy reshape. Per-tick alpha had to be order-of-magnitude higher to make ±10 positions worthwhile.

## Strategy Architecture

| Round | Primary engine | Secondary | Tertiary |
|---|---|---|---|
| 1 | ACO anchor-blend MM | IPR greedy long | (none) |
| 2 | R1 algo unchanged | Manual MAF + I&E game theory | — |
| 3 | HYDROGEL AR(1) MM | BS options quoting | VEL passive delta hedge |
| 4 | R3 trader (unchanged) | Mark composite-flow tilt + cooldown | Manual exotic options portfolio |
| 5 | Directional hold (13 products) | Per-product tiered MM (TIER3 / blacklist / HEDGED_NO_SKEW) | (Phase 14 OBI / XGBoost — researched, not shipped) |

## Mean-Reversion Dynamics

| Round | Product | Lag-1 ACF | AR(1) ρ | MM viable? |
|---|---|---|---|---|
| 1 | ACO | strongly negative | ρ₁ = −0.495 | yes (R1 cornerstone) |
| 1 | IPR | trending +0.1/tick | drift, not reversion | no — directional |
| 3 | HYDROGEL | negative | small=0.094, large=0.237 (calibrated) | yes (R3 cornerstone) |
| 5 | all 50 | ~0 | ≈ +0.999 | **no** — random walk with drift |

R5's AR(1) ≈ 0.999 is the empirical reason directional holding replaced MM as primary engine.

## Backtester / Calibration Story

| Round | Local-vs-real-engine ratio | Method to calibrate |
|---|---|---|
| 1 | unknown (Jasper backtester had time-priority bug) | v2 fix: book-anchor quoting |
| 3 | local × 0.93 ≈ real | Phase 1: full-day Results-log comparison |
| 4 | same as R3 (same products + engine) | inherited |
| 5 | local × ~1/8.6 ≈ real (with `--match-trades all`) | Documented in `README.md`; v34/v35 comparison; exact replication script not preserved |

## Key Decisions per Round

| Round | Key decisions |
|---|---|
| 1 | v2 book-anchor fix (price priority); v3 anchor blend (15% toward 10000); magnitude-bucketed ρ; never-sell IPR |
| 2 | Bayesian-Nash MAF bid; exact I&E optimum (16, 48, 36) at 110,065 |
| 3 | D1 VEL passive-only · D2 IV-z passive-only · D3-D4 strike segmentation · D5 OBI off · D6 anchor_w=0.20 · D7 keep calibrated · D8 box null · D11 Bio-Pods (755, 840) |
| 4 | D12 Mark composite flow · D13 state.timestamp anchor · D14 own_trades + market_trades · D15-D17 manual portfolio (chooser/binary/skip 60C) |
| 5 | D18 directional-not-MM · D19 OOS_DAY=4 · D20 Prosperity logs > local · D21 blacklist > aggressive MM · D22 HEDGED_NO_SKEW · D23 PEBBLES basket · D24 STRAWBERRY add · D25 v42 final |

## Manual Challenges

| Round | Challenge | Method | Theoretical | Realized |
|---|---|---|---|---|
| 1 | Dryland Flax + Ember Mushroom | Clearing-price engineering | 71,500 | **71,500** (exact, rank #72; common-knowledge) |
| 2 | MAF bid framework | Find break-even bid b* | b* = 3,000 | **bid ACCEPTED**, 3K paid; volume bonus absorbed by IPR cap |
| 2 | Invest & Expand | EV across log×linear×rank | 110,065 (FOC) | **+153,345** (1.39× FOC); submitted (18,60,22) bottom-heavy-tilt was right |
| 3 | Bio-Pods Celestial Gardeners | Symmetric Bayesian-Nash | NE = (755,840), 81.67/cp | **+75,237.51** (submitted (760,855); N=1,000 cps; 75.24/cp = 92% of NE) |
| 4 | AETHER_CRYSTAL exotic options | BS pricing + structural hedging | E[+175,200] | **+57,516** (33%); common-knowledge, V-shaped path |
| 5 | Ashflow Alpha (Ignith news) | Archetype classification + p* = s/2 | 140,100 | **+95,214** (68%); 6 directionally right, Magma+Ashes magnitude tiny |

## What Worked Across Rounds

| Pattern | Used in |
|---|---|
| EDA before strategy (regime check + ACF + Hurst) | R1, R3, R5 |
| Magnitude-bucketed ρ | R1 (`grid_rho_magnitude.py`) → R3 HYDROGEL |
| Anchor blend (Bayesian shrinkage to known prior) | R1 ACO, R3 HYDROGEL |
| All-days-improve OOS gate (parameter sweeps) | R3 (every phase), R5 (Phase 13/14) |
| Pre-registered OOS day | R5 (Phase 14 explicit `OOS_DAY=4`) |
| Single-file constraint (no scipy) | R3 (pure-math BS), R5 (stateless trader) |
| Anti-regression gate (don't break the baseline) | R3 Phase 11, R4 Phase 12 |
| Static replication for exotic options | R4 (chooser, binary spread, KO) |
| Cross-version evidence aggregation | R5 (N=12 Prosperity logs → blacklist) |

## What Didn't Work / Failed Hypotheses

| Failed approach | When | Why it failed |
|---|---|---|
| OBI on HYDROGEL | R3 Phase 3 | Statistically real (R²=0.089) but execution cost > edge |
| Aggressive IV-z taking | R3 v2 | Delta-hedge slippage > vol edge |
| VEL spread-crossing | R3 v2 | −90K on day 2 alone |
| Box-and-lines signal | R3 Phase 11 | HYDROGEL mean-reverts too strongly for boxes to form |
| VEV_6000/6500 sell-at-bid=0 | R4 Phase 12 Change A | Local backtester valued at mid=0.5; EV=0 either way |
| Aggressive Mark 22 tracking | R4 | 184 events/day would dominate composite flow score |
| Local-CV reclassification (v35) | R5 | Local-BT 8.6× fill inflation; wrong distribution |
| TIER3 removal (v40) | R5 | Adverse-selection scales **with** volume, not against |
| BLACK_HOLES flip to −10 (v37) | R5 | Prosperity-window vs full-day conflict product |
| GRU / XGBoost / SDE synthetic for production | R5 (Phase 15/16 ML lab) | Sign accuracy 0.49 (worse than chance OOS); valid R² −0.17 |
| Lead-lag mining at 1–20 tick horizons | R5 | 0/36,750 tests survive Bonferroni — confirmed null |
| **R5 v42 directional bets on PANEL_2X4 / BLACK_HOLES** | R5 (post-result) | Realized −$3,822 / −$4,914 on Day 5; v36's call to drop them was actually correct on the realized day |
| **MICROCHIP_SQUARE in DEFAULT_MM** | R5 (post-result) | Adverse-selection picked off our quotes on a strong-drift day; lost $18,636 alone (1/3 of round drag); blacklist-by-drift-magnitude criterion would have caught it |
| **Common-knowledge manual analysis (R1, R3, R4)** | R1, R3, R4 (post-result) | When manual is symmetric-information, optimization gives no edge over the median solver; ~1,600–2,200 teams arrived at same trades in R4 |
| **Manual EV uniform optimism** (initial post-result framing) | All 5 rounds | REJECTED — only R4 badly missed (33%); R1 exact, R2 over-FOC, R3 92% of NE, R5 matches archetype hit rate |

## What Changed in Tooling

| Round | Tooling addition |
|---|---|
| 1 | EDA harness (`eda.py`); edge-hunt iteration scripts |
| 3 | Phase 1 backtest engine; pure-math BS engine; `run_round3.py` |
| 4 | `run_round4.py`; counterparty scan in market_trades + own_trades |
| 5 | `run_round5.py` (no TTE block); `eda2/` package with HAC + BH-FDR + parallel-analysis PCA + Lo-MacKinlay VR; `analyze_prosperity_logs.py` for cross-version aggregation; `drift_audit.py` for window comparison |

## Links

[[Overview]] · [[Concepts/Glossary]] · [[Carry_Forward]] · [[Backtests/PnL_Timeline]] · [[Research/Decisions_Log]] · [[Rounds/Round1_findings]] · [[Rounds/Round2_findings]] · [[Rounds/Round3_findings]] · [[Rounds/Round4_findings]] · [[Rounds/Round5_findings]]

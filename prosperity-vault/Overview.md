---
type: competition
tags: [overview, all-rounds, synthesis, post-competition, final-result]
sources:
  - .planning/PROJECT.md
  - report/report.tex
  - round{0..5}/README.md
  - prosperity-vault/Rounds/Round{0..5}_findings.md
  - prosperity-vault/User_Reported_Anchors.md
updated: 2026-05-08
---

# IMC Prosperity 4 — Competition Overview

## Final Result (received 2026-05-08)

| Metric | Value |
|---|---|
| **Final overall rank** | **#346 / 18,803 teams (top 1.84%)** |
| Algorithmic rank | #537 |
| **Manual rank** | **#204** (better than algo) |
| **Country rank** | **#11** (strongest sub-ranking) |
| Final GOAT XIREC | **383,727** (R3+R4+R5 cumulative) |
| Field | 30,703 players · 18,803 teams · 1,549 universities · 117 countries |

### Per-round PnLs

| Round | Algo PnL | Manual PnL | Round Total |
|---|---|---|---|
| R1 | +98,172 | +71,500 | 169,672 |
| R2 | +91,529 | +153,345 | 244,874 |
| R3 | +40,800 | +75,238 | 116,038 |
| R4 | +57,048 | +57,516 | 114,564 |
| R5 | +57,911 | +95,214 | 153,125 |

### Cumulative leaderboard rankings at end of each round (canonical)

| Round | Overall | Algorithmic | Manual | Country |
|---|---|---|---|---|
| R1 | ~#2,000 | ~#1,400 | #72 *(≈ #3,000 w/o ties)* | #59 |
| R2 | #1,522 | #857 | #801 | #59 |
| R3 | #802 | #830 | #234 *(≈ #1,200 w/o ties)* | #30 |
| R4 | #592 | #809 | #406 | #21 |
| **R5 final** | **#346** | **#537** | **#204** | **#11** |

GOAT decomposition: **algo 155,759 (40.6%)**, **manual 227,968 (59.4%)** — manuals delivered 60% of final XIREC despite the algo representing the bulk of project hours. Algo cumul-rank trajectory ~1,400 → 857 → 830 → 809 → **537** (~860 places gained); country-rank improved fastest (59 → **#11**). Both R1 and R3 manuals had massive-tie regimes (deterministic clearing-price for R1, symmetric NE for R3 Bio-Pods). See [[User_Reported_Anchors]] for provenance.

## What We Did

IMC Prosperity 4 is a university-level algorithmic trading competition hosted by IMC Trading. Competitors write a single-file Python algorithm (`trader.py`) that runs per-tick against a simulated limit-order-book exchange. Allowed imports: `datamodel`, `jsonpickle`, standard library. Currency: **XIREC** (synthetic profit units).

**Profile:** Solo competitor. MPSI/MP* → MEng CS/ML → MSc DS&BA. Strong math/ML background; learned market microstructure through the competition. Result: **#346 / 18,803 (top 1.84%)** — top-decile country (#11).

## Quick Start (read these first if you're new)

If you just opened the wiki and want the fastest orientation:

1. **[[Concepts/Glossary]]** — XIREC, GOAT, Mark, TIER3, HEDGED_NO_SKEW, etc.
2. **[[Cross_Round_Comparison]]** — what stayed the same, what changed, round to round
3. **[[Concepts/Backtester_vs_Competition]]** — the central R5 lesson
4. **[[Backtests/PnL_Timeline]]** — every round's PnL with verified Prosperity numbers
5. **[[Research/Decisions_Log]]** — D1–D20+ canonical architectural decisions

Then drill down by round: [[Rounds/Round1_findings]], [[Rounds/Round2_findings]], [[Rounds/Round3_findings]], [[Rounds/Round4_findings]], [[Rounds/Round5_findings]].

## Round Summary

| Round | Duration | Theme | Realized contribution | Cumulative rank |
|---|---|---|---|---|
| 0 (Tutorial) | — | EMERALDS, TOMATOES — platform familiarization | — | — |
| 1 | 72h | "Trading Groundwork" — ACO mean-reversion + IPR trend | ~168K (website-scaled, qualifier) | ~#2,000 |
| 2 | 72h | "Growing Your Outpost" — manual MAF + Invest & Expand | I&E ~155K + ACO/IPR carry | #1,522 (qualifier 414,546 cumul) |
| 3 | 48h | "Gloves Off" — HYDROGEL + VELVETFRUIT + 10 VEV options | **116,037** (algo + Bio-Pods manual) | #802 (GOAT begins) |
| 4 | 48h | "The More The Merrier" — Mark counterparty + AETHER exotics manual | **114,564** (algo + AC manual) | #592 |
| 5 | 48h | "The Final Stretch" — 50 products / 10 cats / limit ±10 + Ashflow Alpha manual | **153,126** (v42 algo + Ashflow) | **#346 (final)** |
| **Total GOAT (R3+R4+R5)** | | | **383,727 XIREC** | **#346 / 18,803 (top 1.84%)** |

## Strategy Map (one trader per round, layered)

**Round 1**: ACO anchor-blend MM (FV = 0.85·EMA + 0.15·10000, magnitude-bucketed ρ) + IPR greedy long (no sells, capture +0.1/tick trend).

**Round 2**: same algo + manual game theory (MAF auction NE, I&E exact optimum at (16,48,36)).

**Round 3**: HYDROGEL AR(1) MM (anchor_w=0.20, ρ_small=0.08, ρ_large=0.42) + VELVETFRUIT passive delta hedge + Black-Scholes options quoting on 10 VEV strikes (per-strike σ from market prices, IV-z passive sizing only). [[Strategies/Mean_Reversion]] · [[Strategies/Options_Quoting]] · [[Strategies/Delta_Hedging]].

**Round 4**: R3 trader + Mark composite flow score (`mark67 - mark49 ≥ ±5` for VEL bid tilt) + Mark 49 cooldown (500ms half-size after detection) + 4 implementation fixes. Manual exotic options portfolio with chooser, binary-put, knockout-put structural edges. [[Strategies/Counterparty_Exploitation]] · [[Strategies/Structural_Hedging]].

**Round 5**: 2-layer trader. **Layer 1 directional**: 13 fixed ±10 positions on multi-day-drift products (build at first tick, hold all day). **Layer 2 MM**: per-product LIMIT (default 10, TIER3=5, BLACKLIST=0), 2-level quoting (inner+outer), inventory skew, HEDGED_NO_SKEW for SNACKPACK CHOC/VAN. [[Strategies/Directional_Holding]] · [[Strategies/TIER3_Market_Making]] · [[Strategies/HEDGED_NO_SKEW]] · [[Strategies/Cross_Version_Blacklist]].

## Verified Real-Prosperity PnL (R5 cross-version)

From `round5/logs/{vN}/*.json` parsed JSON activitiesLog:

```text
v1=$19,995  v9=$37,284  v11=$36,113  v14=$33,901  v21=$23,270
v23=$52,620 v25=$52,440 v26=$54,120  v27=$61,450  v31=$53,473
v34=$62,299 v35=$53,360 v36=$78,799  v39=$38,258  v40=$52,788
v42=$72,000 (user-reported, log not in repo)
v37,v38,v41: not measured (backtester slots not burned)
```

v36 = backtester local-optimum (not submitted). **v42 = submitted final, $72K backtester (deliberately lower than v36 to avoid overfitting), realized R5 algo $57,911 full-day (the pre-result $163K estimate was 3× over).** R5 round total $153,125 (algo+manual). v34 = best estimated full-day among earlier versions.

The realized R5 contribution (153,126) lands close to the full-day estimate, but interpretation depends on the unobserved algo/manual split. If the Ashflow Alpha manual realized close to its theoretical $140,100, the algo contribution was modest (~$13K) — surprising given the backtester. If the manual underperformed, the algo carried most of the round (~$140K, near the full-day estimate). Without a Prosperity-side itemization we cannot disambiguate. See [[User_Reported_Anchors]] for the full discussion.

## The Three Round-5 Insights (load-bearing across the wiki)

1. **Backtester ≠ competition** ([[Concepts/Backtester_vs_Competition]]). Prosperity backtester runs first 10% of day 4; competition scores full day. Different optimal strategies.
2. **Adverse selection scales with volume** ([[Concepts/Adverse_Selection]]). MM losses on tight-spread products scale linearly with LIMIT. Blacklist (LIMIT=0) > TIER3 (LIMIT=5) > default (LIMIT=10) for products where bracket `s̄ + α < 0`.
3. **Lead-lag null result** ([[Concepts/Lead_Lag]]). 0/36,750 CCF tests survive Bonferroni at α = 1.36×10⁻⁶. No tradable lead-lag in R5.

## Carry-forward Lessons (what I'd do from day 1 in Prosperity 5)

See [[Carry_Forward]] for the full list. Top 5:

1. **Pre-register OOS day** as a top-level constant before any analysis runs. Phase 13's MICROCHIP_SQUARE flip is the canonical example of why this matters.
2. **Never trust local backtester for tier decisions** — only real-engine logs. The local-BT 8.6× fill inflation broke v35.
3. **Distinguish backtester window from scoring window**. If unsure, optimize for the **longer** window.
4. **HAC standard errors** for tick-data regressions. Naive OLS is biased downward (overstates significance).
5. **For tightly anti-correlated pairs (|ρ| > 0.85)**, MM with HEDGED_NO_SKEW > 2× directional positions.

## Links

[[Competition/Game_Mechanics]] · [[Competition/Round_Schedule]] · [[Backtests/PnL_Timeline]] · [[Concepts/Glossary]] · [[Cross_Round_Comparison]] · [[Carry_Forward]] · [[Research/Decisions_Log]] · [[Strategies/Round5_Version_History]]

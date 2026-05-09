---
type: competition
tags: [schedule, rounds, products]
sources: [context/Round Schedule.txt, context/Round 0/Position Limits & More Context.txt, context/Round 1/Round 1 - "Trading groundwork".txt, context/Round 2/# Round 2 - "Growing Your Outpost".txt, context/Round 3/# Round 3 - "Gloves Off".txt, context/Round 4/# Round 4 - "The More The Merrier".txt]
updated: 2026-04-27
---

# Round Schedule

## Overview

IMC Prosperity 4 runs 16 simulation days split across 5 rounds (+ tutorial).

| Round | Nickname | Duration | Status | Products |
|-------|----------|----------|--------|---------|
| Round 0 | Tutorial | — | Complete | EMERALDS, TOMATOES |
| Round 1 | "Trading Groundwork" | 72h | Complete | + RAINFOREST_RESIN, KELP, SQUID_INK |
| Round 2 | "Growing Your Outpost" | 72h | Complete | + new products (MAF/manual focus) |
| Round 3 | "Gloves Off" | 48h | **Active** | + HYDROGEL_PACK, VELVETFRUIT_EXTRACT, VEV_* options |
| Round 4 | "The More The Merrier" | 48h | Upcoming | TBD |
| Round 5 | — | 48h | Upcoming | TBD |

## Round 0 — Tutorial

- **Products:** EMERALDS (very stable, pure MM), TOMATOES (more volatile)
- **Goal:** Learn the submission system, get familiar with order book mechanics
- **Manual trading:** Inactive during tutorial
- **EDA performed:** Price overview, ACF/PACF, order book depth, trade flow, Hurst exponent (plots in `plots/round0/`)

## Round 1 — "Trading Groundwork"

- **New products:** RAINFOREST_RESIN, KELP, SQUID_INK
- **Result:** ~263K XIREC
- **Key insight:** RAINFOREST_RESIN is extremely stable (FV ≈ 10,000) — pure symmetric MM dominates. SQUID_INK is too volatile for naive quoting.
- See [[Rounds/Round1_findings]]

## Round 2 — "Growing Your Outpost"

- **Algo:** Continued MM on Round 1 products
- **Manual Part 1:** MAF bid framework (auction-style bidding)
- **Manual Part 2:** Invest & Expand — optimal allocation (15, 50, 35) found via EV calculation
- See [[Rounds/Round2_findings]]

## Round 3 — "Gloves Off"

- **New products:** HYDROGEL_PACK (delta-1 mean-reversion), VELVETFRUIT_EXTRACT (options underlying), VEV_* vouchers (vanilla call options)
- **Options TTE:** 7 Solvenarian days from day 0, declining to 5 by day 2 (TTE=[7.0, 6.0, 5.0])
- **Key challenge:** Black-Scholes pricing without scipy; flow asymmetry on OTM options (94–98% bid-hit)
- **Submission status:** Ready — `vault/round3_final_trader.py` (39,394 bytes)
- See [[Rounds/Round3_findings]]

## Round 4 — "The More The Merrier"

- **Status:** Upcoming
- **Data available:** `data/round4/` (prices + trades for days 1–3)
- See [[Rounds/Round4_Preview]]

## Key Deadlines

- Submit before round timer expires — last successful upload is locked in
- Can upload as many times as you want; only the active algorithm is used
- Results from previous rounds remain visible in dashboard after they close

## Links

[[Competition/Game_Mechanics]] · [[Overview]] · [[Rounds/Round1_findings]] · [[Rounds/Round3_findings]]

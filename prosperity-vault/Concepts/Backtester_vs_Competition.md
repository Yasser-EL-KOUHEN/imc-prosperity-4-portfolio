---
type: concept
tags: [round5, backtester, scoring-window, drift, optimal-strategy, conflict-products, post-result]
sources:
  - round5/research/drift_audit.py
  - round5/research/full_day_optimal.py
  - round5/plots/drift_audit.csv
  - round5/plots/full_day_optimal.csv
  - round5/strategies/round5_v36_trader.py
  - round5/strategies/round5_v37_trader.py
  - round5/strategies/round5_v40_trader.py
  - performance/algorithmic trading/round 5/581865.json
updated: 2026-05-08
---

# Backtester vs Competition Scoring (the central R5 lesson)

## Realized Result (2026-05-08)

| Metric | Value |
|---|---|
| v42 backtester (first 10% of Day 4) | **$72,000** |
| v42 realized full-day (Day 5 competition) | **$57,911** |
| **Ratio (full-day / backtester)** | **0.804** |

**The full-day was *less* than the backtester window.** The pre-result framing assumed the full-day-to-backtester multiplier would be > 1 (estimated ~$163K full-day from `full_day_optimal.csv`). The realized 0.80 ratio is a 30% live-vs-test gap.

### Reconciliation with the 8.6× inflation thesis

The thesis said: backtester runs 10% of day with 8.6× over-fill, so net multiplier vs full-day equivalent ≈ 0.10 × 8.6 = **0.86**. Predicted full-day from $72K backtester = $72K / 0.86 = **$83.7K**. Realized $57,911 = **0.69 of prediction**.

The 0.86 cancellation thesis is roughly correct but slightly off. The realized 0.80 ratio implies the effective inflation was **~12.5×** rather than 8.6× (since 0.10 × 12.5 = 1.25, and 1/1.25 = 0.80). Or equivalently: Day 5 had different drift patterns than the historical Days 2/3/4, and several v42 directional bets failed on Day 5 specifically:
- PANEL_2X4 +10: realized −$3,822 (Day 5 drifted negative; full-day-positive signal in training data was wrong for Day 5)
- BLACK_HOLES +10: realized −$4,914 (same — v36's call to drop would have been correct)
- PEBBLES_S −10: realized −$24,852 (single biggest directional loss; basket reversal)

**v36's verdict on Day 5 specifically:** v36 had blacklisted PANEL_2X4 and BLACK_HOLES. On the realized Day 5, both drifted in v36's predicted direction. **v36 would have been correct** on these two products. The $6,799 backtester gap that v42 paid for "robustness" did not pay off on Day 5. Rank-against-field still favored v42 (algo round-rank #287, the strongest of all 5 rounds), so the *relative* call was right; the *absolute* bet on those two products was wrong.

### Per-product realized vs full_day_optimal.csv prediction

| Product | full_day_optimal (predicted) | Realized | Verdict |
|---|---|---|---|
| GALAXY_SOUNDS_BLACK_HOLES +10 | +$13,155 expected | −$4,914 | Day 5 reversed the full-window pattern |
| PANEL_2X4 +10 | +$8,895 expected | −$3,822 | same |
| PEBBLES_M −10 | (small) | +$35,275 | unexpected basket asymmetry helped |
| PEBBLES_S −10 | predicted neutral | −$24,852 | unexpected reversal |
| MICROCHIP_OVAL −10 | small expected | −$2,649 | mild reversal |

The training-window forecast (`full_day_optimal.csv`) and the Day 5 realization disagreed on **3 of the 13 directional positions** in load-bearing ways (BLACK_HOLES, PANEL_2X4, PEBBLES_S). The other 10 mostly behaved in line.

## What It Is

## What It Is

The Prosperity local backtester runs the **first 10% of Day 4** (~100K of 1M timestamps). The competition leaderboard scores on the **full day** (or whatever day IMC chose for live evaluation — confirmed to be the full day for R5).

These two evaluation regimes can produce **different optimal strategies**. The backtester optimum is not the competition optimum. The R5 chapter spent v34 → v42 untangling this.

**ML analogy:** This is **train/eval distribution mismatch** in disguise. Your model selection (v36 won the backtester) optimizes for the training distribution; deployment uses a different distribution (full day vs first-10%). Cross-validation on the wrong split gives wrong answers no matter how careful the methodology.

## How Big Is the Gap?

Per `round5/plots/full_day_optimal.csv`:

| Product | Day-2 PW | Day-3 PW | Day-4 PW | Day-2 FW | Day-3 FW | Day-4 FW | Conflict? |
|---|---|---|---|---|---|---|---|
| GALAXY_SOUNDS_BLACK_HOLES | −85.5 | −53.5 | −65.0 | +1,446.5 | +688.5 | +1,320.5 | **YES** |
| PANEL_2X4 | +100 | +84 | −341 (mixed) | +738 | +738 | +894.5 | drift partial |
| SLEEP_POD_LAMB_WOOL | (small −) | (small −) | (small −) | +404 | +396 | +16 | drift partial |
| SNACKPACK_STRAWBERRY | small | small | small | +436 | +358 | +98 | full-day-only |

PW = Prosperity window (first 100K ts). FW = full window (all 1M ts).

GALAXY_SOUNDS_BLACK_HOLES is the **canonical conflict product**: the two windows literally **point in opposite directions** every day. Trusting the PW evidence (v37) flipped the directional sign and lost $26K of full-day PnL.

## The v34 → v42 Cycle in This Frame

| Version | Optimized for... | Backtester ($) | Full-day estimate ($) |
|---|---|---|---|
| v34 | (default — both windows in tension) | 62,299 | **152,730** ⭐ |
| v36 | Prosperity window | **78,799** ⭐ | 130,680 |
| v37 | Prosperity window (BH flip) | ~79,000 | 117,425 (−$26K!) |
| v38 | Both-window-consistent only | 38,258 | (defensive) |
| v39 | Full-day window | 38,258 | (high-variance) |
| v40 | (full-day extrapolation, TIER3 wrong) | 52,788 | ~140,000 |
| v41 | v34 + minimal full-day add | ~62,000 | ~153,500 |
| **v42** | **anti-overfitting compromise (SUBMITTED)** | **72,000** | **~163,000** ⭐ |

⭐ marks the metric-specific winner. v36 is the **backtester champion**. v34/v42 are the **competition champions**.

## v42 is Deliberately Not the Backtester Champion

The **explicit design rationale** for v42 was to avoid overfitting the Prosperity backtester window. v42 measured $72,000 — **$6,799 lower than v36's $78,799**. This gap was accepted because:

1. **What v36 sacrificed for the higher backtester score**: PANEL_2X4 +$8,895 full-day directional gain (blacklisted in v36 because PW first-10%-of-day shows −$3,452) and BLACK_HOLES +$13,155 full-day directional gain (also dropped from v36's directional). v36's blacklist over-fit to the first-10% evidence.
2. **What v42 paid for**: keeping PANEL_2X4 and BLACK_HOLES directional (full-day positive drift) while still blacklisting the 8 confirmed cross-version losers. Combines v34's full-day-correct directional setup with v36's aggressive blacklist methodology.
3. **The cost of robustness**: $6,799 of backtester PnL. The expected full-day return on that robustness: $33K+ (the recovered PANEL_2X4 + BLACK_HOLES contributions).

This is the operationalization of the central R5 principle: **the backtester is a regression-detection tool, not an optimization target.** Use it to confirm a new version doesn't regress in the dev window. Don't use it to select among versions when full-day evidence disagrees.

**ML analogy**: v42 is the **regularization-aware best model** while v36 is the **dev-set local optimum**. In any ML pipeline where the dev set is a biased prefix of the test set, the right choice is not "max dev metric" — it's "max dev metric subject to robustness checks." The robustness check here was `drift_audit.csv` showing PW ≠ FW for PANEL_2X4 and BLACK_HOLES.

## Why the Difference Exists

The Prosperity backtester samples **only the first 10%** because that's the window IMC's grader uses for the dev-time iteration loop. But:

1. **Drifts can change sign within a day** (BH starts negative, recovers strongly)
2. **MM losses scale with trading time** (10× more ticks = 10× more adverse selection bleeding)
3. **Spread-cross costs are one-time** for directional bets, but cumulative for MM

A directional bet that loses $X in the first 10% can recover to +$10X by end of day if drift is monotone. An MM strategy that loses $Y in the first 10% will typically lose ~$10Y on the full day (linear in trading time). These two scaling laws **break the rank order** between strategies.

## How to Detect Conflict Products

`round5/research/drift_audit.py` produces `drift_audit.csv` with these columns:

```text
product, pw_d2, pw_d3, pw_d4, pw_total, pw_sign_consistent,
         fw_d2, fw_d3, fw_d4, fw_total, fw_sign_consistent,
         conflict
```

`conflict = True` when `pw_sign_consistent != 0 AND fw_sign_consistent != 0 AND pw_sign_consistent != fw_sign_consistent`. In R5, the only product flagged conflict=True is **GALAXY_SOUNDS_BLACK_HOLES**. Everything else either has consistent windows (the easy case) or has mixed signs in at least one window (use the full-day signal).

## Decision Rule (v42's choice)

For each product, when picking the directional sign:

```text
if both windows sign-consistent AND agree         → use that sign with HIGH confidence
if both windows sign-consistent AND disagree      → use FULL-DAY (the longer window wins)
if one window mixed, the other sign-consistent    → use the sign-consistent one (usually FW)
if both windows mixed                             → don't trade directional; use MM
```

For blacklist decisions: the cross-version Prosperity log evidence is N=12 ; **but** for products in the conflict set, blacklist judgments need full-day evidence too. v42 specifically does NOT blacklist PANEL_2X4 or BLACK_HOLES even though they have negative cross-version Prosperity averages — because their **full-day** drift is positive.

## Pre-Registration Discipline

To avoid P-hacking the OOS day after seeing results:
- `OOS_DAY = 4` is a top-level constant in `eda2.py`, committed before any analysis ran
- The drift_audit.py does **not** "search" for the right window — both PW and FW are output side-by-side, and the rule for picking is documented above

This is the textbook anti-leakage move from ML. **Pre-register your evaluation, then commit.**

## ML Analogy

Backtester-vs-competition is **train-time vs deployment-time distribution shift** with the same underlying data. The features (mid prices, order books) are identical; only the **observation window** differs. Models that look great on a 10% prefix can be catastrophically wrong on the full sequence — exactly how a regression that fits the first 10 epochs of a learning curve can predict a flat plateau when the actual curve has a phase transition at epoch 20.

The defensive move is **window-robust selection**: pick strategies that win on **both** windows, even if neither is the per-window champion. v42 isn't the backtester champion (v36) and isn't the pure-full-day champion (v39 which dropped PEBBLES_XL) — it's the version that **avoids the catastrophes on either side**.

## Links

[[Rounds/Round5_findings]] · [[Strategies/Round5_Version_History]] · [[Strategies/Cross_Version_Blacklist]] · [[Strategies/Directional_Holding]] · [[Backtests/Phase13_R5_Directional]] · [[Concepts/Adverse_Selection]] · [[Research/Round5_Scripts]]

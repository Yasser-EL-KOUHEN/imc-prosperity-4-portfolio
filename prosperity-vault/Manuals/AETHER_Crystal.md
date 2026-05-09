---
type: manual
tags: [round4, manual, exotic-options, aether-crystal, chooser, binary, knockout, common-knowledge]
sources:
  - report/report.tex (§Round 4 Manual)
  - context/Round 4/
  - performance/manual trading/round 4/Manual Trading Results.txt
  - performance/manual trading/round 4/Distribution Exotic Products Positions Competitors/
updated: 2026-05-08
---

# Round 4 Manual — AETHER_CRYSTAL Exotic Options Portfolio

**Submitted:** 12-instrument portfolio · **E[PnL]:** +175,200 (BS-priced) · **Realized: +57,516.23 (rank #316)** · **Method:** Black-Scholes + structural-edge identification on chooser, binary, KO

> **Verified result (Prosperity result page, 2026-05-08):** **+57,516.23 realized**. End-of-R4 cumulative manual rank **#316**. Realization ratio: 57,516 / 175,200 = **0.328** — the worst single-manual realization in the GOAT phase.

## The Mechanic

A one-shot exotic-options manual on the underlying AETHER_CRYSTAL (AC). 12 instruments to choose from at fixed prices; we choose volume and direction (BUY/SELL) on each. Settled at expiry against the realized AC mid path; no unwinding before settlement.

Instruments include:
- **Vanilla puts/calls** at strikes 35, 40, 45, 50, 60 (one or two-week tenors)
- **Chooser** at strike 50 (decide call-or-put at decision time)
- **Binary put** at strike 40 (pays fixed amount if AC < 40 at expiry, else 0)
- **Knockout put** at strike 45 (pays like vanilla put if barrier never crossed; else 0)

## Submission and Realized Per-Instrument PnL

| Instrument | Side | Vol | Per-unit P&L | Total P&L |
|---|---|---|---|---|
| AC (underlying) | BUY | 0 | +183.21 | 0 |
| AC_50_P (put 50) | BUY | 50 | +370.10 | **+18,505.03** |
| AC_50_C (call 50) | BUY | 50 | +628.31 | **+31,415.57** |
| AC_35_P (put 35) | BUY | 50 | +184.87 | +9,243.40 |
| AC_40_P (put 40) | SELL | 50 | −495.09 | **−24,754.41** |
| AC_45_P (put 45) | BUY | 50 | +405.61 | +20,280.48 |
| AC_60_C (call 60) | BUY | 0 | −564.80 | 0 |
| AC_50_P_2 (2w put 50) | BUY | 50 | −282.40 | −14,119.75 |
| AC_50_C_2 (2w call 50) | BUY | 50 | −468.84 | −23,442.21 |
| **AC_50_CO (chooser 50)** | SELL | 50 | +1,087.08 | **+54,354.22** |
| AC_40_BP (binary put 40) | SELL | 50 | +300.00 | +15,000.00 |
| AC_45_KO (knockout 45) | BUY | 500 | −57.93 | **−28,966.10** |
| **TOTAL** | | | | **+57,516.23** |

## R4 was a common-knowledge manual

Critical finding from the per-instrument peer-position distributions (`performance/manual trading/round 4/Distribution Exotic Products Positions Competitors/`): **we aligned with peer consensus on every single one of the 12 instruments. Not one contrarian trade.**

| Instrument | Our position | Peer dominant cluster (n teams) |
|---|---|---|
| AC | 0 | 0 (~1,600) |
| AC_50_P | +50 | +50 long (~1,400) |
| AC_50_C | +50 | +50 long (~1,000) |
| AC_35_P | +50 | +50 long (~1,600) |
| AC_40_P | −50 | −50 short (~1,800) |
| AC_45_P | +50 | +50 long (~1,600) |
| AC_60_C | 0 | 0 (~1,400) |
| AC_50_P_2 | +50 | +50 long (~2,200) — extreme consensus |
| AC_50_C_2 | +50 | +50 long (~1,800) |
| AC_50_CO | −50 | −50 short (~2,000) — extreme consensus |
| AC_40_BP | −50 | −50 short (~2,000) — extreme consensus |
| AC_45_KO | +500 | +500 long (~1,600) — extreme consensus |

**The 33% realization vs E[+175,200] is a field-level outcome, not us-specific.** Roughly 1,600–2,200 teams made each of the same trades. Our +57,516 is approximately what *every BS-pricing solver* realized.

This makes R4 the **third common-knowledge manual** in Prosperity 4, joining:
- R1 (deterministic clearing-price)
- R3 (symmetric Bayesian-Nash)
- **R4 (BS-pricing consensus)**

The two non-common-knowledge manuals — R2 (peer-prior I&E, realization 1.39×) and R5 (archetype taxonomy, realization 0.68×) — both rewarded asymmetric analysis.

## Implied AC mid path: V-shaped / volatile

Combining the realized payoffs:
- **AC_50_C won** AND **AC_50_P won** ⇒ AC traded both above and below 50 along the path (otherwise one would have expired worthless)
- **AC_45_P won** ⇒ AC dipped below 45 at some point
- **AC_40_P sold lost** ⇒ AC at expiry was below 40 (not just intraday)
- **AC_45_KO bought lost** ⇒ knockout barrier was breached (AC dropped below 45 — confirming the dip)
- **AC_40_BP sold won** ⇒ AC closed *above* 40 at expiry

**Synthesis:** AC dipped sharply below 45 (knocking out the KO and putting the 40_P-seller in the money), then **rebounded above 40 by expiry**. The path was V-shaped or U-shaped, not monotone. The vanilla puts (35, 45, 50) all paid because the path crossed through their strikes; the seller of 40_P paid because the path crossed *and* closed below 40 (or close to it).

## Why this lost 67% of E[PnL]

The Black-Scholes E[PnL] of +175,200 assumed:
- Greek-symmetric pricing of vanillas (we'd capture the structural mispricing)
- Knockout barrier with single-leg expectation
- Chooser pricing for symmetric vol

The realized path violated all three:
- **Path-dependent KO triggered**: the +500 vol KO position lost $28,966 because the barrier was breached (a high-probability event under realized vol, not the BS-default-vol assumed)
- **2w vanillas decayed OTM**: AC_50_P_2 and AC_50_C_2 (2-week tenors) lost $37,562 combined because the path didn't move enough by week-2 expiry
- **Chooser sold won big**: this leg paid +$54,354 because the chooser was overpriced — a structural edge we identified, but ~2,000 other teams identified it too

**Net:** the structural edges (chooser sold, binary sold, vanilla 50C/50P bought) paid out at roughly BS-EV. The path-dependent legs (KO, 2w vanillas, sold 40P) lost enough to bring the round to 33% realization. The diagnosis is **path-dependent BS pricing failure under V-shaped underlying**, not "Greek-asymmetry under unidirectional drift" as initially diagnosed.

## ML analogy

The portfolio is analogous to an **ensemble model where most base models share the same systematic bias**. Each of the 12 instruments is BS-priced as if the underlying followed a Brownian path. Under the realized V-shape, several base models (KO, 2w vanillas) all under-perform together because their pricing assumptions co-vary with the same realized-path feature (path crossing 45 or 40). The ensemble does *not* diversify when the base models share a hidden dependency — same as ensembling regressors that all use the same feature and miss the same regime change.

## Lessons (carry-forward)

1. **In a common-knowledge manual, your realized PnL is bounded by the field's collective error.** The competitive game is at the margin where reasonable people disagree (e.g., AC_50_C had ~310 contrarian shorts), not at the level of "is this BS-priced fair".
2. **Stress-path the portfolio under V-shape and U-shape underlying scenarios**, not just terminal-distribution moments. KO and 2w-vanilla legs are particularly path-sensitive.
3. **Reduce position size on path-dependent legs.** The +500 vol on AC_45_KO was 10× the size of any other leg; even at the consensus position, it dominated the loss.
4. **For exotic option manuals: identify which legs are *common knowledge* (consensus = no edge) vs which are *contested* (rank lift available).** Allocate more to contested legs.

## Links

[[Rounds/Round4_findings]] · [[Performance/Manual_Per_Round]] · [[Manuals/Bio_Pods]] · [[Concepts/Black_Scholes]] · [[Concepts/Chooser_Option]] · [[Concepts/Binary_Option]] · [[Concepts/Knockout_Option]] · [[Products/AETHER_CRYSTAL]] · [[Carry_Forward]]

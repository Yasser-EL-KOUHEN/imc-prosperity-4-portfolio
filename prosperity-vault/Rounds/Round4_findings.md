---
type: round
tags: [round4, complete, counterparty, aether-crystal, exotic-options]
sources: [.planning/phases/12-counterparty-exploitation/, vault/round4_trader.py, report/report.tex §Round 4, log.md 2026-04-28 entries]
updated: 2026-05-06
---

# Round 4 — "The More The Merrier"

## Status

**Complete** — algo submitted; manual portfolio submitted

- `vault/round4_trader.py` — 1,008 lines — anti-regression gate **153,566 PASS**, 4 fixes applied (Phase 12)
- Manual portfolio designed and risk-structured; expected **+175,200 XIRECs** (+58.4 pre-mul × 3000)

## Realized Result (2026-05-08)

**R4 GOAT contribution: 114,564** — end-of-R4 cumulative GOAT 230,601, rank **#592** (improved from #802).

| Component | Realized PnL |
|---|---|
| R4 algo (HYDROGEL + VEL + Mark-counterparty signals) | **+57,048** |
| R4 manual (AETHER_CRYSTAL 12-instrument exotic portfolio) | **+57,516** |
| R4 round total | 114,564 |

**End-of-R4 cumulative ranks:** Overall #592 · Algo #809 · Manual #406 · Country #21.

R4 algo at +57,048 is solid — over-performed the ~$48K/day baseline. The Mark-counterparty signals (composite flow tilt + Mark 49 cooldown) and the 4 Phase-12 fixes likely contributed; the live-only signals were neutral on backtest but appear to have added value on the real engine.

**R4 manual at +57,516 vs E[+175,200] = 32.8% realization — the worst miss in the GOAT phase.** Diagnosis refined after viewing all 12 peer-distribution images (`performance/manual trading/round 4/`):

**R4 was a common-knowledge manual.** We aligned with peer consensus on every single one of the 12 instruments — not one contrarian trade. Roughly 1,600–2,200 teams made each of the same trades. Our +57,516 is approximately what *every BS-pricing solver* realized. **The 33% realization is a field-level outcome, not us-specific.** Manual rank #316 (mid-pack of ~6,000 attempters) confirms.

This makes R4 the **third common-knowledge manual** in Prosperity 4, alongside R1 (deterministic clearing-price) and R3 (symmetric Bayesian-Nash). The two non-common-knowledge manuals — R2 (peer-prior I&E) and R5 (archetype taxonomy) — both rewarded asymmetric analysis and outperformed common-knowledge manuals on realization-vs-effort.

**Implied AC path: V-shaped / volatile.** Both AC_50_C and AC_50_P paid off (AC traded both above and below 50). AC_45_P paid off (AC dipped below 45). AC_45_KO bought lost (knockout barrier breached). AC_40_P sold lost (closed below 40). AC_40_BP sold won (closed above 40). The picture: AC dipped below 45 (knocking out the KO and putting the 40_P seller in the money), then rebounded above 40 by expiry. **Path-dependent BS pricing failure under V-shape**, not "Greek-asymmetry under unidirectional drift" as initially diagnosed.

**Lesson, sharpened:** in a common-knowledge manual, your realized PnL is bounded by the field's collective error. The competitive game is at the margin where reasonable people disagree (e.g., AC_50_C had ~310 contrarian shorts), not at "is this BS-priced fair". For path-dependent legs (KO, 2w vanillas), reduce position size or hedge — the +500 vol on AC_45_KO was 10× the size of any other leg and dominated the loss. See [[Manuals/AETHER_Crystal]] and [[Performance/Manual_Per_Round]].

---

## Round Context

**Theme:** Great Orbital Ascension Trials (GOAT) round 2. Round 3 PnL persists into the GOAT cumulative.

**Two parallel challenges:**
1. **Algorithmic — "Hello, I'm Mark"**: Same products as Round 3 (HYDROGEL, VELVETFRUIT_EXTRACT, 10 VEV vouchers) but with **counterparty IDs disclosed** in `Trade.buyer` / `Trade.seller` fields.
2. **Manual — "Vanilla Just Isn't Exotic Enough"**: One-shot trade in AETHER_CRYSTAL underlying + 11 vanilla and exotic option contracts. Hold to expiry, no unwinding.

**TTE schedule for Round 4 (1-indexed):** Day 1 → 7d, Day 2 → 6d, Day 3 → 5d. Fixed in Phase 12 via `DAY_TTE: Dict[int, float] = {1: 7.0, 2: 6.0, 3: 5.0}`.

---

## Algorithmic Challenge — Counterparty Exploitation (Phase 12)

### Mark Counterparty Taxonomy (4,281 trades over 3 days)

| Mark | Role | Net VEL | Behaviour |
|------|------|---------|-----------|
| Mark 67 | **Dip buyer** (+bullish) | +1,510 | NEVER sells. Buys at ask₁ at local lows. 92.7% buys at below-5-MA. |
| Mark 49 | **Local-high seller** (-bearish) | −956 | Posts asks, waits to be hit. ~36 events/day. |
| Mark 22 | OTM call short-seller + VEL taker | −551 VEL | Systematically shorts OTM calls (VEV_5300–6500) to Mark 01; also hits VEL bids (~184 events/day total); excluded from mark_net (frequency mismatch) |
| Mark 01 | OTM call buyer + VEL maker | — | Buys VEV_5300/5400/5500/6000/6500 from Mark 22 |
| Mark 14 | Primary HYD market maker | −44 HYD | 100% bilateral with Mark 38 |
| Mark 38 | HYD MM (mirror of 14) | +34 HYD | Alternates maker/taker with Mark 14 |
| Mark 55 | Symmetric VEL taker | −43 | Likely arbitrageur |

### Three Implemented Signals

1. **Composite flow score (`mark_net`)**: +1 per Mark 67 buy tick, −1 per Mark 49 sell tick. Tilt VEL passive bid by +3 when `mark_net ≥ 5` (bullish), trim by 2 when `mark_net ≤ −3` (bearish).
2. **Signal C (Mark 49 local-high cooldown)**: When Mark 49 detected in `state.market_trades` OR `state.own_trades`, halve VEL bid size for next 500ms (5 ticks). Cooldown anchored on `state.timestamp` (not stale `trade.timestamp`).
3. **DAY_TTE alignment**: Round 4 day numbering is 1-indexed; legacy 0-indexed list replaced with explicit dict.

### Bugs Found and Fixed (4)

| # | Bug | Fix | Gate |
|---|-----|-----|------|
| 1 | Change A (sell VEV_6000/6500 at bid=0) caused −900 local regression | Reverted; net EV = 0 anyway (sell at 0, expire worthless) | 153,566 |
| 2 | `mark49_last_ts` used `trade.timestamp` (prior tick CSV) instead of `state.timestamp` | Removed from scan; set in `Trader.run()` at detection | unchanged |
| 3 | `scan_counterparty_flow()` ran before day-start reset; stale prior-day trades contaminated mark_net | Moved scan into `else` branch (non-day-start only) | unchanged |
| 4 | Scanned only `state.market_trades`; missed direct fills with us | Iterate `(market_trades, own_trades)` both | unchanged (live-server impact) |

See: [[Strategies/Counterparty_Exploitation]] · [[Backtests/Phase12_Counterparty]]

---

## Manual Challenge — Vanilla Just Isn't Exotic Enough

**Underlying:** AETHER_CRYSTAL · GBM with σ=2.51, r=0, 4 steps/day, 252 days/yr · contract size ×3000 multiplier

### BS Fair Values vs Market

| Product | BS fair | Bid | Ask | Edge |
|---|---|---|---|---|
| AC_50_C / AC_50_P (3w) | 12.03 | 12.00 | 12.05 | ~0 |
| **AC_50_C_2 / AC_50_P_2 (2w)** | **9.87** | 9.70 | 9.75 | **+0.12 buy** |
| AC_50_CO (chooser, K=50) | **21.90** | 22.20 | 22.30 | **+0.30 sell** |
| AC_40_BP (binary put, payout 10) | **4.768** | 5.00 | 5.10 | **+0.232 sell** |
| AC_45_KO (KO put, B=35) | **0.22** | 0.15 | 0.175 | **+0.045 buy** |

### Final Risk-Structured Portfolio (12 instruments)

| # | Instrument | Side | Vol | Edge (pre-mul) |
|---|---|---|---|---|
| 1 | AETHER | — | 0 | 0 |
| 2 | AC_50_P | BUY | 50 | −1.0 |
| 3 | AC_50_C | BUY | 50 | −1.0 |
| 4 | AC_35_P | BUY | 50 | +0.25 |
| 5 | AC_40_P | SELL | 50 | −0.30 |
| 6 | AC_45_P | BUY | 50 | −0.75 |
| 7 | AC_60_C | — | 0 | 0 |
| 8 | AC_50_P_2 | BUY | 50 | +6.05 |
| 9 | AC_50_C_2 | BUY | 50 | +6.05 |
| 10 | AC_50_CO | SELL | 50 | +15.0 |
| 11 | AC_40_BP | SELL | 50 | +11.6 |
| 12 | AC_45_KO | BUY | 500 | +22.5 |
| | **Total** | | | **+58.4 → +175,200 XIRECs** |

### Three Structural Edges Captured

1. **Chooser arbitrage** (Sell CO + Buy C(21d) + Buy P(14d)): static replication for r=0 GBM. Edge +0.40/unit. See [[Concepts/Chooser_Option]].
2. **Binary cliff elimination** (Sell BP + Buy P50 + Sell P40): bull put spread bounds max loss from −5 to −0.55 per pair. See [[Strategies/Structural_Hedging]].
3. **2w ATM mispricing**: Both call and put underpriced by +0.12. Captured via direct buy + chooser hedge leg.

### What I Skipped and Why

- **AETHER underlying**: −0.025 edge either side, portfolio delta already balanced
- **AC_60_C**: +0.004 sell edge, but naked short OTM call has unbounded upside risk at σ=2.51 — advisor principle "don't let position control you" applies

---

## Cumulative PnL

| Phase | Source | PnL Δ |
|-------|--------|-------|
| Round 3 baseline | All 11 phases | 153,566 |
| Phase 12 (counterparty) | Live-only signals; backtest neutral | +0 local, ? live |
| Manual portfolio | E[+175,200] across 100 sims | E[+175,200] |

---

## Links

[[Rounds/Round3_findings]] · [[Strategies/Counterparty_Exploitation]] · [[Strategies/Structural_Hedging]] · [[Backtests/Phase12_Counterparty]] · [[Products/AETHER_CRYSTAL]] · [[Concepts/Chooser_Option]] · [[Concepts/Binary_Option]] · [[Concepts/Knockout_Option]] · [[Marks/Mark_67]] · [[Marks/Mark_49]] · [[Marks/Mark_22]] · [[Marks/Mark_01]] · [[Marks/Mark_14]] · [[Marks/Mark_38]] · [[Marks/Mark_55]]

---
type: round
tags: [round3, complete, hydrogel, options, black-scholes, baseline-153566]
sources:
  - round3/README.md
  - round3/trader.py
  - round3/trader_final.py
  - round3/research/
  - round3/backtests/
  - context/Round 3/# Round 3 - Gloves Off.txt
  - report/report.tex (§Bio-Pod, §Phase10Addendum2)
  - .planning/phases/{03..11}/SUMMARY.md
updated: 2026-05-01
---

# Round 3 — "Gloves Off"

## Status

**Complete.** Submitted: `round3/trader_final.py` (39,394 bytes). Local 3-day baseline: **153,566 XIREC**. Real-engine PnL ≈ local × 0.93 per Phase 1 calibration ([[Backtests/Phase1_Backtest_Calibration]]).

## Realized Result (2026-05-08)

**R3 GOAT contribution: 116,038** — first GOAT entry, end-of-R3 cumulative rank **#802**.

> **Trader-version timeline (clarified 2026-05-08):**
> - **R3 submission: `performance/.../486282.py`** (880 lines) — generated the $40,800 algo PnL with pre-Phase-4 params (small_rho=0.12, large_rho=0.48, TTE=5.0)
> - `round3/trader.py` (991 lines) — pre-submission research version with extra scaffolding
> - `round3/trader_final.py` (940 lines) — **40% improved post-R3 refinement** (Phase 4 ρ sweep + Phase 10 TTE recal applied: small_rho=0.08, large_rho=0.42, TTE=7.0). Used as the **R4 basis**, not submitted to R3.
>
> Phase 4 / Phase 10 / Phase 11 outputs describe the post-R3 refinement that informed R4, not what was submitted to R3. See [[Performance/Submission_Verification]].
>
> **Submitted Bio-Pods bids: (760, 855)**, NOT (755, 840) as initially derived. The user shaded both bids slightly upward from the symmetric NE.

| Component | Realized PnL |
|---|---|
| R3 algo (`486282.py`, "v3"-stripped) | **+40,800** |
| R3 manual (Bio-Pods (760, 855)) | **+75,238** |
| R3 round total | 116,038 |

**End-of-R3 cumulative ranks:** Overall #802 · Algo #830 · Manual **#234** *(≈ #1,200 without ties)* · Country #30.

R3 algo at +40,800 is the weakest of the 5 rounds. Local-3-day baseline was 153,566 (~$51K/day); realized 40,800 = ~80% of one-day-of-3 baseline. Likely causes: HYDROGEL real-engine fills lower than local; VEV options carried less per-tick alpha than estimated.

**R3 manual was a tie regime.** Displayed cumul rank #234, but without ties ≈ **#1,200**. Bio-Pods at the symmetric Bayesian-Nash equilibrium (b₁=755, b₂=840) is common-knowledge among solvers: many teams converged on the same NE bids and earned identical realized PnL. The display rank #234 is non-deterministic tie-breaking. The optimization still gave a real rank lift over non-solvers, but no edge among solvers.

Implied counterparty count: 75,238 / 81.67 ≈ 921 — unusually high. Either the per-counterparty EV was higher than 81.67 (favorable reserve draws) or our derivation undercounted the unit. The takeaway: Bio-Pods paid out at roughly 2× the EV per counterparty we modeled.

---

## Round Context

**Theme:** "Great Orbital Ascension Trials" (GOAT) — leaderboard resets to zero for all teams. Round 3 is the first GOAT round; all prior PnL is wiped.

**Products:** `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, 10 `VELVETFRUIT_EXTRACT_VOUCHER` options

**VEV Vouchers:** Labeled `VEV_4000` through `VEV_6500`. Cannot be exercised before expiry. Inventory does not carry over. Open positions liquidated at hidden fair value at round end.

**TTE Schedule:**

| Historical Day | TTE |
|----------------|-----|
| Day 0 (tutorial) | 8 days |
| Day 1 (Round 1) | 7 days |
| Day 2 (Round 2) | 6 days |
| **Round 3 start** | **5 days** |

---

## Position Limits

| Product | Limit |
|---------|-------|
| HYDROGEL_PACK | 200 |
| VELVETFRUIT_EXTRACT | 200 |
| Each VEV_XXXX | 300 |

---

## Manual Challenge — "The Celestial Gardeners' Guild"

**Setup:** Trade against counterparties with uniformly distributed reserve prices ∈ {670, 675, 680, …, 920} (51 levels at increments of 5). Fair sell price = **920**.

**Mechanic:** Submit two bids (b1, b2):
- If b1 > reserve price → trade at b1, profit = 920 − b1
- If b2 > reserve price AND b2 > avg(all teams' b2) → trade at b2, profit = 920 − b2
- If b2 > reserve price BUT b2 ≤ avg(b2) → trade at b2 with penalty:

$$\text{PnL} \times \left(\frac{920 - \overline{b_2}}{920 - b_2}\right)^3$$

### Bayesian-Nash Equilibrium Solution

At symmetric Nash equilibrium (all players bid identically, so avg(b2) = b2*), expected profit per counterparty reduces to:

$$f(b_1, b_2) = \frac{b_1 - 670}{255}(920 - b_1) + \frac{b_2 - b_1}{255}(920 - b_2)$$

FOC linear system: $2b_1 - b_2 = 670$, $-b_1 + 2b_2 = 920$

Continuous solution: $b_1^* = 753.\overline{3}$, $b_2^* = 836.\overline{6}$

**Discrete grid snap:** $(b_1^*, b_2^*) = \mathbf{(755, 840)}$, verified by exhaustive 51×51 search.

| Optimal property | Value |
|-----------------|-------|
| Per-counterparty EV | **81.67 XIRECs** |
| First-bid trades | 1/3 of counterparties (17 levels: 670–750) |
| Second-bid trades | 1/3 of counterparties (17 levels: 755–835) |
| No trade | 1/3 of counterparties (17 levels: 840–920, margin too thin) |
| Total EV (30–60 counterparties) | ~2,500–5,000 XIRECs |

**Stability:** All ±1 grid-step deviations underperform. Deviation b2 → 835 trips the cubic penalty (−4.43 pts). The equilibrium is a sharp diagonal maximum.

---

## Products

| Product | Type | Strategy |
|---------|------|---------|
| HYDROGEL_PACK | Delta-1 commodity, mean-reverting | AR(1) EMA market making |
| VELVETFRUIT_EXTRACT | Options underlying | Passive delta hedge only |
| VEV_4000 | Deep ITM call option | Passive MM (size=6) |
| VEV_5000 | ITM call | Bid-only quoting |
| VEV_5100 | Near-ITM call | Bid-only quoting |
| VEV_5200 | Near-ITM call | Bid-only quoting |
| VEV_5300 | Slightly ITM call | Two-sided passive |
| VEV_5400 | ATM call | Two-sided passive |
| VEV_5500 | OTM call | Two-sided passive |
| VEV_6000 | Far OTM call | Sell-only (infrastructure, 0 fills) |
| VEV_6500 | Far OTM call | Sell-only (infrastructure, 0 fills) |

---

## Round 3 Timeline

| Date | Event |
|------|-------|
| 2026-04-26 | Phase 1–2 complete (backtest engine + parameter sweep) |
| 2026-04-27 | Phase 3–9 complete (HYDROGEL signal, options, OBI, safety) |
| 2026-04-27 | Phase 10 complete — VEV_4000 added, TTE/σ recalibrated |
| 2026-04-27 | Phase 11 complete — box signal REJECTED (null result) |

---

## Phase Completion Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Backtest Engine | ✅ Complete |
| 2 | Parameter Sweep Infrastructure | ✅ Complete |
| 3 | HYDROGEL Signal Core | ✅ Complete |
| 4 | HYDROGEL Tuning | ✅ Complete |
| 5 | VELVETFRUIT Hedge Validation | ✅ Complete |
| 6 | Options Black-Scholes Engine | ✅ Complete |
| 7 | Options Quoting Logic | ✅ Complete |
| 8 | Options OBI Integration | ✅ Complete |
| 9 | Safety Hardening | ✅ Complete |
| 10 | Submission Pipeline | ✅ Complete |
| 11 | Box-and-Lines Signal | ✅ Complete (null result) |

---

## Final Backtest Performance

**Local backtest total: 153,566 XIREC** (overestimates official by ~16.6x)

| Product | d0 | d1 | d2 | 3d Total |
|---------|----|----|-----|---------|
| HYDROGEL_PACK | 50,942 | 43,735 | 36,963 | 131,640 |
| VELVETFRUIT_EXTRACT | 4,154 | 1,044 | 138 | 5,336 |
| VEV_4000 | 3,000 | 2,150 | −956 | 4,194 |
| VEV_5100 | 20 | 3,370 | 4,263 | 7,653 |
| VEV_5200 | 227 | 237 | 1,463 | 1,927 |
| VEV_5300 | 195 | 133 | 1,756 | 2,084 |
| Others | 140 | 419 | 973 | 1,532 |
| **TOTAL** | **58,678** | **51,088** | **43,800** | **153,566** |

---

## Key Research Findings

| Finding | Evidence | Implication |
|---------|----------|------------|
| HYDROGEL is mean-reverting | lag-1 ACF = −0.1292 | AR(1) MM is the right strategy |
| OBI for HYDROGEL is net-negative | Phase 3: −5,218 over 3d; v7 full: −14,487 | OBI disabled (β=0.0) |
| VEV hedger + OBI = disaster | v7 trial: −14,573 on VEV alone | Never use aggressive hedging |
| VEV 5000/5200 flow is 94-98% bid-hit | Microstructure EDA | Bid-only quoting on ITM strikes |
| IV smile: ATM has lowest vol | IV surface: σ=0.230 at strike 5400 | Per-strike sigma necessary |
| VEV_4000 passive MM is profitable | Phase 10: +6,887 | Deep ITM options earn reliably |
| Box signal is null for HYDROGEL | Phase 11: all 9 configs fail gate | Mean-reversion already exploits deviations |

---

## Submission Checklist

```
[OK] Syntax (source + vault):  ast.parse OK
[OK] Imports (source + vault): 0 violations
[OK] os removed from vault:    import os removed
[OK] Debug output:             0 bare print() calls
[OK] Smoke test:               day 0 PnL = 58,678
[OK] File size:                39,394 bytes (< 200,000)
STATUS: READY FOR SUBMISSION
```

---

## Links

[[Products/HYDROGEL_PACK]] · [[Products/VELVETFRUIT_EXTRACT]] · [[Products/Options/VEV_5300]] · [[Strategies/Mean_Reversion]] · [[Strategies/Options_Quoting]] · [[Backtests/PnL_Timeline]] · [[Backtests/Phase10_Submission]] · [[Research/Decisions_Log]] · [[Rounds/Round4_Preview]]

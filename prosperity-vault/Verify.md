---
type: reference
tags: [provenance, verification, numeric-claims, ground-truth, final-result]
sources:
  - prosperity-vault/CLAUDE.md
  - prosperity-vault/User_Reported_Anchors.md
  - Prosperity website final leaderboard (2026-05-08)
updated: 2026-05-08
---

# Verify — Provenance Table for Every Numeric Claim

## Final Competition Result (resolved 2026-05-08)

### Overall

| Claim | Value | Class | Source |
|---|---|---|---|
| Final overall rank | **#346 / 18,803** | USER | Prosperity website 2026-05-08 |
| Algorithmic rank (overall) | #537 | USER | Same |
| Manual rank (overall) | #204 | USER | Same |
| Country rank | #11 | USER | Same |
| Final GOAT XIREC | 383,727 | USER | Same |
| Field size | 30,703 / 18,803 / 1,549 univ / 117 countries | USER | Prosperity website |
| Total XIRECs (all teams) | 1,153,901,776 | USER | Same |
| Average XIREC per round (all teams) | 52,675 | USER | Same |

### Per-round algo PnL

| Claim | Value | Class | Source |
|---|---|---|---|
| R1 algo realized | +98,172 | USER | Prosperity per-round screenshot 2026-05-08 |
| R2 algo realized | +91,529 | USER | Same |
| R3 algo realized | +40,800 | USER | Same |
| R4 algo realized | +57,048 | USER | Same |
| R5 algo realized (v42) | +57,911 | USER | Same |
| Sum across all 5 rounds (algo) | 345,460 | DERIVED | sum |
| GOAT algo (R3+R4+R5) | 155,759 | DERIVED | 40,800 + 57,048 + 57,911 |

### Per-round manual PnL

| Claim | Value | Class | Source |
|---|---|---|---|
| R1 manual realized | +71,500 | USER | Same |
| R2 manual realized (I&E (18,60,22)) | +153,345 | USER | Same |
| R3 manual realized (Bio-Pods) | +75,238 | USER | Same |
| R4 manual realized (AC exotics) | +57,516 | USER | Same |
| R5 manual realized (Ashflow Alpha) | +95,214 | USER | Same |
| Sum across all 5 rounds (manual) | 452,813 | DERIVED | sum |
| GOAT manual (R3+R4+R5) | 227,968 | DERIVED | 75,238 + 57,516 + 95,214 |

### Cumulative leaderboard rankings at end of each round (CANONICAL)

| Round | Overall | Algorithmic | Manual | Country | Class | Source |
|---|---|---|---|---|---|---|
| R1 | ~#2,000 | ~#1,400 | #72 (no-ties ~#3,000) | #59 | USER | leaderboard 2026-05-08 |
| R2 | #1,522 | #857 | #801 | #59 | USER | Same |
| R3 | #802 | #830 | #234 (no-ties ~#1,200) | #30 | USER | Same |
| R4 | #592 | #809 | #406 | #21 | USER | Same |
| R5 | #346 | #537 | #204 | #11 | USER | Same |

### GOAT progression

| Claim | Value | Class | Source |
|---|---|---|---|
| End-of-R2 cumulative (qualifier) | 414,546 (#1,522) | USER | Same |
| End-of-R3 GOAT | 116,037 (#802) | USER | Same |
| End-of-R4 GOAT | 230,601 (#592) | USER | Same |
| End-of-R5 GOAT (FINAL) | 383,727 (#346) | USER | Same |
| R3 contribution | 116,038 (algo+manual) | DERIVED | 40,800 + 75,238 |
| R4 contribution | 114,564 | DERIVED | 57,048 + 57,516 |
| R5 contribution | 153,125 | DERIVED | 57,911 + 95,214 |
| Manual % of GOAT | 59.4% | DERIVED | 227,968 / 383,727 |

### Realization vs estimates

| Claim | Value | Class | Source |
|---|---|---|---|
| R1 manual: realized vs theoretical | 71,500 / 71,500 = 1.00 | DERIVED | exact |
| R2 manual: realized vs FOC theoretical | 153,345 / 110,065 = 1.39 | DERIVED | (18,60,22) over-performed FOC |
| R3 manual: implied counterparty count | 75,238 / 81.67 ≈ 921 | DERIVED | unusually high; suggests EV/CP > 81.67 |
| R4 manual: realized vs E[PnL] | 57,516 / 175,200 = 0.328 | DERIVED | worst realization in GOAT phase |
| R5 manual: realized vs theoretical | 95,214 / 140,100 = 0.679 | DERIVED | partial archetype misclassification |
| R5 algo: realized vs backtester | 57,911 / 72,000 = 0.804 | DERIVED | full-day < backtester window |
| R5 algo: realized vs inflation-adjusted prediction | 57,911 / 83,720 = 0.692 | DERIVED | live-vs-test gap ~30% |

### Tie caveats — BOTH R1 and R3 manuals had massive ties

| Claim | Value | Class | Source |
|---|---|---|---|
| R1 manual displayed rank (cumul) | #72 | USER | Same |
| R1 manual without-ties rank | ~#3,000 | USER | User-reported tie caveat |
| R3 manual displayed rank (cumul) | #234 | USER | Same |
| R3 manual without-ties rank | ~#1,200 | USER | User-reported tie caveat |
| Earlier "displayed ~#70 / true ~#1,200" memory | merged R1 display + R3 without-ties | — | Both caveats are real and now preserved separately |



> This table maps every load-bearing number in the vault to its **source of truth**. Three classes:
> - **REPO** — verifiable by reading a specific file in the repo right now
> - **USER** — held only by the user (ground truth from Prosperity server/website, not captured in any file)
> - **DERIVED** — computed from REPO or USER data; formula shown

---

## Competition Structure

| Claim | Value | Class | Source |
|---|---|---|---|
| Number of R5 products | 50 | REPO | `context/Round 5/` briefing txt |
| Number of R5 categories | 10 | REPO | `context/Round 5/` briefing txt |
| R5 position limit | ±10 (all products) | REPO | `round5/strategies/round5_v1_trader.py` |
| R3 HYDROGEL position limit | 200 | REPO | `round3/trader.py` |
| R3 VEL position limit | 200 | REPO | `round3/trader.py` |
| R3 VEV option limit | 300 | REPO | `round3/trader.py` |
| Prosperity backtester window | First 10% of Day 4 (~100K of 1M timestamps) | REPO | `README.md` / `.planning/` docs |
| 8.6× fill inflation (local vs Prosperity) | ×8.6 | REPO | `README.md` (v34/v35 comparison note; exact script not preserved) |

---

## Round 1 Algo PnL

| Claim | Value | Class | Source |
|---|---|---|---|
| Local backtest (v3, R1) | 291,170 XIREC | REPO | `round1/backtests/` |
| Prosperity competition R1 | ~168,000 XIREC | USER | Prosperity website (not captured in any file) |
| ACO component (website-scaled) | ~53,116 × (168/291) ≈ 31K | DERIVED | R1 local × website/local ratio |
| IPR ceiling occupancy | 99.2% (238,054/240,000) | REPO | `round1/research/` EDA scripts |

---

## Round 1 Manual (Intarian Welcome)

| Claim | Value | Class | Source |
|---|---|---|---|
| Dryland Flax: BUY 5k @ 29 | 5k units | DERIVED | Order-book clearing analysis; `report/report.tex §Dryland Flax` |
| Dryland Flax PnL | 5,000 XIREC | DERIVED | 5,000 × (30 − 29) |
| Ember Mushroom: BUY 35k @ 18 | 35k units | DERIVED | Order-book clearing analysis |
| Ember Mushroom PnL | 66,500 XIREC | DERIVED | 35,000 × (19.90 − 18) |
| Combined manual R1 | 71,500 XIREC | DERIVED | Sum |
| Reported manual R1 | ~70,000 XIREC | USER | Round-level Prosperity website reporting |

---

## Round 2 MAF Auction

| Claim | Value | Class | Source |
|---|---|---|---|
| MAF bid submitted | 3,000 XIREC | REPO | `round2/trader.py` `bid()` method |
| V_extra (website-scaled) | [5K, 7K] XIREC | DERIVED | R1 website PnL × ACO volume-sensitivity estimate |
| V_extra (local, naive) | ~10–13K | DERIVED | Local backtest (inflated; not used for decision) |
| Win probability estimate | ~80% | DERIVED | Peer-bid prior (median ~1,500, right-skewed) |
| Expected profit at b=3,000 | ~2,400 XIREC | DERIVED | 0.80 × (6,000 − 3,000) |
| **MAF bid: ACCEPTED** | yes | USER/DERIVED | algo JSON 362752 raw 94,529 vs reported 91,529 = 3,000 fee paid |
| Realized V_extra | ≈ 0 (volume-bump absorbed by IPR cap) | DERIVED | R1 IPR 79,255 vs R2 IPR 79,199 — essentially identical |
| Net MAF impact | ≈ −3K to −6K vs not bidding | DERIVED | fee paid minus negligible volume lift |

---

## Round 2 Manual (Invest & Expand)

| Claim | Value | Class | Source |
|---|---|---|---|
| Optimal allocation (uniform prior) | (xR=16, xS=48, xV=36) | DERIVED | Exhaustive grid search; `report/report.tex §Round 2 Part C` |
| PnL at (16,48,36) | 110,065 XIREC | DERIVED | R(16)×S(48)×V(36) − 50×500 under uniform-rank proxy |
| Final recommendation | (18, 60, 22) | DERIVED | Multi-prior sensitivity analysis |
| Minimax robust allocation | (20, 70, 10) | DERIVED | Worst-case analysis over peer priors |
| Realized I&E PnL | ~155,000 XIREC | USER | Prosperity website (referenced in round summary table) |

---

## Round 3 Algo

| Claim | Value | Class | Source |
|---|---|---|---|
| HYDROGEL AR(1) coefficient ρ₁ | −0.495 | REPO | `round3/research/hydrogel_audit.py` |
| HYDROGEL best MM PnL (3 days) | 153,566 XIREC | REPO | `round3/backtests/` Phase 10 |
| VEV passive-only improvement | +839 XIREC | REPO | `round3/research/vev_passive_comparison.py` |
| VEV_4000 add (Phase 10) | +6,887 XIREC | REPO | Phase 10 PLAN.md / backtest |
| OBI signal disabled | β=0 | REPO | `round3/trader.py` |
| Phase 13 R5 baseline | 261,461 XIREC (3 days) | REPO | `.planning/phases/13-*/SUMMARY.md` |

---

## Round 3 Manual (Bio-Pods)

| Claim | Value | Class | Source |
|---|---|---|---|
| Theoretical Bayesian-Nash bids | (b₁=755, b₂=840) | DERIVED | FOC system; grid search; `round3/research/biopod_solver.py` |
| **Actually submitted bids** | **(b₁=760, b₂=855)** | USER | Prosperity result page (slight upward shading) |
| Per-counterparty EV at NE (theoretical) | 81.67 XIREC | DERIVED | f(755,840) under symmetric-NE |
| **N counterparties (verified)** | **1,000** at each bid level | USER | Prosperity result page (335+665, 404+596) |
| Realized Bio-Pods PnL | **+75,237.51** | USER | Prosperity result page |
| Per-CP realized at b₁=760 | 53.60 XIREC/cp | DERIVED | 53,600 / 1,000 |
| Per-CP realized at b₂=855 | 21.64 XIREC/cp | DERIVED | 21,637.51 / 1,000 |
| Combined per-CP realized | 75.24 (= 92% of NE EV) | DERIVED | 75,237.51 / 1,000 |
| Avg peer first bid | 768 | USER | Distribution graph |
| Avg peer second bid | 859 | USER | Distribution graph |
| Reserve distribution grid | {670, 675, …, 920}, 51 levels | REPO | `context/Round 3/` |

---

## Round 5 Algo — Version History

| Claim | Value | Class | Source |
|---|---|---|---|
| v9 Prosperity backtester PnL | $16,527 | REPO | `round5/logs/` or `round5/plots/` |
| v11 Prosperity backtester PnL | $26,218 | REPO | Same |
| v14 Prosperity backtester PnL | $46,621 | REPO | Same |
| v21 Prosperity backtester PnL | $61,756 | REPO | Same |
| v23 Prosperity backtester PnL | $70,000 | REPO | Same |
| v34 Prosperity backtester PnL | $72,891 | REPO | Same |
| v36 Prosperity backtester PnL | $78,799 | REPO | Same |
| **v42 Prosperity backtester PnL** | **$72,000** | **USER** | **Stated by user 2026-05-05; not in any repo file** |
| v42 submitted | yes | USER | User confirmed |
| v36 not submitted (deliberate) | yes | USER | User confirmed ("didn't want to overfit") |
| **v42 R5 GOAT contribution (algo+manual combined)** | **153,126** | **USER/DERIVED** | leaderboard 2026-05-08; derived as 383,727 − 230,601 |
| Backtester→full-day implied ratio (v42, if manual ≈ Ashflow theoretical) | ~1.94× | DERIVED | (153,126 − 140,100) / 72,000 if all manual realized; or 153,126/72,000 = 2.13× if no manual |

---

## Round 5 Algo — Key Parameters

| Claim | Value | Class | Source |
|---|---|---|---|
| AR(1) ≈ 0.999 across all 50 products | ≈0.999 | REPO | `round5/research/eda.py` AR(1) fit |
| 13 directional products in v42 | 13 | REPO | `round5/strategies/round5_v42_trader.py` TARGETS_DIR |
| 11 MM_BLACKLIST products | 11 | REPO | `round5/strategies/round5_v42_trader.py` MM_BLACKLIST |
| 2 TIER3 products | 2 | REPO | `round5/strategies/round5_v42_trader.py` TIER3_PRODUCTS |
| 2 HEDGED_NO_SKEW products | 2 | REPO | `round5/strategies/round5_v42_trader.py` HEDGED_NO_SKEW |
| SNACKPACK CHOC/VAN ρ (exact) | −0.915909 | REPO | `round5/plots/within_category_xcorr_summary.csv` row 2 |
| Lead-lag tests run | 36,750 | REPO | `round5/research/lead_lag.py` |
| Bonferroni α for lead-lag | 1.36×10⁻⁶ | DERIVED | 0.05 / 36,750 |
| Lead-lag survivors | 0 | REPO | `round5/plots/round5/lead_lag/lead_lag_pairs.csv` |
| Phase 15 valid_R² | −0.169 | REPO | `round5/runs/` alpha_lab output |
| Phase 15 sign_accuracy | 0.4915 | REPO | Same |

---

## Round 5 Manual (Ashflow Alpha)

| Claim | Value | Class | Source |
|---|---|---|---|
| Budget | 1,000,000 XIREC | REPO | `context/Round 5/` |
| Fee formula | fee = 100 × p² | REPO | `context/Round 5/` |
| Optimal formula | p* = s/2 | DERIVED | FOC; `report/report.tex §Ashflow Alpha` |
| Budget constraint binding? | No (Σp* = 85%) | DERIVED | 25+16+14+12+12+6 = 85 |
| Model PnL at optimum | 140,100 XIREC | DERIVED | Σ 100 × p*²_i |
| **Realized Ashflow Alpha PnL** | **+95,214** | USER | Prosperity result page |
| Realization ratio | 0.679 | DERIVED | 95,214 / 140,100 |
| Lava cake SELL 25% realized | +95,884 | USER | Prosperity result page |
| Pyroflex SELL 12% realized | +9,041 | USER | Same |
| Thermalite BUY 16% realized | +9,856 | USER | Same |
| Sulfur reactor BUY 6% realized | +6,854 | USER | Same |
| **Magma ink BUY 12% realized (MISCLASSIFIED)** | −11,727 | USER | Same |
| **Ashes of the Phoenix SELL 14% realized (MISCLASSIFIED)** | −14,694 | USER | Same |
| Volcanic / Obsidian / Scoria | 0 (correctly skipped) | USER | Same |
| Archetype hit rate | 4/6 = 67% | DERIVED | matches realization ratio |

---

## Round 4 Manual (AETHER_CRYSTAL exotic options)

| Claim | Value | Class | Source |
|---|---|---|---|
| Realized total | +57,516.23 | USER | Prosperity result page |
| AC_50_CO (chooser SELL 50) | +54,354.22 (biggest winner) | USER | Same |
| AC_50_C (call BUY 50) | +31,415.57 | USER | Same |
| AC_45_P (put BUY 50) | +20,280.48 | USER | Same |
| AC_50_P (put BUY 50) | +18,505.03 | USER | Same |
| AC_40_BP (binary put SELL 50) | +15,000.00 | USER | Same |
| AC_35_P (put BUY 50) | +9,243.40 | USER | Same |
| **AC_45_KO (knockout BUY 500)** | **−28,966.10** (biggest loser) | USER | Same |
| **AC_40_P (put SELL 50)** | **−24,754.41** | USER | Same |
| AC_50_C_2 (2w call BUY 50) | −23,442.21 | USER | Same |
| AC_50_P_2 (2w put BUY 50) | −14,119.75 | USER | Same |
| Implied AC path | V-shaped/volatile (touched <40 then rebounded) | DERIVED | reconciliation of winner/loser pattern |

## Round 4 Manual Counterparty Taxonomy

| Claim | Value | Class | Source |
|---|---|---|---|
| Mark 67 net VEL (3 days) | +1,510 | REPO | `.planning/phases/12-counterparty-exploitation/RESEARCH.md` |
| Mark 49 net VEL (3 days) | −956 | REPO | Same |
| Mark 22 option events/day | ~184 | REPO | Same |
| Mark 01 VEL appearances | 1,843 | REPO | Same |
| Mark 55 trades/day | ~400 | REPO | Same |
| Mark 14 HYDROGEL net (3 days) | −44 | REPO | Same |
| Mark 38 HYDROGEL net (3 days) | +34 | REPO | Same |

---

## Notation

- **REPO**: Open `report/report.tex`, the relevant source `.py`, or the data CSV listed — the exact number should appear there. If it doesn't, the REPO classification is wrong and should be corrected here.
- **USER**: The user has stated this number directly. It is not in any file. Do not compute or estimate it — quote the user exactly and log the date of the statement.
- **DERIVED**: A calculation. Re-derivable from the formula shown. These are exact if the inputs are REPO/USER; otherwise they carry the uncertainty of the estimated inputs.

## Links

[[User_Reported_Anchors]] · [[Concepts/Glossary]] · [[Final_Competition_Result]] · [[Backtests/PnL_Timeline]] · [[CLAUDE]]

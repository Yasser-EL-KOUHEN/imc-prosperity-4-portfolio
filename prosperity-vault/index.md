# Prosperity Vault — Master Index

> Read this first when answering any query. Find relevant pages, then drill in.
> Updated: 2026-05-06 · Total pages: 125+ · Competition: complete (final pass)

---

## Meta

| Page | Summary |
|------|---------|
| [[CLAUDE]] | Wiki schema, directory structure, workflows, conventions, key R5 facts |
| [[Overview]] | High-level competition synthesis (R1→R5), quick-start path, strategy map |
| [[log]] | Append-only operation log |

---

## Quick Start (read these first if you're new)

| Page | Summary |
|------|---------|
| [[Concepts/Glossary]] | XIREC, GOAT, Mark, TIER3, HEDGED_NO_SKEW, HAC, BH-FDR, OOS — all R5 terms |
| [[Cross_Round_Comparison]] | What stayed the same and what changed, round to round |
| [[Concepts/Backtester_vs_Competition]] | The central R5 lesson — first-10% vs full-day |
| [[Backtests/PnL_Timeline]] | Every round's PnL with verified Prosperity numbers |
| [[Carry_Forward]] | The 20 rules I'd take into the next competition |
| [[Final_Competition_Result]] | Submitted versions + measured PnL anchors |
| [[User_Reported_Anchors]] | Facts held only by the user — v42=$72K, realized manual PnLs, leaderboard rank |
| [[v34_vs_v36_vs_v42]] | Canonical 3-way comparison of the three key R5 submission versions |
| [[Verify]] | Provenance table for every load-bearing number (REPO / USER / DERIVED) |

---

## Rounds (chronology)

| Page | Summary |
|------|---------|
| [[Rounds/Round0_Tutorial]] | Tutorial: EMERALDS, TOMATOES; EDA and first submissions |
| [[Rounds/Round1_findings]] | ~263K — ACO anchor-blend MM (ρ=−0.495); IPR greedy long (99.2% ceiling) |
| [[Rounds/Round2_findings]] | ACO+IPR carryover; MAF b*=3,000; I&E exact optimum (16,48,36)=110,065 |
| [[Rounds/Round3_findings]] | Options + HYDROGEL; Bio-Pods manual; baseline 153,566 |
| [[Rounds/Round4_findings]] | Phase 12 counterparty (Mark taxonomy); manual portfolio E[+175,200 XIRECs] |
| [[Rounds/Round4_Preview]] | Pre-work scoping doc (2026-04-27); superseded by Round4_findings |
| [[Rounds/Round5_Preview]] | Mid-round capture: 50 products in 10 cats; Ashflow Alpha 85%/140,100 manual |
| [[Rounds/Round5_findings]] | **Post-mortem** — v1→v42 evolution; backtester ≠ competition; v42 final |

---

## Concepts (with ML analogies)

### Foundational

| Page | Summary |
|------|---------|
| [[Concepts/Market_Microstructure]] | **Hub page** — fill priority, maker/taker, adverse selection, Prosperity fill model, capacity management |
| [[Concepts/AR1_Process]] | AR(1) coefficient: −0.495 (HYDROGEL) vs ≈+0.999 (R5); why this determines strategy architecture |
| [[Concepts/fair_value]] | Estimating true price: mid, VWAP, theoretical; ML analogy = ŷ |
| [[Concepts/inventory_risk]] | Position skew, accumulation, limit enforcement; ML analogy = regularization |
| [[Concepts/Position_Limits]] | Hard position caps, cap enforcement pattern, safety gates |
| [[Concepts/Spread_Dynamics]] | Bid-ask spread, passive vs aggressive quoting, spread as profit margin |
| [[Concepts/Order_Book_Imbalance]] | OBI formula, statistical calibration, when it helps vs hurts |

### Options (R3, R4)

| Page | Summary |
|------|---------|
| [[Concepts/Black_Scholes]] | BS call formula, greeks, pure-math implementation (no scipy) |
| [[Concepts/Implied_Volatility]] | IV surface, per-strike σ, Newton-Raphson solver, IV z-score signal |
| [[Concepts/Chooser_Option]] | **R4** Static replication chooser = C(T) + P(T_c) for r=0 |
| [[Concepts/Binary_Option]] | **R4** Digital N(−d₂) pricing + cliff risk + spread approximation |
| [[Concepts/Knockout_Option]] | **R4** Merton barrier formula + Broadie-Glasserman discrete adjustment |

### Round 5 (key insights)

| Page | Summary |
|------|---------|
| [[Concepts/Backtester_vs_Competition]] | **The central R5 lesson** — Prosperity backtester = first 10% of day 4; competition = full day |
| [[Concepts/Adverse_Selection]] | Why MM bleeds on tight-spread products; loss scales with volume; remedy = blacklist or TIER3 |
| [[Concepts/Lead_Lag]] | Confirmed null: 0/36,750 CCF tests survive Bonferroni at α=1.36×10⁻⁶ |
| [[Concepts/Glossary]] | All R5 terminology — XIREC, GOAT, Marks, TIER3, HAC, BH-FDR, AR(1), etc. |

---

## Strategies

### Foundational

| Page | Summary |
|------|---------|
| [[Strategies/market_making]] | Core MM theory: symmetric quotes around fair value, spread = profit |
| [[Strategies/Mean_Reversion]] | AR(1) reversion model; EMA fair value; magnitude-bucketed coefficients |
| [[Strategies/Delta_Hedging]] | Options delta hedge via passive VELVETFRUIT joining; no spread-crossing |
| [[Strategies/Options_Quoting]] | BS pricing, IV surface, one-sided vs two-sided quoting by flow asymmetry |
| [[Strategies/OBI_Signal]] | Order book imbalance as fair value adjustment; calibrated betas; disabled for HYDROGEL |
| [[Strategies/manual_trading]] | Round 2 manual tasks: MAF bid framework, Invest & Expand game theory |

### Round 4

| Page | Summary |
|------|---------|
| [[Strategies/Counterparty_Exploitation]] | Mark taxonomy + composite flow + Signal C cooldown + own_trades fix |
| [[Strategies/Structural_Hedging]] | Layering vanillas to neutralise exotic discontinuities |

### Round 5

| Page | Summary |
|------|---------|
| [[Strategies/Directional_Holding]] | Fixed ±10 positions on multi-day drift products; AR(1)≈0.999 forces this shape |
| [[Strategies/TIER3_Market_Making]] | Reduced LIMIT (5 instead of 10) for adverse-selection-prone products |
| [[Strategies/HEDGED_NO_SKEW]] | Structural pairs MM (SNACKPACK CHOC/VAN ρ=−0.916): bigger inner size, no skew |
| [[Strategies/Cross_Version_Blacklist]] | N=12 Prosperity log aggregation; avg ≤ −$500 AND 0/12 positive → blacklist |
| [[Strategies/Round5_Version_History]] | Full v1→v42 changelog with PnL costs/saves per decision |
| [[Strategies/Ashflow_Alpha_News_Trading]] | **R5 manual SUBMITTED** archetype classification; $p^*=s/2$ optimum; 85% / 140,100 fees |

---

## Products

### Round 1–2

| Page | Summary |
|------|---------|
| [[Products/ASH_COATED_OSMIUM]] | ACO — stable FV≈10,000; AR(1) ρ₁=−0.495; anchor-blend MM; v3 53,116 XIREC |
| [[Products/INTARIAN_PEPPER_ROOT]] | IPR — +0.1/tick trend; greedy long; 238,054/240,000 ceiling (99.2%); never sell |

### Round 3 (HYDROGEL + VEV options)

| Page | Summary |
|------|---------|
| [[Products/HYDROGEL_PACK]] | AR(1) mean-reversion MM; bucketed coefficients; OBI disabled; best earner (131,640) |
| [[Products/VELVETFRUIT_EXTRACT]] | Options underlying; passive delta hedge only; no spread-crossing |
| [[Products/Options/VEV_4000]] | Deep ITM (S−K≈1,250); two-sided; +4,194 XIREC over 3 days |
| [[Products/Options/VEV_5000]] | Deep ITM call bid-only; 94-98% bid-hit flow; σ=0.242 |
| [[Products/Options/VEV_5100]] | Near-ITM bid-only; gamma-scalp +$6.5/voucher/day; +7,653 XIREC |
| [[Products/Options/VEV_5200]] | Near-ITM call bid-only; σ=0.244 |
| [[Products/Options/VEV_5300]] | Active two-sided; strongest OBI signal (β=0.65, R²=0.125); σ=0.245 |
| [[Products/Options/VEV_5400]] | ATM call two-sided; σ=0.230 (lowest vol — smile trough) |
| [[Products/Options/VEV_5500]] | OTM call two-sided; σ=0.249; OBI β=0.49 |
| [[Products/Options/VEV_6000]] | Deep OTM; sell-only ask=1; bid=0 trap (Phase 12 Change A reverted) |
| [[Products/Options/VEV_6500]] | Deepest OTM; sell-only; same setup as VEV_6000 |

### Round 4 (AETHER_CRYSTAL exotic options)

| Page | Summary |
|------|---------|
| [[Products/AETHER_CRYSTAL]] | Manual underlying; GBM σ=251%, r=0; bid 49.975 / ask 50.025 |
| [[Products/Options/AC_50_C]] | 3w ATM call; BS fair 12.03; chooser arb leg |
| [[Products/Options/AC_50_P]] | 3w ATM put; BS fair 12.03; binary spread leg |
| [[Products/Options/AC_50_C_2]] | 2w ATM call; BS fair 9.87; **+0.121 buy edge** |
| [[Products/Options/AC_50_P_2]] | 2w ATM put; BS fair 9.87; chooser leg + **+0.121 buy edge** |
| [[Products/Options/AC_35_P]] | 3w OTM put; KO knockout partial hedge |
| [[Products/Options/AC_40_P]] | 3w OTM put; binary spread short leg |
| [[Products/Options/AC_45_P]] | 3w OTM put; general downside tail hedge |
| [[Products/Options/AC_60_C]] | 3w OTM call; SKIPPED (naked short tail risk) |
| [[Products/Options/AC_50_CO]] | **Chooser** K=50 T+21/14; **+0.30 sell edge**; static replication |
| [[Products/Options/AC_40_BP]] | **Binary put** K=40 payout 10; **+0.232 sell edge**; cliff hedged |
| [[Products/Options/AC_45_KO]] | **Knock-out put** K=45 B=35; **+0.045 buy edge**; bounded loss |

### Round 5 (50 products / 10 categories / limit ±10)

| Page | Summary |
|------|---------|
| [[Products/Round5_Categories]] | Overview — all 50 products, day-2 mid ranges, outliers per category |
| [[Products/PEBBLES]] | Basket trade (XL +10, S/M/L/XS −10); strongest within-category structure |
| [[Products/SNACKPACK]] | CHOC/VAN HEDGED_NO_SKEW (ρ=−0.916); STRAW +10, PIST −10 directional |
| [[Products/PANEL]] | PANEL_2X4 +10 directional (conflict product, full-day +); 3 of 5 BLACKLIST |
| [[Products/MICROCHIP]] | OVAL −10 (R5 workhorse, both-window-consistent); SQUARE = OOS-flip cautionary tale |
| [[Products/UV_VISOR]] | AMBER −10, RED +10 (twin of MICROCHIP_OVAL — both-window-consistent) |
| [[Products/OXYGEN_SHAKE]] | GARLIC +10 (top single-product +$19K); 2 BLACKLIST losers |
| [[Products/GALAXY_SOUNDS]] | BLACK_HOLES = canonical conflict product (PW− vs FW+); v37 mistake page |
| [[Products/SLEEP_POD]] | LAMB_WOOL = most-blacklisted product (failed at +10, default MM, every config) |
| [[Products/ROBOT]] | DISHES zero-fill, LAUNDRY un-TIER3 disaster; IRONING surprise top earner |
| [[Products/TRANSLATOR]] | Tightest-spread category in R5; SPACE_GRAY zero-fill blacklisted |

---

## Counterparty Profiles (Round 4)

| Page | Summary |
|------|---------|
| [[Marks/Mark_67]] | **Dip buyer** — +1,510 net VEL; buys only at ≥5MA lows; never sells; regime signal for directional entry |
| [[Marks/Mark_49]] | **Local-high seller** — −956 net VEL; passive at local highs; 500ms cooldown timing signal |
| [[Marks/Mark_22]] | **OTM call short-seller** — 184 events/day; excluded from mark_net (frequency mismatch); Change A revert |
| [[Marks/Mark_01]] | **VEL MM + long OTM buyer** — Mark 22's bilateral counterpart; ~neutral VEL, accumulates OTM calls at 0 cost |
| [[Marks/Mark_14]] | **Primary HYDROGEL MM** — 100% bilateral with Mark_38; tight-spread maker; VEV_4000 presence |
| [[Marks/Mark_38]] | **Mark_14 mirror** — bilateral partner; tick-alternating maker roles; net ≈ 0 by construction |
| [[Marks/Mark_55]] | **Symmetric taker/arbitrageur** — ~400/day VEL; net ≈ 0; excluded from mark_net; market-efficiency signal |

---

## Manual Challenge Derivations

| Page | Summary |
|------|---------|
| [[Manuals/Dryland_Flax]] | **R1 Intarian Welcome** — BUY 5k @ 29 (Flax) + BUY 35k @ 18 (Mushroom); clearing-price engineering; 71,500 total |
| [[Manuals/MAF]] | **R2 Market Access Fee** — b*=3,000 XIREC; website-scaled V_extra [5K,7K]; 6:1 asymmetric regret; ~80% win |
| [[Manuals/Invest_and_Expand]] | **R2 I&E** — (xR=16,xS=48,xV=36)=110,065; log×linear×rank FOC system; exhaustive grid search |
| [[Manuals/Bio_Pods]] | **R3 Bio-Pods** — (b₁=755,b₂=840) Bayesian-Nash equilibrium; f*=81.67/CP; cubic penalty cliff at Δb₂=−1 |
| [[Manuals/Ashflow_Alpha]] | **R5 Ashflow Alpha** — p*=s/2 exact formula; 6/9 goods; 85% allocation; 140,100 model PnL; realized 95,214 (back-solved s_i: 6 directionally right, Magma + Ashes magnitude tiny) |
| [[Manuals/AETHER_Crystal]] | **R4 AC exotic portfolio** — 12 instruments; common-knowledge regime; realized 57,516 (33% of E[+175,200]); V-shaped path |

---

## Performance (official Prosperity-issued results, post-competition)

| Page | Summary |
|------|---------|
| [[Performance/Algo_Per_Round]] | Real-engine per-product PnL from submission JSONs; **MAF accepted** (raw 94,529 vs reported 91,529); R5 v42 bucket decomposition (DIRECTIONAL +67K, HEDGED +10K, DEFAULT_MM −16K [MICROCHIP_SQUARE −18.6K alone], TIER3 −2.7K, BLACKLIST 0); full 50-product table |
| [[Performance/Manual_Per_Round]] | Per-instrument manual breakdowns + peer-distribution graphs; Bio-Pods actually submitted at (760,855), N=1000 cps, 75.24/cp realized; Ashflow back-solved s_i per archetype; R4 = common-knowledge regime (we aligned with consensus on all 12 instruments) |
| [[Performance/Submission_Verification]] | Provenance ledger: R4 and R5 vault traders match submission exactly; **R1 vault is v3 but actually-submitted was v2**; **R3 vault has 2 candidates, neither matches submission** |

---

## Backtests

### Round 3 (Phases 1–11)

| Page | Summary |
|------|---------|
| [[Backtests/Phase1_Backtest_Calibration]] | Local vs server tolerance: +7.2% overestimate; ×0.93 calibration |
| [[Backtests/Phase2_Sweep_Infrastructure]] | Env-var injection; 24-config sweep; baseline IS optimum; anchor_w=0.20 dominates; 16–20× local inflation confirmed |
| [[Backtests/Phase3_HYDROGEL_FV]] | Fair value trace: corr=0.96 with time, 3-day 43,281; mean-reversion confirmed |
| [[Backtests/Phase4_Rho_Sweep]] | 49-config grid; winner small=0.08/large=0.42 (+1,927 vs reference) |
| [[Backtests/Phase5_VEV_Passive]] | Passive-only vs baseline: +839; VEV standalone +581 on day 0 |
| [[Backtests/Phase6_BS_Verify]] | BS prices match reference within 3.7e-4; sigma table verified |
| [[Backtests/Phase7_Options_Quoting]] | All quoting gates PASS; options aggregate −745 but 2/3 positive days |
| [[Backtests/Phase8_OBI_Sweep]] | All 8 beta configs identical (146,415); OBI sub-resolution vs passive edges |
| [[Backtests/Phase9_Safety]] | All safety gates PASS: limits, imports, edge cases; 146,415 confirmed |
| [[Backtests/Phase10_Submission]] | VEV_4000 (+6,887) + TTE/σ recal (+265) → 153,567; READY FOR SUBMISSION |
| [[Backtests/Phase11_Box_Signal]] | Box signal null result; best 153,568 (1/3 days gate fails); baseline preserved |

### Round 4 (Phase 12)

| Page | Summary |
|------|---------|
| [[Backtests/Phase12_Counterparty]] | Anti-regression PASS 153,566; 4 fixes (Change A revert, ts, race, own_trades) |

### Round 5 (Phases 13–15)

| Page | Summary |
|------|---------|
| [[Backtests/Phase13_R5_Directional]] | 7 products, ±10 directional hold; 261,461 GRAND TOTAL; OOS 118,083 (PASS) |
| [[Backtests/Phase14_R5_Setup]] | Phase 14 Plan 00 — eda2 package + xgboost/arch installed; OOS_DAY=4 pre-registered |
| [[Backtests/Phase14_R5_EDA]] | Six-analysis EDA results: F (XGBoost AUROC OOS=0.653) graduates; rest dead ends |
| [[Backtests/Phase15_AlphaLab]] | ML deadends — alpha_lab valid_R²=−0.169, sign_acc=0.49 (worse than chance OOS) |

### Cross-round timeline

| Page | Summary |
|------|---------|
| [[Backtests/PnL_Timeline]] | **R1 → R5 progression**, with verified real-Prosperity PnL for v1, v9, v11, v14, v21, v23, v25, v26, v27, v31, v34, v35, v36, v39, v40 |

---

## Parameters

| Page | Summary |
|------|---------|
| [[Parameters/HYDROGEL_Params]] | All calibrated HYDROGEL values: ρ_small=0.08, ρ_large=0.42, anchor_w=0.20, inv_skew=0.03 |
| [[Parameters/VELVETFRUIT_Params]] | VEV passive-only flag, LIMIT=200, hedge thresholds |
| [[Parameters/Options_Params]] | Per-strike σ, OBI β table, TTE schedule {1: 7.0, 2: 6.0, 3: 5.0}, bid-only flags |
| [[Parameters/Round5_Params]] | **v42 final config** — all 13 directional products, MM_BLACKLIST(11), TIER3(2), HEDGED_NO_SKEW(2) |

---

## Research

| Page | Summary |
|------|---------|
| [[Research/Decisions_Log]] | **D1–D25** canonical architectural decisions with rationale and backtest evidence |
| [[Research/Round1_Scripts]] | EDA, ACO sweep, edge hunt scripts from R1 research |
| [[Research/Round3_Scripts]] | Full R3 research pipeline: microstructure, IV, OBI, sweeps |
| [[Research/Round5_Scripts]] | R5 EDA: Phase 13 directional, Phase 14 six-analysis, drift_audit, lead_lag (null), pairs, cross-version blacklist |

---

## Competition

| Page | Summary |
|------|---------|
| [[Competition/Game_Mechanics]] | How Prosperity 4 works: submission, order matching, leaderboard, XIREC |
| [[Competition/Round_Schedule]] | 5 rounds, timing, deadlines, products per round |

---

## Off-Wiki Reference (orphans by design)

| Page | Summary |
|------|---------|
| [[Daily/Agentic Tooling]] | How the vault + GSD + MCP + Claude Code workflow was set up (2026-04-27) |
| `Daily/2026-04-26.md` | Daily session log (sparse) |
| `Theory/Theory - Quantitative Trading.pdf` | Outside-the-competition reading |
| `Theory/After Competition - Honest assessment Theory Trading Report.txt` | 30-line self-rated assessment of the theory PDF (93/100) |
| `Theory/Theory_Quantitative_Trading.tex` | LaTeX source for theory PDF |
| `Untitled.canvas` | Obsidian canvas — informal notes |
| `Products/RAINFOREST_RESIN.md`, `KELP.md`, `SQUID_INK.md` | Stub pages for non-existent P4 products (Prosperity 3 leftovers) |

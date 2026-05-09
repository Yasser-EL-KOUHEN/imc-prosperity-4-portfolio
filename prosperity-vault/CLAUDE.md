# Prosperity Vault — Wiki Schema & Maintenance Guide

> This file tells Claude (and future-me) how this wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki.

---

## What This Wiki Is

A **persistent, compounding knowledge base** for the IMC Prosperity 4 trading competition (now finished). It sits between the raw source files (code, backtests, context docs, planning artifacts) and any query session. Knowledge is compiled once and kept current — not re-derived on every question.

Three layers:
1. **Raw sources** — code in `round0/` … `round5/`, `shared/`, planning docs in `.planning/`, IMC briefings in `context/`, full LaTeX writeup in `report/`. Immutable. Never modify.
2. **This wiki** — `prosperity-vault/`. Claude owns this layer. Creates, updates, cross-links pages.
3. **This schema** — the document you're reading. Co-evolved over time.

---

## Repo Layout (post-reorganization, 2026-04-30)

```
Trading Competition IMC/
├── round0/   tutorial: EMERALDS, TOMATOES
├── round1/   ASH_COATED_OSMIUM (ACO), INTARIAN_PEPPER_ROOT (IPR), EMERALDS
├── round2/   manual: Invest & Expand 15/50/35; algo continuation
├── round3/   HYDROGEL_PACK, VELVETFRUIT_EXTRACT, VEV options 4000–6500
├── round4/   AETHER_CRYSTAL exotic options manual; Mark-counterparty algo
├── round5/   50 products in 10 categories; v1→v42 strategy evolution
├── shared/   datamodel, prosperity_bootstrap, options helpers (shared lib)
├── context/  IMC official round briefings + game-mechanics txt
├── report/   report.tex (full LaTeX writeup — most comprehensive single source)
├── .planning/ phase-by-phase decision trail (PLAN.md, SUMMARY.md, RESEARCH.md)
└── prosperity-vault/ this wiki
```

Each `roundN/` typically has: `README.md`, `findings.md` (R1–R3 only), `trader.py`, `backtests/`, `data/`, `logs/`, `plots/`, `research/`. Round 5 also has `strategies/` (43 versioned trader files: round5_v1 … round5_v42) and `runs/` (ML training artifacts).

---

## Vault Directory Structure

```
prosperity-vault/
├── CLAUDE.md              ← this file (schema)
├── index.md               ← master page index (content-oriented)
├── log.md                 ← append-only operation log (chronological)
├── Overview.md            ← high-level competition synthesis (R1→R5, quick start)
├── Cross_Round_Comparison.md   ← what changed round-to-round
├── Carry_Forward.md       ← lessons for the next competition
├── Final_Competition_Result.md ← submitted versions + verified PnL anchors
│
├── Competition/           ← meta-competition facts
│   ├── Game_Mechanics.md
│   └── Round_Schedule.md
│
├── Products/              ← one page per tradeable instrument family
│   ├── ASH_COATED_OSMIUM.md
│   ├── INTARIAN_PEPPER_ROOT.md
│   ├── HYDROGEL_PACK.md
│   ├── VELVETFRUIT_EXTRACT.md
│   ├── AETHER_CRYSTAL.md
│   ├── Round5_Categories.md     ← 50 products, 10 categories overview
│   ├── PEBBLES.md               ← Round 5 category page
│   ├── SNACKPACK.md
│   ├── PANEL.md
│   ├── MICROCHIP.md
│   ├── UV_VISOR.md
│   ├── OXYGEN_SHAKE.md
│   ├── GALAXY_SOUNDS.md
│   ├── SLEEP_POD.md
│   ├── ROBOT.md
│   ├── TRANSLATOR.md
│   └── Options/           ← per-strike option pages (Round 3 VEV, Round 4 AC)
│
├── Strategies/            ← trading strategy concept pages
│   ├── market_making.md   ← (lowercase filename — keep)
│   ├── Mean_Reversion.md
│   ├── Delta_Hedging.md
│   ├── Options_Quoting.md
│   ├── OBI_Signal.md
│   ├── manual_trading.md
│   ├── Counterparty_Exploitation.md       (R4)
│   ├── Structural_Hedging.md              (R4)
│   ├── Ashflow_Alpha_News_Trading.md      (R5 manual)
│   ├── Directional_Holding.md             (R5 algo — fixed ±10 by drift)
│   ├── TIER3_Market_Making.md             (R5 — reduced LIMIT for adverse-selection)
│   ├── HEDGED_NO_SKEW.md                  (R5 — structural pairs MM)
│   ├── Cross_Version_Blacklist.md         (R5 — N=12 log evidence)
│   └── Round5_Version_History.md          (R5 — v1→v42 changelog)
│
├── Concepts/              ← finance/quant concept pages (with ML analogies)
│   ├── fair_value.md
│   ├── inventory_risk.md
│   ├── Black_Scholes.md
│   ├── Implied_Volatility.md
│   ├── Order_Book_Imbalance.md
│   ├── Position_Limits.md
│   ├── Spread_Dynamics.md
│   ├── Chooser_Option.md                  (R4)
│   ├── Binary_Option.md                   (R4)
│   ├── Knockout_Option.md                 (R4)
│   ├── AR1_Process.md                     (AR(1) −0.495 vs +0.999 — determines strategy architecture)
│   ├── Market_Microstructure.md           (fill priority, maker/taker, adverse selection, fill model)
│   ├── Adverse_Selection.md               (R5)
│   ├── Lead_Lag.md                        (R5 — null result)
│   ├── Backtester_vs_Competition.md       (R5 — first-10%-of-day vs full-day)
│   └── Glossary.md                        (XIREC, GOAT, Mark, TIER3, HAC, etc.)
│
├── Parameters/            ← all calibrated parameter values with evidence
│   ├── HYDROGEL_Params.md
│   ├── VELVETFRUIT_Params.md
│   ├── Options_Params.md
│   └── Round5_Params.md   (v42 full config)
│
├── Backtests/             ← per-phase backtest results with actual numbers
│   ├── PnL_Timeline.md    (R1→R5 with verified Prosperity numbers)
│   ├── Phase{1,2,3..14}_*.md (R3 + R4 + R5; Phase2 = sweep infrastructure)
│   └── Phase15_AlphaLab.md (R5 ML deadends)
│
├── Research/              ← research script inventory + decisions
│   ├── Round1_Scripts.md
│   ├── Round3_Scripts.md
│   ├── Round5_Scripts.md
│   └── Decisions_Log.md
│
├── Rounds/                ← per-round synthesis
│   ├── Round0_Tutorial.md
│   ├── Round1_findings.md
│   ├── Round2_findings.md
│   ├── Round3_findings.md
│   ├── Round4_findings.md
│   ├── Round5_Preview.md   (mid-round capture)
│   └── Round5_findings.md  (post-mortem of v1→v42 + competition outcome)
│
├── Marks/                 ← per-counterparty profiles (R4 Mark taxonomy)
│   ├── Mark_01.md         ← VEL MM + long OTM call buyer
│   ├── Mark_14.md         ← Primary HYDROGEL MM (bilateral with Mark_38)
│   ├── Mark_22.md         ← OTM call short-seller (excluded from mark_net)
│   ├── Mark_38.md         ← Mark_14's mirror partner
│   ├── Mark_49.md         ← Local-high seller (passive, 500ms cooldown signal)
│   ├── Mark_55.md         ← Symmetric taker / likely arbitrageur
│   └── Mark_67.md         ← Dip buyer (+1,510 net VEL; never sells)
│
├── Manuals/               ← per-round manual challenge derivations
│   ├── Dryland_Flax.md    ← R1: BUY 5k @ 29; clearing-price engineering; 71,500 total
│   ├── MAF.md             ← R2: b*=3,000; ACCEPTED but volume bonus absorbed by IPR cap
│   ├── Invest_and_Expand.md ← R2: submitted (18,60,22) — over-FOC; rank #2,801; realized 153,345
│   ├── Bio_Pods.md        ← R3: NE (755,840) but submitted (760,855); N=1,000 cps; realized 75,238
│   ├── AETHER_Crystal.md  ← R4: 12-instrument exotic portfolio; common-knowledge regime; realized 57,516
│   └── Ashflow_Alpha.md   ← R5: p*=s/2; 4-of-6 archetypes; back-solved s_i; realized 95,214
│
├── User_Reported_Anchors.md  ← facts held by user, not in any repo file
├── v34_vs_v36_vs_v42.md      ← canonical 3-way version comparison
├── Verify.md                 ← provenance table for every numeric claim (REPO/USER/DERIVED)
│
├── Performance/           ← official Prosperity-issued results (algo JSON parses + manual breakdowns)
│   ├── Algo_Per_Round.md  ← per-product real-engine PnL from submission JSONs; v42 bucket decomposition
│   ├── Manual_Per_Round.md ← per-instrument manual results + peer distributions; back-solved s_i
│   └── Submission_Verification.md ← provenance ledger: vault traders vs actually-submitted .py files
│
├── Daily/                 ← session logs (sparse)
└── Theory/                ← outside-the-competition reading
```

---

## Page Frontmatter Format

Every wiki page should have YAML frontmatter:

```yaml
---
type: product | strategy | concept | backtest | round | research | competition | parameters
tags: [tag1, tag2]
sources: [relative/path/to/source1, relative/path/to/source2]
updated: YYYY-MM-DD
---
```

- `type` classifies the page for Dataview queries
- `tags` allow thematic grouping (e.g. `options`, `round3`, `calibrated`, `round5`, `null-result`)
- `sources` trace back to raw source files (use the **new** post-reorganization paths: `round5/strategies/round5_v34_trader.py`, NOT `rounds/round5/strategies/...`)
- `updated` tracks staleness

---

## Link Conventions

- **Wikilinks**: `[[Page]]` for same-folder, `[[Folder/Page]]` for cross-folder
- **Aliases**: `[[Folder/Page|Display text]]`
- **External**: standard markdown `[text](url)`
- **Every page** should link to at least 2 other wiki pages
- **Concept pages** must always have an ML analogy section (user background: MPSI/MP* → MEng CS/ML → MSc DS&BA)
- **Wikilink filename = on-disk filename** — Obsidian-style wikilinks are case-sensitive on Linux/Mac. Existing pages with lowercase filenames (`fair_value.md`, `inventory_risk.md`, `market_making.md`, `manual_trading.md`) must be linked with that exact case.

---

## Index Protocol

`index.md` is content-oriented. Structure:
- Grouped by category (Concepts, Strategies, Products, Rounds, Backtests, Research, Parameters, Competition)
- Each entry: `- [[Page]] — one-line summary`
- Sort within each group by centrality (most cross-referenced pages first)
- Update on every ingest or new page

When answering a query, read `index.md` first to find relevant pages, then drill in.

---

## Log Protocol

`log.md` is append-only. Entry format:

```
## [YYYY-MM-DD] operation | Description
- bullet points about what happened
- pages created/updated
```

Operations: `ingest`, `query`, `lint`, `build`, `decision`, `result`

Parse recent entries: `grep "^## \[" log.md | tail -5`

---

## Tooling Setup

This wiki was built and maintained using the **GSD + Obsidian + MCP + Claude Code** agentic workflow. Claude reads and writes vault pages directly via MCP; the GSD framework structures each working session into phases (PLAN → SUMMARY → execute). See [[Daily/Agentic Tooling]] for the setup note from the day the workflow was initialized.

---

## Workflows

### Ingest (adding a new source)

1. Read the source file
2. Identify key facts/decisions/results
3. Update existing pages that the source touches (add to their `sources:` frontmatter)
4. Create new pages for concepts not yet covered
5. Update `index.md`
6. Append to `log.md`
7. Check for contradictions with existing pages

### Query (answering a question)

1. Read `index.md` to find relevant pages
2. Read those pages
3. Synthesize answer (with page citations)
4. If the answer is valuable, file it back as a new wiki page
5. Append to `log.md`

### Lint (health check)

Look for:
- Contradictions between pages (e.g. parameter values that disagree)
- Stale claims superseded by newer backtests / decisions
- Orphan pages (no inbound links)
- Concepts mentioned but lacking their own page
- Missing cross-references
- Data gaps that could be filled by reading more source files

---

## Key Round 5 Domain Facts (preserve accurately)

These are the load-bearing facts of the Round 5 chapter — every R5 page should be consistent with them.

1. **Backtester ≠ competition scoring.** The Prosperity local backtester runs the **first 10% of Day 4** (~100K of 1M timestamps). Competition scoring runs the **full day**. The two metrics can have **different optimal strategies** — and they did. v36 won the backtester ($78,799) but v34 had the best estimated full-day PnL ($152,730). This reframing is the single most important Round 5 insight. See [[Concepts/Backtester_vs_Competition]].

2. **Local-backtester inflation.** Running with `--match-trades all` is documented to give roughly **8.6× inflated fills** vs the real Prosperity matching engine (figure cited in `README.md`, derived from a v34/v35 local-vs-Prosperity comparison; the exact replication script is not preserved in the repo). v35 was tuned on local data and failed because of this — the local "evidence" was the wrong signal. v36's pivot used the **N=12 cross-version Prosperity log** (real engine, real fills) instead.

3. **Final submitted strategy: v42.** Measured Prosperity backtester PnL: **~$72,000** (user-reported; not derivable from repo since v42 log isn't pulled back). v36 had a **higher** backtester score ($78,799) but v42 was submitted because **v36 over-fit to the Prosperity-window evidence** and dropped two products (PANEL_2X4, BLACK_HOLES) whose full-day drift is positive. The −$6,799 backtester gap was the deliberate cost of robustness; expected full-day return on that cost: ~+$33K. Composition:
   - **13 directional positions** at fixed ±10 (12 from v34's setup + SNACKPACK_STRAWBERRY +10)
   - **8 confirmed losers blacklisted** from MM (7 ex-TIER3 products + SLEEP_POD_LAMB_WOOL — confirmed across N=12 Prosperity logs)
   - **2 small-loss TIER3** kept at LIMIT=5 (MICROCHIP_RECTANGLE, OXYGEN_SHAKE_EVENING_BREATH)
   - **HEDGED_NO_SKEW** for SNACKPACK CHOCOLATE+VANILLA (ρ=−0.916 structural pair, MM with bigger inner size 8 and no inventory skew)
   - Layer-1 directional → Layer-2 per-product-tiered MM with skew
   - **The deliberate non-optimization to backtester is itself a load-bearing decision** — see [[Concepts/Backtester_vs_Competition]] and [[Strategies/Round5_Version_History]].

4. **Structural pairs exploited**:
   - SNACKPACK CHOCOLATE / VANILLA: **ρ = −0.916** (3-day avg of return correlations from `round5/plots/within_category_xcorr_summary.csv`) → HEDGED_NO_SKEW (bigger inner size 8, no inventory skew)
   - PEBBLES sub-variants: ρ ≈ −0.5 (PEBBLES_XL +10 vs PEBBLES_S/M/L/XS −10 directional basket)

5. **Lead-lag null result.** 36,750 CCF tests (1,225 pairs × 5 lags × 3 days × 2 directions = 36,750), Bonferroni α = 0.05/36750 = **1.36e-6**. Zero pairs survived. This is a **confirmed null result**, not a failure to test. See [[Concepts/Lead_Lag]].

6. **ML experiments failed PnL gate.** GRU, XGBoost, SDE-synthetic data augmentation, block bootstrap — all failed the Phase 13 baseline gate. Phase 13 was locked. The XGBoost classifier in Phase 14 reached AUROC OOS = 0.653 statistically but never produced PnL improvement on full evaluation. Document as dead ends, not silenced failures.

7. **TIER3 was correct.** TIER3 = products where MM loses to **adverse selection** (informed counterparties picking off our quotes). The correct response is smaller LIMIT (5 instead of 10) — reduced exposure cuts the bleeding. v40 removed TIER3 (LIMIT 5 → 10) on the false hypothesis "more trades on full day = recovery"; this **doubled** the loss. The mistake: more adverse selection scales with volume, not less. v41 restored TIER3.

8. **AR(1) ≈ 0.999 across all 50 R5 products.** Mean-reversion impossible. Designed alpha is multi-day **directional drift**, not lag-1 reversion. This is why R5 strategy structure is "directional hold + tiered MM" — opposite of HYDROGEL's AR(1) MM in R3.

---

## Calibration Sources

| Parameter | Source file |
|-----------|-------------|
| HYDROGEL AR(1) coefficients | `round3/research/hydrogel_audit.py` |
| OBI betas (R3 products) | `round3/research/microstructure_eda.py` |
| Per-strike IV sigma (VEV) | `round3/research/iv_surface.py` |
| Rho sweep winner | `round3/research/hydrogel_sweep.py` + Phase 4 grid |
| VEV passive-only decision | `round3/research/vev_passive_comparison.py` |
| TTE / live sigma | Phase 10 Addendum 2 recalibration |
| R5 directional targets (Phase 13) | `round5/research/eda.py` |
| R5 full-day drift signs | `round5/research/full_day_optimal.py` → `plots/round5/full_day_optimal.csv` |
| R5 Prosperity-window vs full-day conflicts | `round5/research/drift_audit.py` → `plots/round5/drift_audit.csv` |
| R5 cross-version blacklist | `round5/research/analyze_prosperity_logs.py` (N=12 versions) |
| R5 lead-lag null result | `round5/research/lead_lag.py` → `plots/round5/lead_lag/lead_lag_pairs.csv` |
| R5 SNACKPACK CHOC/VAN ρ=−0.92 | `round5/research/pairs_analysis.py` → `plots/round5/within_category_xcorr_summary.csv` |
| R5 Phase 14 EDA (A–F) | `round5/research/eda2/*.py` → `plots/round5/eda2/*.csv` |

---

## Known Contradictions

| Page | Contradiction | Resolution |
|------|--------------|------------|
| `Research/Decisions_Log.md` | PROJECT.md says `anchor_weight=0.0` locked; trader.py v6 uses `anchor_w=0.20` | v6 deliberately increased anchor_w (dominant improvement). Planning doc is stale. |
| `Backtests/Phase3_HYDROGEL_FV.md` | OBI enabled in experiment but disabled (0.0) by default in trader.py | OBI was tested (Phase 3 experiment) and found net-negative; kept disabled. |
| Phase 13 vault page (pre-2026-04-30) | Said `status: PLANNED, implementation pending` | Phase 13 actually executed and produced $261,461 GRAND TOTAL. Vault page updated 2026-04-30. |
| v37 BH flip | docstring claimed "+$1,324 expected gain"; actual full-day PnL was −$26K vs v34 | The Prosperity-window drift signal contradicted the full-day drift on BLACK_HOLES. Documented in `Concepts/Backtester_vs_Competition`. |

---
type: competition
tags: [final, submitted, v42, r5, post-competition, leaderboard, result]
sources:
  - round5/strategies/round5_v42_trader.py
  - round5/logs/v34/575850.json
  - round5/logs/v36/578532.json
  - round5/logs/v40/579308.json
  - round5/README.md
  - prosperity-vault/log.md
  - prosperity-vault/User_Reported_Anchors.md
  - Prosperity website final leaderboard (screenshots, 2026-05-08)
updated: 2026-05-08
---

# Final Competition Result

## Final Leaderboard (received 2026-05-08)

| Metric | Value | Notes |
|---|---|---|
| **Final overall rank** | **#346 / 18,803** | top 1.84% |
| Algorithmic | #537 | weakest sub-rank — backtester gap visible |
| Manual | #204 | manuals outperformed algo |
| **Country** | **#11** | strongest sub-rank |
| Final GOAT XIREC | **383,727** | R3+R4+R5 cumulative |

### Per-round PnLs (verified 2026-05-08)

| Round | Algo PnL | Manual PnL | Round Total | Cumul. |
|---|---|---|---|---|
| R1 | +98,172 | **+71,500** | 169,672 | 169,672 |
| R2 | +91,529 | +153,345 | 244,874 | 414,546 |
| R3 | +40,800 | +75,238 | 116,038 | 116,037 (GOAT begins) |
| R4 | +57,048 | +57,516 | 114,564 | 230,601 |
| R5 | **+57,911** | +95,214 | 153,125 | **383,727** |

### Cumulative leaderboard rankings at end of each round (CANONICAL)

| Round | Overall | Algorithmic | Manual | Country |
|---|---|---|---|---|
| R1 | ~#2,000 | ~#1,400 | **#72** *(≈ #3,000 without ties)* | #59 |
| R2 | #1,522 | #857 | #801 | #59 |
| R3 | #802 | #830 | **#234** *(≈ #1,200 without ties)* | #30 |
| R4 | #592 | #809 | #406 | #21 |
| **R5 (final)** | **#346** | **#537** | **#204** | **#11** |

**Algo cumulative-rank trajectory:** ~1,400 → 857 → 830 → 809 → **537**. Monotonic improvement — the algo rank moved up by ~860 places.

**Manual cumulative-rank trajectory:** ~3,000 (without-ties) → 801 → ~1,200 (without-ties) → 406 → **#204**. Strongly monotonic.

**Country trajectory:** 59 → 59 → 30 → 21 → **#11**. Steepest improvement; dropped 48 places.

### GOAT decomposition (R3+R4+R5 only)

| Component | XIREC | % of GOAT |
|---|---|---|
| Algo (R3+R4+R5) | 155,759 | 40.6% |
| Manual (R3+R4+R5) | 227,968 | **59.4%** |
| **Total** | **383,727** | 100% |

**Manuals delivered 60% of the final XIREC** despite the algo representing the bulk of project hours. This is the central post-result insight.

### Tie caveats (BOTH R1 and R3 manuals)

The user clarified that **both** manuals had massive-tie regimes:
- **R1 manual** displayed #72; without ties ≈ **#3,000**. Dryland Flax + Ember Mushroom is a deterministic clearing-price-engineering puzzle — every solver produces the same orders and same realized PnL. The display rank is essentially random tie-breaking.
- **R3 manual** displayed #234; without ties ≈ **#1,200**. Bio-Pods at the symmetric NE (b₁=755, b₂=840) is similarly common-knowledge among solvers.

The earlier conversation collapsed both into a single "displayed ~#70, real ~#1,200" memory, which fused R1's display rank with R3's without-ties rank. Both caveats are real and need to be preserved separately.

## Submitted Algorithm

**`round5/strategies/round5_v42_trader.py`** — submitted as the final R5 entry. See [[Parameters/Round5_Params]] for the full configuration.

**Verified Prosperity backtester PnL: ~$72,000.** This is **lower than v36's $78,799 backtester champion** — by design. The team explicitly chose v42 over v36 to **avoid overfitting to the Prosperity backtester window** (first 10% of Day 4). The $6,799 backtester gap was the cost of keeping PANEL_2X4 and BLACK_HOLES directional (their full-day drift is positive even though Prosperity-window drift is negative). See [[Concepts/Backtester_vs_Competition]] for the central rationale.

## Submitted Manuals

| Round | Submission | Result |
|---|---|---|
| 1 | Dryland Flax: BUY 5,000 @ 29 | +5,000 XIREC |
| 2 | I&E (16, 48, 36) | 110,065 XIREC |
| 3 | Bio-Pods (b₁, b₂) = (755, 840) | EV ≈ 81.67/cp × N counterparties |
| 4 | Exotic options portfolio (12 instruments) | E[+58.4 × 3000 mul] = E[+175,200] |
| 5 | Ashflow Alpha — 6 of 9 goods, 85% allocated | 140,100 fees / model net PnL = 140,100 |

## Verified Real-Engine Performance (R5 cross-version)

> Numbers below are **measured** by parsing `activitiesLog` from each version's JSON Prosperity log and summing per-product `profit_and_loss` at the last timestamp. Window = first 100K timestamps of Day 4 (the Prosperity backtester window).

```text
v1   $19,995    7-product directional only (Phase 13 baseline)
v9   $37,284    + aggressive MM, multi-level, skewed
v11  $36,113
v14  $33,901    + local-BT-derived blacklist (mostly wrong)
v21  $23,270    + 2-level depth
v23  $52,620    Prosperity-informed redesign
v25  $52,440
v26  $54,120    + per-product TIER1/3/BLACKLIST
v27  $61,450    best-of synthesis
v31  $53,473
v34  $62,299    + PEBBLES basket + HEDGED_NO_SKEW
v35  $53,360    local-CV reclassification (FAILED)
v36  $78,799    cross-version N=12 blacklist (BACKTESTER CHAMPION)
v39  $38,258    full-day-bet (dropped PEBBLES_XL — wrong window)
v40  $52,788    TIER3 removal mistake
```

## What's NOT in the Repo

The Prosperity log JSON files for **v37**, **v38**, **v41**, and **v42** were not pulled back to `round5/logs/{vN}/*.json`. The **measured v42 backtester PnL ($72K) is user-reported**, not derivable by parsing the repo's log files.

Reasons documented in `log.md`:

- **v37** was committed locally but not run on Prosperity (the docstring estimated ~$79K based on first 10% extrapolation; the BH flip was suspected to break full-day so the team didn't burn a Prosperity slot on it)
- **v38** was the defensive fallback; not run
- **v41 = v34 + STRAWBERRY** was effectively identical to v34 + 1 marginal directional; not separately tested
- **v42** was submitted to the competition leaderboard, ran on the Prosperity backtester at ~$72K, and was the **chosen final submission**. The activitiesLog JSON for v42 was not pulled back to the repo, so per-product PnL breakdown for v42 cannot be computed by the JSON-parse pipeline used for the other versions

~~**Pre-result framing (SUPERSEDED 2026-05-08):**~~ The full-day estimate (~$163K) was derived from `round5/plots/full_day_optimal.csv` × position size + observed blacklist saves.

**Actual:** the v42 submission JSON (`performance/algorithmic trading/round 5/581865.json`) is now in the repo — **realized R5 algo PnL = $57,911 full-day**. The $163K pre-result estimate over-stated by ~3×; the full-day was *less* than the $72K backtester window (ratio 0.80). See [[Performance/Algo_Per_Round]] for the full 50-product breakdown by strategy bucket.

## How to Get the Real Number

If the user pulls the v42 Prosperity log back into `round5/logs/v42/{submissionId}.json`, the same parse logic used for v34/v36/v40 will produce the verified PnL:

```python
import json
with open('round5/logs/v42/{ID}.json') as f: data = json.load(f)
rows = data['activitiesLog'].strip().split('\n')[1:]
last_pnl = {}
for row in rows:
    parts = row.split(';')
    if len(parts) >= 17:
        try: last_pnl[parts[2]] = float(parts[-1])
        except: pass
print(f'v42 measured PnL: ${sum(last_pnl.values()):,.0f}')
```

## Submission Pipeline (R3 era, applied to all rounds)

The submission checklist from R3 Phase 9 / 10:

- [x] Syntax (source + vault): `ast.parse OK`
- [x] Imports: 0 violations (only `datamodel`, `jsonpickle`, stdlib)
- [x] `os` removed from vault (R3 specific — the Phase 10 build pipeline strips env-var-based config branches)
- [x] Debug output: 0 bare `print()` calls
- [x] Smoke test: produces valid orders on day-0 first tick
- [x] File size < 200,000 bytes
- [x] Anti-regression gate: doesn't break the previous baseline

## Realized Cumulative XIREC (verified from leaderboard)

| Round | Realized contribution | Cumulative GOAT | Cumulative rank |
|---|---|---|---|
| R1 | (qualifier only — does not enter GOAT) | — | ~#2,000 |
| R2 | (qualifier only — total 414,546 R1+R2) | — | #1,522 |
| **R3** | **116,037** | 116,037 | #802 |
| **R4** | **114,564** | 230,601 | #592 |
| **R5** | **153,126** | **383,727** | **#346** |

**GOAT total: 383,727 XIREC; final overall #346 / 18,803 teams.**

### Reconciliation against pre-result estimates (per-component)

| Component | Pre-result estimate | Realized | Ratio |
|---|---|---|---|
| R1 algo | ~$84K (website-scaled) | 98,172 | 1.17 (over-performed) |
| R1 manual | 71,500 | 71,500 | **1.00** (exact) |
| R2 algo (raw, before MAF fee) | similar to R1 | 94,529 | 0.96 |
| R2 MAF bid | accepted ⇒ −3,000 fee | bid was paid | volume bonus absorbed by IPR cap |
| R2 algo (net of MAF fee) | — | 91,529 | net 0.93 vs R1 |
| R2 manual | 110K (FOC) / 432K (bottom-heavy) | 153,345 | over-FOC; (18,60,22) was correct |
| R3 algo | ~$143K (3-day) | 40,800 (1-day) | ~$48K expected/day → 0.85 |
| R3 manual (Bio-Pods at submitted (760,855)) | 81.67/cp × N=1000 = 81,670 | 75,237.51 | **0.92** (per-cp 75.24 vs theoretical 81.67) |
| R4 algo | ~$48K/day baseline | 57,048 | 1.19 (over-performed) |
| R4 manual | E[+175,200] | 57,516 | **0.33** (path-dependent BS failures) |
| R5 algo (v42) | $72K BT / $163K pre-result est (SUPERSEDED) | **57,911** | 0.80 vs BT |
| R5 manual (Ashflow, 4 of 6 archetypes correct) | 140,100 | 95,214 | **0.68** (matches 4/6 hit rate) |

**Revised pattern:** the picture is **not** "manual EVs were systematically optimistic". It's much more nuanced:
- R1 manual realized **exactly** the theoretical 71,500 — clean clearing-price engineering
- R2 manual **over**-performed the FOC theoretical (153,345 vs 110,065) — submitting (18,60,22) over the FOC was the right call
- R3 manual realized 75,238 at rank #234 — solid even after the common-knowledge tie regime
- R4 manual was **the** underperformer at 33% of EV — Greek-asymmetric exotic options bit hard
- R5 manual realized 68% of theoretical — partial archetype misclassification in Ashflow

The story is "**R4 manual missed badly; everything else was within reason**". The R4 exotic options portfolio was the costliest single decision of the GOAT phase.

### Backtester-vs-real consistency for v42 — RESOLVED

- v42 backtester (first 10% of Day 4): **$72,000**
- v42 R5 algo realized (full Day 5): **$57,911**
- **Ratio: 0.80** — full-day was *less* than the backtester window

Reconciliation with the 8.6× inflation thesis:
- Backtester runs 10% of day with 8.6× over-fill → net multiplier 0.86 vs full-day-equivalent
- Predicted full-day from $72K: $72K / 0.86 = $83.7K
- Realized $57.9K = **69% of prediction** → live-vs-test gap of ~30%

This is normal: **Day 5 had different drift patterns than the historical Days 2/3/4** that informed v42's directional list. Some directional positions that worked on training data didn't resolve favorably on the actual competition day. The encouraging side: rank **#287 / 18,803 (top 1.5%)** for R5 algo despite the absolute PnL gap — the v42 design was strong against the field even when the realized day was unfavorable.

## Caveats

- All R5 algo numbers above are **measured first-10%-of-day** + estimates extrapolated. The real competition full-day PnL for v42 is unknown until the log is retrieved.
- Manual EVs are expected values across counterparty distributions; realized values varied per simulation seed.
- The cumulative is meaningful only as a rough scale. Round-by-round leaderboard placement was not recorded in the repo.

## Links

[[Strategies/Round5_Version_History]] · [[Parameters/Round5_Params]] · [[Backtests/PnL_Timeline]] · [[Rounds/Round5_findings]] · [[Concepts/Backtester_vs_Competition]] · [[Overview]]

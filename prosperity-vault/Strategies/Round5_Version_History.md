---
type: strategy
tags: [round5, changelog, evolution, v1-v42, traders]
sources:
  - round5/strategies/
  - round5/README.md
  - log.md (2026-04-29 → 2026-04-30 entries)
updated: 2026-04-30
---

# Round 5 — Version History (v1 → v42)

> Canonical changelog for the 43 trader files in `round5/strategies/`. Each entry distills the docstring into the three things that matter: **what changed, why, and what happened**. PnL columns are first-10%-of-day-4 (Prosperity backtester) unless marked "full day".

## Quick Reference

| Version | Idea | Backtester PnL |
|---|---|---|
| v1 | 7-product directional hold (Phase 13 baseline) | local 261,461 (3-day) |
| v2–v8 | MM layer experiments + skew tuning | various |
| **v9** | aggressive MM, full LIMIT, multi-level, skewed | **local 669K** (inflated) |
| v10–v13 | minor tweaks; queue join experiments | — |
| **v14** | v9 + MM_BLACKLIST (local-BT-derived) | local-tuned |
| v15–v20 | inventory-skew refinements | — |
| **v21** | v20 + 2-level queue depth | **local 699K** |
| v22 | tighter MM | — |
| **v23** | **Prosperity-informed redesign** — drop directional disasters | Prosperity-validated |
| v24, v25 | minor refinements | — |
| **v26** | per-product MM_LIMIT calibrated from v9 Prosperity log (TIER1/3/BLACKLIST) | +$10K vs v23 |
| **v27** | best-of v9/v23/v26 synthesis | foundation for v34 |
| v28–v33 | iterations on Prosperity log evidence | — |
| **v34** | + PEBBLES_M/L directional + HEDGED_NO_SKEW for SNACKPACK CHOC/VAN | **$62,299 backtester** · est $152,730 full day |
| v35 | local-CV reclassification (FAILED — local ≠ Prosperity) | $53K |
| **v36** | cross-version N=12 blacklist (drop LAMB_WOOL etc.) | **$78,799 backtester (winner)** · est $130,680 full day |
| v37 | v36 + GALAXY_SOUNDS_BLACK_HOLES flipped to −10 | $78K backtester · catastrophic full day |
| v38 | defensive — only 2 both-window-consistent dirs | $38,258 |
| v39 | full-day bet — drop PEBBLES_XL, restore PANEL_2X4 | $38K (wrong window) |
| v40 | v34 + un-TIER3 + 2 new directional | $52,788 (TIER3 removal mistake) |
| v41 | v34 + SNACKPACK_STRAWBERRY +10 (TIER3 kept) | ~$62K |
| **v42** | **v41 + 8 confirmed losers blacklisted** | **$72K measured backtester** · **realized $57,911 full-day** (Day 5 competition; ratio 0.80) · pre-result ~$163K estimate was 3× over **[SUBMITTED]** |

---

## v1 — Phase 13 Baseline (Pure Directional)

7 products, fixed ±10, aggressive spread crossing, hold all day. No MM. Selected by OOS validation (train days 2+3, OOS day 4):

```python
TARGETS = {
    "MICROCHIP_OVAL":            -10,
    "PEBBLES_XL":                +10,
    "OXYGEN_SHAKE_GARLIC":       +10,
    "GALAXY_SOUNDS_BLACK_HOLES": +10,
    "PEBBLES_S":                 -10,
    "PEBBLES_XS":                -10,
    "PANEL_2X4":                 +10,
}
```

3-day local backtest: **+261,461 GRAND TOTAL**, day-4 OOS **+118,083** (all 7 products positive). See [[Backtests/Phase13_R5_Directional]].

## v9 — Aggressive MM Layer

Added a market-making layer on the remaining 43 products. Full LIMIT=10, multi-level (inner+outer quotes), inventory-skewed at |pos| ≥ 6. Inner size 6, outer size 4. **MIN_SPREAD=2** triggers MM.

Expanded directional set to 13 products (added UV_VISOR_AMBER/RED, SNACKPACK_PISTACHIO/STRAWBERRY/CHOCOLATE, SLEEP_POD_LAMB_WOOL).

Local backtester reported 669K — this was the moment the team realized **local was inflating fills** vs the real Prosperity engine. v9's real Prosperity result was much smaller; the v9 log became the seed for the Tier classification in v26.

## v14 — Local-BT-Derived MM_BLACKLIST

Added `MM_BLACKLIST` from local-BT loss-fitting:
```python
MM_BLACKLIST = {
    "PEBBLES_M", "ROBOT_MOPPING", "GALAXY_SOUNDS_SOLAR_FLAMES",
    "UV_VISOR_MAGENTA", "TRANSLATOR_SPACE_GRAY", "ROBOT_VACUUMING",
    "PANEL_1X2", "PANEL_4X4",
}
```

This blacklist was later **mostly wrong** on real Prosperity (local-BT artifacts). PEBBLES_M was in the local blacklist but turned out to be a +$1,487 directional in v34's Prosperity run.

## v21 — 2-Level Queue Depth

Added `OUTER_SIZE=4` quotes at `best_bid - 1 / best_ask + 1` to capture sweeps. Inner stays at touch, outer one tick away. Local 699K (still inflated).

## v23 — Prosperity-Informed Redesign

**The first version built from real Prosperity log evidence.** Key changes:
- **Removed SLEEP_POD_LAMB_WOOL** from directional (largest Prosperity loss: −$5,978)
- **NO blacklist** — the local blacklist was overfit; v9's "losers" mostly earn on Prosperity
- Conservative MM_LIMIT=8 with inventory skew
- Quote-frequency throttle: skip MM every other tick to reduce overtrading noise

This was the breakthrough version — switching from local-BT logic to real-engine logic.

## v26 — Per-Product Tiered MM

Introduced the four-tier system from v9 Prosperity log evidence:

```python
TIER1 (MM_LIMIT=10):   top earners > $2K (9 products: PANEL_4X4, TRANSLATOR_GRAPHITE_MIST,
                        UV_VISOR_ORANGE, TRANSLATOR_ECLIPSE_CHARCOAL, MICROCHIP_TRIANGLE,
                        ROBOT_IRONING, TRANSLATOR_ASTRO_BLACK, SLEEP_POD_NYLON, SLEEP_POD_POLYESTER)
TIER2 (MM_LIMIT=8):    default
TIER3 (MM_LIMIT=5):    small losers $-500 to $-3K (10 products)
TIER4 (BLACKLIST):     big losers > $3K (3 products: TRANSLATOR_SPACE_GRAY,
                        GALAXY_SOUNDS_PLANETARY_RINGS, ROBOT_DISHES — zero-fill on Prosperity)
```

Plus `HEDGED_PRODUCTS` bumped to TIER1 for structurally hedged pairs.

## v27 — Best-of-Each Synthesis

Combined v9's aggression (MM_LIMIT_DEFAULT=10, SKEW=6), v23's directional cleanup, v26's TIER3. Foundation for v34.

## v34 — Structural Pairs + Backtester Best Baseline

Two new edges:
- **PEBBLES basket completion**: PEBBLES_M (−10), PEBBLES_L (−10) added to directional. Anti-correlated with PEBBLES_XL (+10), so the basket is structurally short small/large with hedged exposure.
- **HEDGED_NO_SKEW** for SNACKPACK CHOCOLATE+VANILLA: bigger inner size (8), normal skew threshold (rarely triggers because pair anti-correlation hedges). See [[Strategies/HEDGED_NO_SKEW]].

12 directional products total. Backtester: **$62,299**. Estimated full-day: **$152,730 (best of all tested versions).**

## v35 — Local-CV Reclassification (FAILED)

Used `queue_priority_bt.py` (`--match-trades worse + 1/10 subsampling`) to reclassify all tiers based on local data. Train days 2+3, OOS day 4.

Findings (all wrong on real Prosperity):
- Drop PEBBLES_M, PEBBLES_L from directional (UNSTABLE/BLACKLIST in local BT)
- Promote PANEL_1X4 from TIER3 to TIER1
- Promote OXYGEN_SHAKE_EVENING_BREATH from TIER3 to TIER1

Backtester: **$53K**. Worse than v34 by ~$9K. The lesson: local-BT data is the **wrong distribution** for tier decisions. Use Prosperity log evidence only.

## v36 — Cross-Version N=12 Blacklist (Backtester Winner)

Aggregated PnL across N=12 Prosperity runs (v1, v9, v11, v14, v21, v23, v25, v26, v27, v31, v34, v35). Blacklist threshold: avg ≤ −$500 AND 0/12 positive.

Result: 11-entry blacklist (3 zero-fill + 8 cross-version losers + 2 deterministic-loss directionals). Removed PANEL_2X4 and GALAXY_SOUNDS_BLACK_HOLES from directional.

Backtester: **$78,799 (highest of any version).** Full-day estimate: **$130,680 — $22K worse than v34** because PANEL_2X4 and BH are first-10%-loss-but-full-day-gain products. See [[Strategies/Cross_Version_Blacklist]].

## v37 — BLACK_HOLES Flip (Catastrophic on Full Day)

Single change vs v36: **flip GALAXY_SOUNDS_BLACK_HOLES from removed-from-directional to directional −10**, on the basis that Prosperity-window drift was negative all 3 days.

```text
Day 2: -85   (negative)
Day 3: -53   (negative)
Day 4: -65   (negative)
```

But the **full-day drift** is strongly positive (+1,446 / +688 / +1,320). The Prosperity-window-vs-full-day **conflict** product. Estimated full-day PnL impact: **−$26K vs v34** (BH +10 → +$13K becomes BH −10 → −$13K, a $26K swing the wrong way).

Lesson: **never trust the Prosperity-window for products in the conflict set.** The drift_audit.csv flags conflict=True for exactly this reason.

## v38 — Defensive Both-Window-Consistent

Reduced directional to **only 2 products** (MICROCHIP_OVAL, UV_VISOR_AMBER) — the only ones sign-consistent across **both** windows AND all 3 days. Minimal blacklist (3 zero-fill only). Default MM at LIMIT=10.

Low-variance submission: $38K backtester. Sacrifices known winners for robustness.

## v39 — Full-Day Bet (Wrong Window for Backtester)

Committed to full-day evidence as the prior. **Dropped PEBBLES_XL/M/L** because their full-day drift is mixed (PEBBLES_XL: +3674, −1552, +4014). **Restored PANEL_2X4 and SLEEP_POD_LAMB_WOOL** to directional (full-day positive). Added SNACKPACK_STRAWBERRY +10.

Backtester: $38K (lost the PEBBLES_XL alpha that **does** show in the first 10%). Trade-off: if competition uses a window longer than the backtester, gains compound.

## v40 — TIER3 Removal Mistake

Hypothesised that TIER3 was Prosperity-backtester-loss-fitting. Removed all 9 TIER3 products → LIMIT=10 default MM. Added SLEEP_POD_LAMB_WOOL +10 and SNACKPACK_STRAWBERRY +10 directional.

**Wrong direction.** Backtester $52,788 — **−$6,536 worse than v34** from the un-TIER3'd 9 products alone. Adverse-selection losses scale **with** trading volume, not against. See [[Strategies/TIER3_Market_Making]].

## v41 — Conservative v34 Refinement

= v34 + SNACKPACK_STRAWBERRY +10 (single new HIGH-confidence directional). **TIER3 kept** (fixes v40 mistake). Dropped SLEEP_POD_LAMB_WOOL +10 (drift only +$110, backtester loss −$5,978 → fragile).

Backtester: ~$62K (similar to v34). Most conservative refinement of v34.

## v42 — Final Submitted: v41 + Aggressive Blacklist

User-directed addition: blacklist 8 confirmed losers (7 ex-TIER3 + SLEEP_POD_LAMB_WOOL).

```python
# v42 = v41 with these 8 promoted from TIER3/default-MM to MM_BLACKLIST:
"OXYGEN_SHAKE_MORNING_BREATH", "GALAXY_SOUNDS_DARK_MATTER", "PANEL_2X2",
"ROBOT_LAUNDRY", "PANEL_1X2", "PANEL_1X4", "OXYGEN_SHAKE_MINT",
"SLEEP_POD_LAMB_WOOL"
```

KEEP at TIER3 (small losses < $200): MICROCHIP_RECTANGLE, OXYGEN_SHAKE_EVENING_BREATH.

**Measured v42 backtester PnL: ~$72,000**. **Realized R5 algo (full Day 5 competition): $57,911** — *less* than the backtester window (ratio 0.80). Pre-result estimate of ~$163K full-day was 3× over.

This is the **chosen submission** despite **not being the backtester champion**. v36 scored $78,799 on the backtester ($6,799 higher); v42 was preferred because:

1. v36's blacklist over-fits to the Prosperity-window evidence — it removes PANEL_2X4 and BLACK_HOLES directional positions
2. v42 keeps both directional while blacklisting the 8 confirmed cross-version losers

**Day-5 reality check:** Both PANEL_2X4 (−$3,822 realized) and BLACK_HOLES (−$4,914 realized) actually drifted down on Day 5 — *v36's call to drop them would have been correct on the realized day*. The $6,799 backtester gap that v42 accepted to keep them did not pay off. Rank-against-field still favored v42 (algo round-rank #287, the strongest of all 5 rounds), but the absolute-PnL bet on these two products was wrong. See [[Performance/Algo_Per_Round]].
3. The competition scores **the full day**, not the first 10%; the $6,799 backtester gap is the *price of robustness*, not a regression

This is the explicit articulation of "design for the scoring window, not the backtester window." The backtester was used as a **gate** (does the new version regress in the dev window?), not as a **target** (maximize the dev-window PnL). [[Concepts/Backtester_vs_Competition]] documents the rationale; [[Carry_Forward|Tier 1 rule #2]] captures it as a takeaway for next year.

The best of v34's full-day directional setup + v36's aggressive blacklist + v34's TIER3 + STRAWBERRY directional. Combined three eras of evidence. **Submitted as final.**

## What Each Decision Cost / Saved

| Decision | Cost / Save |
|---|---|
| Pure directional v1 | $261K baseline (3-day) |
| Add MM layer (v9) | +inflated locally, +real on Prosperity |
| Drop LAMB_WOOL directional (v23) | Saved −$5,978/run |
| Per-product TIERs (v26) | +$10K vs v23 |
| PEBBLES_M/L basket completion (v34) | +$2K Prosperity |
| HEDGED_NO_SKEW for CHOC/VAN (v34) | +modest, structurally robust |
| Local-BT reclassification (v35) | **Lost ~$9K** vs v34 |
| N=12 cross-version blacklist (v36) | +$16K backtester, **−$22K full-day** |
| BH flip −10 (v37) | **−$26K full-day** |
| Drop PEBBLES_XL (v39) | **−$40K** of single-day alpha |
| Un-TIER3 (v40) | **−$6.5K** backtester (−$25K full-day est) |
| STRAWBERRY directional (v41) | +$925 |
| Aggressive blacklist (v42) | +$11,849 backtester, +$30–35K full-day est |

## Links

[[Rounds/Round5_findings]] · [[Strategies/Directional_Holding]] · [[Strategies/TIER3_Market_Making]] · [[Strategies/HEDGED_NO_SKEW]] · [[Strategies/Cross_Version_Blacklist]] · [[Concepts/Backtester_vs_Competition]] · [[Backtests/Phase13_R5_Directional]] · [[Backtests/Phase14_R5_EDA]]

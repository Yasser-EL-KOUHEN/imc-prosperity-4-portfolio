---
type: strategy
tags: [round5, blacklist, prosperity-logs, evidence-aggregation, n-equals-12]
sources:
  - round5/strategies/round5_v36_trader.py
  - round5/strategies/round5_v42_trader.py
  - round5/research/analyze_prosperity_logs.py
  - round5/logs/
updated: 2026-04-30
---

# Cross-Version Blacklist (N=12 Prosperity Log Aggregation)

## What It Is

A method for deciding which products to **exclude entirely** (`MM_BLACKLIST`) from the MM layer, by aggregating per-product PnL across **all real-Prosperity runs we ever submitted** — N=12 versions × 1 day-4 run each = 12 independent samples per product, with the **real Prosperity matching engine** (not the local backtester).

The output is a per-product (avg PnL, n-positive ratio) table. Products with `avg ≤ −$500 AND 0/12 positive` are blacklisted. Products with smaller losses are kept (TIER3 or default MM).

## Why N=12 Cross-Version Beats N=1 Per-Version

A single Prosperity log is N=1 evidence per product. v9's log alone is what v23/v26 used to design tiers. But **N=1 has high variance** — a product can lose $500 on one run by random fill timing and earn $500 on the next.

**N=12 cross-version aggregation** stabilizes the estimate:
- Different versions trade different counterparty mixes against the product
- Different days had different market conditions baked into the engine state
- A product that loses in **0 of 12** runs is reliably a winner; one that loses in **12 of 12** is reliably a loser

This is the same principle as **bagging** in ML — N models on N bootstrap samples gives a lower-variance estimate than one model on the full sample.

The 12 versions whose Prosperity logs were aggregated: v1, v9, v11, v14, v21, v23, v25, v26, v27, v31, v34, v35.

## Decision Threshold

```text
BLACKLIST  if  (avg PnL across 12 versions <= -$500) AND (0 of 12 runs positive)
TIER3      if  (small loss but mixed positivity) OR (avg ∈ [-$500, $0])
DEFAULT MM if  (avg > $0)
```

The −$500 threshold was chosen conservatively: small losses (−$30 to −$409 avg) are kept at default tier as likely noise. Only consistent, meaningful losses graduate to BLACKLIST.

## v36 → v42 Blacklist Evolution

### v36 (cross-version blacklist introduced — 11 entries)

```python
MM_BLACKLIST = {
    # v34 inheritance (zero-fill — earn $0 anyway, safe to skip)
    "TRANSLATOR_SPACE_GRAY",
    "GALAXY_SOUNDS_PLANETARY_RINGS",
    "ROBOT_DISHES",

    # NEW (avg <= -$500 AND 0/12 positive across N=12 versions)
    "SLEEP_POD_LAMB_WOOL",          # avg -$3,905 (was tier-2 default)
    "GALAXY_SOUNDS_DARK_MATTER",    # avg -$1,503 (was TIER3)
    "OXYGEN_SHAKE_MORNING_BREATH",  # avg -$1,487 (was TIER3)
    "PANEL_2X2",                    # avg -$1,328 (was TIER3)
    "PANEL_1X4",                    # avg -$1,033 (was TIER3)
    "OXYGEN_SHAKE_MINT",            # avg -$959   (was TIER3)
    "PANEL_1X2",                    # avg -$946   (was TIER3)
    "ROBOT_LAUNDRY",                # avg -$917   (was TIER3)

    # NEW (deterministic per-run loss in directional layer)
    "PANEL_2X4",                    # avg -$3,452 (was directional +10) — REVERTED in v42
    "GALAXY_SOUNDS_BLACK_HOLES",    # avg -$732   (was directional +10) — REVERTED in v42
}
```

v36 was the **backtester winner** at $78,799 — but two of its blacklist entries (PANEL_2X4 and BLACK_HOLES) were **wrong on the full day**. Their −$3,452 / −$732 losses are **first-10%-of-day** losses; on the **full day** they recover to +$8,895 / +$13,155 respectively. The conflict products from `drift_audit.csv`. See [[Concepts/Backtester_vs_Competition]].

### v42 (final — 11 entries, conflict products removed)

```python
MM_BLACKLIST = {
    # v34 inheritance (zero-fill)
    "TRANSLATOR_SPACE_GRAY",
    "GALAXY_SOUNDS_PLANETARY_RINGS",
    "ROBOT_DISHES",

    # 7 ex-TIER3 confirmed losers (LIMIT=5 wasn't enough)
    "OXYGEN_SHAKE_MORNING_BREATH",  # v34 -$1,258, v40 -$2,410
    "GALAXY_SOUNDS_DARK_MATTER",    # v34 -$938,   v40 -$2,384
    "PANEL_2X2",                    # v34 -$1,464, v40 -$2,180
    "ROBOT_LAUNDRY",                # v34 -$1,000, v40 -$1,782
    "PANEL_1X2",                    # v34 -$929,   v40 -$1,654
    "PANEL_1X4",                    # v34 -$1,007, v40 -$1,626
    "OXYGEN_SHAKE_MINT",            # v34 -$969,   v40 -$1,384

    # ex-default-MM consistent loser
    "SLEEP_POD_LAMB_WOOL",          # v34 -$4,284 default MM, v40 -$5,978 directional
    # PANEL_2X4 and GALAXY_SOUNDS_BLACK_HOLES NOT in v42 blacklist —
    # their cross-version losses are first-10% artifacts; full-day positive
}
```

The 8 newly added losers were all members of **v40's un-TIER3 disaster** — v40 promoted 9 ex-TIER3 products to LIMIT=10 and lost ~$6,536 in the backtester relative to v34. Of those 9, the 7 listed above plus SLEEP_POD_LAMB_WOOL were the consistent losers; 2 (MICROCHIP_RECTANGLE −$128, OXYGEN_SHAKE_EVENING_BREATH −$30) had only nominal losses and stayed at TIER3.

## Pitfall — Why You Can't Use Local-BT Logs for This

The N=12 **must** be from real Prosperity runs. Local backtester logs are not equivalent:
- `--match-trades all` inflates fills 8.6× — different fill rates → different PnL distribution
- Local counterparty mix differs from real Prosperity
- v35 was an N=2 train + N=1 OOS local-BT reclassification and produced a wrong answer (see [[Rounds/Round5_findings|Insight 2]])

**Aggregate only deployment-distribution data.** Any other source biases the estimate.

## ML Analogy

Cross-version aggregation is **bag-of-models on the data side**: instead of bootstrapping the data, we bootstrap **across models** (each version's strategy is a different "model" sampling the same product's adverse-selection process). The avg PnL is the bagged expectation; the n-positive ratio is the empirical CDF probability.

The blacklist threshold (`avg ≤ −$500 AND 0/12 positive`) is a conservative **dual-criterion** rule: both the **mean** and the **probability mass** must agree. A product with avg = −$1,000 but 4/12 positive (high variance) shouldn't be blacklisted — it has a tail of upside.

## Post-Result Validation (2026-05-08)

The 11-product MM_BLACKLIST realized **exactly $0** on Day 5 — no trades placed, no PnL accumulated, perfectly disabled:

| Product | Realized | Cross-version basis |
|---|---|---|
| TRANSLATOR_SPACE_GRAY, GALAXY_SOUNDS_PLANETARY_RINGS, ROBOT_DISHES | 0 each | v34 inheritance (zero-fill products) |
| OXYGEN_SHAKE_MORNING_BREATH, GALAXY_SOUNDS_DARK_MATTER, PANEL_2X2, ROBOT_LAUNDRY, PANEL_1X2, PANEL_1X4, OXYGEN_SHAKE_MINT | 0 each | 7 ex-TIER3 confirmed losers |
| SLEEP_POD_LAMB_WOOL | 0 | ex-default-MM consistent loser |
| **Total** | **$0** | exact |

**The cross-version log mechanism worked exactly as designed for products that fit its dual-criterion rule.** Without the blacklist, projecting v34's measured losses on these 11 products to a full Day-5 ratio (~10× longer time × inflation factor) would have leaked an estimated ~$30K–$45K. Saving exactly $0 vs that counterfactual was the win.

### The criterion's blind spot — MICROCHIP_SQUARE

MICROCHIP_SQUARE was *not* in the blacklist (its cross-version log history was inconsistent — some versions positive, some negative — so it didn't meet the `0/12 positive` condition). It stayed in DEFAULT_MM and **lost $18,636** on Day 5 from adverse selection during a strong-drift event.

**Lesson for v43-style refinement:** the cross-version dual-criterion rule is correct for *consistent* losers but blind to *inconsistent-but-large-magnitude* losers. A complementary criterion — **drift-magnitude** (any product whose realized one-day directional drift exceeds N bps gets escalated to TIER3 or BLACKLIST) — would have caught MICROCHIP_SQUARE. The two criteria together (cross-version mean + drift magnitude) form a more complete bias-variance rule.

## Links

[[Rounds/Round5_findings]] · [[Strategies/TIER3_Market_Making]] · [[Strategies/Round5_Version_History]] · [[Concepts/Backtester_vs_Competition]] · [[Concepts/Adverse_Selection]] · [[Performance/Algo_Per_Round]]

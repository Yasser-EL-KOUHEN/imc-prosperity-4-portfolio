---
type: backtest
tags: [phase3, hydrogel, fair-value, obi, calibration, post-r3]
sources: [backtests/phase3_fair_value_trace.md, backtests/phase3_obi_experiment.md, backtests/phase3_rho_experiment.md]
updated: 2026-05-08
---

# Phase 3: HYDROGEL Fair Value Experiments

> **Submission attribution (clarified 2026-05-08):** Phase 3's FV/OBI/ρ research informed the Phase 4 sweep; the **post-Phase-4 winning parameters** (small_rho=0.08, large_rho=0.42) were baked into `round3/trader_final.py` (the R4 basis), not into the R3 submission `486282.py` (which used pre-refinement params 0.12/0.48). HYDROGEL real-engine PnL: R3 $55,100 (un-refined params), R4 $56,200 (refined). See [[Performance/Submission_Verification]].

## 1. Fair Value Trace (Day 1)

**Source:** `backtests/timeseries_day1.csv` (10,000 ticks, HYDROGEL_PACK)

| Metric | Value |
|--------|-------|
| Mid-price range | 9,908.5 – 10,079.0 (range = 170.5 ticks) |
| Mid-price mean | 9,992.06 |
| Mid-price stdev | 37.61 |
| cum_pnl start | 0 |
| cum_pnl end | **43,281** |
| cum_pnl max | 46,498 |
| Max drawdown | −9,729 |
| **corr(cum_pnl, timestamp)** | **0.9576** — earnings strongly time-correlated |
| Max abs position | 0 (settlement effect) |

Sample trajectory:
| Timestamp | Mid | Cum PnL |
|-----------|-----|---------|
| 0 | 9,958 | 0 |
| 199,900 | 10,016 | 13,739 |
| 399,900 | 9,941 | 12,733 |
| 599,900 | 10,023 | 27,729 |
| 999,900 | 10,015 | 43,281 |

**Conclusion:** Mean-reversion pull confirmed. Earnings accrue monotonically with time (corr=0.96) — this is not luck.

---

## 2. OBI Experiment: β=11.2 vs β=0.0

**Source:** `backtests/phase3_obi_experiment.md`

| Day | No OBI (β=0) | OBI β=11.2 | Delta |
|-----|-------------|-----------|-------|
| 0 | 51,788 | 50,389 | **−1,399** ⚠️ |
| 1 | 46,978 | 47,175 | +197 |
| 2 | 41,982 | 37,966 | **−4,016** ⚠️ |
| **Total** | **140,748** | **135,530** | **−5,218** |

**Decision:** OBI DISABLED (β=0.0). Must improve ALL 3 days — fails days 0 and 2.

**Why OBI hurts despite t=31 significance:**
- R²=0.089 — explains <9% of variance
- OBI overlay shifts quotes away from the mean-reversion target
- Anchor pull (anchor_w=0.20) earns more than OBI adjusts

---

## 3. Rho Experiment: AR(1) Calibrated vs Sweep Winner

**Source:** `backtests/phase3_rho_experiment.md`

| Day | Sweep winner (0.12/0.48) | Calibrated AR(1) (0.094/0.237) | Delta |
|-----|------------------------|-------------------------------|-------|
| 0 | 51,788 | 53,827 | +2,039 |
| 1 | 46,978 | 47,352 | +374 |
| 2 | 41,982 | 39,944 | **−2,038** ⚠️ |
| **Total** | **140,748** | **141,123** | **+375** |

**Decision:** Keep sweep winner (0.12/0.48). Calibrated rho fails day 2 (gate: improve ALL 3 days).

**Why calibrated underperforms day 2:**
- Day 2 (TTE=6d) has different microstructure than days 0–1
- Lower rho (0.094 vs 0.12) means less aggressive reversion on large moves → misses profitable trades on day 2 specifically
- Phase 4 fine grid then found true optimum: small=0.08, large=0.42

---

## Links

[[Products/HYDROGEL_PACK]] · [[Strategies/Mean_Reversion]] · [[Strategies/OBI_Signal]] · [[Backtests/Phase4_Rho_Sweep]] · [[Parameters/HYDROGEL_Params]]

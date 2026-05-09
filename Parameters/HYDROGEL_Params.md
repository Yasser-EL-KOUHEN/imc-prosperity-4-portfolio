---
type: reference
tags: [hydrogel, parameters, calibrated, round3, round4, post-r3]
sources: [round3/trader_final.py, round4/trader.py, performance/algorithmic trading/round 3/486282.py, backtests/phase2_back04_best_config.md, backtests/phase3_rho_experiment.md, backtests/phase4_rho_sweep.md, backtests/phase4_inv_skew_sweep.md, backtests/phase3_obi_experiment.md]
updated: 2026-05-08
---

# HYDROGEL_PACK Parameters

> **Submission attribution (clarified 2026-05-08):** the parameter set documented below is the **post-R3 refinement** baked into `round3/trader_final.py` (the R4 basis). The **R3 submission `486282.py` used earlier values:** `small_move_rho=0.12`, `large_move_rho=0.48`. Both parameter sets produced near-identical real-engine HYDROGEL PnL (R3 $55,100 vs R4 $56,200, 1.99% variance) — the underlying alpha was robust to either calibration. The Phase 4 sweep winner (0.08, 0.42) made it into R4 and beyond, not R3. See [[Performance/Submission_Verification]].

The values below describe the R4 parameter set (as submitted to R4 and used for the realized R4 algo PnL of +$57,048). For the R3 submission's exact parameters, see `performance/algorithmic trading/round 3/486282.py`. Env-var overrides preserved for backtesting.

---

## EMA Fair Value Model

| Parameter | Value | Env var | Source |
|-----------|-------|---------|--------|
| `alpha` (EMA smoothing) | **0.35** | `HYDRO_ALPHA` | v6 sweep: plateau over [0.20, 0.50] |
| `anchor_weight` | **0.20** | `HYDRO_ANCHOR_W` | v6 sweep: dominant improvement (doubled from 0.10→0.20) |
| `anchor_price` | 10,000 | — | Fixed competition reference |
| `small_move_threshold` | 2.0 ticks | — | Fixed |
| `large_move_threshold` | 5.0 ticks | — | Fixed |
| `small_move_rho` | **0.08** | `HYDRO_SMALL_RHO` | Phase 4 fine grid winner |
| `large_move_rho` | **0.42** | `HYDRO_LARGE_RHO` | Phase 4 fine grid winner |

> ⚠️ Planning docs say anchor_weight=0.0 (locked). Code has 0.20. Code is correct. Docs are stale.

---

## Quoting Parameters

| Parameter | Value | Env var | Source |
|-----------|-------|---------|--------|
| `take_threshold` | **2.5** ticks | `HYDRO_TAKE_THRESH` | v6 sweep |
| `passive_edge` | 1.2 ticks | — | Fixed |
| `inv_skew` | **0.03** | `HYDRO_INV_SKEW` | Phase 4 inv_skew sweep (only winner) |
| `passive_quote_size` | 32 units base | — | Fixed |
| `aggressive_size` | 30 (edge<5), 60 (edge≥5) | — | Fixed |
| `spread_threshold` | 16 ticks | — | Fixed — min spread to post passive quotes |

---

## OBI Signal

| Parameter | Value | Env var | Note |
|-----------|-------|---------|------|
| `obi_beta` | **0.0 (disabled)** | `HYDRO_OBI_BETA` | Calibrated: 11.2 (R²=0.089, t=31); net-negative in backtest (-5,218 over 3d) |

---

## Box-and-Lines Signal (Phase 11 — Wired but Off)

| Parameter | Value | Env var | Note |
|-----------|-------|---------|------|
| `box_window` (N) | 200 | `HYDRO_BOX_N` | BNL-02: compromise between signal quality and warm-up |
| `box_bid_alpha` | **0.0 (default)** | `HYDRO_BOX_ALPHA` | BNL-05 REJECTED: all 9 configs fail 2/3-day gate |

---

## Position Limit

| Parameter | Value |
|-----------|-------|
| `LIMIT` | **200** |

---

## v6 Sweep Summary (Phase 2 + Phase 4 Together)

Phase 2 found: `alpha=0.35, anchor_w=0.20, take_thresh=2.5` as the dominant triple.
Phase 4 refined: `small_rho=0.08, large_rho=0.42, inv_skew=0.03`.

Phase 2 key note: The baseline config was Pareto-dominant in the initial 47-config grid — no perturbation improved it. Phase 4 grid then swept rho jointly and found the true optimum.

---

## AR(1) Calibration (from research, for reference)

| Bucket | Move range | AR(1) coef | In-code rho |
|--------|-----------|-----------|-------------|
| Small | 2–5 ticks | -0.094 | 0.08 (sweep winner, slightly lower) |
| Large | ≥5 ticks | -0.237 | 0.42 (sweep winner, higher) |

The sweep winner over-reverts vs pure AR(1) calibration — this acts as a profit multiplier on the passive MM strategy because HYDROGEL's spread is wide enough to absorb the over-correction.

---

## Links

[[Products/HYDROGEL_PACK]] · [[Strategies/Mean_Reversion]] · [[Backtests/Phase4_Rho_Sweep]] · [[Concepts/inventory_risk]] · [[Research/Decisions_Log]]

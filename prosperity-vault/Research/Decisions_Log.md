---
type: research
tags: [decisions, architecture, locked, rationale, all-rounds]
sources:
  - .planning/PROJECT.md
  - .planning/STATE.md
  - .planning/phases/12-counterparty-exploitation/SUMMARY.md
  - .planning/phases/13-r5-directional-trading/13-01-SUMMARY.md
  - .planning/phases/14-r5-strategy-deepening/
  - round3/backtests/
  - round5/strategies/round5_v{34,36,40,41,42}_trader.py
  - report/report.tex
updated: 2026-05-01
---

# Architectural Decisions Log

All locked decisions with evidence and rationale. These are NOT to be reopened without new data.

---

## D1: VELVETFRUIT passive-only hedging

**Decision:** `VEV_PASSIVE_ONLY=True` — never cross the spread for hedging

**Evidence:** Phase 5 experiment. Passive-only beats baseline on all 3 days (+839 total). v2's spread-crossing lost −90K on day 2. The v7 full-OBI trial also confirmed this: additional voucher trades from OBI triggered more VEV spread-crossings, costing −14,573 on VEV alone.

**Why:** Execution cost of spread-crossing outweighs hedge accuracy benefit when options position is small. Passive hedging accumulates correctly over many ticks.

**Status:** LOCKED. Confirmed by Phase 5 all-days-win gate.

---

## D2: IV z-score as passive sizing bias only (not aggressive taking)

**Decision:** `iv_zscore` adjusts passive quote size, not aggressive takes

**Evidence:** v2 aggressive z-take was net-negative after delta-hedge slippage was paid (documented in v2 post-mortem).

**Why:** An elevated IV z-score signals that options may be mispriced, but aggressively taking those options generates a delta exposure that costs more to hedge (spread-crossing) than the vol edge earns.

**Status:** LOCKED.

---

## D3: Active strikes {5300, 5400, 5500} for two-sided quoting

**Decision:** Two-sided passive quoting only on these three strikes

**Evidence:** Microstructure EDA shows symmetric flow on these strikes (vs asymmetric on 5000/5200). Best OBI R² signals.

**Status:** LOCKED (Phase 7 verified).

---

## D4: Bid-only quoting on {5000, 5100, 5200}

**Decision:** Never generate ask orders for these strikes

**Evidence:** 94–98% of observed trades hit the bid — sell-side orders would face adverse selection almost universally.

**Implementation detail:** Multiple guards in code: `bid_only=True`, `allow_sell=False`, delta-bypass conditions also blocked (OPT-05 strictness). Not just a flag — structurally enforced.

**Status:** LOCKED (Phase 7 verified, OPT-05 gate PASS).

---

## D5: OBI disabled for HYDROGEL (obi_beta=0.0)

**Decision:** Do not use OBI signal for HYDROGEL fair value adjustment

**Evidence:**
- Phase 3 experiment (isolated): OBI β=11.2 → net **−5,218** over 3 days (hurt days 0 and 2 significantly)
- v7 full deployment (all products): OBI on all products → **−14,487** total regression (129,056 vs v6 baseline 143,543); HYDROGEL alone: −5,219
- v7b (HYDROGEL β halved to 5.5, voucher OBI on): 135,936 (−7,607)
- v7c (HYDROGEL β halved, all voucher OBI off): 143,065 (−478) — still slightly net-negative

**Why:** R²=0.089 — OBI explains <9% of HYDROGEL variance. The signal shifts quotes away from the mean-reversion target, causing missed fills during strong reversion moves. Even aggressive shrinkage cannot make OBI net-positive on HYDROGEL.

**Note:** The calibrated beta (11.2) is statistically significant (t=31) but the execution cost of OBI-triggered trades outweighs the edge in all configurations tested.

**Status:** LOCKED. OBI wired via env var for future testing, but default=0.0.

---

## D6: anchor_weight=0.20 for HYDROGEL

**Decision:** `anchor_weight=0.20` (pull toward 10,000 anchor)

**Evidence:** v6 joint sweep (hydrogel_sweep.py). Doubling anchor_w from 0.10 to 0.20 was the dominant improvement in v6, generating many more passive fills inside the 16-wide spread. All top-5 v6 configs share w=0.20 (plateau across α and τ).

**⚠️ Contradiction with planning docs:** `PROJECT.md` and `STATE.md` list "anchor_weight=0.0 — Locked". These documents are stale. The code (anchor_w=0.20) is authoritative. The planning docs were written for an earlier version and not updated after v6 recalibration.

**Status:** LOCKED at 0.20. Planning docs need update.

---

## D7: OBI betas set in ACTIVE_CONFIG but sub-resolution

**Decision:** Keep calibrated OBI betas (0.65/0.46/0.49) in options ACTIVE_CONFIG even though Phase 8 shows all configs tie

**Evidence:** Phase 8 sweep — all 8 configs (±20% perturbations) produce identical 146,415.

**Why:** OBI adjustments are sub-resolution in backtest (discrete price levels) but may differentiate in live trading where order book is noisier. Retaining calibrated values has zero backtest cost and potential live upside.

**Status:** LOCKED (retained, not zero-ed).

---

## D8: Box-and-lines signal REJECTED

**Decision:** HYDRO_BOX_ALPHA=0.0, VEV_BOX_BETA=0.0 (defaults — signal disabled)

**Evidence:** Phase 11 Plan 02. 9-config sweep: best result is N=100, α=0.7 → 153,568 (+2), only 1/3 days improved. Gate requires ≥2/3 days improved. All 9 configs fail.

**Why:** HYDROGEL is continuously mean-reverting toward 10,000 — support/resistance boxes form and break immediately. Median box persistence = 0 ticks across all window sizes.

**Status:** LOCKED (null result). Signal code remains wired for future research with new data.

---

## D9: Box N=200 chosen (BNL-02)

**Decision:** Box detection window N=200 (even though signal is disabled)

**Evidence:** BNL-02 sweep showed median persistence = 0 for all N. N=200 chosen as compromise: small enough to warm up quickly (200 ticks), large enough to capture meaningful range structure if it exists.

**Status:** Locked as infrastructure default.

---

## D10: No compound untested changes (research §8)

**Decision:** VEV box beta sweep skipped — no HYDRO winner

**Rationale:** Do not stack two experimental signals simultaneously. If HYDRO box fails, running VEV box on top of a failed HYDRO box creates confounded results.

**Status:** Policy decision. Applies to all future signal research.

---

## D11: Bio-Pod bids — Bayesian-Nash equilibrium solution

**Decision:** Submit b1=755, b2=840 for the Round 3 Bio-Pod manual auction

**Evidence:** Full Bayesian-Nash derivation (report §Bio-Pod):
- 51 reserve price levels, uniform on {670, 675, ..., 920}; resell at 920
- Symmetric-NE continuous solution: b1*=753.3̄, b2*=836.6̄; discrete snap → (755, 840)
- Exhaustive 51×51 grid search confirms (755, 840) is the unique global maximum
- Per-counterparty EV = 81.67 XIRECs; each bid covers exactly 17/51 reserve levels
- Stability: all ±1 grid-step deviations strictly worse; cubic penalty makes b2 deviation −4.43 pts

**Why:** The optimal structure is elegant: three equally-likely outcomes per counterparty (first-bid trade / second-bid trade / no trade), each covering 1/3 of the reserve distribution. Bid too high → margin collapse; bid too low → miss counterparties unnecessarily.

**Status:** LOCKED (mathematical optimum, not data-driven).

---

---

## D12: Mark composite flow score (R4)

**Decision:** Track `mark_net = (Mark 67 buy events) − (Mark 49 sell events)`; tilt VEL passive bid by +3 when ≥ 5 (bullish), trim by 2 when ≤ −3 (bearish). Reset at day boundary.

**Evidence:** R4 RESEARCH §Mark taxonomy. Mark 67 net +1,510 VEL across 3 days (never sells, 92.7% buy at below-5-MA = local lows). Mark 49 net −956 VEL (passive local-high seller, ~36 events/day). Mark 22 excluded (frequency mismatch 184/day vs 50/36).

**Why:** Streaming Bayesian-evidence accumulator (SPRT-style). Two reliable Mark-signals are enough to define a regime; mixing in higher-frequency Marks would dominate the score.

**Status:** LOCKED for R4 submission. Backtest-neutral (CSV is deterministic; Mark IDs are baked in). Live impact unknown but designed to fail safe.

---

## D13: Mark 49 cooldown anchor on `state.timestamp` not `trade.timestamp` (R4)

**Decision:** When Mark 49 detected, halve VEL passive bid size for 500ms (5 ticks). Anchor cooldown on `state.timestamp` at detection time, not `trade.timestamp` from the Trade object.

**Evidence:** Phase 12 bug 2: `mark49_last_ts = trade.timestamp` produced stale anchor (the trade timestamp refers to the prior tick due to one-tick lag in the Prosperity datamodel).

**Why:** The cooldown is meant to suppress quoting after detection of Mark 49 in the current tick. The Trade object's `timestamp` is the tick the trade *happened*, not the tick we *observed* it.

**Status:** LOCKED.

---

## D14: Scan both `state.market_trades` and `state.own_trades` (R4)

**Decision:** Counterparty scanner iterates `(state.market_trades, state.own_trades)` for VEL trades, not just `market_trades`.

**Evidence:** Phase 12 bug 4: `state.market_trades` only contains trades where neither side is the bot. Direct fills with us go to `state.own_trades`. Pre-fix, ticks where Mark 67 took our ask exclusively were undercounted by 100%.

**Why:** Prosperity datamodel splits trades into two non-overlapping collections; both are needed for a complete view of counterparty activity.

**Status:** LOCKED.

---

## D15: AETHER_CRYSTAL chooser arbitrage (R4 manual)

**Decision:** SELL AC_50_CO (chooser, K=50, T=21d/14d), BUY AC_50_C (3w call), BUY AC_50_P_2 (2w put). Static replication for r=0 GBM.

**Evidence:** Chooser fair value = max(C(T), P(T_c)) at chooser-decision time T_c. Under r=0, put-call parity gives static replication: chooser = C(T) + P(T_c). Market chooser bid = 22.20 vs BS fair = 21.90 → +0.30 sell edge per unit.

**Why:** Pure no-arbitrage edge. Volume 50, contract multiplier 3000 → +0.30 × 50 × 3000 = +45,000 XIREC if filled at the bid. Hedged exactly by the long C+P legs.

**Status:** Submitted in R4 manual portfolio.

---

## D16: AETHER_CRYSTAL binary cliff hedge (R4 manual)

**Decision:** SELL AC_40_BP (binary put, K=40, payout 10), BUY AC_50_P (3w put), SELL AC_40_P (3w put). Bull put spread bounds max loss.

**Evidence:** Binary put fair = N(−d₂) × payout = 4.768 vs market bid 5.00 → +0.232 sell edge. Naked sell exposes us to max loss = payout = 10 per unit if S < 40 at expiry. The bull put spread (long 50P short 40P) caps the downside at the strike differential, reducing per-pair max loss from −5 to −0.55.

**Why:** Cliff payoffs (binaries) are dangerous to short naked. The vanilla spread converts the cliff into a smooth payoff, sacrificing some edge for bounded risk.

**Status:** Submitted in R4 manual portfolio. See [[Strategies/Structural_Hedging]].

---

## D17: AC_60_C SKIPPED (R4 manual)

**Decision:** Do NOT take the +0.004 sell edge on AC_60_C (3w OTM call).

**Evidence:** σ = 251%, K = 60 (OTM by ~$10), no hedge in the portfolio. Naked short OTM call has unbounded upside risk. Edge per unit (+0.004) × 50 units × 3000 mul = +600 XIREC; potential blow-up loss is unbounded.

**Why:** "Don't let position control you" advisor principle. Tiny edges with unbounded loss tails are negative-EV after risk-adjustment.

**Status:** LOCKED. The portfolio delta is already balanced without this leg.

---

## D18: R5 directional-not-MM strategy shape (R5)

**Decision:** R5 uses a 2-layer architecture: Layer 1 directional (fixed ±10 on multi-day-drift products) + Layer 2 MM (everything else, with TIER3/blacklist refinements). Do NOT attempt R3-style passive MM as the primary engine.

**Evidence:** EDA finding: **AR(1) ρ ≈ 0.999 across all 50 R5 products** (`round5/research/eda.py`). Mean-reversion impossible at tick level. Position limit ±10 caps inventory; with no reversion to harvest, MM-spread alone cannot recoup adverse-selection cost on tight-spread products.

**Why:** Strategy shape must match data shape. R3 had ρ_AR1 ≈ −0.13 (clean reversion, MM works); R5 has ρ_AR1 ≈ 0.999 (random walk with drift, directional works).

**Status:** LOCKED at Phase 13. All v1→v42 iterations preserved this architecture.

---

## D19: OOS_DAY = 4 pre-registered constant (R5)

**Decision:** Top-level constant `OOS_DAY = 4` in `round5/research/eda2/loaders.py`, committed before any analysis ran. Train days = [2, 3]. Day 4 is **never** used for parameter fitting.

**Evidence:** Phase 13 MICROCHIP_SQUARE flip — train days 2+3 showed +$2,456/+$3,438; day-4 OOS reversed to −$2,278. A signal that scores well on the train average can be entirely driven by 1 of 2 train days.

**Why:** Pre-registration is the textbook anti-leakage move from ML. If you can change the OOS day after seeing results, you can always P-hack a "win".

**Status:** LOCKED for all R5 analyses.

---

## D20: Cross-version Prosperity log evidence > local backtester (R5)

**Decision:** Tier and blacklist decisions use the N=12 Prosperity log evidence (`round5/research/analyze_prosperity_logs.py`), NOT local backtester data.

**Evidence:** v35 was a careful local-CV reclassification (train-test split, OOS gating). It dropped PEBBLES_M/L from directional and promoted PANEL_1X4/EVENING_BREATH to TIER1 — all wrong on real Prosperity. v35 underperformed v34 by ~$9K. Local backtester `--match-trades all` is documented as ~8.6× fill-inflated vs real Prosperity (per `README.md`; the exact comparison script is not preserved but the empirical conclusion is canonical).

**Why:** Distribution shift. Local-BT counterparty mix differs from real Prosperity. Train/eval discipline only helps if both halves come from the deployment distribution.

**Status:** LOCKED. v36→v42 all use Prosperity logs only for tier/blacklist decisions.

---

## D21: Adverse-selection-prone products → blacklist, not aggressive MM (R5)

**Decision:** Products with avg PnL ≤ −$500 across N=12 Prosperity runs AND 0/12 positive runs are excluded from MM entirely (`MM_BLACKLIST`). Borderline products (small loss, mixed positivity) get reduced LIMIT (`TIER3 = 5`).

**Evidence:** v40 hypothesised "more trades on full day = recovery" and removed TIER3 (LIMIT 5 → 10) on 9 products. **Backtester loss vs v34: −$6,536, concentrated in those 9 products.** Promoting LAMB_WOOL to directional +10: −$5,978.

**Why:** Adverse-selection losses scale **with** trading volume, not against. If `s̄_p + α_p < 0` for product p, every trade is negative-EV; more trades = more losses. The L2-style "shrink LIMIT" works at the margin; for hopeless products, the L1 (LIMIT=0 / blacklist) is correct.

**Status:** LOCKED in v42. 7 ex-TIER3 products + LAMB_WOOL blacklisted.

---

## D22: HEDGED_NO_SKEW for SNACKPACK CHOC/VAN (R5)

**Decision:** SNACKPACK_CHOCOLATE and SNACKPACK_VANILLA are MM'd with bigger inner size (8 vs default 6) and standard skew threshold (rarely triggers). The natural ρ = −0.916 anti-correlation between them provides the inventory hedge.

**Evidence:** `round5/plots/within_category_xcorr_summary.csv` shows ρ_returns = −0.915909 across days 2/3/4 (day-averaged). Strongest contemporaneous within-category anti-correlation in the dataset alongside STRAW/RASP (−0.924).

**Why:** When two products are tightly anti-correlated, per-product inventory skew over-regularizes — the inventory risk on one is naturally offset by inverse inventory on the partner. Letting positions accumulate freely with bigger quotes captures more spread without adding aggregate exposure.

**Status:** LOCKED from v34 through v42 (every revision preserved this).

---

## D23: PEBBLES basket directional completion (R5)

**Decision:** PEBBLES_XL +10 (long), PEBBLES_S −10, PEBBLES_M −10, PEBBLES_L −10, PEBBLES_XS −10 — long the largest, short all others.

**Evidence:** Within-category correlation analysis (`round5/research/pairs_analysis.py`): PEBBLES sub-variants are anti-correlated with PEBBLES_XL at ρ ≈ −0.5. Sign-stable drifts on all 3 days for PEBBLES_S/XS; mixed for M/L (added in v34 as basket completion based on category-level correlation, not individual drift).

**Why:** Structural basket: when PEBBLES_XL goes up, the smaller pebbles tend down. The directional bet captures both sides of the basket trend instead of fighting it. v34 verified this is +$2K Prosperity.

**Status:** LOCKED in v42.

---

## D24: SNACKPACK_STRAWBERRY +10 directional (R5)

**Decision:** Add SNACKPACK_STRAWBERRY +10 to TARGETS_DIR in v41/v42.

**Evidence:** Day-2/3/4 drifts: +436 / +358 / +98 (all positive). Backtester loss only −$199 (favorable risk/reward). Considered SLEEP_POD_LAMB_WOOL similarly but day-4 drift was only +16 → rejected (recovery fragile).

**Why:** Sign-stable across 3 days + small backtester loss + meaningful full-day drift = directional add. The criterion is not "biggest drift" but "stable sign + favorable backtester-to-full-day-drift ratio".

**Status:** LOCKED in v42.

---

## D25: v42 final blacklist of 8 confirmed losers (R5)

**Decision:** Blacklist 7 ex-TIER3 (`OXYGEN_SHAKE_MORNING_BREATH`, `GALAXY_SOUNDS_DARK_MATTER`, `PANEL_2X2`, `ROBOT_LAUNDRY`, `PANEL_1X2`, `PANEL_1X4`, `OXYGEN_SHAKE_MINT`) + `SLEEP_POD_LAMB_WOOL`. Keep MICROCHIP_RECTANGLE and OXYGEN_SHAKE_EVENING_BREATH at TIER3.

**Evidence:** v34 + v40 backtester evidence: each blacklisted product loses meaningfully in BOTH versions. v40's un-TIER3 of these 7 doubled the loss vs v34's TIER3. LAMB_WOOL: −$4,284 (v34 default-MM) and −$5,978 (v40 directional +10) — losing in every configuration tried.

**Why:** Combines v36's aggressive blacklist methodology (cross-version evidence) with v34's full-day-correct directional setup. Best of both lineages.

**Status:** LOCKED, **submitted as final v42**.

---

## Links

[[Products/HYDROGEL_PACK]] · [[Products/VELVETFRUIT_EXTRACT]] · [[Strategies/OBI_Signal]] · [[Strategies/Counterparty_Exploitation]] · [[Strategies/Directional_Holding]] · [[Strategies/TIER3_Market_Making]] · [[Strategies/HEDGED_NO_SKEW]] · [[Strategies/Cross_Version_Blacklist]] · [[Backtests/Phase3_HYDROGEL_FV]] · [[Backtests/Phase8_OBI_Sweep]] · [[Backtests/Phase11_Box_Signal]] · [[Backtests/Phase12_Counterparty]] · [[Backtests/Phase13_R5_Directional]] · [[Concepts/Backtester_vs_Competition]] · [[Concepts/Adverse_Selection]] · [[Parameters/HYDROGEL_Params]] · [[Parameters/Round5_Params]]

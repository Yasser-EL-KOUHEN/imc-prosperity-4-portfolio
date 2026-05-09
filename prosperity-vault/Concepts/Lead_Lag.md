---
type: concept
tags: [round5, lead-lag, cross-correlation, null-result, multiple-testing, bonferroni]
sources:
  - round5/research/lead_lag.py
  - round5/research/lead_lag_within_cat.py
  - round5/plots/lead_lag/lead_lag_pairs.csv
  - round5/plots/lead_lag/top_leaders.csv
  - round5/plots/lead_lag/asymmetry_scores.csv
updated: 2026-04-30
---

# Lead-Lag Cross-Correlation (R5 Null Result)

## What It Is

For two products A and B, the **lagged cross-correlation function** is:

$$\rho_{A \to B}(k) = \mathrm{corr}(r_A[t], r_B[t + k])$$

where `r_X[t] = mid_X[t+1] − mid_X[t]` is the tick return. If A "leads" B, we expect $\rho_{A \to B}(k) > 0$ for some lag $k > 0$ — A's move at time $t$ predicts B's move $k$ ticks later.

**Tradable lead-lag** would let us trade B based on observed moves in A. This is a classic intraday alpha and is well-documented for ETFs vs constituents, futures vs spot, etc.

**ML analogy:** Lead-lag is a **causal-prediction features test** — does $r_A$ at time $t$ contain incremental information about $r_B$ at time $t+k$ beyond $r_B$'s own past? In ML terms: feature importance of A's lagged returns in a model predicting B's next return.

## R5 Methodology

`round5/research/lead_lag.py` ran the test exhaustively:

```python
LAGS = [1, 2, 5, 10, 20]      # tick units
RHO_MIN = 0.10                 # tradable threshold
ASYMMETRY_MIN = 0.05           # clearly directional, not bidirectional
```

**Filters applied for "tradeable" leader-follower pair**:
1. `|ρ| > 0.10` at best lag
2. Bonferroni-corrected p-value < 0.05
3. Same-direction lead on **all** of days 2, 3, 4 (stability)
4. Asymmetry score > 0.05 — `S(A→B) = max_{k>0} ρ_{A→B}(k) − max_{k>0} ρ_{B→A}(k)` (clearly directional, not bidirectional)

## Bonferroni Correction Math

**n_tests** = pairs × lags × days × directions
       = $\binom{50}{2} \times 5 \times 3 \times 2$
       = $1{,}225 \times 5 \times 3 \times 2$
       = **36,750**

**Bonferroni α** = $0.05 / 36{,}750$ ≈ **1.36×10⁻⁶**

This is appropriately conservative for a search this wide. With 36,750 independent tests at nominal α=0.05, you'd expect ~1,837 false positives by chance — Bonferroni protects against finding "lead-lag" that is just multiple-testing noise.

## Result: Zero Pairs Survived

`plots/round5/lead_lag/top_leaders.csv` has **header only** — no rows. Zero pairs passed the filter chain.

| Filter | Pairs surviving |
|---|---|
| Initial 36,750 tests computed | 36,750 |
| `|ρ|` ≥ 0.10 | small handful |
| Bonferroni p < 1.36e-6 | very few |
| 3-day same-direction stability | 0 |
| Asymmetry score > 0.05 | 0 |

## Why This Is a Confirmed Null, Not a Failure to Find

A null result is meaningful when the test had **adequate power** to detect a real effect. Here:
- N=10,000 ticks per product per day → standard error on |ρ| is ~1/√10,000 = 0.01 per day, ~0.006 across 3 days. The 0.10 threshold is 10–17 standard errors above noise.
- 1,225 pair × 5 lag × 3 day grid covered every plausible relationship
- Bonferroni at α=0.05/36,750 = 1.36e-6 corresponds to z-score ≈ 4.85 — strong enough to reject most spurious findings
- Asymmetry score filter prevents claiming "lead" for symmetric (bidirectional) relationships

The data **could** have produced a tradable lead-lag if one existed at this scale. It didn't. R5 has **no exploitable lead-lag at the tested horizons** (1 to 20 ticks).

## What This Doesn't Rule Out

- **Cross-day or session-level lead-lag** (slower than 20 ticks)
- **Lead-lag conditional on regime** (e.g. only during news events)
- **Higher-order dependencies** that aren't captured by linear correlation
- **Within-pair structural relationships** that aren't lead-lag (e.g. SNACKPACK CHOC/VAN ρ=−0.92 is **contemporaneous** anti-correlation, not lead-lag)

In R5's actual structure, all tradable cross-product alpha came from **contemporaneous correlation** (pairs trading via HEDGED_NO_SKEW; PEBBLES basket directional). Lead-lag was simply absent.

## Pitfalls Avoided

- **Spurious cross-correlation in random walks.** Two independent random walks of length N have sample correlation ~N(0, 1/√N). For N=10,000, σ ≈ 0.01 — and with 1,225 pairs, you expect several |ρ| > 0.05 by chance. **Mitigation:** correlations were computed on **first differences** (tick returns), not levels. Random-walk-on-levels spurious correlation does not transfer to returns.
- **Multiple testing inflation.** At naive α=0.05, ~1,837 false positives expected. **Mitigation:** Bonferroni at α=0.05/n_tests = 1.36e-6 (also could have used BH-FDR; Bonferroni is more conservative and we used it for a clean null).
- **Day-specific outliers.** A pair could lead on day 2 only. **Mitigation:** required same-direction lead on **all 3 days**.

## ML Analogy: Why a Null Result Is Valuable

In ML, a feature that fails a per-fold + multiple-testing-corrected test is a feature you **don't add to the model**. It's not "we couldn't find the right hyperparameter" — it's "this feature has no predictive content at the resolution we measured."

For R5, the null result **simplified strategy design**: no need to add lead-lag computation to the trader, no need to maintain cross-product state, no need to debug latency in cross-product signal flow. The competition's "embedded patterns" hint pointed to within-product drift and within-category basket structure — not lead-lag.

This is the right kind of null result: **strong test, conservative correction, clean result**, properly documented in `plots/round5/lead_lag/lead_lag_pairs.csv` (all 36,750 rows preserved for re-analysis).

## Within-Category Variant (also null)

`round5/research/lead_lag_within_cat.py` ran the same test restricted to within-category pairs (5×4/2 = 10 pairs per category × 10 categories = 100 pairs × 5 lags × 3 days × 2 directions = 3,000 tests). Bonferroni at 0.05/3,000 = 1.67e-5. **Same null result** — `within_cat_strict.csv` has no surviving rows under the strict filter.

## Links

[[Rounds/Round5_findings]] · [[Concepts/Order_Book_Imbalance]] · [[Strategies/HEDGED_NO_SKEW]] · [[Backtests/Phase14_R5_EDA]] · [[Concepts/Backtester_vs_Competition]] · [[Research/Round5_Scripts]]

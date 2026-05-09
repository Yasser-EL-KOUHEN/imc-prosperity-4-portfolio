---
type: manual
tags: [round2, manual, first-price-auction, bidding-game, maf]
sources:
  - report/report.tex (§Round 2 Part B: MAF bid game theory)
  - context/Round 2/# Round 2 - "Growing Your Outpost".txt
updated: 2026-05-02
---

# Round 2 Manual — Market Access Fee (MAF) Auction

**Submitted:** $b = 3{,}000$ XIREC · **Method:** Asymmetric-regret-aware blind first-price bid

> **Verified outcome (algo JSON, 2026-05-08): MAF bid was ACCEPTED.** The R2 algo JSON (submission 362752) shows raw PnL **94,529** before the MAF fee. User-reported R2 algo of **91,529** = 94,529 − **3,000** (bid amount paid). The earlier "rejected" inference was *wrong* — it conflated normal day-to-day variance with the MAF fee.
>
> **Why the bid didn't visibly help:** The +25% quote-flow bonus was largely absorbed by structural caps. R1 IPR $79,255 vs R2 IPR $79,199 — **essentially identical** (IPR was bandwidth-saturated near +0.1/tick capacity). R1 ACO $18,917 vs R2 ACO $15,330 — within normal variance. Net effect of MAF participation: roughly **−3K to −6K** vs not bidding (the bid fee minus any small lift). **Lesson revised:** the bid wasn't too low (we won the auction); the *value* of winning was lower than the BS-implied $5–7K because the strategy was bandwidth-saturated, not quote-bound.

## The Mechanic

Top 50% of bidders (by bid amount) win **+25% quote flow** for Round 2 and pay their bid (first-price). Bid is **blind** — submitted before peer bids are revealed.

Payoff:

$$\pi(b) = \begin{cases}
V_{\text{extra}} - b & \text{if } b > B_{\text{med}} \text{ (accepted)} \\
0 & \text{if } b \leq B_{\text{med}}
\end{cases}$$

Where $V_{\text{extra}}$ = expected PnL lift from +25% volume, $B_{\text{med}}$ = median bid (unknown).

## Estimating $V_{\text{extra}}$ (website-scaled)

The Round-1 local backtester reported 291,170 XIREC; the **website actually scored 168K**. The ~42% gap is queue-illusion cost — even `--match-trades=worse` under-models real-server queue priority. **All $V_{\text{extra}}$ estimates must be scaled to website PnL, not local.**

**Per-product estimate at +25% volume:**

| Product | Website PnL | $+25\%$ effect | $V_{\text{extra}}$ contribution |
|---|---|---|---|
| **IPR** | ~140K | Greedy-aggressive takes; near-ceiling regardless of queue | $\le 500$ (only saves accumulation latency) |
| **ACO** | $\approx 53{,}116 \times \frac{168}{291} \approx 31$K | Passive fills are queue-sensitive; +25% quotes ⇒ more fill opportunities | $\approx 0.2 \times 31 \approx 6$K |

**Point estimate:** $V_{\text{extra}} \in [5{,}000, 7{,}000]$ XIREC website-scaled (NOT $10$–$13$K as a naive read of the local backtest would suggest).

## Asymmetric Regret

- **Miss low** (bid below median, lose entirely): lose full $V_{\text{extra}} \approx 6$K
- **Miss high** (bid above optimum, paid more than necessary): lose only the excess

**Regret ratio: $V_{\text{extra}} / 1\text{K} = 6$-to-1 against under-bidding.** Under loss-aversion, you bid **higher** than the EV-optimal bid because the downside of losing the auction is much worse than the downside of overpaying.

## Expected-Profit Sweep

Peer-bid prior: median $\sim$1,500, right-skewed (many bid 0, few bid 10K+).

| $b$ | $p(b > B_{\text{med}})$ | $\pi$ at $V_{\text{ex}}=6$K | $\pi$ at $V_{\text{ex}}=10$K |
|---|---|---|---|
| 1,000 | 0.35 | 1,750 | 3,150 |
| 2,000 | 0.60 | 2,400 | 4,800 |
| **3,000** | **0.80** | **2,400** | **5,600** |
| 4,000 | 0.90 | 1,800 | 5,400 |
| 5,000 | 0.95 | 950 | 4,750 |

**Optimum:** $b = 3{,}000$ — peak at $V_{\text{ex}}=6$K, **near-peak** at $V_{\text{ex}}=10$K, **80% win probability** under the peer prior.

## Why Not 4,000 (More Conservative)?

A bid of 4,000 raises win probability to ~90% but reduces expected PnL because:
- At $V_{\text{ex}}=6$K, $\pi(4000) = 0.9 \times 2{,}000 = 1{,}800$ (worse than $\pi(3000) = 2{,}400$)
- The bid 3,000 already covers 80% of the win probability mass; the marginal 10% costs +1,000 in bid

The 3,000 / 4,000 choice is essentially an **expected-value vs sleep-at-night** tradeoff. The user chose EV.

## Recommendation Code

```python
class Trader:
    def bid(self) -> int:
        return 3000
    def run(self, state):  # unchanged from Round 1
        ...
```

Note: the `bid()` method is **ignored** by the local backtester and in R1/3/4/5 submissions. This is a Round-2-only construct.

## ML Analogy

Bidding under peer-uncertainty is a **bandit with delayed feedback**: you commit to a bid before observing the peer median. The asymmetric regret structure makes this a **risk-averse decision-theoretic problem**, not a pure-EV problem. The right framework is **expected utility** with a concave utility function, but in practice the EV-maximization with a small upward shift (80% win threshold) approximates this without explicit utility-curve fitting.

The peer-prior estimation is the load-bearing assumption. If the actual peer median is 5K instead of 1.5K, the decision flips entirely.

## Realized vs Expected

| | Expected | Realized |
|---|---|---|
| Bid | 3,000 | 3,000 (submitted) |
| Win probability | 80% | **(not yet provided)** — see [[User_Reported_Anchors]] |
| $V_{\text{extra}}$ realized | $[5K, 7K]$ | **(not yet provided)** |

The realized R2 algo PnL minus the expected R1-carryover PnL is the empirical $V_{\text{extra}}$. Both are unknown to the wiki without user-provided ground truth.

## Links

[[Rounds/Round2_findings]] · [[Manuals/Invest_and_Expand]] · [[Manuals/Bio_Pods]] · [[Strategies/manual_trading]] · [[User_Reported_Anchors]] · [[Carry_Forward]] · [[Performance/Algo_Per_Round]] · [[Performance/Manual_Per_Round]]

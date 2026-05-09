---
type: round
tags: [round2, complete, manual, maf, invest-expand, aco, ipr]
sources: [rounds/round2/trader.py, report/report.tex, .planning/STATE.md]
updated: 2026-04-27
---

# Round 2 — "Growing Your Outpost"

## Status

Complete — 3-part structure: algo trading (ACO + IPR) + MAF bid + Invest & Expand manual.

## Final-Result Reconciliation (2026-05-08)

R2, like R1, was qualifier-only — does **not** enter the final GOAT total (R3+R4+R5 = 383,727). End-of-R2 cumulative was **414,546 XIREC** at rank **#1,522**.

| Component | Realized PnL |
|---|---|
| R2 algo (ACO + IPR + MAF bid=3,000) | **+91,529** |
| R2 manual (Invest & Expand at (18,60,22)) | **+153,345** |
| R2 round total | 244,874 |

**End-of-R2 cumulative ranks:** Overall #1,522 · Algo #857 · Manual #801 · Country #59.

**R2 manual at +153,345 over-performed** the FOC-optimal theoretical (110,065 at (16,48,36)). Submitting (18,60,22) — the bottom-heavy-prior allocation — was the right call. Realized V(22) = **0.38** (Prosperity-reported hit rate), between uniform-rank (0.276) and bottom-heavy (0.900). The actual peer-prior was meaningfully bottom-heavy. Speed rank: **#2,801**.

**MAF correction (REVERSED):** the bid was **ACCEPTED**, not rejected. Algo JSON shows raw R2 PnL = **94,529** before the fee; the user-reported 91,529 = 94,529 − **3,000** (= fee paid). Earlier "rejected" inference was wrong — the −7K gap was not no-bid baseline, it was a small day-to-day variance (−3,643 raw) plus the 3,000 fee. R1 IPR ($79,255) and R2 IPR ($79,199) were essentially identical, meaning the +25% volume bonus was absorbed by IPR's bandwidth cap. **Revised lesson:** the bid won the auction; the *value* of winning was lower than the BS-implied $5–7K because the strategy was bandwidth-saturated, not quote-bound. See [[Performance/Algo_Per_Round|algo per-round breakdown]] and [[Manuals/MAF]].

---

## Part 1: Algorithmic Trading

**Products:** Same as Round 1 — ASH_COATED_OSMIUM (ACO) + INTARIAN_PEPPER_ROOT (IPR)

- Trading logic **identical** to Round 1 v3 (FV anchor blend, book-anchored quotes, greedy IPR accumulation)
- Round 2 `trader.py` adds only one method: `Trader.bid()` returning the MAF bid
- No new products were introduced for the algo component

See [[Products/ASH_COATED_OSMIUM]] and [[Products/INTARIAN_PEPPER_ROOT]] for full strategy details.

---

## Part 2: MAF Bid Framework

**Type:** Market Access Fee auction — one-time sealed bid for bonus quote volume

**Mechanism:**
- Submit a bid *b* in XIREC
- Win if `b ≥ threshold` (threshold drawn from unknown distribution)
- If you win: pay *b*, receive extra quote volume worth `V_extra = 6,000 XIREC` (website-scaled)
- Net profit if winning: `V_extra − b`

### Asymmetric-Regret Analysis

Let `p(b)` ≈ probability of winning at bid level `b`. Objective:

```
E[profit] = p(b) × (V_extra − b)
```

For `V_extra = 6,000` and competitor bid distribution modelled as sparse:

| b (bid) | P(win) | Net if win | E[profit] |
|---------|--------|------------|-----------|
| 1,000 | ~30% | 5,000 | 1,500 |
| 2,000 | ~55% | 4,000 | 2,200 |
| **3,000** | **~80%** | **3,000** | **2,400** |
| 4,000 | ~92% | 2,000 | 1,840 |
| 5,000 | ~98% | 1,000 | 980 |

**Winner: b* = 3,000 XIREC** — maximises E[profit] at ~80% win probability and ~3,000 XIREC net gain.

Asymmetric regret: overbidding is cheap (you win but pay more); underbidding is expensive (you lose the volume bonus entirely). This justifies bidding higher than the naive EV midpoint.

### Code

```python
def bid(self) -> int:
    return 3000  # ~80% win probability at V_extra=6K; ~3K net profit
```

---

## Part 3: Invest & Expand

**Type:** Portfolio allocation manual problem — allocate 100 points across 3 investment options

**Setup:** Three investment pillars — **Research** (log return, saturates at 200K), **Scale** (linear return), **Visibility** (rank-based multiplier, competitive). Budget cost = 500 × (xR+xS+xV). See [[Manuals/Invest_and_Expand]] for the full derivation.

### Solution Method

Enumerate all valid integer allocations summing to 100, compute expected value for each, find the maximum.

**Exact mathematical optimum:**

```
x_R = 16,  x_S = 48,  x_V = 36
PnL = 110,065 XIREC
```

> Common near-miss: (15, 50, 35) — close but NOT optimal. The correct solution is (16, 48, 36).

### Key Lesson

Gut-feel allocation (20, 40, 40) was significantly worse. When the search space is small enough to enumerate fully (~5,000 integer triples), always enumerate — intuition fails on non-linear return surfaces.

**ML analogy:** Grid search over a discrete hyperparameter space. The objective function (expected PnL) is not convex, so gradient intuition misleads. Exhaustive search on a small grid is exact and cheap.

---

## Lessons from Round 2

| Lesson | Category |
|--------|---------|
| EV calculation beats intuition for allocation problems | Manual trading |
| Asymmetric regret analysis for auction bids: overbid slightly | Manual bidding |
| Enumerate fully when the search space is tractable | General research |
| Algo PnL and manual PnL are independent — treat separately | Competition mechanics |
| Game theory applies to sealed-bid auctions | Manual bidding |

---

## Links

[[Products/ASH_COATED_OSMIUM]] · [[Products/INTARIAN_PEPPER_ROOT]] · [[Strategies/manual_trading]] · [[Manuals/MAF]] · [[Manuals/Invest_and_Expand]] · [[Rounds/Round1_findings]] · [[Rounds/Round3_findings]] · [[Competition/Game_Mechanics]]

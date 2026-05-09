---
type: manual
tags: [round1, manual, stale-order-book, clearing-price, auction, intarian-welcome]
sources:
  - report/report.tex (§Dryland Flax; §Ember Mushroom; §Round 1 Manual Summary)
  - context/Round 1/# Round 1 - "Growing Your Outpost".txt
updated: 2026-05-06
---

# Round 1 Manual — "Intarian Welcome" Auction

**Combined outcome:** 71,500 XIREC · **Method:** Stale-order-book clearing-price engineering

> **Verified result (leaderboard 2026-05-08):** **+71,500 realized**. End-of-R1 cumulative manual rank **#72** (≈ **#3,000 without ties**). Realized exactly the theoretical (5,000 + 66,500) — clearing-price engineering executed cleanly. The display rank #72 is essentially random tie-breaking: Dryland Flax + Ember Mushroom is a deterministic puzzle and many teams solved it identically.

Round 1's manual challenge ("Intarian Welcome") is a **stale double-auction**: the order book is shown to all players before the clearing event. Each participant can submit one order. The clearing price $P^*$ is the price that maximises traded volume. Each participant gets filled at $P^*$ if their bid/ask is compatible, but only the marginal volume needed to achieve $V(P^*)$ fills.

**Two goods were available:** Dryland Flax and Ember Mushroom.

---

## Good 1 — Dryland Flax

**Liquidation price = 30; no fees. Net per unit = 30 − P*.**

### Stale Order Book

| Bids | | | Asks | |
|---|---|---|---|---|
| Volume | Price | | Price | Volume |
| 30k | 30 | | 28 | 40k |
| 5k | 29 | | 31 | 20k |
| 12k | 28 | | 32 | 20k |
| 28k | 27 | | 33 | 30k |

### Without Our Order

| $P$ | Supply ($\leq P$) | Demand ($\geq P$) | $V(P) = \min$ |
|---|---|---|---|
| 28 | 40k | 47k | **40k ← clearing** |
| 29 | 40k | 35k | 35k |
| 30 | 40k | 30k | 30k |

Without us, $P^* = 28$ (volume 40k). At $P^* = 28$, bids above 28 total 35k; existing 12k@28 absorbs the remaining 5k. **We get 0 fills** (queue position lost to existing 12k@28).

### Shifting Clearing to P* = 29

Adding our bid $B \geq 29$, quantity $Q$:

$$V(29) = \min(40\text{k},\; 35\text{k} + Q) = 40\text{k} \iff Q \geq 5\text{k}$$

With $Q = 5\text{k}$, $V(29) = V(28) = 40\text{k}$; tie broken **upward** to $P^* = 29$.

At $P^* = 29$: supply 40k; bids $> 29$ fill 30k; existing 5k@29 fills 5k; remaining capacity $= 40\text{k} - 30\text{k} - 5\text{k} = 5\text{k}$ → **we fill 5k**.

### Optimal Order

$$\text{BUY } 5{,}000 @ 29 \quad \Rightarrow \quad \Pi_{\text{Flax}} = 5{,}000 \times (30 - 29) = \mathbf{5{,}000} \text{ XIREC}$$

**Why not bid higher?**
- Bidding $\geq 30$ shifts $P^* = 30$, yield per unit $= 30 - 30 = 0$.
- Bidding $\leq 28$ leaves $P^* = 28$, zero fills.
- Minimum required quantity $Q = 5\text{k}$ to overcome the tie.

---

## Good 2 — Ember Mushroom

**Liquidation = 20; total fee = 0.10. Net per unit = 19.90 − P*.**

### Stale Order Book

| Bids | | | Asks | |
|---|---|---|---|---|
| Volume | Price | | Price | Volume |
| 43k | 20 | | 12 | 20k |
| 17k | 19 | | 13 | 25k |
| 6k | 18 | | 14 | 35k |
| 5k | 17 | | 15 | 6k |
| 10k | 16 | | 16 | 5k |
| 5k | 15 | | 18 | 10k |
| 10k | 14 | | 19 | 12k |
| 7k | 13 | | | |

### Analysis

The book is heavily bid-side heavy (43k @ 20 alone). The clearing analysis shows that BUY orders @ 18 create a volume equilibrium at $P^* = 18$, where the demand side (bids ≥ 18 = 6k+17k+43k = 66k + our Q) exceeds supply at 18 (35k+25k+20k = 80k total supply below 18... need more detailed volume curve analysis).

Working from the report's solution: **BUY 35k @ 18** → clears at $P^* = 18$ → fills 35,000 units.

$$\Pi_{\text{Mushroom}} = 35{,}000 \times (19.90 - 18) = 35{,}000 \times 1.90 = \mathbf{66{,}500} \text{ XIREC}$$

---

## Combined Result

| Good | Order | Clearing $P^*$ | Our fill | Profit |
|---|---|---|---|---|
| Dryland Flax | BUY 5k @ 29 | 29 | 5,000 | **5,000** |
| Ember Mushroom | BUY 35k @ 18 | 18 | 35,000 | **66,500** |
| **Combined** | | | | **71,500** |

Reported as ~70,000 XIREC in the round summary (rounding / reconciliation difference).

## ML Analogy

The clearing-price engineering problem is a **mechanism design problem**: you observe the existing aggregate demand/supply curve (the stale book) and choose a bid that shifts the equilibrium price — essentially a **policy choice under known constraints**.

The minimum-viable-quantity calculation ($Q \geq 5\text{k}$ for Flax) is equivalent to finding the **minimum intervention** that shifts a threshold: the analogy is adding training examples to move a decision boundary. The boundary here is the clearing price argmax.

The "bid exactly $P^* - 1$" insight (bid 29 when target clearing is 29, not 30) is the critical **off-by-one correctness** that separates 5K profit from 0. In classification terms: the margin matters at the decision boundary, not away from it.

## Links

[[Rounds/Round1_findings]] · [[Strategies/manual_trading]] · [[Manuals/MAF]] · [[Manuals/Invest_and_Expand]] · [[User_Reported_Anchors]] · [[Performance/Manual_Per_Round]]

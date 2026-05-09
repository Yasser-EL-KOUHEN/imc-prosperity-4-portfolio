---
type: strategy
tags: [round1, round2, round3, round5, manual, game-theory, ev, auction]
sources:
  - report/report.tex (§R1 manual; §R2 Part B,C; §R3 Bio-Pods; §R5 Ashflow Alpha)
  - prosperity-vault/Manuals/
updated: 2026-05-06
---

# Manual Trading Strategy — Hub

Each round includes a manual trading challenge alongside the algorithmic one. Manual trades are scored independently from the algo and require game theory or optimization reasoning.

> **Detailed derivations live in `Manuals/`.** This page is a cross-round summary hub.

---

## Round 1 — Intarian Welcome (Stale Order Book)

**See [[Manuals/Dryland_Flax]] for full derivation.**

Two goods (Dryland Flax, Ember Mushroom). Stale double-auction: see the order book before placing one order. The clearing price $P^*$ maximizes traded volume; your order can shift it.

- Dryland Flax: BUY 5k @ 29 → shifts clearing from 28 to 29 → **5,000 XIREC**
- Ember Mushroom: BUY 35k @ 18 → fills 35k → **66,500 XIREC**
- **Combined: 71,500 XIREC**

---

## Round 2 — MAF Auction + Invest & Expand

### Part A — MAF (Market Access Fee)

**See [[Manuals/MAF]] for full derivation.**

Blind first-price auction: top 50% of bidders win +25% quote flow, pay their bid.

- **Submitted bid: b* = 3,000 XIREC** (website-scaled V_extra ≈ 6K; ~80% win probability)
- Key insight: asymmetric regret (6:1 against under-bidding) shifts optimal b above EV-optimal

### Part B — Invest & Expand

**See [[Manuals/Invest_and_Expand]] for full derivation.**

Allocate $(x_R, x_S, x_V)$ with sum ≤ 100 across Research (log), Scale (linear), Visibility (rank-based). Budget cost = 500 × sum.

- **Submitted: (xR=16, xS=48, xV=36) → PnL = 110,065 XIREC** (uniform-rank prior)
- Final recommendation (multi-prior robust): **(18, 60, 22)**
- Minimax safe (never negative): **(20, 70, 10)**

---

## Round 3 — Bio-Pods (Bayesian-Nash Equilibrium)

**See [[Manuals/Bio_Pods]] for full derivation.**

Sealed-bid auction over 51-level grid {670…920}. Two bids $(b_1, b_2)$, each counterparty has a uniform reserve price.

- **Bayesian-Nash equilibrium: $(b_1, b_2) = (755, 840)$, $f^* = 81.67$ XIREC per counterparty**
- Cubic penalty cliff at $\Delta b_2 = -1$ (−4.43 pts) — stability is sharp downward, shallow upward

---

## Round 5 — Ashflow Alpha (Ignith Exchange)

**See [[Manuals/Ashflow_Alpha]] and [[Strategies/Ashflow_Alpha_News_Trading]] for full derivation.**

9 goods, B = 1,000,000 XIREC, quadratic fee. $\text{fee}_i = 100 \cdot p_i^2$, net $= 100 \cdot p_i(s_i - p_i)$.

- **Exact optimum: $p_i^* = s_i / 2$** (ridge regression analogy)
- **Submitted: 85% total, 6/9 goods → 140,100 XIREC model net PnL**
- Key: archetype classification (mechanical recall vs stale hype), not Gaussian sentiment

---

## General Principles

1. **Model the math explicitly** — even a simple EV calculation beats intuition
2. **Identify the structural form** — log? linear? rank-competitive? — before solving
3. **Asymmetric regret changes the optimum** — under-bidding in MAF costs 6× more than over-bidding
4. **Game theory applies** — in rank-based competitions (I&E), peer behaviour is a hidden parameter; sensitivity analysis across peer priors is required
5. **Manual is independent** — manual PnL doesn't affect algo PnL

## Links

[[Manuals/Dryland_Flax]] · [[Manuals/MAF]] · [[Manuals/Invest_and_Expand]] · [[Manuals/Bio_Pods]] · [[Manuals/Ashflow_Alpha]] · [[Rounds/Round2_findings]] · [[Competition/Game_Mechanics]] · [[Overview]]

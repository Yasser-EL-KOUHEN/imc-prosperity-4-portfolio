---
type: concept
tags: [microstructure, fill-model, queue-position, adverse-selection, spread, maker-taker]
sources:
  - report/report.tex (§Capacity Management; §Fill Model; §Backtester vs Competition)
  - round5/research/eda.py
  - .planning/phases/12-counterparty-exploitation/RESEARCH.md
  - round3/research/microstructure_eda.py
updated: 2026-05-06
---

# Market Microstructure

The mechanics of how orders get filled, who fills them, and what that costs.

---

## Maker vs Taker

| Role | How | Cost/Revenue |
|---|---|---|
| **Maker (passive)** | Post a limit order; wait to be filled by someone else | Earns spread if filled; pays opportunity cost if price moves away |
| **Taker (aggressive)** | Hit an existing quote; cross the spread | Pays spread; guarantees immediate fill |

In Prosperity, posting at `best_bid + 1` (just inside the spread) is passive. Posting at `best_ask` (crossing to buy at the current ask) is aggressive. Most Prosperity strategies mix both.

---

## Queue Position and Fill Priority

Within a price level, orders fill in **FIFO order** (first-posted, first-filled). In Prosperity:

- The local backtester uses `--match-trades better` (your order fills before same-price others) by default, or `--match-trades all` (ignores queue entirely — everyone at the same price fills). Both **overstate** fill rates vs the real server.
- The real Prosperity engine enforces queue priority: if there are 100 units already resting at your price, you only fill after those 100.
- This is the source of the **8.6× local fill inflation** (R5: `--match-trades all` vs real server) and the **~16–20× local inflation** documented in Phase 2 (R3 HYDROGEL).

**Practical implication:** Never size a strategy based on local-backtest fills. Use real-Prosperity-log fills as the calibration source.

---

## Adverse Selection

**Definition:** The risk that the counterparty who fills your passive quote is better-informed than you. They fill you when the price is about to move against you; they don't fill you when the price is about to move in your favor.

**Why it matters in R5:**

The R5 BLACKLIST and TIER3 classifications exist entirely because of adverse selection:

1. You post a passive bid at `mid − 1` and `mid − 2`
2. An informed counterparty hits your bid when they know the price is about to drop
3. You buy at `mid − 1`, price drops to `mid − 10` → you lose 9 ticks on that fill
4. The uninformed flow that would pay `mid + 1` (completing the round-trip) never arrives
5. Net result: fills cost you money rather than earning spread

**Signature:** The product's PnL from MM is negative even when you're "making the spread." The spread capture is overwhelmed by adverse fill timing.

**Adverse selection scales with volume (the v40 mistake):** If you double LIMIT (more exposure), adverse selection loss approximately doubles. v40 raised LIMIT from 5 to 10 for TIER3 products — "more volume = more fills = recovery." Result: losses doubled. The correct response to adverse selection is **less exposure**, not more. See [[Concepts/Adverse_Selection]].

---

## Spread Components

The bid-ask spread compensates the market maker for three costs:

| Component | Description | R5 relevance |
|---|---|---|
| **Inventory holding cost** | Risk from price moving against a position | Managed by position skew, LIMIT cap |
| **Adverse selection cost** | Informed flow picking off quotes | The dominant cost in BLACKLIST products |
| **Order processing cost** | Operational overhead per trade | Minimal in algo trading |

For HYDROGEL (R3): inventory holding is the dominant cost → AR(1) correction + skew manages it.
For R5 TIER3/BLACKLIST products: adverse selection dominates → LIMIT reduction or exclusion is the only remedy.

---

## The Prosperity Fill Model in Detail

### Local backtester (`--match-trades all`)
- Every order at or better than the counterparty price fills
- No queue: your order fills even if it arrives after existing same-price orders
- **Inflated fills vs real server**

### Real Prosperity engine
- FIFO queue at each price level
- Orders that arrive after existing same-price orders fill only if sufficient volume crosses
- **Lower fill rates** — especially for passive orders in liquid markets

### Consequence for strategy design
The Phase 1 / Phase 2 work established a ~16–20× local inflation for R3 HYDROGEL. The Phase 13 Phase 17 work documented the local `--match-trades all` inflation for R5. This is why the cross-version Prosperity log (N=12 versions) is the correct calibration source — it uses real-server fills, not local ones.

---

## Order Book Depth and Quote Size

For a market with `best_bid` and `best_ask`:
- Quoting at `best_bid + 1` (inner touch) means you're just inside the spread — first in the new best bid queue
- Quoting at `best_bid` means you join the existing queue at that price — lower fill probability
- Quoting at `best_bid - 1` (outer) is less aggressive — wider spread capture but fewer fills

**R5 parameters:**
- `MM_INNER_SIZE = 6`: post 6 units at the inner touch (high fill probability, tighter spread)
- `MM_OUTER_SIZE = 4`: post 4 units one tick outside (some fills at wider spread)
- `MIN_SPREAD = 2`: only quote if spread ≥ 2 ticks (1-tick markets have no room for edge)

---

## Capacity Management Pattern

From `round3/trader.py` and `round5/strategies/round5_v42_trader.py`:

```python
# After processing immediate fills, remaining capacity sets passive order size
c_plus  = LIMIT - pos - Q_immediate_buy   # capacity for more buys
c_minus = LIMIT + pos - Q_immediate_sell  # capacity for more sells

# Passive orders sized exactly to consume remaining capacity
bid_qty = min(INNER_SIZE, c_plus)
ask_qty = min(INNER_SIZE, c_minus)
```

This ensures you **never breach the position limit** while **maximising fill opportunities** within it. The pattern is shared between R3 HYDROGEL and R5 default MM.

---

## Mark Counterparties as Microstructure Signals

In Round 4, counterparty IDs became visible in `Trade.buyer` / `Trade.seller`. This allows:
- **Flow toxicity detection**: Mark 67 = dip buyer → his buys coincide with local lows → his presence is a bullish signal
- **Cooldown logic**: after Mark 49 (local-high seller) fills, reduce bid size for 500ms (he sells at tops → don't buy at tops)
- **Bilateral MM identification**: Mark 14 + Mark 38 bilateral loop = existing top-of-book → out-quote them by 1 tick

See [[Marks/Mark_67]] · [[Marks/Mark_49]] · [[Marks/Mark_22]] for specific profiles.

---

## ML Analogy

Market microstructure is **online learning with adversarial label noise**. The labels (future price direction) are provided by a mixture of:
- Informed traders (adversarially selected samples — they only label when they're right)
- Noise traders (random labels — benign)

**Adverse selection** is exactly the scenario where the adversarial fraction dominates on the fills you receive. A passive MM strategy that learns from fills is being trained on adversarially selected examples — the classic poisoning attack in adversarial ML. The remedy is the same: **reduce the batch size** (TIER3: LIMIT 5) or **reject that data source entirely** (BLACKLIST: LIMIT 0).

The fill model inflation (local vs real server) is the **train/test distribution mismatch** problem: your local "test set" uses a different fill distribution than the production environment. You overfit to the local metric and underperform in deployment.

## Links

[[Concepts/Adverse_Selection]] · [[Concepts/AR1_Process]] · [[Concepts/Spread_Dynamics]] · [[Concepts/inventory_risk]] · [[Concepts/Order_Book_Imbalance]] · [[Concepts/Backtester_vs_Competition]] · [[Strategies/market_making]] · [[Strategies/TIER3_Market_Making]] · [[Strategies/Cross_Version_Blacklist]] · [[Marks/Mark_67]] · [[Marks/Mark_49]]

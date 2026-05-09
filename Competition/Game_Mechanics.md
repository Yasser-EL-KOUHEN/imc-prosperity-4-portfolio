---
type: competition
tags: [mechanics, rules, exchange]
sources: [context/Game Mechanics Overview.txt, context/Trading glossary.txt, context/Writing an Algorithm in Python.txt]
updated: 2026-04-27
---

# Game Mechanics

## The Exchange Model

Prosperity runs a **limit order book exchange** — the standard model of most real financial markets. Each tick, your `trader.py` receives a `TradingState` object describing the current order book for every product and your current positions, then returns a list of `Order` objects.

**Key constraint:** Your algorithm runs in isolation — no interaction with other teams' bots. You trade against IMC's own market-making bots.

## Order Types in Prosperity

Only **limit orders** are supported:
- **Bid order** (BUY): fills at `price ≤ your_price` — you buy at the ask or better
- **Ask order** (SELL): fills at `price ≥ your_price` — you sell at the bid or better

**Order matching:** Price-time priority. Incoming orders match against the best available resting orders first; if multiple orders at the same price, oldest executes first.

**Passive vs aggressive:**
- *Passive* (resting): post a bid below best ask, post an ask above best bid → waits for the market to come to you → earns spread
- *Aggressive* (crossing): post a bid ≥ best ask, post an ask ≤ best bid → executes immediately → pays spread

Market making is passive by default; aggressive orders are used only when the edge is large enough to justify crossing.

## Submission Format

- **Single file:** `trader.py` — must contain a `Trader` class with a `run(state: TradingState) -> dict[str, list[Order]]` method
- **Allowed imports:** `datamodel`, `jsonpickle`, `typing`, `collections`, `math`, `os`, `__future__`
- **No scipy, numpy, pandas** — not available in the competition environment
- **State persistence:** Use `state.trader_data` (a string) serialised via `jsonpickle` to persist state across ticks
- **File size limit:** < 200,000 bytes

## Scoring

- **Currency:** XIREC (synthetic profit units)
- **End-of-day settlement:** Open positions are liquidated at a hidden fair value (`--merge-pnl` in the backtester mirrors this)
- **Leaderboard:** Overall (algo + manual), Algorithmic-only, Manual-only, Country tabs
- **No penalty for breaching position limits** in the simulator itself, but the competition has hard limits — exceeding them disqualifies that product's trades for the tick

## Position Limits

Each product has a hard position limit. Exceeding it is a submission error. See [[Concepts/Position_Limits]].

| Product | Limit |
|---------|-------|
| HYDROGEL_PACK | ±200 |
| VELVETFRUIT_EXTRACT | ±200 |
| VEV_* vouchers | ±300 |
| RAINFOREST_RESIN | ±50 (Round 1) |
| KELP | ±50 (Round 1) |

## Dashboard Features

- **A.R.I.A. Uplinks** — video briefings at the start of each round with product information
- **Debug logs** — downloadable from the dashboard after submission; show per-tick order fills
- **Outpost view** — visual representation of PnL and rank

## Local Backtester

`prosperity3bt` (the official backtester) runs your trader against historical log files. Key flags:

| Flag | Effect |
|------|--------|
| `--merge-pnl` | End-of-day MTM settlement (always use this) |
| `--match-trades all` | Match all available counterparty trades |
| `--timeseries` | Export per-tick position + PnL as CSV |
| `--no-out` | Suppress raw log file |
| `--no-progress` | Suppress progress bar (useful for scripting) |

**Important bias:** Local backtest runs ~10x more ticks than the official simulator and has a more optimistic fill model. Local PnL is ~16x the official value for total, ~20x for HYDROGEL specifically. **Use local as a directional signal only, not for absolute PnL forecasting.**

## Links

[[Competition/Round_Schedule]] · [[Concepts/Position_Limits]] · [[Concepts/Spread_Dynamics]] · [[Overview]]

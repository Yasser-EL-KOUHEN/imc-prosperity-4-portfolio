---
type: round
tags: [round0, tutorial, eda, emeralds, tomatoes]
sources: [logs/round0/16386.py, logs/round0/16386.log, plots/round0/]
updated: 2026-04-27
---

# Round 0 — Tutorial

## Purpose

The tutorial round exists to:
1. Familiarise with submission mechanics (upload, dashboard, debug logs)
2. Run first EDA on market data
3. Test a basic market making strategy
4. Select an On-Board Advisor (locked after tutorial)

Manual trading is **inactive** during tutorial.

---

## Products

| Product | Characteristics | Strategy |
|---------|----------------|---------|
| **EMERALDS** | Very stable, low volatility | Pure MM around known FV |
| **TOMATOES** | More volatile, some trending | MM with dynamic FV |

These products do not appear in later rounds.

---

## EDA Performed

Plots generated in `plots/round0/`:

For each product (EMERALDS, TOMATOES):
- `_01_price_overview.png` — mid-price time series, spread distribution
- `_02_acf_pacf.png` — autocorrelation / partial autocorrelation
- `_03_order_book.png` — order book depth at different price levels
- `_04_trade_flow.png` — trade direction and size distribution
- `_05_hurst.png` — Hurst exponent (H<0.5 → mean-reverting)

**EMERALDS finding:** Very stable; Hurst < 0.5 confirms mean-reversion. Nearly constant fair value ≈ 10,000. Direct precursor to the ASH_COATED_OSMIUM (ACO) strategy in Round 1 — same stable-FV mean-reverting structure.

**TOMATOES finding:** More volatile; ACF shows shorter-lived autocorrelation. Mean-reverting but noisier. Foreshadows the challenges of quoting more volatile products.

---

## First Submission

Round 0 submission: `logs/round0/16386.py` (initial trader version)
- Results: `logs/round0/16386.log` (sandbox log)
- Strategy: basic symmetric MM on both products

---

## Lessons Carried Forward

| Lesson | Applied In |
|--------|-----------|
| Very stable products → fixed FV works best | ACO in Round 1 (FV anchor at 10,000) |
| Spread tuning is the main lever | All MM products |
| ACF/PACF workflow for stationarity test | All EDA |
| Hurst exponent as regime indicator | HYDROGEL_PACK research (Round 3) |

---

## Links

[[Competition/Game_Mechanics]] · [[Rounds/Round1_findings]] · [[Products/ASH_COATED_OSMIUM]] · [[Strategies/market_making]]

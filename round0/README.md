# Round 0 — Tutorial

**Products:** EMERALDS, TOMATOES  
**Position limit:** ±20

Tutorial round used to understand the platform, data format, and backtester.

## Strategy
- EMERALDS: pure mean reversion (price reverts to known fair value ~10,000)
- TOMATOES: exploratory EDA

## Files
- `trader.py` — submitted trader
- `data/` — price and trade CSVs (days −2, −1)
- `logs/` — Prosperity platform log
- `sandbox_logs/` — local backtester runs
- `plots/` — price overview, ACF/PACF, order book, trade flow, Hurst exponent

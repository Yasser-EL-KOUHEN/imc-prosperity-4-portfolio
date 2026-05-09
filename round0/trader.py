"""
Prosperity 4 — Main Trader
===========================

Round 0 (Tutorial) products:
  - EMERALDS  : stable fair value = 10000, market-make inside bot spread
  - TOMATOES  : drifting fair value, AR(1) mean-reversion, adaptive EMA

Strategy logic
--------------
For both products, the core loop is identical:
  1. Estimate fair value (FV).
  2. Take any bot quote that is strictly better than FV (free edge).
  3. Post passive orders just inside the bot spread to capture aggressive-bot flow.
  4. Skew quotes based on current inventory to avoid hitting position limits.

Mathematical motivation
-----------------------
EMERALDS: FV = 10000 (constant, std ≈ 0.72).  Bot spread = 9992 / 10008.
  By posting passive buy at (bot_bid + 1) = 9993 and sell at (bot_ask - 1) = 10007,
  every bot that was going to cross the spread trades with us instead, at a
  price that is 7 ticks more favourable to them — and 7 ticks profitable for us.
  Expected edge per fill = ±7 XIREC.

TOMATOES: FV = mid − phi·(mid − last_mid)  (pure AR(1) 1-step predictor;
  EMA_ALPHA=1 makes the EMA term equal to current mid, leaving only the
  mean-reversion correction).  Bot spread ≈ 13–14 ticks (two regimes).
  Regime-switching: phi=0.05 in tight-spread regime (spread≤13, AR(1)=−0.30),
  phi=0.00 in wide-spread regime (spread=14, AR(1)≈0).
  We quote at ±5 from FV (grid-optimised; mild inventory skew S=1).
"""

from datamodel import Order, TradingState
from typing import List, Dict, Any
import jsonpickle
import math


# ============================================================
# Per-product strategy classes
# ============================================================

class EmeraldsStrategy:
    """
    Pure market-making strategy for EMERALDS.

    FV = 10000 (empirically constant).
    Bot spread = 9992 bid / 10008 ask (±8 from FV).

    Actions:
      - Immediately take any ask ≤ FV (bot occasionally quotes at 10000).
      - Immediately take any bid ≥ FV (bot occasionally quotes at 10000).
      - Post passive BUY  at bot_bid + 1 = 9993  (7 ticks below FV).
      - Post passive SELL at bot_ask - 1 = 10007  (7 ticks above FV).
      - Size = remaining capacity after immediate fills.
    """

    PRODUCT = "EMERALDS"
    FAIR_VALUE = 10000
    BOT_BID = 9992      # lowest normal bot bid
    BOT_ASK = 10008     # highest normal bot ask
    PASSIVE_BUY  = BOT_BID  + 1   # = 9993
    PASSIVE_SELL = BOT_ASK - 1    # = 10007

    def __init__(self, position_limit: int = 20):
        self.position_limit = position_limit

    def orders(self, state: TradingState) -> List[Order]:
        od = state.order_depths.get(self.PRODUCT)
        if od is None:
            return []

        pos = state.position.get(self.PRODUCT, 0)
        orders: List[Order] = []

        # Remaining capacity (how much we can still buy / sell)
        buy_cap  = self.position_limit - pos   # > 0 means we can still buy
        sell_cap = self.position_limit + pos   # > 0 means we can still sell

        # ── Step 1: Take immediately profitable bot quotes ──────────────
        # Take all asks ≤ FV (we buy below or at fair value)
        for ask in sorted(od.sell_orders.keys()):
            if ask > self.FAIR_VALUE or buy_cap <= 0:
                break
            qty = min(-od.sell_orders[ask], buy_cap)
            orders.append(Order(self.PRODUCT, ask, qty))
            buy_cap  -= qty
            pos      += qty

        # Take all bids ≥ FV (we sell above or at fair value)
        for bid in sorted(od.buy_orders.keys(), reverse=True):
            if bid < self.FAIR_VALUE or sell_cap <= 0:
                break
            qty = min(od.buy_orders[bid], sell_cap)
            orders.append(Order(self.PRODUCT, bid, -qty))
            sell_cap -= qty
            pos      -= qty

        # ── Step 2: Post passive orders inside bot spread ───────────────
        # Passive BUY at 9993 (1 tick better than bot bid 9992)
        if buy_cap > 0:
            orders.append(Order(self.PRODUCT, self.PASSIVE_BUY, buy_cap))

        # Passive SELL at 10007 (1 tick better than bot ask 10008)
        if sell_cap > 0:
            orders.append(Order(self.PRODUCT, self.PASSIVE_SELL, -sell_cap))

        return orders


class TomatoesStrategy:
    """
    Adaptive market-making strategy for TOMATOES.

    Fair value: FV = mid − phi*(mid − last_mid)  (AR(1) 1-step predictor).
    With EMA_ALPHA=1, the EMA collapses to mid, leaving only the AR(1) term.

    Regime-switching AR(1) coefficient:
      - Tight spread (≤13, ~55% of time, AR(1)=−0.30): phi = AR1_COEF_TIGHT
      - Wide  spread (=14, ~45% of time, AR(1)≈ 0.00): phi = AR1_COEF_WIDE

    Passive quotes at ±QUOTE_OFFSET from FV, inventory-skewed by SKEW_RANGE.
    """

    PRODUCT = "TOMATOES"

    # ── Tunable parameters ──────────────────────────────────────────────
    # EMA_ALPHA = 1.0 means _ema ≡ mid (no smoothing).
    # Combined with the AR(1) correction, FV = mid - AR1_COEF*(mid - last_mid).
    # Grid search (pos_limit=80): best is (a=1.0, Q=5, S=1).
    # S=1 adds minimal skew that controls inventory without sacrificing edge.
    EMA_ALPHA    = 1.00   # EMA decay: 1.0 = pure current mid (AR(1)-only FV)
    QUOTE_OFFSET = 5      # ticks inside FV for passive quotes (grid-optimised)
    SKEW_RANGE   = 1      # mild inventory skew: (pos/limit)*1 ticks

    # ── Regime-switching AR(1) correction ───────────────────────────────
    # EDA: TOMATOES has two distinct spread regimes.
    #   Tight  (spread ≤ 13, ~55% of time): statistical AR(1) = −0.303
    #   Wide   (spread  = 14, ~45% of time): statistical AR(1) ≈  0.000
    # The market-making optimal coefficient differs from the statistical one:
    # heavy correction misaligns quotes vs bot crossing thresholds.
    # AR1_COEF_TIGHT = 0.05 is the grid-searched global optimum; applying it
    # only in the tight regime (where AR(1) is non-zero) and 0 in the wide
    # regime avoids unnecessary FV shifts when the market is effectively a RW.
    # Re-run the grid search per-regime to further refine these values.
    TIGHT_SPREAD_MAX = 13    # spread ≤ this → tight regime
    AR1_COEF_TIGHT   = 0.05  # correction coef in tight regime (grid-optimised)
    AR1_COEF_WIDE    = 0.00  # correction coef in wide regime  (AR(1) ≈ 0)

    # ── OBI signal: NOT usable for asymmetric sizing ────────────────────
    # EDA: OBI corr(next return) = 0.38 in tight regime (non-zero 12% of time).
    # Backtested OBI_SIZE_SKEW ∈ {0.50, 1.00}: zero PnL change in both cases.
    # Root cause: passive edge (5 ticks) >> OBI directional signal
    # (E[Δmid|OBI=1] ≈ 0.38 × σ ≈ 0.51 ticks).  Sizing down sacrifices
    # more passive edge than the directional gain compensates.
    # Revisit when half-spread < 1 tick (OBI signal > passive edge).

    def __init__(self, position_limit: int = 20):
        self.position_limit = position_limit
        self._ema: float = None
        self._last_mid: float = None

    # ── State serialisation helpers ─────────────────────────────────────
    # Only _last_mid matters: with EMA_ALPHA=1, _ema is always overwritten
    # to mid on the very next tick, so persisting it is a no-op.
    def get_state(self) -> dict:
        return {"last_mid": self._last_mid}

    def set_state(self, d: dict) -> None:
        self._last_mid = d.get("last_mid")

    # ── Fair value estimation ────────────────────────────────────────────
    def _update_ema(self, mid: float) -> None:
        if self._ema is None:
            self._ema = mid
        else:
            self._ema = self.EMA_ALPHA * mid + (1 - self.EMA_ALPHA) * self._ema

    def _fair_value(self, mid: float, spread: float) -> float:
        """
        Two-component FV:
          1. EMA(mid)         — tracks slow intraday drift
          2. AR(1) correction — −phi * last_change  (mean-reversion)

        Regime-switching: use AR1_COEF_TIGHT when spread ≤ TIGHT_SPREAD_MAX
        (statistically significant mean-reversion), AR1_COEF_WIDE otherwise
        (spread=14 regime has AR(1) ≈ 0, correction adds noise).
        """
        fv = self._ema if self._ema is not None else mid
        if self._last_mid is not None:
            last_change = mid - self._last_mid
            coef = (self.AR1_COEF_TIGHT
                    if spread <= self.TIGHT_SPREAD_MAX
                    else self.AR1_COEF_WIDE)
            fv -= coef * last_change
        return fv

    # ── Main order generation ────────────────────────────────────────────
    def orders(self, state: TradingState) -> List[Order]:
        od = state.order_depths.get(self.PRODUCT)
        if od is None:
            return []

        # Mid price from order book
        best_bid = max(od.buy_orders.keys())  if od.buy_orders  else None
        best_ask = min(od.sell_orders.keys()) if od.sell_orders else None
        if best_bid is None or best_ask is None:
            return []
        mid    = (best_bid + best_ask) / 2
        spread = best_ask - best_bid

        self._update_ema(mid)
        fv = self._fair_value(mid, spread)
        self._last_mid = mid

        pos = state.position.get(self.PRODUCT, 0)
        orders: List[Order] = []

        buy_cap  = self.position_limit - pos
        sell_cap = self.position_limit + pos

        # ── Step 1: Take immediately profitable bot quotes ───────────────
        for ask in sorted(od.sell_orders.keys()):
            if ask >= fv or buy_cap <= 0:
                break
            qty = min(-od.sell_orders[ask], buy_cap)
            orders.append(Order(self.PRODUCT, ask, qty))
            buy_cap -= qty
            pos     += qty

        for bid in sorted(od.buy_orders.keys(), reverse=True):
            if bid <= fv or sell_cap <= 0:
                break
            qty = min(od.buy_orders[bid], sell_cap)
            orders.append(Order(self.PRODUCT, bid, -qty))
            sell_cap -= qty
            pos      -= qty

        # ── Step 2: Inventory-skewed passive quotes (anchored to raw fv) ─
        skew = (pos / self.position_limit) * self.SKEW_RANGE

        passive_bid = math.floor(fv - self.QUOTE_OFFSET - skew)
        passive_ask = math.ceil (fv + self.QUOTE_OFFSET - skew)

        # Ensure bid < ask (prevent crossed passive quotes)
        if passive_bid >= passive_ask:
            passive_ask = passive_bid + 1

        if buy_cap > 0:
            orders.append(Order(self.PRODUCT, passive_bid, buy_cap))

        if sell_cap > 0:
            orders.append(Order(self.PRODUCT, passive_ask, -sell_cap))

        return orders


# ============================================================
# Main Trader class (submitted to Prosperity)
# ============================================================

class Trader:
    """
    Combines per-product strategies.  State is persisted via traderData.
    """

    POSITION_LIMITS = {
        "EMERALDS": 80,
        "TOMATOES": 80,
    }

    def bid(self) -> int:
        """Required for Round 2 (sealed-bid auction). Placeholder."""
        return 0

    def run(self, state: TradingState):
        # ── Deserialise persisted state ──────────────────────────────────
        saved: Dict[str, Any] = {}
        if state.traderData:
            try:
                saved = jsonpickle.decode(state.traderData)
            except Exception:
                saved = {}

        tomatoes_state = saved.get("tomatoes", {})

        # ── Instantiate strategies ───────────────────────────────────────
        emeralds = EmeraldsStrategy(
            position_limit=self.POSITION_LIMITS.get("EMERALDS", 40)
        )
        tomatoes = TomatoesStrategy(
            position_limit=self.POSITION_LIMITS.get("TOMATOES", 40)
        )
        tomatoes.set_state(tomatoes_state)

        # ── Generate orders ──────────────────────────────────────────────
        result: Dict[str, List[Order]] = {}

        if "EMERALDS" in state.order_depths:
            result["EMERALDS"] = emeralds.orders(state)

        if "TOMATOES" in state.order_depths:
            result["TOMATOES"] = tomatoes.orders(state)

        # ── Serialise state for next iteration ───────────────────────────
        new_saved = {
            "tomatoes": tomatoes.get_state(),
        }
        trader_data = jsonpickle.encode(new_saved)

        conversions = 0
        return result, conversions, trader_data

"""
Prosperity 4 -- Round 1 Trader  (v2 -- book-anchored passive quotes)
=====================================================================

Fix applied vs v1
-----------------
  v1 BUG: passive quotes computed as FV +/- QUOTE_OFFSET.
    For IPR: pb = floor(FV-6) = mid-6 = bot_bid  (competing, time-priority lost)
             pa = ceil(FV+6)  = mid+7 > bot_ask   (outside spread, never fills)
    Result: almost zero passive fills on real exchange.
    Jasper (match-trades=all) ignores time priority -> inflated 263K backtest PnL.

  v2 FIX:
    ACO: anchor to book: passive_bid = best_bid+1, passive_ask = best_ask-1.
         Always exactly 1 tick inside bot's spread -> guaranteed fills on real exchange.
    IPR: aggressive-only strategy.  Take ALL available asks immediately to build
         max-long position (80 units) as fast as possible, then hold.
         Post passive buy at best_bid+1 with any remaining buy_cap.
         Never post passive sells (hold the long to ride the +0.1/tick trend).

Round 1 products
-----------------
  ASH_COATED_OSMIUM (ACO)  -- position limit 80
    Stable FV ~10000.  AR(1) on mid-price changes = -0.495 (strong mean reversion).
    Bot spread = 16 ticks (+/-8 from mid).
    Strategy: symmetric MM 1 tick inside bot's spread, FV-based aggressive takes.

  INTARIAN_PEPPER_ROOT (IPR)  -- position limit 80
    Linear trend: +0.1/tick (+1000/day).  AR(1) on detrended returns = -0.495.
    Bot spread ~13 ticks (+/-6.5 from mid).
    Strategy: greedy long accumulation.  Take every ask, hold max position.
    PnL source: 80 units * +1000/day * 3 days = 240 000 XIREC trend PnL.
"""

from datamodel import Order, TradingState
from typing import List, Dict, Any
import jsonpickle
import math


# ============================================================
# ASH_COATED_OSMIUM strategy
# ============================================================

class ACOStrategy:
    """
    Symmetric market-making for ASH_COATED_OSMIUM.

    AR(1) correction:  after a +delta move, FV = EMA - 0.40*delta (sell-biased).
    Passive quotes anchored to the order book: best_bid+1 / best_ask-1.
    This guarantees we are INSIDE the bot's spread (not at it), so we
    have price priority and will fill before the bot does.

    Aggressive takes: consume any ask < FV or bid > FV (free edge).
    """

    PRODUCT       = "ASH_COATED_OSMIUM"
    EMA_ALPHA     = 0.50
    AR1_COEF      = 0.40

    def __init__(self, position_limit: int = 80):
        self.position_limit = position_limit
        self._ema:      float = None
        self._last_mid: float = None

    def get_state(self) -> dict:
        return {"ema": self._ema, "last_mid": self._last_mid}

    def set_state(self, d: dict) -> None:
        self._ema      = d.get("ema")
        self._last_mid = d.get("last_mid")

    def _fair_value(self, mid: float) -> float:
        """
        FV = EMA(mid) - AR1*(mid - last_mid)
        EMA anchors near the long-run mean (~10000).
        AR(1) term shifts FV toward the expected reversal.
        """
        if self._ema is None:
            self._ema = mid
        else:
            self._ema = self.EMA_ALPHA * mid + (1 - self.EMA_ALPHA) * self._ema

        fv = self._ema
        if self._last_mid is not None:
            fv -= self.AR1_COEF * (mid - self._last_mid)
        return fv

    def orders(self, state: TradingState) -> List[Order]:
        od = state.order_depths.get(self.PRODUCT)
        if od is None or not od.buy_orders or not od.sell_orders:
            return []

        best_bid = max(od.buy_orders.keys())
        best_ask = min(od.sell_orders.keys())
        mid      = (best_bid + best_ask) / 2

        fv = self._fair_value(mid)
        self._last_mid = mid

        pos      = state.position.get(self.PRODUCT, 0)
        buy_cap  = self.position_limit - pos
        sell_cap = self.position_limit + pos
        orders: List[Order] = []

        # -- Aggressive: take any bot quote that crosses FV --
        for ask_p in sorted(od.sell_orders.keys()):
            if ask_p >= fv or buy_cap <= 0:
                break
            qty = min(-od.sell_orders[ask_p], buy_cap)
            orders.append(Order(self.PRODUCT, ask_p, qty))
            buy_cap -= qty
            pos     += qty

        for bid_p in sorted(od.buy_orders.keys(), reverse=True):
            if bid_p <= fv or sell_cap <= 0:
                break
            qty = min(od.buy_orders[bid_p], sell_cap)
            orders.append(Order(self.PRODUCT, bid_p, -qty))
            sell_cap -= qty
            pos      -= qty

        # -- Passive: 1 tick inside bot's spread (price priority over bot) --
        # Bot spread ~16 ticks.  best_bid+1 and best_ask-1 are inside that spread.
        passive_bid = best_bid + 1
        passive_ask = best_ask - 1
        if passive_bid >= passive_ask:
            # Spread too tight (shouldn't happen for ACO), skip passive
            return orders

        if buy_cap > 0:
            orders.append(Order(self.PRODUCT, passive_bid,  buy_cap))
        if sell_cap > 0:
            orders.append(Order(self.PRODUCT, passive_ask, -sell_cap))

        return orders


# ============================================================
# INTARIAN_PEPPER_ROOT strategy
# ============================================================

class IPRStrategy:
    """
    Greedy long-accumulation for INTARIAN_PEPPER_ROOT.

    The price trends up +0.1/tick = +1000/day.  Holding 80 units for 3 days
    captures 80 * 3000 = 240 000 XIREC in trend PnL alone.

    Strategy: reach max-long (80 units) as fast as possible and hold.
      1. Aggressively take ALL available asks each tick (up to buy_cap).
      2. Post passive buy at best_bid+1 for any remaining buy_cap.
      3. NEVER post passive sells (we want to hold the long).

    No skew needed: we are purely directional.
    No FV condition on aggressive buys: we want 80 units regardless of price.
    """

    PRODUCT       = "INTARIAN_PEPPER_ROOT"

    def __init__(self, position_limit: int = 80):
        self.position_limit = position_limit

    def get_state(self) -> dict:
        return {}

    def set_state(self, d: dict) -> None:
        pass

    def orders(self, state: TradingState) -> List[Order]:
        od = state.order_depths.get(self.PRODUCT)
        if od is None or not od.buy_orders or not od.sell_orders:
            return []

        best_bid = max(od.buy_orders.keys())
        best_ask = min(od.sell_orders.keys())

        pos     = state.position.get(self.PRODUCT, 0)
        buy_cap = self.position_limit - pos
        orders: List[Order] = []

        if buy_cap <= 0:
            return []  # already at max long, hold

        # -- Aggressive: take ALL available asks immediately --
        for ask_p in sorted(od.sell_orders.keys()):
            if buy_cap <= 0:
                break
            qty = min(-od.sell_orders[ask_p], buy_cap)
            orders.append(Order(self.PRODUCT, ask_p, qty))
            buy_cap -= qty

        # -- Passive: 1 tick above best bid for remaining capacity --
        if buy_cap > 0:
            orders.append(Order(self.PRODUCT, best_bid + 1, buy_cap))

        return orders


# ============================================================
# Main Trader class
# ============================================================

class Trader:
    """Combines ACO and IPR strategies. State persisted via traderData."""

    POSITION_LIMITS = {
        "ASH_COATED_OSMIUM":    80,
        "INTARIAN_PEPPER_ROOT": 80,
    }

    def run(self, state: TradingState):
        # Deserialise persisted state
        saved: Dict[str, Any] = {}
        if state.traderData:
            try:
                saved = jsonpickle.decode(state.traderData)
            except Exception:
                saved = {}

        # Instantiate strategies
        aco = ACOStrategy(position_limit=self.POSITION_LIMITS["ASH_COATED_OSMIUM"])
        ipr = IPRStrategy(position_limit=self.POSITION_LIMITS["INTARIAN_PEPPER_ROOT"])

        aco.set_state(saved.get("aco", {}))
        ipr.set_state(saved.get("ipr", {}))

        # Generate orders
        result: Dict[str, List[Order]] = {}

        if "ASH_COATED_OSMIUM" in state.order_depths:
            result["ASH_COATED_OSMIUM"] = aco.orders(state)

        if "INTARIAN_PEPPER_ROOT" in state.order_depths:
            result["INTARIAN_PEPPER_ROOT"] = ipr.orders(state)

        # Serialise state for next iteration
        trader_data = jsonpickle.encode({
            "aco": aco.get_state(),
            "ipr": ipr.get_state(),
        })

        conversions = 0
        return result, conversions, trader_data
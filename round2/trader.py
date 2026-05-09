"""
Prosperity 4 -- Round 1+2 Trader  (v3 -- FV anchor blend, MAF bid=3000)
=======================================================================

Round 2 adds only Trader.bid() returning 3000 XIREC as the Market
Access Fee bid for +25% extra quote volume. Asymmetric-regret analysis
(see prosperity_report.tex sec:r2_maf): ~80% win probability at this
bid, ~3K net profit at website-scaled V_extra=6K.
Trading logic for ACO/IPR is unchanged from Round 1 v3.

v3 improvement vs v2 (selected via aco_opt_sweep.py)
----------------------------------------------------

v3 improvement vs v2 (selected via aco_opt_sweep.py)
----------------------------------------------------
  ACO: FV now blends fast EMA with the known FV prior 10000:
         FV_base = 0.85 * EMA(mid) + 0.15 * 10000
         FV      = FV_base - rho(|dmid|) * dmid
       Justified by EDA: FV mean 10000, std ~5/day (strong prior).
       Sweep under --match-trades=worse: ACO 51,040 -> 53,116 (+4.1%, +2,076
       XIREC 3-day), robust on EVERY day.  Total PnL 289,094 -> 291,170.
       Rejected alternatives (all fail the per-day anti-overfit gate):
         inventory skew (k*pos shift)  -- loses passive-fill edge
         inventory gate (rho downscale)-- AR(1) still predictive when loaded
         slow-EMA anchor               -- injects noise; FV is stationary

Background on v2 fix (kept)
---------------------------
  v1 BUG: passive quotes computed as FV +/- QUOTE_OFFSET.
    IPR: pa = ceil(FV+6) > bot_ask -> never fills
    Jasper (match-trades=all) ignored time priority -> inflated 263K backtest.
  v2: book-anchored passive quotes at best_bid+1 / best_ask-1 (guaranteed
      price priority over the bot).

Round 1 products
-----------------
  ASH_COATED_OSMIUM (ACO)  -- position limit 80
    Stable FV ~10000. AR(1) on mid-price changes = -0.495 (strong reversion).
    Bot spread = 16 ticks.
    Strategy: symmetric MM 1 tick inside bot's spread, FV-based takes,
    FV anchored 15% toward 10000.

  INTARIAN_PEPPER_ROOT (IPR)  -- position limit 80
    Linear trend: +0.1/tick (+1000/day).
    Strategy: greedy long accumulation, no passive sells.
"""

from datamodel import Order, TradingState
from typing import List, Dict, Any
import jsonpickle


# ============================================================
# ASH_COATED_OSMIUM strategy
# ============================================================

class ACOStrategy:
    """
    Symmetric market-making for ASH_COATED_OSMIUM.

    FV = anchor_blend(EMA, 10000) - rho(|dmid|) * dmid
      anchor_blend = 0.85*EMA + 0.15*10000 (Bayesian shrinkage toward the
                     known FV mean; EDA: std ~5/day)
      rho = 0.25 (|dmid|<2), 0.60 (|dmid|<5), 0.74 (|dmid|>=5)

    Passive quotes anchored to the order book: best_bid+1 / best_ask-1
    (price priority over the bot, guaranteed fills ahead of it).

    Aggressive takes: consume any ask < FV or bid > FV (free edge).
    """

    PRODUCT       = "ASH_COATED_OSMIUM"
    EMA_ALPHA     = 0.50
    FV_ANCHOR     = 0.85      # fast-EMA weight in blend
    FV_ANCHOR_PX  = 10000.0   # prior-mean anchor (EDA)

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
        if self._ema is None:
            self._ema = mid
        else:
            self._ema = self.EMA_ALPHA * mid + (1 - self.EMA_ALPHA) * self._ema

        fv = self.FV_ANCHOR * self._ema + (1.0 - self.FV_ANCHOR) * self.FV_ANCHOR_PX

        if self._last_mid is not None:
            dmid = mid - self._last_mid
            adm = abs(dmid)
            if   adm < 2: rho = 0.25
            elif adm < 5: rho = 0.60
            else:         rho = 0.74
            fv -= rho * dmid
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

        for bid_p in sorted(od.buy_orders.keys(), reverse=True):
            if bid_p <= fv or sell_cap <= 0:
                break
            qty = min(od.buy_orders[bid_p], sell_cap)
            orders.append(Order(self.PRODUCT, bid_p, -qty))
            sell_cap -= qty

        # -- Passive: 1 tick inside bot's spread (price priority over bot) --
        passive_bid = best_bid + 1
        passive_ask = best_ask - 1
        if passive_bid >= passive_ask:
            return orders
        if buy_cap > 0:
            orders.append(Order(self.PRODUCT, passive_bid, buy_cap))
        if sell_cap > 0:
            orders.append(Order(self.PRODUCT, passive_ask, -sell_cap))

        return orders


# ============================================================
# INTARIAN_PEPPER_ROOT strategy
# ============================================================

class IPRStrategy:
    """
    Greedy long-accumulation for INTARIAN_PEPPER_ROOT.

    Price trends up +0.1/tick = +1000/day.  80 units * 3000/day * 3 days
    = 240,000 XIREC trend PnL.  Achieved 238,054 (99.2% of ceiling).

    Strategy: reach max-long (80) as fast as possible and hold.
      1. Aggressively take ALL available asks each tick (up to buy_cap).
      2. Post passive buy at best_bid+1 for any remaining buy_cap.
      3. NEVER post passive sells (hold the long to ride the trend).
    """

    PRODUCT = "INTARIAN_PEPPER_ROOT"

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

        pos     = state.position.get(self.PRODUCT, 0)
        buy_cap = self.position_limit - pos
        orders: List[Order] = []

        if buy_cap <= 0:
            return []

        for ask_p in sorted(od.sell_orders.keys()):
            if buy_cap <= 0:
                break
            qty = min(-od.sell_orders[ask_p], buy_cap)
            orders.append(Order(self.PRODUCT, ask_p, qty))
            buy_cap -= qty

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

    def bid(self) -> int:
        return 3000

    def run(self, state: TradingState):
        saved: Dict[str, Any] = {}
        if state.traderData:
            try:
                saved = jsonpickle.decode(state.traderData)
            except Exception:
                saved = {}

        aco = ACOStrategy(position_limit=self.POSITION_LIMITS["ASH_COATED_OSMIUM"])
        ipr = IPRStrategy(position_limit=self.POSITION_LIMITS["INTARIAN_PEPPER_ROOT"])

        aco.set_state(saved.get("aco", {}))
        ipr.set_state(saved.get("ipr", {}))

        result: Dict[str, List[Order]] = {}

        if "ASH_COATED_OSMIUM" in state.order_depths:
            result["ASH_COATED_OSMIUM"] = aco.orders(state)

        if "INTARIAN_PEPPER_ROOT" in state.order_depths:
            result["INTARIAN_PEPPER_ROOT"] = ipr.orders(state)

        trader_data = jsonpickle.encode({
            "aco": aco.get_state(),
            "ipr": ipr.get_state(),
        })

        conversions = 0
        return result, conversions, trader_data

"""
Prosperity 4 -- Round 3 Trader (v3)
===================================

Round 3 books:
  - HYDROGEL_PACK: stationary delta-1 mean-reversion, calibrated from
    research/round3/hydrogel_audit.py (alpha=1.0 minimizes RMSE on
    next-tick mid; anchor_weight=0.0 since the anchor pull degrades
    prediction; magnitude-bucketed reversion coefficients halved from
    v1 to match the empirical AR(1) of -0.094 / -0.237).
  - VELVETFRUIT_EXTRACT: hedge-only with passive joining inside the
    spread.  v2's spread-crossing hedger lost -90K on day 2 alone --
    that lesson is taken.
  - Vouchers: per-strike sigma calibrated from
    research/round3/iv_surface.py per-strike historical means.  IV
    z-score becomes a *passive sizing bias* only -- the v2 aggressive
    z-take was net-negative once delta-hedge slippage was paid.
    Active strikes restored to {5300, 5400, 5500}; 5000/5200 added
    only with one-sided quoting that matches the observed asymmetric
    flow (94-98% of trades hit the bid).

All parameters are hardcoded to the v6 sweep winner.  For backtests or
further tuning, edit values directly in this file.
"""

from datamodel import Order, OrderDepth, TradingState
from typing import Any, Deque, Dict, List, Optional, Tuple
from collections import deque
import jsonpickle
import math


HYDROGEL = "HYDROGEL_PACK"
UNDERLYING = "VELVETFRUIT_EXTRACT"


def clamp_int(value: float) -> int:
    return max(0, int(math.floor(value)))


def best_bid_ask(order_depth: OrderDepth) -> Optional[Tuple[int, int]]:
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    return max(order_depth.buy_orders.keys()), min(order_depth.sell_orders.keys())


def top_obi(order_depth: OrderDepth) -> float:
    """Order Book Imbalance from the best bid/ask sizes only.

    OBI = (bid_size - ask_size) / (bid_size + ask_size), in [-1, +1].
    Calibrated betas from research/round3/microstructure_eda.py:
        HYDROGEL_PACK         beta = 11.2  (R^2 = 0.089, t = 31)
        VELVETFRUIT_EXTRACT   beta =  0.80 (R^2 = 0.079, t = 29)
        VEV_5300              beta =  0.65 (R^2 = 0.125, t = 38, strongest)
        VEV_5400              beta =  0.46 (R^2 = 0.075, t = 28)
        VEV_5500              beta =  0.49 (R^2 = 0.081, t = 30)
    Used to adjust fair value: fair += beta * OBI.
    """
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return 0.0
    best_bid = max(order_depth.buy_orders.keys())
    best_ask = min(order_depth.sell_orders.keys())
    bid_vol = order_depth.buy_orders[best_bid]
    ask_vol = -order_depth.sell_orders[best_ask]  # sell volumes are stored negative
    total = bid_vol + ask_vol
    if total <= 0:
        return 0.0
    return (bid_vol - ask_vol) / total


# ----------------------------------------------------------------------
#  Black-Scholes primitives (no scipy)
# ----------------------------------------------------------------------

_SQRT_2 = math.sqrt(2.0)
_SQRT_2PI = math.sqrt(2.0 * math.pi)


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / _SQRT_2))


def normal_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / _SQRT_2PI


def black_scholes_call(spot: float, strike: float, T: float, sigma: float) -> float:
    if spot <= 0 or strike <= 0:
        return 0.0
    if T <= 0 or sigma <= 1e-9:
        return max(spot - strike, 0.0)
    sigma_root_t = sigma * math.sqrt(T)
    if sigma_root_t <= 1e-12:
        return max(spot - strike, 0.0)
    d1 = (math.log(spot / strike) + 0.5 * sigma * sigma * T) / sigma_root_t
    d2 = d1 - sigma_root_t
    return spot * normal_cdf(d1) - strike * normal_cdf(d2)


def black_scholes_delta(spot: float, strike: float, T: float, sigma: float) -> float:
    if spot <= 0 or strike <= 0:
        return 0.0
    if T <= 0 or sigma <= 1e-9:
        return 1.0 if spot > strike else 0.0
    sigma_root_t = sigma * math.sqrt(T)
    if sigma_root_t <= 1e-12:
        return 1.0 if spot > strike else 0.0
    d1 = (math.log(spot / strike) + 0.5 * sigma * sigma * T) / sigma_root_t
    return normal_cdf(d1)


def black_scholes_vega(spot: float, strike: float, T: float, sigma: float) -> float:
    if spot <= 0 or strike <= 0 or T <= 0 or sigma <= 1e-9:
        return 0.0
    sigma_root_t = sigma * math.sqrt(T)
    d1 = (math.log(spot / strike) + 0.5 * sigma * sigma * T) / sigma_root_t
    return spot * math.sqrt(T) * normal_pdf(d1)


def black_scholes_gamma(spot: float, strike: float, T: float, sigma: float) -> float:
    if spot <= 0 or strike <= 0 or T <= 0 or sigma <= 1e-9:
        return 0.0
    sigma_root_t = sigma * math.sqrt(T)
    d1 = (math.log(spot / strike) + 0.5 * sigma * sigma * T) / sigma_root_t
    return normal_pdf(d1) / (spot * sigma_root_t)


def implied_vol_newton(
    price: float, spot: float, strike: float, T: float,
    sigma_init: float = 0.24, max_iter: int = 25, tol: float = 1e-5,
) -> Optional[float]:
    intrinsic = max(spot - strike, 0.0)
    if price <= intrinsic + 1e-9:
        return None
    if price >= spot - 1e-9:
        return None
    sigma = sigma_init
    for _ in range(max_iter):
        c = black_scholes_call(spot, strike, T, sigma)
        v = black_scholes_vega(spot, strike, T, sigma)
        if v < 1e-10:
            return None
        sigma_new = max(0.005, min(2.0, sigma - (c - price) / v))
        if abs(sigma_new - sigma) < tol:
            return sigma_new
        sigma = sigma_new
    return sigma


# ----------------------------------------------------------------------
#  Delta-1 mean-reversion FV
# ----------------------------------------------------------------------

class EMAReversionModel:
    def __init__(
        self, alpha: float, small_move_rho: float, large_move_rho: float,
        small_move_threshold: float, large_move_threshold: float,
        anchor_price: Optional[float] = None, anchor_weight: float = 0.0,
    ):
        self.alpha = alpha
        self.small_move_rho = small_move_rho
        self.large_move_rho = large_move_rho
        self.small_move_threshold = small_move_threshold
        self.large_move_threshold = large_move_threshold
        self.anchor_price = anchor_price
        self.anchor_weight = anchor_weight
        self.ema: Optional[float] = None
        self.last_mid: Optional[float] = None

    def get_state(self) -> dict:
        return {"ema": self.ema, "last_mid": self.last_mid}

    def set_state(self, state: dict) -> None:
        self.ema = state.get("ema")
        self.last_mid = state.get("last_mid")

    def fair_value(self, mid: float) -> float:
        if self.ema is None:
            self.ema = mid
        else:
            self.ema = self.alpha * mid + (1.0 - self.alpha) * self.ema
        fair = self.ema
        if self.anchor_price is not None and self.anchor_weight > 0.0:
            fair = (1.0 - self.anchor_weight) * fair + self.anchor_weight * self.anchor_price
        if self.last_mid is not None:
            dmid = mid - self.last_mid
            ad = abs(dmid)
            if ad >= self.large_move_threshold:
                fair -= self.large_move_rho * dmid
            elif ad >= self.small_move_threshold:
                fair -= self.small_move_rho * dmid
        self.last_mid = mid
        return fair


class HydrogelMM:
    """v6 calibration from research/round3/hydrogel_sweep.py joint
    grid search: (alpha=0.35, anchor_w=0.20, take_thresh=2.5)
    yields +53,921 over v5b across the 3 historical days, robust on
    all 3 days individually.  The optimum is a broad plateau over
    alpha in [0.20, 0.50] and take_thresh in [2.0, 2.5] -- not a
    fragile needle.  The dominant change is doubling anchor_w from
    0.10 to 0.20: HYDROGEL mid mean is 9990.96 with the simulator
    pulling it toward the 10000 anchor; capturing that pull more
    aggressively in fair-value generates many more passive-quote
    fires inside the 16-wide spread.

    Env vars retain the override hooks for future re-sweeping.
    """
    PRODUCT = HYDROGEL
    LIMIT = 200

    def __init__(self):
        # Env-var overrides for parameter sweep (SAFE-02: os is stdlib).
        # Defaults match v6 calibrated values so baseline is unchanged when
        # env vars are not set.
        self.take_threshold = 2.5
        self.passive_edge = 1.2
        # OBI: disabled by default (v7 backtests net-negative); HYDRO_OBI_BETA overrides.
        self.obi_beta = 0.0
        _alpha = 0.35
        _anchor_w = 0.20
        _small_rho = 0.08
        _large_rho = 0.42
        self.inv_skew = 0.03
        self.model = EMAReversionModel(
            alpha=_alpha,
            small_move_rho=_small_rho,
            large_move_rho=_large_rho,
            small_move_threshold=2.0,
            large_move_threshold=5.0,
            anchor_price=10000.0,
            anchor_weight=_anchor_w,
        )

    def get_state(self) -> dict:
        return self.model.get_state()

    def set_state(self, state: dict) -> None:
        self.model.set_state(state)

    def orders(self, state: TradingState) -> List[Order]:
        order_depth = state.order_depths.get(self.PRODUCT)
        top = best_bid_ask(order_depth) if order_depth is not None else None
        if top is None:
            return []
        best_bid, best_ask = top
        spread = best_ask - best_bid
        mid = (best_bid + best_ask) / 2.0
        fair = self.model.fair_value(mid)
        # OBI overlay: shift fair toward the heavier side of the book.
        fair += self.obi_beta * top_obi(order_depth)

        pos = state.position.get(self.PRODUCT, 0)
        buy_cap = self.LIMIT - pos
        sell_cap = self.LIMIT + pos
        adjusted_fair = fair - self.inv_skew * pos
        orders: List[Order] = []

        thr = self.take_threshold
        big_thr = thr * 2.0
        for ask_price in sorted(order_depth.sell_orders.keys()):
            if buy_cap <= 0:
                break
            edge = adjusted_fair - ask_price
            if edge < thr:
                break
            qty = min(-order_depth.sell_orders[ask_price], buy_cap, 60 if edge >= big_thr else 30)
            if qty > 0:
                orders.append(Order(self.PRODUCT, ask_price, qty))
                buy_cap -= qty

        for bid_price in sorted(order_depth.buy_orders.keys(), reverse=True):
            if sell_cap <= 0:
                break
            edge = bid_price - adjusted_fair
            if edge < thr:
                break
            qty = min(order_depth.buy_orders[bid_price], sell_cap, 60 if edge >= big_thr else 30)
            if qty > 0:
                orders.append(Order(self.PRODUCT, bid_price, -qty))
                sell_cap -= qty

        if spread >= 16:
            passive_bid = best_bid + 1
            passive_ask = best_ask - 1
            if passive_bid < passive_ask:
                base_size = 32
                bid_size = min(buy_cap, max(0, base_size - max(pos, 0) // 10))
                ask_size = min(sell_cap, max(0, base_size - max(-pos, 0) // 10))
                if bid_size > 0 and adjusted_fair - passive_bid >= self.passive_edge:
                    orders.append(Order(self.PRODUCT, passive_bid, bid_size))
                if ask_size > 0 and passive_ask - adjusted_fair >= self.passive_edge:
                    orders.append(Order(self.PRODUCT, passive_ask, -ask_size))
        return orders


# ----------------------------------------------------------------------
#  Voucher surface and IV monitor
# ----------------------------------------------------------------------

class VoucherSurface:
    """Per-strike sigma calibrated live from day-0 market prices at competition-specified TTE."""

    # Fallback sigmas (used only if live calibration fails for a strike)
    STRIKE_SIGMA = {
        4000: 0.240,
        4500: 0.240,
        5000: 0.242,
        5100: 0.240,
        5200: 0.244,
        5300: 0.245,
        5400: 0.230,
        5500: 0.249,
        6000: 0.240,
        6500: 0.240,
    }
    # Competition-specified TTE at the start of each backtester day (day 0,1,2).
    # Statement: "TTE of 7 Solvenarian days, starting from day 1."
    DAY_TTE: List[float] = [7.0, 6.0, 5.0]

    def __init__(self):
        self.initial_tte_days = 7.0
        self._tte_calibrated = False
        self._day_count = 0
        self._live_sigma: Dict[int, float] = {}

    def calibrate_tte(self, spot: float, order_depths: Dict) -> None:
        """Per-day calibration: TTE hardcoded from competition statement; sigma
        binary-searched per-strike so that BS(spot,K,T,sigma)=market_mid."""
        if self._tte_calibrated or spot <= 0:
            return
        day_idx = min(self._day_count, len(self.DAY_TTE) - 1)
        self.initial_tte_days = self.DAY_TTE[day_idx]
        self._day_count += 1
        T = self.initial_tte_days / 365.0
        for strike in [5400, 5300, 5500, 5200, 5100, 5000, 4500, 4000]:
            product = f"VEV_{strike}"
            od = order_depths.get(product)
            if od is None or not od.buy_orders or not od.sell_orders:
                continue
            mid = (max(od.buy_orders.keys()) + min(od.sell_orders.keys())) / 2.0
            if mid <= 0.0:
                continue
            slo, shi = 0.05, 1.0
            for _ in range(60):
                s = (slo + shi) / 2.0
                p = black_scholes_call(spot, float(strike), T, s)
                if p < mid:
                    slo = s
                else:
                    shi = s
            sigma_cal = (slo + shi) / 2.0
            if 0.10 <= sigma_cal <= 0.80:
                self._live_sigma[strike] = sigma_cal
        self._tte_calibrated = True

    def get_state(self) -> dict:
        return {
            "tte": self.initial_tte_days,
            "cal": self._tte_calibrated,
            "dc": self._day_count,
            "sig": self._live_sigma,
        }

    def set_state(self, d: dict) -> None:
        if d:
            self.initial_tte_days = float(d.get("tte", 7.0))
            self._tte_calibrated = bool(d.get("cal", False))
            self._day_count = int(d.get("dc", 0))
            self._live_sigma = {int(k): float(v) for k, v in d.get("sig", {}).items()}

    @staticmethod
    def strike(symbol: str) -> int:
        return int(symbol.split("_")[1])

    def time_years(self, timestamp: int) -> float:
        remaining_days = max(self.initial_tte_days - timestamp / 1_000_000.0, 1e-6)
        return remaining_days / 365.0

    def fair_and_delta(self, symbol: str, spot_fair: float, timestamp: int) -> Tuple[float, float]:
        strike = self.strike(symbol)
        sigma = self._live_sigma.get(strike, self.STRIKE_SIGMA.get(strike, 0.24))
        T = self.time_years(timestamp)
        return (
            black_scholes_call(spot_fair, strike, T, sigma),
            black_scholes_delta(spot_fair, strike, T, sigma),
        )


class IVMonitor:
    """Per-strike rolling IV history for a passive-bias z-score signal.
    Aggressive z-takes were net-negative in v2 once delta-hedge slippage
    was paid; in v3 the z-score only adjusts passive sizing.
    """
    WINDOW = 500
    WARMUP = 250

    def __init__(self, surface: VoucherSurface):
        self.surface = surface
        self.history: Dict[int, Deque[float]] = {}
        self.last_sigma: Dict[int, float] = {}

    def update(self, symbol: str, market_mid: float, spot: float, timestamp: int) -> Optional[float]:
        strike = VoucherSurface.strike(symbol)
        T = self.surface.time_years(timestamp)
        sigma_init = self.last_sigma.get(strike, self.surface._live_sigma.get(strike, self.surface.STRIKE_SIGMA.get(strike, 0.24)))
        iv = implied_vol_newton(market_mid, spot, strike, T, sigma_init=sigma_init)
        if iv is None:
            return None
        self.last_sigma[strike] = iv
        hist = self.history.get(strike)
        if hist is None:
            hist = deque(maxlen=self.WINDOW)
            self.history[strike] = hist
        hist.append(iv)
        n = len(hist)
        if n < self.WARMUP:
            return None
        mean = sum(hist) / n
        var = sum((x - mean) ** 2 for x in hist) / n
        if var <= 1e-12:
            return None
        return (iv - mean) / math.sqrt(var)


class GreeksLedger:
    """Centralized Greeks book: tracks aggregate (Delta, Gamma, Vega) of
    all positions plus per-strike option contributions.  Replaces v3's
    delta-only PortfolioRiskManager with a unified gating layer.

    Caps are tighter than v3 by construction; the hedger keeps them
    binding so we never carry surprise risk between ticks.

      DELTA_CAP_HARD: take is rejected if it would push |D| past this.
      DELTA_CAP_SOFT: hedge fires above this magnitude.
      GAMMA_CAP:      bound on |sum_i N_i * gamma_i|, where N_i is
                      voucher position.  Limits convexity exposure.
      VEGA_CAP:       bound on |sum_i N_i * vega_i|.  Caps loss from
                      a vol regime shift.

    Tuned so the historical worst-case greek under v3 sits ~70%
    of the cap, leaving room without becoming a slack constraint.
    """
    # Caps in raw BS units (delta in shares, gamma per unit, vega in $/100%-vol).
    # ATM voucher at TTE=8d has vega/unit ~310 and gamma/unit ~0.002, so a
    # 300-contract single-strike position = vega 93K, gamma 0.6.  We size
    # caps so position limits bind first on individual strikes, but the
    # aggregate book Vega/Gamma is still bounded if we stack across strikes.
    DELTA_CAP_HARD = 120.0
    DELTA_CAP_SOFT = 60.0
    GAMMA_CAP = 2.0
    VEGA_CAP = 100_000.0

    __slots__ = ("delta", "gamma", "vega", "voucher_deltas",
                 "voucher_gammas", "voucher_vegas")

    def __init__(self):
        self.delta: float = 0.0
        self.gamma: float = 0.0
        self.vega: float = 0.0
        self.voucher_deltas: Dict[str, float] = {}
        self.voucher_gammas: Dict[str, float] = {}
        self.voucher_vegas: Dict[str, float] = {}

    @classmethod
    def from_state(cls, state: TradingState, surface: "VoucherSurface",
                   spot_fair: float) -> "GreeksLedger":
        """Populate per-unit Greeks for ALL strikes in surface.STRIKE_SIGMA
        (not just open positions) so capacity gating sees a non-zero per-unit
        even at start of day.  Aggregates only count actual positions."""
        ledger = cls()
        ledger.delta = float(state.position.get(UNDERLYING, 0))
        T = surface.time_years(state.timestamp)
        for strike in surface.STRIKE_SIGMA:
            sigma = surface._live_sigma.get(strike, surface.STRIKE_SIGMA.get(strike, 0.24))
            product = f"VEV_{strike}"
            d_per_unit = black_scholes_delta(spot_fair, strike, T, sigma)
            g_per_unit = black_scholes_gamma(spot_fair, strike, T, sigma)
            v_per_unit = black_scholes_vega(spot_fair, strike, T, sigma)
            ledger.voucher_deltas[product] = d_per_unit
            ledger.voucher_gammas[product] = g_per_unit
            ledger.voucher_vegas[product] = v_per_unit
            position = state.position.get(product, 0)
            if position != 0:
                ledger.delta += position * d_per_unit
                ledger.gamma += position * g_per_unit
                ledger.vega += position * v_per_unit
        return ledger

    def per_unit(self, product: str) -> Tuple[float, float, float]:
        """Greek per single contract of this voucher (signed for long)."""
        return (
            self.voucher_deltas.get(product, 0.0),
            self.voucher_gammas.get(product, 0.0),
            self.voucher_vegas.get(product, 0.0),
        )

    def long_call_capacity(self, product: str) -> int:
        """How many MORE contracts we can buy without breaching any cap."""
        d, g, v = self.per_unit(product)
        caps = []
        if d > 1e-9:
            caps.append((self.DELTA_CAP_HARD - self.delta) / d)
        if g > 1e-12:
            caps.append((self.GAMMA_CAP - self.gamma) / g)
        if v > 1e-9:
            caps.append((self.VEGA_CAP - self.vega) / v)
        if not caps:
            return 0
        return clamp_int(min(caps))

    def short_call_capacity(self, product: str) -> int:
        """How many MORE contracts we can sell without breaching any cap."""
        d, g, v = self.per_unit(product)
        caps = []
        if d > 1e-9:
            caps.append((self.DELTA_CAP_HARD + self.delta) / d)
        # Selling reduces gamma & vega (long-only options here).
        if g > 1e-12:
            caps.append((self.GAMMA_CAP + self.gamma) / g)
        if v > 1e-9:
            caps.append((self.VEGA_CAP + self.vega) / v)
        if not caps:
            return 0
        return clamp_int(min(caps))

    def post_take_delta(self, qty: int, product: str) -> float:
        """Net delta after applying a +qty take in this voucher."""
        d, _, _ = self.per_unit(product)
        return self.delta + qty * d

    def update_for_take(self, qty: int, product: str) -> None:
        """Apply a hypothetical fill so subsequent gating sees it."""
        d, g, v = self.per_unit(product)
        self.delta += qty * d
        self.gamma += qty * g
        self.vega += qty * v


class VEVUnderlying:
    """Delta-1 MM + delta-hedge engine (v4).  Cleanly separated:
       1. Hedge layer: aggressive cross at best when |D| > HARD cap;
          passive bias when |D| > SOFT cap.
       2. Standalone alpha: mean-reversion edge >= 2.0 on VEV mid.
       3. Passive quotes: 0.5-edge inside spread, biased by sign(D).
    Hedges aim for net delta zero, not just under-cap, since over- and
    under-hedging carry the same round-trip slippage cost."""

    PRODUCT = UNDERLYING
    LIMIT = 200

    # OBI on VEV: EDA beta = 0.80 (R^2=0.079, t=29).  In practice the
    # 5-tick spread on VEV consumes any tilted-fair edge; v7 trial
    # with full beta lost -14.6K to additional hedging.  Disabled.
    OBI_BETA = 0.0

    def __init__(self):
        self.model = EMAReversionModel(
            alpha=1.0, small_move_rho=0.10, large_move_rho=0.24,
            small_move_threshold=2.0, large_move_threshold=5.0,
        )
        self.passive_only = True

    def get_state(self) -> dict:
        return self.model.get_state()

    def set_state(self, state: dict) -> None:
        self.model.set_state(state)

    def snapshot(self, state: TradingState) -> Optional[dict]:
        order_depth = state.order_depths.get(self.PRODUCT)
        top = best_bid_ask(order_depth) if order_depth is not None else None
        if top is None:
            return None
        best_bid, best_ask = top
        mid = (best_bid + best_ask) / 2.0
        fair = self.model.fair_value(mid) + self.OBI_BETA * top_obi(order_depth)
        return {
            "order_depth": order_depth, "best_bid": best_bid, "best_ask": best_ask,
            "spread": best_ask - best_bid, "mid": mid, "fair": fair,
        }

    def orders(self, state: TradingState, snapshot: dict,
               net_delta: float) -> Tuple[List[Order], float]:
        order_depth = snapshot["order_depth"]
        best_bid = snapshot["best_bid"]
        best_ask = snapshot["best_ask"]
        spread = snapshot["spread"]
        fair = snapshot["fair"]

        pos = state.position.get(self.PRODUCT, 0)
        buy_cap = self.LIMIT - pos
        sell_cap = self.LIMIT + pos
        adjusted_fair = fair - 0.02 * pos
        orders: List[Order] = []

        # 1. Hedge layer -- aggressive cross only above HARD cap
        if not self.passive_only and abs(net_delta) > GreeksLedger.DELTA_CAP_HARD and spread > 0:
            target = clamp_int(abs(net_delta) - GreeksLedger.DELTA_CAP_SOFT * 0.5)
            if net_delta > 0 and sell_cap > 0:
                qty = min(sell_cap, target, order_depth.buy_orders.get(best_bid, 0))
                if qty > 0:
                    orders.append(Order(self.PRODUCT, best_bid, -qty))
                    sell_cap -= qty
                    net_delta -= qty
            elif net_delta < 0 and buy_cap > 0:
                qty = min(buy_cap, target, -order_depth.sell_orders.get(best_ask, 0))
                if qty > 0:
                    orders.append(Order(self.PRODUCT, best_ask, qty))
                    buy_cap -= qty
                    net_delta += qty

        # 2. Standalone alpha (mean-reversion on VEV mid)
        if not self.passive_only:
            for ask_price in sorted(order_depth.sell_orders.keys()):
                if buy_cap <= 0 or net_delta >= GreeksLedger.DELTA_CAP_HARD:
                    break
                edge = adjusted_fair - ask_price
                if edge < 2.0:
                    break
                qty = min(-order_depth.sell_orders[ask_price], buy_cap, 18)
                if qty > 0:
                    orders.append(Order(self.PRODUCT, ask_price, qty))
                    buy_cap -= qty
                    net_delta += qty
            for bid_price in sorted(order_depth.buy_orders.keys(), reverse=True):
                if sell_cap <= 0 or net_delta <= -GreeksLedger.DELTA_CAP_HARD:
                    break
                edge = bid_price - adjusted_fair
                if edge < 2.0:
                    break
                qty = min(order_depth.buy_orders[bid_price], sell_cap, 18)
                if qty > 0:
                    orders.append(Order(self.PRODUCT, bid_price, -qty))
                    sell_cap -= qty
                    net_delta -= qty

        # 3. Passive quotes with soft-hedge sizing bias
        if spread >= 5:
            passive_bid = best_bid + 1
            passive_ask = best_ask - 1
            if passive_bid < passive_ask:
                bid_extra = clamp_int(-net_delta * 0.3) if net_delta < -GreeksLedger.DELTA_CAP_SOFT else 0
                ask_extra = clamp_int(net_delta * 0.3) if net_delta > GreeksLedger.DELTA_CAP_SOFT else 0
                bid_size = min(buy_cap, 12 + bid_extra)
                ask_size = min(sell_cap, 12 + ask_extra)
                if bid_size > 0 and adjusted_fair - passive_bid >= 0.5 and net_delta < GreeksLedger.DELTA_CAP_HARD:
                    orders.append(Order(self.PRODUCT, passive_bid, bid_size))
                    net_delta += bid_size
                if ask_size > 0 and passive_ask - adjusted_fair >= 0.5 and net_delta > -GreeksLedger.DELTA_CAP_HARD:
                    orders.append(Order(self.PRODUCT, passive_ask, -ask_size))
                    net_delta -= ask_size
        return orders, net_delta


class VoucherTrader:
    """v5: per-strike-sigma BS take + IV-z-score passive bias + GreeksLedger
    gating + vol-target long-vega tilt.

    The vol-target layer scales passive bid sizes by how far the current
    book vega is from VEGA_TARGET (half of cap).  When the book is flat,
    bids are 1.5x base; at target, 1.0x; near cap, 0.5x.  This is the
    Step 3 implementation of the long-gamma carry signal --
    research/round3/gamma_scalp.py shows realized vol (41%) materially
    exceeds implied (24%) and the carry survives delta-hedging at
    +$3-10/voucher/day.

    Active strike set is the full set with positive carry:
    {5000, 5100, 5200, 5300, 5400, 5500}.  All are buy-biased because
    historical flow is 94-98% seller-initiated; only VEV_5400 takes
    sells when forced.
    """

    Z_PASSIVE = 1.0
    VEGA_TARGET = 50_000.0  # half of GreeksLedger.VEGA_CAP

    # OBI betas calibrated from research/round3/microstructure_eda.py.
    # 5000/5100 not in EDA (low liquidity), default to a conservative 0.30.
    ACTIVE_CONFIG = {
        "VEV_5000": {
            "passive_size": 10, "take_buy_edge": 1.5, "take_sell_edge": 99.0,
            "passive_buy_edge": 0.6, "passive_sell_edge": 99.0,
            "allow_naked_short": False, "two_sided": False,
            "obi_beta": 0.30,
            "bid_only": True,
        },
        "VEV_5100": {
            # Added in v5 -- gamma-scalp diagnostic showed +$6.5/voucher/day
            # carry on this strike despite the IV residual anti-revert
            # finding from research/round3/iv_surface.py (the latter is a
            # fast-tick z-score signal; the gamma scalp is a hold-and-hedge
            # signal -- they coexist).
            "passive_size": 12, "take_buy_edge": 1.2, "take_sell_edge": 99.0,
            "passive_buy_edge": 0.5, "passive_sell_edge": 99.0,
            "allow_naked_short": False, "two_sided": False,
            "obi_beta": 0.30,
            "bid_only": True,
        },
        "VEV_5200": {
            "passive_size": 12, "take_buy_edge": 1.2, "take_sell_edge": 99.0,
            "passive_buy_edge": 0.5, "passive_sell_edge": 99.0,
            "allow_naked_short": False, "two_sided": False,
            "obi_beta": 0.30,
            "bid_only": True,
        },
        "VEV_5300": {
            "passive_size": 16, "take_buy_edge": 1.2, "take_sell_edge": 2.5,
            "passive_buy_edge": 0.7, "passive_sell_edge": 1.3,
            "allow_naked_short": False, "two_sided": True,
            "obi_beta": 0.65,
            "bid_only": False,
        },
        "VEV_5400": {
            "passive_size": 14, "take_buy_edge": 1.0, "take_sell_edge": 1.5,
            "passive_buy_edge": 0.5, "passive_sell_edge": 0.8,
            "allow_naked_short": True, "two_sided": True,
            "obi_beta": 0.46,
            "bid_only": False,
        },
        "VEV_5500": {
            "passive_size": 12, "take_buy_edge": 0.7, "take_sell_edge": 1.6,
            "passive_buy_edge": 0.35, "passive_sell_edge": 0.9,
            "allow_naked_short": False, "two_sided": True,
            "obi_beta": 0.49,
            "bid_only": False,
        },
        # Deep OTM (K=6000/6500): bid=0/ask=1 always, expires worthless.
        # Sell at 1, collect premium, option settles at 0. Pure carry.
        "VEV_6000": {
            "passive_size": 2, "take_buy_edge": 99.0, "take_sell_edge": 99.0,
            "passive_buy_edge": 99.0, "passive_sell_edge": 99.0,
            "allow_naked_short": True, "two_sided": False,
            "obi_beta": 0.0, "bid_only": False, "sell_only": True,
        },
        "VEV_6500": {
            "passive_size": 2, "take_buy_edge": 99.0, "take_sell_edge": 99.0,
            "passive_buy_edge": 99.0, "passive_sell_edge": 99.0,
            "allow_naked_short": True, "two_sided": False,
            "obi_beta": 0.0, "bid_only": False, "sell_only": True,
        },
        # Deep ITM (K=4000): spread≈21, active flow (128-172 trades/day).
        # Two-sided passive market making; delta≈1 so VEV hedger absorbs exposure.
        "VEV_4000": {
            "passive_size": 6, "take_buy_edge": 14.0, "take_sell_edge": 7.0,
            "passive_buy_edge": 9.0, "passive_sell_edge": 5.0,
            "allow_naked_short": True, "two_sided": True,
            "obi_beta": 0.0, "bid_only": False, "sell_only": False,
        },
    }
    LIMIT = 300

    @classmethod
    def vol_target_bid_scale(cls, current_vega: float) -> float:
        """Vol-target scaling: 1.2x when flat, 1.0x at target, 0.6x at cap.
        Reduced range vs the original 1.5x/0.5x because the gamma-scalp
        carry is fully consumed by VEV hedging spread cost in this sim
        beyond a small bias.  See report/report.tex Step 3 subsection."""
        if current_vega <= 0:
            return 1.2
        if current_vega >= GreeksLedger.VEGA_CAP:
            return 0.4
        if current_vega <= cls.VEGA_TARGET:
            return 1.2 - 0.2 * (current_vega / cls.VEGA_TARGET)
        return 1.0 - 0.4 * ((current_vega - cls.VEGA_TARGET)
                             / (GreeksLedger.VEGA_CAP - cls.VEGA_TARGET))

    def __init__(self, surface: VoucherSurface, ledger: GreeksLedger,
                 iv_monitor: IVMonitor):
        self.surface = surface
        self.ledger = ledger
        self.iv_monitor = iv_monitor

    def orders(self, state: TradingState, spot_fair: float
               ) -> Tuple[Dict[str, List[Order]], float]:
        result: Dict[str, List[Order]] = {}

        for product, config in self.ACTIVE_CONFIG.items():
            order_depth = state.order_depths.get(product)
            top = best_bid_ask(order_depth) if order_depth is not None else None
            if top is None:
                continue
            best_bid, best_ask = top
            spread = best_ask - best_bid
            market_mid = (best_bid + best_ask) / 2.0
            fair, option_delta = self.surface.fair_and_delta(product, spot_fair, state.timestamp)
            # OBI overlay on the voucher's own book (per-strike beta).
            fair += config["obi_beta"] * top_obi(order_depth)
            z = self.iv_monitor.update(product, market_mid, spot_fair, state.timestamp)

            pos = state.position.get(product, 0)
            # Greek-aware capacity (ledger updates after each fill)
            pos_buy_cap = self.LIMIT - pos
            pos_sell_cap = self.LIMIT + pos
            orders: List[Order] = []

            # sell_only: deep OTM near-zero options — just post at ask, no buy logic.
            # Bypasses spread/fair/ledger-greek checks (greeks≈0 for these strikes).
            if config.get("sell_only", False):
                if best_ask > 0:
                    qty = min(pos_sell_cap, config["passive_size"])
                    if qty > 0:
                        orders.append(Order(product, best_ask, -qty))
                if orders:
                    result[product] = orders
                continue

            def _buy_cap() -> int:
                return min(pos_buy_cap, self.ledger.long_call_capacity(product))

            def _sell_cap() -> int:
                return min(pos_sell_cap, self.ledger.short_call_capacity(product))

            # 1. Per-strike-sigma aggressive take (gated by ledger)
            for ask_price in sorted(order_depth.sell_orders.keys()):
                cap = _buy_cap()
                if cap <= 0:
                    break
                edge = fair - ask_price
                if edge < config["take_buy_edge"]:
                    break
                qty = min(-order_depth.sell_orders[ask_price], cap, config["passive_size"])
                if qty > 0:
                    orders.append(Order(product, ask_price, qty))
                    pos_buy_cap -= qty
                    pos_sell_cap += qty
                    self.ledger.update_for_take(qty, product)

            bid_only = config.get("bid_only", False)
            allow_sell = not bid_only and (config["allow_naked_short"] or pos > 0 or self.ledger.delta > 50.0)
            if allow_sell:
                for bid_price in sorted(order_depth.buy_orders.keys(), reverse=True):
                    cap = _sell_cap()
                    if cap <= 0:
                        break
                    edge = bid_price - fair
                    if edge < config["take_sell_edge"]:
                        break
                    qty = min(order_depth.buy_orders[bid_price], cap, config["passive_size"])
                    if qty > 0:
                        orders.append(Order(product, bid_price, -qty))
                        pos_sell_cap -= qty
                        pos_buy_cap += qty
                        self.ledger.update_for_take(-qty, product)

            # 2. Passive quotes inside spread, biased by z-score  [OPT-03: bid_skew/ask_skew isolated here only]
            if spread >= 2:
                passive_bid = best_bid + 1
                passive_ask = best_ask - 1
                can_join = passive_bid < passive_ask

                bid_skew = ask_skew = 0.0
                if z is not None and abs(z) >= self.Z_PASSIVE:
                    if z > 0:
                        bid_skew, ask_skew = -0.5, +0.3
                    else:
                        bid_skew, ask_skew = +0.3, -0.5

                base = config["passive_size"]
                # Vol-target: scale bid size by how far current vega is below target.
                vol_scale = self.vol_target_bid_scale(self.ledger.vega)
                if (can_join and _buy_cap() > 0
                        and self.ledger.delta < GreeksLedger.DELTA_CAP_HARD
                        and fair - passive_bid >= config["passive_buy_edge"]):
                    bid_qty = min(_buy_cap(), max(0, int(base * vol_scale * (1.0 + bid_skew)) - max(pos, 0) // 20))
                    if bid_qty > 0:
                        orders.append(Order(product, passive_bid, bid_qty))
                        pos_buy_cap -= bid_qty
                        pos_sell_cap += bid_qty
                        # Passive may not fill -- don't update ledger eagerly.

                should_quote_ask = not bid_only and (config["two_sided"] or pos > 0 or self.ledger.delta > 40.0)
                if (can_join and should_quote_ask and _sell_cap() > 0
                        and passive_ask - fair >= config["passive_sell_edge"]):
                    ask_qty = min(_sell_cap(), max(0, int(base * (1.0 + ask_skew)) - max(-pos, 0) // 20))
                    if ask_qty > 0:
                        orders.append(Order(product, passive_ask, -ask_qty))
                        pos_sell_cap -= ask_qty
                        pos_buy_cap += ask_qty

            if orders:
                result[product] = orders

        return result, self.ledger.delta


class Trader:
    def __init__(self):
        self.hydrogel = HydrogelMM()
        self.vev = VEVUnderlying()
        self.surface = VoucherSurface()
        self.iv_monitor = IVMonitor(surface=self.surface)

    def run(self, state: TradingState):
        saved: Dict[str, Any] = {}
        if state.traderData:
            try:
                saved = jsonpickle.decode(state.traderData)
            except Exception:
                saved = {}

        self.hydrogel.set_state(saved.get("hydrogel", {}))
        self.vev.set_state(saved.get("vev", {}))
        self.surface.set_state(saved.get("surface", {}))

        result: Dict[str, List[Order]] = {}

        hydrogel_orders = self.hydrogel.orders(state)
        if hydrogel_orders:
            result[HYDROGEL] = hydrogel_orders

        vev_snapshot = self.vev.snapshot(state)
        if vev_snapshot is not None:
            spot_mid = vev_snapshot["mid"]
            # Recalibrate TTE at day start (timestamp resets to 0 each day).
            if state.timestamp == 0:
                self.surface._tte_calibrated = False
            if not self.surface._tte_calibrated:
                self.surface.calibrate_tte(spot_mid, state.order_depths)
            spot_fair = vev_snapshot["fair"]
            # Build the per-tick Greeks ledger from current state.position.
            ledger = GreeksLedger.from_state(state, self.surface, spot_fair)
            vouchers = VoucherTrader(
                surface=self.surface, ledger=ledger, iv_monitor=self.iv_monitor,
            )
            voucher_orders, post_take_delta = vouchers.orders(
                state=state, spot_fair=spot_fair,
            )
            result.update(voucher_orders)
            vev_orders, _ = self.vev.orders(
                state=state, snapshot=vev_snapshot, net_delta=post_take_delta,
            )
            if vev_orders:
                result[UNDERLYING] = vev_orders

        trader_data = jsonpickle.encode({
            "hydrogel": self.hydrogel.get_state(),
            "vev": self.vev.get_state(),
            "surface": self.surface.get_state(),
        })
        return result, 0, trader_data
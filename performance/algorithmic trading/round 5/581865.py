"""Round 5 v42: v41 + blacklist 8 confirmed losers (7 TIER3 + LAMB_WOOL).

User instruction: blacklist 8 products that consistently lose in both v34
and v40 backtesters. The 7 TIER3 products were lose-by-design at LIMIT=5;
SLEEP_POD_LAMB_WOOL was the v40 directional disaster (too risky for $110 gain).

Changes vs v41:
  - REMOVE 7 from TIER3, ADD to MM_BLACKLIST:
    OXYGEN_SHAKE_MORNING_BREATH, GALAXY_SOUNDS_DARK_MATTER, PANEL_2X2,
    ROBOT_LAUNDRY, PANEL_1X2, PANEL_1X4, OXYGEN_SHAKE_MINT
  - ADD SLEEP_POD_LAMB_WOOL to MM_BLACKLIST (was default MM in v34/v41,
    lost -$4,284 v34 / -$5,978 v40 directional)

KEEP at TIER3 (small losses, not worth blacklisting yet):
  - MICROCHIP_RECTANGLE (-$128 in v34)
  - OXYGEN_SHAKE_EVENING_BREATH (-$30 in v34)

Expected backtester gain vs v41: ~$11,849
  - Save the 7 TIER3 losses (now $0 instead of -$1K each at LIMIT=5): ~$7,565
  - Save SLEEP_POD_LAMB_WOOL default-MM loss: ~$4,284
Estimated v42 backtester PnL: ~$74K (vs v41 ~$62K, vs v36 $78K).

Expected full-day gain: blacklisting prevents adverse-selection losses
that scale with trading volume. On full day with 10x more trades, the
MM-loss on these products would have been ~$30-35K. Blacklist saves all of it.

Trade-off: we forgo any chance these products earn money on full day.
Given consistent loss across 12 versions in backtester, that chance is low.

Recommended over v41 if user prefers the more aggressive blacklist.
"""

from datamodel import Order, OrderDepth, TradingState
from typing import Dict, List


LIMIT: int = 10

# v41 directional positions (v34 + STRAWBERRY +10)
TARGETS_DIR: Dict[str, int] = {
    "MICROCHIP_OVAL": -10,
    "PEBBLES_XL": +10,
    "OXYGEN_SHAKE_GARLIC": +10,
    "GALAXY_SOUNDS_BLACK_HOLES": +10,
    "PEBBLES_S": -10,
    "PEBBLES_XS": -10,
    "PANEL_2X4": +10,
    "UV_VISOR_AMBER": -10,
    "UV_VISOR_RED": +10,
    "SNACKPACK_PISTACHIO": -10,
    "PEBBLES_M": -10,
    "PEBBLES_L": -10,
    "SNACKPACK_STRAWBERRY": +10,
}

ALL_R5_PRODUCTS: List[str] = [
    "GALAXY_SOUNDS_DARK_MATTER", "GALAXY_SOUNDS_BLACK_HOLES",
    "GALAXY_SOUNDS_PLANETARY_RINGS", "GALAXY_SOUNDS_SOLAR_WINDS",
    "GALAXY_SOUNDS_SOLAR_FLAMES",
    "SLEEP_POD_SUEDE", "SLEEP_POD_LAMB_WOOL", "SLEEP_POD_POLYESTER",
    "SLEEP_POD_NYLON", "SLEEP_POD_COTTON",
    "MICROCHIP_CIRCLE", "MICROCHIP_OVAL", "MICROCHIP_SQUARE",
    "MICROCHIP_RECTANGLE", "MICROCHIP_TRIANGLE",
    "PEBBLES_XS", "PEBBLES_S", "PEBBLES_M", "PEBBLES_L", "PEBBLES_XL",
    "ROBOT_VACUUMING", "ROBOT_MOPPING", "ROBOT_DISHES",
    "ROBOT_LAUNDRY", "ROBOT_IRONING",
    "UV_VISOR_YELLOW", "UV_VISOR_AMBER", "UV_VISOR_ORANGE",
    "UV_VISOR_RED", "UV_VISOR_MAGENTA",
    "TRANSLATOR_SPACE_GRAY", "TRANSLATOR_ASTRO_BLACK",
    "TRANSLATOR_ECLIPSE_CHARCOAL", "TRANSLATOR_GRAPHITE_MIST",
    "TRANSLATOR_VOID_BLUE",
    "PANEL_1X2", "PANEL_2X2", "PANEL_1X4", "PANEL_2X4", "PANEL_4X4",
    "OXYGEN_SHAKE_MORNING_BREATH", "OXYGEN_SHAKE_EVENING_BREATH",
    "OXYGEN_SHAKE_MINT", "OXYGEN_SHAKE_CHOCOLATE", "OXYGEN_SHAKE_GARLIC",
    "SNACKPACK_CHOCOLATE", "SNACKPACK_VANILLA", "SNACKPACK_PISTACHIO",
    "SNACKPACK_STRAWBERRY", "SNACKPACK_RASPBERRY",
]

# v34's blacklist + 8 confirmed losers from user's analysis
MM_BLACKLIST: set = {
    # v34 inheritance (zero-fill)
    "TRANSLATOR_SPACE_GRAY",
    "GALAXY_SOUNDS_PLANETARY_RINGS",
    "ROBOT_DISHES",
    # NEW: 7 ex-TIER3 losers (LIMIT=5 wasn't enough; full skip is safer)
    "OXYGEN_SHAKE_MORNING_BREATH",  # v34 -$1,258, v40 -$2,410
    "GALAXY_SOUNDS_DARK_MATTER",    # v34 -$938,   v40 -$2,384
    "PANEL_2X2",                    # v34 -$1,464, v40 -$2,180
    "ROBOT_LAUNDRY",                # v34 -$1,000, v40 -$1,782
    "PANEL_1X2",                    # v34 -$929,   v40 -$1,654
    "PANEL_1X4",                    # v34 -$1,007, v40 -$1,626
    "OXYGEN_SHAKE_MINT",            # v34 -$969,   v40 -$1,384
    # NEW: ex-default-MM consistent loser
    "SLEEP_POD_LAMB_WOOL",          # v34 -$4,284 default MM, v40 -$5,978 directional
}

# Reduced TIER3 — only the small-loss products that don't justify blacklisting
TIER3_PRODUCTS: set = {
    "MICROCHIP_RECTANGLE",          # v34 -$128 (tiny)
    "OXYGEN_SHAKE_EVENING_BREATH",  # v34 -$30 (basically zero)
}

MM_PRODUCTS: List[str] = [p for p in ALL_R5_PRODUCTS
                          if p not in TARGETS_DIR and p not in MM_BLACKLIST]

MM_LIMIT_DEFAULT: int = 10
MM_LIMIT_TIER3: int = 5
MM_INNER_SIZE: int = 6
MM_OUTER_SIZE: int = 4
MIN_SPREAD: int = 2
SKEW_THRESHOLD_DEFAULT: int = 6
SKEW_THRESHOLD_TIER3: int = 3

HEDGED_NO_SKEW: set = {"SNACKPACK_CHOCOLATE", "SNACKPACK_VANILLA"}


def best_bid_ask(od):
    if not od.buy_orders or not od.sell_orders:
        return None
    return max(od.buy_orders.keys()), min(od.sell_orders.keys())


def get_mm_settings(product: str) -> tuple[int, int, int, int]:
    if product in TIER3_PRODUCTS:
        return MM_LIMIT_TIER3, 3, 2, SKEW_THRESHOLD_TIER3
    if product in HEDGED_NO_SKEW:
        return MM_LIMIT_DEFAULT, 8, 2, SKEW_THRESHOLD_DEFAULT
    return MM_LIMIT_DEFAULT, MM_INNER_SIZE, MM_OUTER_SIZE, SKEW_THRESHOLD_DEFAULT


class Trader:
    def run(self, state: TradingState) -> tuple[dict, int, str]:
        result: Dict[str, List[Order]] = {}

        for product, target in TARGETS_DIR.items():
            od = state.order_depths.get(product)
            if od is None: continue
            ba = best_bid_ask(od)
            if ba is None: continue
            best_bid, best_ask = ba
            pos = state.position.get(product, 0)
            delta = target - pos
            if delta == 0: continue
            orders: List[Order] = []
            if delta > 0:
                qty = min(delta, LIMIT - pos)
                if qty > 0: orders.append(Order(product, best_ask, qty))
            else:
                qty = max(delta, -LIMIT - pos)
                if qty < 0: orders.append(Order(product, best_bid, qty))
            if orders: result[product] = orders

        for product in MM_PRODUCTS:
            od = state.order_depths.get(product)
            if od is None: continue
            ba = best_bid_ask(od)
            if ba is None: continue
            best_bid, best_ask = ba
            spread = best_ask - best_bid
            if spread < MIN_SPREAD: continue

            mm_limit, inner_size, outer_size, skew_threshold = get_mm_settings(product)
            pos = state.position.get(product, 0)
            buy_room = mm_limit - pos
            sell_room = mm_limit + pos
            if buy_room <= 0 and sell_room <= 0: continue

            bid_offset = 1
            ask_offset = 1
            if product not in HEDGED_NO_SKEW:
                if pos >= skew_threshold:
                    bid_offset = 0
                elif pos <= -skew_threshold:
                    ask_offset = 0

            orders: List[Order] = []
            if buy_room > 0:
                bid_qty = min(buy_room, inner_size)
                bid_price = best_bid + bid_offset
                if bid_price < best_ask:
                    orders.append(Order(product, bid_price, bid_qty))
                    buy_room -= bid_qty
            if sell_room > 0:
                ask_qty = min(sell_room, inner_size)
                ask_price = best_ask - ask_offset
                if ask_price > best_bid:
                    orders.append(Order(product, ask_price, -ask_qty))
                    sell_room -= ask_qty

            if spread >= 3 and buy_room > 0:
                bid_qty = min(buy_room, outer_size)
                if bid_qty > 0:
                    orders.append(Order(product, best_bid, bid_qty))
            if spread >= 3 and sell_room > 0:
                ask_qty = min(sell_room, outer_size)
                if ask_qty > 0:
                    orders.append(Order(product, best_ask, -ask_qty))

            if orders: result[product] = orders

        return result, 0, ""
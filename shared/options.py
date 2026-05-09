from __future__ import annotations

import math


SECONDS_PER_ROUND = 1_000_000
TRADING_DAYS_PER_YEAR = 365.0
ROUND3_HISTORICAL_START_DAYS = {
    0: 8.0,
    1: 7.0,
    2: 6.0,
}


def parse_voucher_strike(symbol: str) -> int:
    try:
        return int(symbol.split("_")[1])
    except (IndexError, ValueError) as exc:
        raise ValueError(f"Unrecognized voucher symbol: {symbol}") from exc


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def time_to_expiry_days(start_days: float, timestamp: int, round_length: int = SECONDS_PER_ROUND) -> float:
    elapsed_days = timestamp / float(round_length)
    return max(start_days - elapsed_days, 1e-6)


def historical_time_to_expiry_days(day: int, timestamp: int) -> float:
    start_days = ROUND3_HISTORICAL_START_DAYS[day]
    return time_to_expiry_days(start_days=start_days, timestamp=timestamp)


def live_time_to_expiry_days(timestamp: int, live_start_days: float = 5.0) -> float:
    return time_to_expiry_days(start_days=live_start_days, timestamp=timestamp)


def time_days_to_years(days: float) -> float:
    return max(days / TRADING_DAYS_PER_YEAR, 1e-9)


def black_scholes_call(spot: float, strike: float, time_years: float, sigma: float) -> float:
    if spot <= 0 or strike <= 0:
        return 0.0
    if time_years <= 0 or sigma <= 1e-9:
        return max(spot - strike, 0.0)

    root_t = math.sqrt(time_years)
    sigma_root_t = sigma * root_t
    if sigma_root_t <= 1e-12:
        return max(spot - strike, 0.0)

    d1 = (math.log(spot / strike) + 0.5 * sigma * sigma * time_years) / sigma_root_t
    d2 = d1 - sigma_root_t
    return spot * norm_cdf(d1) - strike * norm_cdf(d2)


def black_scholes_delta(spot: float, strike: float, time_years: float, sigma: float) -> float:
    if spot <= 0 or strike <= 0:
        return 0.0
    if time_years <= 0 or sigma <= 1e-9:
        return 1.0 if spot > strike else 0.0

    root_t = math.sqrt(time_years)
    sigma_root_t = sigma * root_t
    if sigma_root_t <= 1e-12:
        return 1.0 if spot > strike else 0.0

    d1 = (math.log(spot / strike) + 0.5 * sigma * sigma * time_years) / sigma_root_t
    return norm_cdf(d1)


def call_fair_and_delta(spot: float, strike: float, time_years: float, sigma: float) -> tuple[float, float]:
    fair = black_scholes_call(spot=spot, strike=strike, time_years=time_years, sigma=sigma)
    delta = black_scholes_delta(spot=spot, strike=strike, time_years=time_years, sigma=sigma)
    return fair, delta

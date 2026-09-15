from black_scholes import (
    black_scholes_call,
    black_scholes_call_dividend
)


def implied_volatility_call(
    market_price,
    S,
    K,
    T,
    r,
    low=0.0001,
    high=5.0,
    tolerance=0.000001
):
    while high - low > tolerance:

        mid = (low + high) / 2

        price = black_scholes_call(
            S,
            K,
            T,
            r,
            mid
        )

        if price > market_price:
            high = mid
        else:
            low = mid

    return (low + high) / 2


def implied_volatility_call_dividend(
    market_price,
    S,
    K,
    T,
    r,
    q,
    low=0.0001,
    high=5.0,
    tolerance=0.000001
):
    while high - low > tolerance:

        mid = (low + high) / 2

        price = black_scholes_call_dividend(
            S,
            K,
            T,
            r,
            mid,
            q
        )

        if price > market_price:
            high = mid
        else:
            low = mid

    return (low + high) / 2

import math
from statistics import NormalDist
def black_scholes_call(S, K, T, r, sigma):
    d1 = (
        math.log(S / K)
        + (r + 0.5 * sigma**2) * T
    ) / (sigma * math.sqrt(T))

    d2 = d1 - sigma * math.sqrt(T)

    N = NormalDist().cdf

    call_price = S * N(d1) - K * math.exp(-r * T) * N(d2)

    return call_price

def black_scholes_put(S, K, T, r, sigma):
    d1 = (
        math.log(S / K)
        + (r + 0.5 * sigma**2) * T
    ) / (sigma * math.sqrt(T))

    d2 = d1 - sigma * math.sqrt(T)

    N = NormalDist().cdf

    put_price = K * math.exp(-r * T) * N(-d2) - S * N(-d1)

    return put_price

def black_scholes_greeks(S, K, T, r, sigma):
    d1 = (
        math.log(S / K)
        + (r + 0.5 * sigma**2) * T
    ) / (sigma * math.sqrt(T))

    d2 = d1 - sigma * math.sqrt(T)

    normal = NormalDist()

    N_d1 = normal.cdf(d1)
    N_d2 = normal.cdf(d2)
    pdf_d1 = normal.pdf(d1)

    # Delta
    call_delta = N_d1
    put_delta = N_d1 - 1

    # Gamma
    gamma = pdf_d1 / (
        S * sigma * math.sqrt(T)
    )

    # Vega
    vega = S * pdf_d1 * math.sqrt(T) / 100

    # Theta
    call_theta = (
        -(S * pdf_d1 * sigma) /
        (2 * math.sqrt(T))
        - r * K * math.exp(-r * T) * N_d2
    ) / 365

    put_theta = (
        -(S * pdf_d1 * sigma) /
        (2 * math.sqrt(T))
        + r * K * math.exp(-r * T) * normal.cdf(-d2)
    ) / 365

    # Rho
    call_rho = (
        K * T * math.exp(-r * T) * N_d2
    ) / 100

    put_rho = (
        -K * T * math.exp(-r * T)
        * normal.cdf(-d2)
    ) / 100

    return {
        "call_delta": call_delta,
        "put_delta": put_delta,
        "gamma": gamma,
        "vega": vega,
        "call_theta": call_theta,
        "put_theta": put_theta,
        "call_rho": call_rho,
        "put_rho": put_rho
    }
def black_scholes_call_dividend(S, K, T, r, sigma, q):
    d1 = (
        math.log(S / K)
        + (r - q + 0.5 * sigma**2) * T
    ) / (sigma * math.sqrt(T))

    d2 = d1 - sigma * math.sqrt(T)

    N = NormalDist().cdf

    call_price = (
        S * math.exp(-q * T) * N(d1)
        - K * math.exp(-r * T) * N(d2)
    )

    return call_price


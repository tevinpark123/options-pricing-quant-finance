import math
import random


def monte_carlo_call(S, K, T, r, sigma, simulations=100000):
    total_payoff = 0

    for _ in range(simulations):
        z = random.gauss(0, 1)

        ST = S * math.exp(
            (r - 0.5 * sigma**2) * T
            + sigma * math.sqrt(T) * z
        )

        payoff = max(ST - K, 0)
        total_payoff += payoff

    average_payoff = total_payoff / simulations

    call_price = math.exp(-r * T) * average_payoff

    return call_price

def monte_carlo_put(S, K, T, r, sigma, simulations=100000):
    total_payoff = 0

    for _ in range(simulations):
        z = random.gauss(0, 1)

        ST = S * math.exp(
            (r - 0.5 * sigma**2) * T
            + sigma * math.sqrt(T) * z
        )

        payoff = max(K - ST, 0)
        total_payoff += payoff

    average_payoff = total_payoff / simulations

    put_price = math.exp(-r * T) * average_payoff

    return put_price

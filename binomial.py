import math


def binomial_call(S, K, T, r, sigma, steps=100):
    dt = T / steps

    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u

    p = (
        math.exp(r * dt) - d
    ) / (u - d)

    option_values = []

    for i in range(steps + 1):
        ST = S * (u ** i) * (d ** (steps - i))
        payoff = max(ST - K, 0)
        option_values.append(payoff)

    for step in range(steps - 1, -1, -1):
        new_values = []

        for i in range(step + 1):
            value = math.exp(-r * dt) * (
                p * option_values[i + 1]
                + (1 - p) * option_values[i]
            )

            new_values.append(value)

        option_values = new_values

    return option_values[0]

def binomial_put(S, K, T, r, sigma, steps=100):
    dt = T / steps

    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u

    p = (
        math.exp(r * dt) - d
    ) / (u - d)

    option_values = []

    for i in range(steps + 1):
        ST = S * (u ** i) * (d ** (steps - i))
        payoff = max(K - ST, 0)
        option_values.append(payoff)

    for step in range(steps - 1, -1, -1):
        new_values = []

        for i in range(step + 1):
            value = math.exp(-r * dt) * (
                p * option_values[i + 1]
                + (1 - p) * option_values[i]
            )

            new_values.append(value)

        option_values = new_values

    return option_values[0]

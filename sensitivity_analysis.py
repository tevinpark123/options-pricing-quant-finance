import matplotlib.pyplot as plt

from black_scholes import black_scholes_call


S = 100
K = 105
T = 1
r = 0.05

# Volatility from 5% to 80%
volatilities = [
    x / 100 for x in range(5, 81)
]

call_prices = []

for sigma in volatilities:

    price = black_scholes_call(
        S,
        K,
        T,
        r,
        sigma
    )

    call_prices.append(price)


plt.figure()

plt.plot(
    [v * 100 for v in volatilities],
    call_prices
)

plt.xlabel("Volatility (%)")
plt.ylabel("Call Option Price ($)")
plt.title("Call Option Price vs Volatility")

plt.grid(True)

plt.savefig(
    "figures/call_price_vs_volatility.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Time to expiration from about 1 week to 2 years
times = [
    x / 365 for x in range(7, 731, 7)
]

time_prices = []

sigma = 0.20

for T_value in times:

    price = black_scholes_call(
        S,
        K,
        T_value,
        r,
        sigma
    )

    time_prices.append(price)


plt.figure()

plt.plot(
    times,
    time_prices
)

plt.xlabel("Time to Expiration (Years)")
plt.ylabel("Call Option Price ($)")
plt.title("Call Option Price vs Time to Expiration")

plt.grid(True)

plt.savefig(
    "figures/call_price_vs_time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

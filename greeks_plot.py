import matplotlib.pyplot as plt

from black_scholes import black_scholes_call, black_scholes_greeks


K = 105
T = 1
r = 0.05
sigma = 0.20

stock_prices = list(range(60, 141))

call_prices = []
deltas = []
gammas = []

for S in stock_prices:
    call_price = black_scholes_call(
        S,
        K,
        T,
        r,
        sigma
    )

    greeks = black_scholes_greeks(
        S,
        K,
        T,
        r,
        sigma
    )

    call_prices.append(call_price)
    deltas.append(greeks["call_delta"])
    gammas.append(greeks["gamma"])


plt.plot(stock_prices, call_prices)

plt.xlabel("Stock Price ($)")
plt.ylabel("Call Option Price ($)")
plt.title("Call Option Price vs Stock Price")

plt.grid(True)

plt.savefig(
    "figures/call_price_vs_stock.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.plot(stock_prices, deltas)

plt.xlabel("Stock Price ($)")
plt.ylabel("Call Delta")
plt.title("Call Delta vs Stock Price")

plt.grid(True)

plt.savefig(
    "figures/call_delta_vs_stock.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.plot(stock_prices, gammas)

plt.xlabel("Stock Price ($)")
plt.ylabel("Gamma")
plt.title("Gamma vs Stock Price")

plt.grid(True)

plt.savefig(
    "figures/gamma_vs_stock.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

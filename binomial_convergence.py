import matplotlib.pyplot as plt

from black_scholes import black_scholes_call
from binomial import binomial_call


S = 100
K = 105
T = 1
r = 0.05
sigma = 0.20

bs_price = black_scholes_call(S, K, T, r, sigma)

step_counts = [
    10,
    25,
    50,
    100,
    250,
    500,
    1000
]

errors = []

for steps in step_counts:

    bin_price = binomial_call(
        S,
        K,
        T,
        r,
        sigma,
        steps
    )

    error = abs(bin_price - bs_price)

    errors.append(error)

    print(
        f"{steps} steps: "
        f"Price = ${bin_price:.4f}, "
        f"Error = ${error:.4f}"
    )


plt.plot(step_counts, errors, marker="o")

plt.xlabel("Number of Binomial Steps")
plt.ylabel("Absolute Pricing Error ($)")
plt.title("Binomial Convergence to Black-Scholes")

plt.grid(True)

plt.savefig(
    "binomial_convergence.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

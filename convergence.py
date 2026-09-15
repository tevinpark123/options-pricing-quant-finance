import random
import matplotlib.pyplot as plt

from black_scholes import black_scholes_call
from monte_carlo import monte_carlo_call


S = 100
K = 105
T = 1
r = 0.05
sigma = 0.20

random.seed(42)

bs_price = black_scholes_call(S, K, T, r, sigma)

simulation_counts = [
    1000,
    5000,
    10000,
    50000,
    100000,
    500000
]

trials = 20

average_errors = []

for simulations in simulation_counts:

    trial_errors = []

    for _ in range(trials):

        mc_price = monte_carlo_call(
            S,
            K,
            T,
            r,
            sigma,
            simulations
        )

        error = abs(mc_price - bs_price)

        trial_errors.append(error)

    average_error = sum(trial_errors) / trials

    average_errors.append(average_error)

    print(
        f"{simulations:,} simulations: "
        f"Average Error = ${average_error:.4f}"
    )


plt.plot(
    simulation_counts,
    average_errors,
    marker="o"
)

plt.xscale("log")

plt.xlabel("Number of Simulations")
plt.ylabel("Average Absolute Pricing Error ($)")
plt.title("Monte Carlo Convergence to Black-Scholes")

plt.grid(True)

plt.savefig(
    "figures/monte_carlo_convergence.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

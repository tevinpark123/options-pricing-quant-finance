import random
import matplotlib.pyplot as plt

from black_scholes import black_scholes_call
from monte_carlo import monte_carlo_call
from binomial import binomial_call


S = 100
K = 105
T = 1
r = 0.05
sigma = 0.20

bs_price = black_scholes_call(S, K, T, r, sigma)


# Monte Carlo settings
simulation_counts = [
    1000,
    5000,
    10000,
    50000,
    100000,
    500000
]

trials = 20

random.seed(42)

mc_errors = []

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

    mc_errors.append(average_error)


# Binomial settings
step_counts = [
    10,
    25,
    50,
    100,
    250,
    500,
    1000
]

binomial_errors = []

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

    binomial_errors.append(error)


# Plot Monte Carlo
plt.plot(
    simulation_counts,
    mc_errors,
    marker="o",
    label="Monte Carlo"
)

# Plot Binomial
plt.plot(
    step_counts,
    binomial_errors,
    marker="o",
    label="Binomial"
)

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Computational Steps / Simulations")
plt.ylabel("Absolute Pricing Error ($)")
plt.title("Convergence Comparison: Monte Carlo vs Binomial")

plt.legend()
plt.grid(True)

plt.savefig(
    "figures/model_convergence_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

import time
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


# -------------------------
# Monte Carlo
# -------------------------

simulation_counts = [
    1000,
    5000,
    10000,
    50000,
    100000
]

mc_times = []
mc_errors = []

trials = 10

random.seed(42)

for simulations in simulation_counts:

    trial_times = []
    trial_errors = []

    for _ in range(trials):

        start = time.perf_counter()

        price = monte_carlo_call(
            S, K, T, r, sigma, simulations
        )

        end = time.perf_counter()

        trial_times.append(end - start)
        trial_errors.append(abs(price - bs_price))

    mc_times.append(sum(trial_times) / trials)
    mc_errors.append(sum(trial_errors) / trials)


# -------------------------
# Binomial
# -------------------------

step_counts = [
    10,
    25,
    50,
    100,
    250,
    500
]

bin_times = []
bin_errors = []

for steps in step_counts:

    trial_times = []

    for _ in range(trials):

        start = time.perf_counter()

        price = binomial_call(
            S, K, T, r, sigma, steps
        )

        end = time.perf_counter()

        trial_times.append(end - start)

    bin_times.append(sum(trial_times) / trials)

    bin_errors.append(
        abs(price - bs_price)
    )


# -------------------------
# Print results
# -------------------------

print("Monte Carlo")
print("--------------------")

for sims, runtime, error in zip(
    simulation_counts,
    mc_times,
    mc_errors
):
    print(
        f"{sims:,} simulations | "
        f"Time: {runtime:.6f}s | "
        f"Error: ${error:.4f}"
    )


print("\nBinomial")
print("--------------------")

for steps, runtime, error in zip(
    step_counts,
    bin_times,
    bin_errors
):
    print(
        f"{steps:,} steps | "
        f"Time: {runtime:.6f}s | "
        f"Error: ${error:.4f}"
    )


# -------------------------
# Graph
# -------------------------

plt.plot(
    mc_times,
    mc_errors,
    marker="o",
    label="Monte Carlo"
)

plt.plot(
    bin_times,
    bin_errors,
    marker="o",
    label="Binomial"
)

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Average Runtime (seconds)")
plt.ylabel("Absolute Pricing Error ($)")
plt.title("Pricing Accuracy vs Computational Runtime")

plt.legend()
plt.grid(True)

plt.savefig(
    "figures/runtime_accuracy_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

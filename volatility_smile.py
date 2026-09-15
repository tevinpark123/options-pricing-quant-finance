


import math
from datetime import date, datetime

import matplotlib.pyplot as plt
import yfinance as yf

from implied_volatility import implied_volatility_call_dividend


# --------------------------------------------------
# 1. Load SPY market data
# --------------------------------------------------

ticker = yf.Ticker("SPY")

history = ticker.history(period="1d")

S = float(history["Close"].iloc[-1])

print(f"SPY Price: ${S:.2f}")


# --------------------------------------------------
# 2. Get SPY dividend yield
# --------------------------------------------------

info = ticker.info

q = info.get("dividendYield", 0)

if q is None:
    q = 0

q = float(q)

# Safety check in case Yahoo returns 1.2 instead of 0.012
if q > 0.20:
    q = q / 100

print(f"Dividend Yield: {q * 100:.2f}%")


# --------------------------------------------------
# 3. Choose an expiration at least 30 days away
# --------------------------------------------------

today = date.today()

expirations = ticker.options

chosen_expiration = None

for expiration in expirations:

    expiration_date = datetime.strptime(
        expiration,
        "%Y-%m-%d"
    ).date()

    days_to_expiration = (
        expiration_date - today
    ).days

    if days_to_expiration >= 30:
        chosen_expiration = expiration
        break


if chosen_expiration is None:
    raise ValueError(
        "Could not find an option expiration at least 30 days away."
    )


print(f"Expiration: {chosen_expiration}")


# --------------------------------------------------
# 4. Calculate time to expiration
# --------------------------------------------------

expiration_date = datetime.strptime(
    chosen_expiration,
    "%Y-%m-%d"
).date()

days = (
    expiration_date - today
).days

T = days / 365

print(f"Days to Expiration: {days}")
print(f"Time to Expiration: {T:.4f} years")


# --------------------------------------------------
# 5. Download option chain
# --------------------------------------------------

option_chain = ticker.option_chain(
    chosen_expiration
)

calls = option_chain.calls


print(
    f"Total call contracts downloaded: "
    f"{len(calls)}"
)


# --------------------------------------------------
# 6. Risk-free interest rate
# --------------------------------------------------

# For now we use 4%.
# Later we can replace this with an actual Treasury rate.

r = 0.04

print(f"Risk-Free Rate: {r * 100:.2f}%")


# --------------------------------------------------
# 7. Calculate implied volatility
# --------------------------------------------------

strikes = []
implied_vols = []


for _, option in calls.iterrows():

    K = float(option["strike"])

    bid = float(option["bid"])
    ask = float(option["ask"])

    # ----------------------------------------------
    # Keep strikes relatively close to SPY price
    # ----------------------------------------------

    if K < S * 0.90:
        continue

    if K > S * 1.10:
        continue


    # ----------------------------------------------
    # Require usable bid / ask quotes
    # ----------------------------------------------

    if bid <= 0:
        continue

    if ask <= 0:
        continue

    if ask < bid:
        continue


    # ----------------------------------------------
    # Use midpoint as estimated market price
    # ----------------------------------------------

    market_price = (
        bid + ask
    ) / 2

    if market_price <= 0:
        continue


    # ----------------------------------------------
    # Check basic theoretical call-price bounds
    #
    # Lower bound:
    # S*e^(-qT) - K*e^(-rT)
    #
    # Upper bound:
    # S*e^(-qT)
    # ----------------------------------------------

    lower_bound = max(
        S * math.exp(-q * T)
        - K * math.exp(-r * T),
        0
    )

    upper_bound = (
        S * math.exp(-q * T)
    )

    if market_price <= lower_bound:
        continue

    if market_price >= upper_bound:
        continue


    # ----------------------------------------------
    # Solve for implied volatility
    # ----------------------------------------------

    try:

        iv = implied_volatility_call_dividend(
            market_price,
            S,
            K,
            T,
            r,
            q
        )

        # Keep reasonable IV values
        if 0.01 < iv < 1.00:

            strikes.append(K)

            implied_vols.append(
                iv * 100
            )

    except Exception:
        continue


# --------------------------------------------------
# 8. Sort results by strike
# --------------------------------------------------

results = sorted(
    zip(strikes, implied_vols)
)

strikes = [
    result[0]
    for result in results
]

implied_vols = [
    result[1]
    for result in results
]


# --------------------------------------------------
# 9. Print results
# --------------------------------------------------

print(
    f"\nContracts used: "
    f"{len(strikes)}"
)

print("\nStrike | Implied Volatility")
print("----------------------------")


for strike, iv in zip(
    strikes,
    implied_vols
):

    print(
        f"${strike:.2f} | "
        f"{iv:.2f}%"
    )


# --------------------------------------------------
# 10. Make sure we actually have data
# --------------------------------------------------

if len(strikes) == 0:

    raise ValueError(
        "No valid option contracts remained after filtering."
    )


# --------------------------------------------------
# 11. Plot volatility smile / skew
# --------------------------------------------------

plt.figure()

plt.plot(
    strikes,
    implied_vols,
    marker="o"
)

plt.axvline(
    S,
    linestyle="--",
    label=f"SPY Spot = ${S:.2f}"
)

plt.xlabel(
    "Strike Price ($)"
)

plt.ylabel(
    "Implied Volatility (%)"
)

plt.title(
    "SPY Implied Volatility Smile\n"
    f"Expiration: {chosen_expiration}"
)

plt.legend()

plt.grid(True)

plt.savefig(
    "figures/spy_volatility_smile.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

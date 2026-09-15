import math
from datetime import date, datetime

import pandas as pd

import matplotlib.pyplot as plt
import yfinance as yf

from implied_volatility import implied_volatility_call_dividend


# --------------------------------------------------
# Market data
# --------------------------------------------------

ticker = yf.Ticker("SPY")

history = ticker.history(period="1d")
S = float(history["Close"].iloc[-1])

info = ticker.info

q = info.get("dividendYield", 0)

if q is None:
    q = 0

q = float(q)

if q > 0.20:
    q = q / 100


print(f"SPY Price: ${S:.2f}")
print(f"Dividend Yield: {q * 100:.2f}%")


# --------------------------------------------------
# Expiration
# --------------------------------------------------

today = date.today()

chosen_expiration = None

for expiration in ticker.options:

    expiration_date = datetime.strptime(
        expiration,
        "%Y-%m-%d"
    ).date()

    days = (
        expiration_date - today
    ).days

    if days >= 30:
        chosen_expiration = expiration
        break


expiration_date = datetime.strptime(
    chosen_expiration,
    "%Y-%m-%d"
).date()

days = (
    expiration_date - today
).days

T = days / 365

print(f"Expiration: {chosen_expiration}")
print(f"Days to Expiration: {days}")


# --------------------------------------------------
# Option chain
# --------------------------------------------------

chain = ticker.option_chain(
    chosen_expiration
)

calls = chain.calls
puts = chain.puts

r = 0.04


# --------------------------------------------------
# We need a put IV solver using put-call parity
# --------------------------------------------------

def implied_volatility_put_dividend(
    market_price,
    S,
    K,
    T,
    r,
    q,
    low=0.0001,
    high=5.0,
    tolerance=0.000001
):

    while high - low > tolerance:

        sigma = (
            low + high
        ) / 2

        # Convert BS call into put using put-call parity
        from black_scholes import black_scholes_call_dividend

        call_price = black_scholes_call_dividend(
            S,
            K,
            T,
            r,
            sigma,
            q
        )

        put_price = (
            call_price
            - S * math.exp(-q * T)
            + K * math.exp(-r * T)
        )

        if put_price > market_price:
            high = sigma
        else:
            low = sigma

    return (
        low + high
    ) / 2


# --------------------------------------------------
# Store results
# --------------------------------------------------

results = []


# --------------------------------------------------
# OTM PUTS
# Strike below spot
# --------------------------------------------------

for _, option in puts.iterrows():

    K = float(
        option["strike"]
    )

    if K >= S:
        continue

    if K < S * 0.90:
        continue

    bid = float(
        option["bid"]
    )

    ask = float(
        option["ask"]
    )

    if bid <= 0 or ask <= 0:
        continue

    if ask < bid:
        continue

    market_price = (
        bid + ask
    ) / 2

    if market_price <= 0:
        continue

    try:

        iv = implied_volatility_put_dividend(
            market_price,
            S,
            K,
            T,
            r,
            q
        )

        if 0.01 < iv < 1:

            results.append(
                (
                    K,
                    iv * 100,
                    "Put"
                )
            )

    except Exception:
        continue


# --------------------------------------------------
# OTM CALLS
# Strike above spot
# --------------------------------------------------

for _, option in calls.iterrows():

    K = float(
        option["strike"]
    )

    if K < S:
        continue

    if K > S * 1.10:
        continue

    bid = float(
        option["bid"]
    )

    ask = float(
        option["ask"]
    )

    if bid <= 0 or ask <= 0:
        continue

    if ask < bid:
        continue

    market_price = (
        bid + ask
    ) / 2

    if market_price <= 0:
        continue

    try:

        iv = implied_volatility_call_dividend(
            market_price,
            S,
            K,
            T,
            r,
            q
        )

        if 0.01 < iv < 1:

            results.append(
                (
                    K,
                    iv * 100,
                    "Call"
                )
            )

    except Exception:
        continue


# --------------------------------------------------
# Sort
# --------------------------------------------------

results.sort(
    key=lambda x: x[0]
)


strikes = [
    x[0]
    for x in results
]

ivs = [
    x[1]
    for x in results
]

types = [
    x[2]
    for x in results
]


print(
    f"\nContracts used: "
    f"{len(results)}"
)


print(
    "\nStrike | IV | Type"
)

print(
    "----------------------------"
)

for strike, iv, option_type in results:

    print(
        f"${strike:.2f} | "
        f"{iv:.2f}% | "
        f"{option_type}"
    )


# --------------------------------------------------
# Save results to CSV
# --------------------------------------------------

df = pd.DataFrame(
    results,
    columns=[
        "Strike",
        "Implied Volatility",
        "Option Type"
    ]
)

df.to_csv(
    "data/spy_otm_volatility_skew_data.csv",
    index=False
)

print(
    "\nSaved data to "
    "spy_otm_volatility_skew_data.csv"
)

# --------------------------------------------------
# Graph
# --------------------------------------------------

plt.figure()

plt.plot(
    strikes,
    ivs,
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
    "SPY OTM Implied Volatility Skew\n"
    f"Expiration: {chosen_expiration}"
)

plt.legend()

plt.grid(True)

plt.savefig(
    "figures/spy_otm_volatility_skew.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

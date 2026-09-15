import math
from datetime import date, datetime

import matplotlib.pyplot as plt
import yfinance as yf

from implied_volatility import implied_volatility_call_dividend


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


expiration_date = datetime.strptime(
    chosen_expiration,
    "%Y-%m-%d"
).date()

days = (
    expiration_date - today
).days

T = days / 365

r = 0.04


option_chain = ticker.option_chain(
    chosen_expiration
)

calls = option_chain.calls


strikes = []
our_ivs = []
yahoo_ivs = []


for _, option in calls.iterrows():

    K = float(option["strike"])

    bid = float(option["bid"])
    ask = float(option["ask"])

    yahoo_iv = float(
        option["impliedVolatility"]
    )

    # Keep strikes near spot
    if K < S * 0.90:
        continue

    if K > S * 1.10:
        continue

    # Valid quotes
    if bid <= 0 or ask <= 0:
        continue

    if ask < bid:
        continue

    market_price = (
        bid + ask
    ) / 2

    if market_price <= 0:
        continue


    # Basic theoretical bounds
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


    try:

        our_iv = implied_volatility_call_dividend(
            market_price,
            S,
            K,
            T,
            r,
            q
        )

        if (
            0.01 < our_iv < 1.0
            and 0.01 < yahoo_iv < 1.0
        ):

            strikes.append(K)

            our_ivs.append(
                our_iv * 100
            )

            yahoo_ivs.append(
                yahoo_iv * 100
            )

    except Exception:
        continue


print(
    f"Contracts compared: "
    f"{len(strikes)}"
)


# ----------------------------
# Mean Absolute Error
# ----------------------------

errors = []

for our_iv, yahoo_iv in zip(
    our_ivs,
    yahoo_ivs
):

    errors.append(
        abs(our_iv - yahoo_iv)
    )


if len(errors) > 0:

    mae = sum(errors) / len(errors)

    print(
        f"Mean Absolute IV Difference: "
        f"{mae:.4f} percentage points"
    )


# ----------------------------
# Graph
# ----------------------------

plt.figure()

plt.plot(
    strikes,
    our_ivs,
    marker="o",
    label="Our IV"
)

plt.plot(
    strikes,
    yahoo_ivs,
    marker="o",
    label="Yahoo IV"
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
    "SPY Implied Volatility Validation\n"
    f"Expiration: {chosen_expiration}"
)

plt.legend()

plt.grid(True)

plt.savefig(
    "figures/iv_validation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

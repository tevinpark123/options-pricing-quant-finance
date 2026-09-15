import yfinance as yf


ticker = yf.Ticker("SPY")

# Current SPY price
history = ticker.history(period="1d")

spot_price = history["Close"].iloc[-1]

print(f"SPY Price: ${spot_price:.2f}")


# Available option expiration dates
expirations = ticker.options

print("\nAvailable Expirations:")

for date in expirations[:10]:
    print(date)

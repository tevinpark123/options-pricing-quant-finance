from black_scholes import (
    black_scholes_call,
    black_scholes_put,
    black_scholes_greeks
)
from monte_carlo import monte_carlo_call, monte_carlo_put
from binomial import binomial_call, binomial_put
from implied_volatility import implied_volatility_call

print("Quant Finance Project Started")

S = 100
K = 105
T = 1
r = 0.05
sigma = 0.20

print("Stock Price:", S)
print("Strike Price:", K)
print("Time to Expiration:", T)
print("Risk-Free Rate:", r)
print("Volatility:", sigma)

call_price = black_scholes_call(S, K, T, r, sigma)

print(f"Black-Scholes Call Price: ${call_price:.2f}")

put_price = black_scholes_put(S, K, T, r, sigma)

print(f"Black-Scholes Put Price: ${put_price:.2f}")

mc_call_price = monte_carlo_call(S, K, T, r, sigma)

print(f"Monte Carlo Call Price: ${mc_call_price:.2f}")

mc_put_price = monte_carlo_put(S, K, T, r, sigma)

print(f"Monte Carlo Put Price: ${mc_put_price:.2f}")

call_error = abs(mc_call_price - call_price)
put_error = abs(mc_put_price - put_price)

call_error_pct = (call_error / call_price) * 100
put_error_pct = (put_error / put_price) * 100

print(f"Call Pricing Error: ${call_error:.2f} ({call_error_pct:.2f}%)")
print(f"Put Pricing Error: ${put_error:.2f} ({put_error_pct:.2f}%)")

binomial_call_price = binomial_call(
    S,
    K,
    T,
    r,
    sigma,
    steps=100
)

print(f"Binomial Call Price: ${binomial_call_price:.2f}")

binomial_put_price = binomial_put(
    S,
    K,
    T,
    r,
    sigma,
    steps=100
)

print(f"Binomial Put Price: ${binomial_put_price:.2f}")

print("\nModel Comparison")
print("------------------------------")
print(f"Black-Scholes Call: ${call_price:.2f}")
print(f"Monte Carlo Call:   ${mc_call_price:.2f}")
print(f"Binomial Call:      ${binomial_call_price:.2f}")

mc_call_error = abs(mc_call_price - call_price)
binomial_call_error = abs(binomial_call_price - call_price)

print("\nCall Pricing Errors")
print("------------------------------")
print(f"Monte Carlo Error: ${mc_call_error:.4f}")
print(f"Binomial Error:    ${binomial_call_error:.4f}")


print("\nPut Comparison")
print("------------------------------")
print(f"Black-Scholes Put: ${put_price:.2f}")
print(f"Monte Carlo Put:   ${mc_put_price:.2f}")
print(f"Binomial Put:      ${binomial_put_price:.2f}")

mc_put_error = abs(mc_put_price - put_price)
binomial_put_error = abs(binomial_put_price - put_price)

print("\nPut Pricing Errors")
print("------------------------------")
print(f"Monte Carlo Error: ${mc_put_error:.4f}")
print(f"Binomial Error:    ${binomial_put_error:.4f}")

greeks = black_scholes_greeks(
    S,
    K,
    T,
    r,
    sigma
)

print("\nOption Greeks")
print("------------------------------")

print(f"Call Delta: {greeks['call_delta']:.4f}")
print(f"Put Delta:  {greeks['put_delta']:.4f}")
print(f"Gamma:      {greeks['gamma']:.4f}")
print(f"Vega:       {greeks['vega']:.4f}")
print(f"Call Theta: {greeks['call_theta']:.4f}")
print(f"Put Theta:  {greeks['put_theta']:.4f}")
print(f"Call Rho:   {greeks['call_rho']:.4f}")
print(f"Put Rho:    {greeks['put_rho']:.4f}")

market_call_price = 8.50

implied_vol = implied_volatility_call(
    market_call_price,
    S,
    K,
    T,
    r
)

print("\nImplied Volatility")
print("------------------------------")
print(f"Market Call Price: ${market_call_price:.2f}")
print(f"Implied Volatility: {implied_vol * 100:.2f}%")

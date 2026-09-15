# Options Pricing & Quantitative Finance Project

## Overview

This project implements and compares several option pricing methods in Python, including Black-Scholes, Monte Carlo simulation, and the binomial tree model.

The project also analyzes option Greeks, numerical convergence, computational accuracy, implied volatility, and real SPY option-chain data.

## Objectives

The goals of this project are to:

- Implement the Black-Scholes option pricing model
- Price European call and put options
- Build a Monte Carlo simulation model
- Build a binomial option pricing model
- Compare numerical pricing methods with Black-Scholes
- Analyze convergence and pricing error
- Measure computational runtime
- Calculate option Greeks
- Study option sensitivity to stock price, volatility, and time
- Estimate implied volatility from observed market prices
- Analyze real SPY option-chain data
- Construct an implied volatility skew using OTM options

## Pricing Models

### Black-Scholes

The project implements the closed-form Black-Scholes model for European call and put options.

Inputs include:

- Stock price
- Strike price
- Time to expiration
- Risk-free interest rate
- Volatility

A dividend-adjusted version is also implemented for SPY.

### Monte Carlo Simulation

Stock prices are simulated using geometric Brownian motion.

The estimated option value is calculated as the discounted average payoff across simulated terminal stock prices.

Monte Carlo pricing is compared against the Black-Scholes analytical benchmark.

### Binomial Tree

A Cox-Ross-Rubinstein style binomial model is implemented by dividing the option's life into discrete time steps and recursively discounting expected option values.

## Convergence Analysis

Monte Carlo simulations were tested at increasing simulation counts.

Repeated trials were used to estimate average pricing error relative to Black-Scholes.

The binomial model was also tested across increasing numbers of tree steps.

The results demonstrate convergence toward the analytical Black-Scholes price as numerical resolution increases.

## Runtime Analysis

Pricing error was compared with computational runtime for both Monte Carlo and binomial methods.

This provides a practical comparison of accuracy and computational cost.

## Option Greeks

The following Greeks were calculated:

- Delta
- Gamma
- Vega
- Theta
- Rho

Sensitivity graphs were generated to illustrate how option values and Greeks change with market conditions.

## Implied Volatility

A numerical implied-volatility solver was developed using binary search.

The solver works backward from an observed market option price to determine the volatility that produces that price under the Black-Scholes framework.

## SPY Market Data

Real SPY option-chain data is retrieved using the yfinance Python library.

The analysis incorporates:

- Real option bid and ask prices
- SPY spot price
- Dividend yield
- Option expiration dates
- Strike prices

Implied volatility is calculated using midpoint option prices.

## Volatility Skew

To reduce distortions from deep in-the-money options, the volatility curve uses:

- Out-of-the-money puts below the SPY spot price
- Out-of-the-money calls above the SPY spot price

The resulting volatility skew demonstrates higher implied volatility for downside strikes.

## Technologies

- Python
- matplotlib
- pandas
- yfinance
- statistics
- math

## Project Structure

```text
options_pricing_project/
├── main.py
├── black_scholes.py
├── monte_carlo.py
├── binomial.py
├── implied_volatility.py
├── convergence.py
├── binomial_convergence.py
├── model_comparison.py
├── runtime_comparison.py
├── greeks_plot.py
├── sensitivity_analysis.py
├── market_data.py
├── volatility_smile.py
├── iv_validation.py
├── otm_volatility_skew.py
│
├── data/
│   └── spy_otm_volatility_skew_data.csv
│
└── figures/

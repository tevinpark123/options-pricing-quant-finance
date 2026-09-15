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

### Monte Carlo Convergence

![Monte Carlo Convergence](figures/monte_carlo_convergence.png)

### Binomial Convergence

![Binomial Convergence](figures/binomial_convergence.png)

### Model Convergence Comparison

![Model Comparison](figures/model_convergence_comparison.png)

Monte Carlo simulations were tested at increasing simulation counts.

Repeated trials were used to estimate average pricing error relative to Black-Scholes.

The binomial model was also tested across increasing numbers of tree steps.

The results demonstrate convergence toward the analytical Black-Scholes price as numerical resolution increases.

## Runtime Analysis

Pricing error was compared with computational runtime for both Monte Carlo and binomial methods.

![Runtime vs Accuracy](figures/runtime_accuracy_comparison.png)

This provides a practical comparison of pricing accuracy and computational cost.

## Option Greeks

### Delta Sensitivity

![Call Delta](figures/call_delta_vs_stock.png)

### Gamma Sensitivity

![Gamma](figures/gamma_vs_stock.png)

The following Greeks were calculated:

- Delta
- Gamma
- Vega
- Theta
- Rho

Sensitivity analysis was also performed with respect to stock price, volatility, and time to expiration.

## Implied Volatility

A numerical implied-volatility solver was developed using binary search.

The solver works backward from an observed market option price to determine the volatility that reproduces that price under the Black-Scholes framework.

## SPY Market Data

Real SPY option-chain data is retrieved using the `yfinance` Python library.

The analysis incorporates:

- Real option bid and ask prices
- SPY spot price
- Dividend yield
- Option expiration dates
- Strike prices

Implied volatility is calculated using midpoint option prices.

## Volatility Skew

### SPY OTM Implied Volatility Skew

![SPY Volatility Skew](figures/spy_otm_volatility_skew.png)

To reduce distortions associated with deep in-the-money contracts, the volatility curve uses:

- Out-of-the-money puts below the SPY spot price
- Out-of-the-money calls above the SPY spot price

The resulting volatility skew demonstrates substantially higher implied volatility for downside strikes.

## Technologies

- Python
- Matplotlib
- pandas
- yfinance
- `statistics`
- `math`

## Project Structure

```text
options_pricing_project/
├── README.md
├── requirements.txt
├── .gitignore
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
    ├── monte_carlo_convergence.png
    ├── binomial_convergence.png
    ├── model_convergence_comparison.png
    ├── runtime_accuracy_comparison.png
    ├── call_price_vs_stock.png
    ├── call_delta_vs_stock.png
    ├── gamma_vs_stock.png
    ├── call_price_vs_volatility.png
    ├── call_price_vs_time.png
    ├── iv_validation.png
    ├── spy_volatility_smile.png
    └── spy_otm_volatility_skew.png

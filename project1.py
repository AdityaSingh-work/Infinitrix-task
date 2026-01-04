import numpy as np
import matplotlib.pyplot as plt

S0 = 100           # Initial stock price
mu = 0.08          # Drift (8%) [represents average tendency of stock price movement {annually}]
sigma = 0.20       # Volatility (20%) [measures uncertainty and randomness of the stock price {annually}]
T = 1.0            # Time horizon (1 year) [time period till an option matures]
N = 1000           # Number of simulated paths [number of monte carlo simulations, higher = more accurate, longer compute time]
dt = 1 / 252       # Daily time step [one trading day in years]
steps = int(T/dt)  # Total time in simulation steps [252 trading days in a year]
K = 105            # Call option strike price

# Generate random shocks
# Shape: (steps, N)
rng = np.random.default_rng()
Z = rng.normal(0, 1, size=(steps, N))   # Same as Z[steps][N], Z[t,i] = random shock at time t for path i

# Simulate GBM paths
S = np.zeros((steps + 1, N))    # Makes a 2D array of zeros with (steps+1) rows [time] and N columns [paths]
S[0] = S0

for t in range(1, steps + 1):                   # Geometric Brownian Motion formula
    S[t] = S[t - 1] * np.exp(                   # Shows next price is based on previous price
        (mu - 0.5 * sigma**2) * dt              # Drift correction
        + sigma * np.sqrt(dt) * Z[t - 1]        # Models daily uncertainty
    )

# Plot all price paths
plt.figure(figsize=(10, 6))
plt.plot(S, linewidth=0.5)
plt.title("Simulated Stock Price Paths (GBM)")
plt.xlabel("Time (Days)")
plt.ylabel("Stock Price")
plt.show()

# Histogram of final prices [will be right skewed due to exponential nature of GBM]
final_prices = S[-1]    # Extract final prices from all paths

plt.figure(figsize=(8, 5))
plt.hist(final_prices, bins=50)
plt.title("Histogram of Final Stock Prices")
plt.xlabel("Final Stock Price")
plt.ylabel("Frequency")
plt.show()

# Simulated statistics
sim_mean = np.mean(final_prices)    # Creates an array of mean final prices from all paths
sim_std = np.std(final_prices)      # Creates an array of std final prices from all paths

# Theoretical statistics
theo_mean = S0 * np.exp(mu * T)                                         # Mean of GBM at time T
theo_std = S0 * np.exp(mu * T) * np.sqrt(np.exp(sigma**2 * T) - 1)      # Std of GBM at time T

# European Call Option Pricing
payoffs = np.maximum(final_prices - K, 0)   # Payoff at maturity for each path
call_price = np.mean(payoffs)               # (No discounting assumed)

# Final Summary Output
print("\nFINAL SUMMARY:")
print()
print(f"Mean final price (Theoretical): ${theo_mean:.2f}")
print(f"Mean final price (Simulated)  : ${sim_mean:.2f}")
print()
print(f"Std final price (Theoretical) : ${theo_std:.2f}")
print(f"Std final price (Simulated)   : ${sim_std:.2f}")
print()
print(f"European Call Option Price (K=105): ${call_price:.2f}")
print()
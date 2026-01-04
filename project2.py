import matplotlib.pyplot as plt

# NPV Function [how much value does a series of future cash flows have in today's currency]
def npv(rate, cash_flows):
    total_value = 0.0
    for t in range(len(cash_flows)):
        total_value += cash_flows[t] / ((1 + rate) ** t) # Each year, money loses it's value exponentially
    return total_value


# Calculating IRRs Using bisection method [rate where NPV = 0] [break-even rate]
# at low discount rates, is the project valuable? (positive NPV)
# at high discount rates, is the project worthless? (negative NPV)
# getting exact IRR analytically is hard, so we use numerical methods
def irr_bisection_interval(cash_flows, low, high, tol=1e-6, max_iter=1000): # Wide range to ensure root is bracketed
    npv_low = npv(low, cash_flows)
    npv_high = npv(high, cash_flows)
    # If NPV does not change sign → no real IRR
    # always profitable or always unprofitable or even multiple IRRs [toxic cash flows]
    if npv_low * npv_high > 0:
        return None
    for x in range(max_iter):
        mid = (low + high) / 2
        npv_mid = npv(mid, cash_flows)

        if abs(npv_mid) < tol:
            return mid

        if npv_low * npv_mid < 0:
            high = mid
            npv_high = npv_mid
        else:
            low = mid
            npv_low = npv_mid

    return mid


# Find all IRRs in case of multiple sign changes in cash flows
# here we make a very big grid of rates and look for sign changes in NPV to bracket roots and then apply bisection method
# for each bracketed root [interval where NPV changes sign]
def find_all_irrs(cash_flows, rate_min=-0.99, rate_max=10.0, step=0.001):
    rates = []
    r = rate_min
    while r <= rate_max:    # Generate rate grid of very small steps
        rates.append(r)
        r += step

    npv_values = [npv(r, cash_flows) for r in rates]    # Calculate NPV at each rate

    intervals = []
    for i in range(len(rates) - 1):      # Find intervals where NPV changes sign to bracket roots
        if npv_values[i] * npv_values[i + 1] < 0:
            intervals.append((rates[i], rates[i + 1]))

    irrs = []
    for low, high in intervals:     # Apply bisection method in each interval to find IRR(s)
        irr = irr_bisection_interval(cash_flows, low, high)
        if irr is not None:
            irrs.append(irr)

    return irrs, rates, npv_values

# Cash flows input and discount rates
cash_flows = []
n = int(input("Enter number of periods (including t=0): "))
for t in range(n):
    cf = float(input(f"Enter cash flow at time t={t}: "))
    cash_flows.append(cf)

discount_rates = [0.0, 0.05, 0.10, 0.15, 0.20]

# Calculate NPV and Print Summary Table
npv_values_table = [npv(r, cash_flows) for r in discount_rates]

print("\nNPV AT DIFFERENT DISCOUNT RATES:")
for r, val in zip(discount_rates, npv_values_table):
    print(f"Rate: {int(r*100)}%  NPV: {val:.2f}")

# Calculate IRR
irrs, rates, npv_curve = find_all_irrs(cash_flows)
print("\nIRR RESULTS:")
if irrs:
    for i, r in enumerate(irrs, 1):
        print(f"IRR {i}: {r * 100}%")
else:
    print("No IRR exists in the given rate range")

# Plot cash flows
plt.figure()
plt.bar(range(len(cash_flows)), cash_flows)
plt.title("Cash Flow Timeline")
plt.xlabel("Time Period")
plt.ylabel("Cash Flow")
plt.axhline(0)
plt.show()

# NPV Profile plot
plot_rates = [r for r in rates if -0.1 <= r <= 10.0]
plot_npvs = [npv(r, cash_flows) for r in plot_rates]
plt.figure()
plt.plot(plot_rates, plot_npvs, label="IRR showing curve")
plt.axhline(0, linewidth=1)
plt.title("NPV Profile")
plt.xlabel("Discount Rate")
plt.ylabel("NPV")
plt.legend()
plt.show()

# Plot IRR(s) on a number line
plt.figure()

for irr in irrs:
    plt.axvline(irr, linestyle="--")
    plt.scatter(irr, 0)

plt.axhline(0)
plt.title("IRR Locations (Full Mathematical Range)")
plt.xlabel("Discount Rate")
plt.yticks([])
plt.show()

# Mulple IRRs indicate complex cash flow structures (annuities always have a single IRR only) and in finance, they 
# produce ambiguity as for the same data, different IRRs can suggest different investment decisions. Hence, NPV is often 
# preferred for decision-making.
# Also no IRR means that the project is either always profitable or always unprofitable across the tested discount rates.
# Time value of money is crucial in finance, and NPV captures this by discounting future cash flows to their present value.
# IRR provides a single rate of return, but NPV gives a more comprehensive view of a project's value.
# a certain amount of money today is worth more than the same amount in the future due to its potential earning capacity.
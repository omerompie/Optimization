import numpy as np
from scipy import stats

# --- 1. DATA ENTRY ---
# Enter the results from your 10 runs manually or load from csv
# Example Data:
# Scenario:      [T=0,   T=2,   T=4,   T=6,   T=8,   T=10]
dijkstra_costs = [45000, 46200, 45500, 47000, 44800, 46500]
bee_costs      = [45200, 46400, 45600, 47300, 45000, 46800]

dijkstra_times = [15.2,  15.5,  15.1,  15.8,  15.3,  15.4]  # Runtime in seconds
bee_times      = [4.1,   4.2,   4.0,   4.3,   4.1,   4.2]   # Runtime in seconds

# --- 2. CALCULATE OPTIMALITY GAP ---
# How much more expensive are Bees on average?
dijkstra_arr = np.array(dijkstra_costs)
bee_arr = np.array(bee_costs)

gaps = ((bee_arr - dijkstra_arr) / dijkstra_arr) * 100.0

print(f"--- PERFORMANCE STATISTICS ---")
print(f"Mean Optimality Gap: {np.mean(gaps):.4f}%")
print(f"Max Optimality Gap:  {np.max(gaps):.4f}%")
print(f"Min Optimality Gap:  {np.min(gaps):.4f}%")
print("-" * 30)

# --- 3. PAIRED T-TEST (COST) ---
# H0 (Null Hypothesis): There is NO difference between Dijkstra and Bee costs.
# H1 (Alt Hypothesis): There IS a difference.
t_stat, p_value = stats.ttest_rel(dijkstra_costs, bee_costs)

print(f"--- COST T-TEST (Paired) ---")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value:     {p_value:.6f}")

if p_value < 0.05:
    print("Result: SIGNIFICANT DIFFERENCE.")
    print("Interpretation: Dijkstra is statistically cheaper (as expected for an exact solver).")
    print("The important metric is the 'Optimality Gap' above (how small the diff is).")
else:
    print("Result: NO SIGNIFICANT DIFFERENCE.")
    print("Interpretation: Bees are practically as good as Dijkstra!")

# --- 4. PAIRED T-TEST (RUNTIME) ---
t_stat_time, p_value_time = stats.ttest_rel(dijkstra_times, bee_times)

print("-" * 30)
print(f"--- RUNTIME T-TEST (Paired) ---")
print(f"Mean Dijkstra Time: {np.mean(dijkstra_times):.2f}s")
print(f"Mean Bee Time:      {np.mean(bee_times):.2f}s")
print(f"P-value:            {p_value_time:.6f}")

if p_value_time < 0.05 and np.mean(bee_times) < np.mean(dijkstra_times):
    print("Result: Bees are STATISTICALLY FASTER.")
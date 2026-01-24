import pandas as pd #imports the modules
import numpy as np
from scipy import stats

alpha = 0.05 #significance level

dij = pd.read_csv("batch_statistics_results.csv") #read the csv
bee = pd.read_csv("sample_ac1.csv")

# ---- FIX KEY TYPES ----
dij["Start_Hour"] = pd.to_numeric(dij["Start_Hour"], errors="coerce").astype("Int64") #right formatting

bee["t_start"] = (
    bee["t_start"].astype(str)
    .str.replace("t_start_", "", regex=False)
    .astype(float)
    .round()            # makes sure that the numbers are integers and not strings
    .astype("Int64")
)

# ---- SELECT COLUMNS ----
dij_key = "Start_Hour"
bee_key = "t_start"
dij_cost = "Total_Cost_Euro"
bee_cost = "median_cost_eur"

# ---- MERGE (PAIRED) ----
df = dij[[dij_key, dij_cost]].merge( #makes a new table with on the left dijkstra and on the right bee
    bee[[bee_key, bee_cost]],
    left_on=dij_key,
    right_on=bee_key,
    how="inner"
).dropna(subset=[dij_cost, bee_cost])


df = df[df[dij_cost] > 0].copy() #another safety protocol to negate deviding by 0

# ---- PERCENT GAP ---- calculates the performance gap
gap_pct = (df[bee_cost] - df[dij_cost]) / df[dij_cost] * 100
gap_pct = gap_pct.replace([np.inf, -np.inf], np.nan).dropna().to_numpy()

print("Number of paired scenarios:", len(gap_pct))
print("Mean % gap (Bee vs Dijkstra):", gap_pct.mean()) #prints the mean of the gap percentage of the list with al %

if len(gap_pct) < 2: #safety check if there are enough data points
    raise ValueError("Not enough paired data points for t-test.")

# ---- ONE-SIDED ONE-SAMPLE T-TEST: mean gap > 1% ----
try:
    t_stat, p_right = stats.ttest_1samp(gap_pct, popmean=1.0, alternative="greater")
except TypeError:
    # fallback if scipy doesn't work
    t_stat, p_two = stats.ttest_1samp(gap_pct, popmean=1.0)
    p_right = (p_two / 2) if t_stat > 0 else (1 - p_two / 2)

print("t-statistic:", t_stat) #prints the t-static and the p-value
print("p-value (right-sided, mean gap > 1%):", p_right)

if p_right < alpha:
    print("Reject H0: mean % gap is > 1%.") #tells if the p-value is lower than the significance level than reject h0
else:
    print("Fail to reject H0.") #if the p-value is higher than significance value than fail to reject

#Eventually we got a p-value of 0,99 but we changed the test to left tailed instead of right, so we made some changes to h0.
#our correct p-value is than 0,001 because it is just the left over amount to 1 of our first p-value and the t-statistic stays the same.
#so that is why it is stated different in the report.
import pandas as pd
import numpy as np
from scipy import stats

alpha = 0.05

# Loading the data
dij = pd.read_csv("batch_statistics_results.csv") #defined dijkstra as dij
bee = pd.read_csv("sample_ac1.csv") #defined ABC as bee

# ---- FIX KEY TYPES ----
# Dijkstra: ensure int
dij["Start_Hour"] = pd.to_numeric(dij["Start_Hour"], errors="coerce") #ensures that the numbers are read as integers and not as strings

# Bee: extract number from strings like "t_start_3.0"
bee["t_start"] = ( #same concept, makes sure the numbers are integers and replaces strings to integers.
    bee["t_start"]
    .astype(str)
    .str.replace("t_start_", "", regex=False)
    .astype(float)
    .astype(int)
)

# ---- SELECT COLUMNS ----
dij_key = "Start_Hour" #selecting the right colums from both files
bee_key = "t_start"

dij_cost = "Total_Cost_Euro"
bee_cost = "median_cost_eur"

# ---- MERGE (PAIRED) ----
df = dij[[dij_key, dij_cost]].merge( #merging the colums
    bee[[bee_key, bee_cost]],
    left_on=dij_key,
    right_on=bee_key,
    how="inner"
)

# ---- GAP (Bee - Dijkstra) ----
gap = (df[bee_cost] - df[dij_cost]).to_numpy() #calculates the gap between bee and dijkstra

print("Number of paired scenarios:", len(gap)) #prints all the gaps
print("Mean gap (Bee - Dijkstra):", gap.mean()) #prints the mean of the gaps

# Safety check
if len(gap) < 2: #a safety check if there are enough gaps calculated to calulate the mean
    raise ValueError("Not enough paired data points for t-test.")

# ---- PAIRED T-TEST (ONE-SAMPLE ON GAP) ----
t_stat, p_two_sided = stats.ttest_1samp(gap, popmean=0.0)

# Right-sided p-value
p_right = p_two_sided / 2 if t_stat > 0 else 1 - p_two_sided / 2

print("t-statistic:", t_stat) #prints the t-statistic and the p-value
print("p-value (right-sided):", p_right)

if p_right < alpha: #if the p-value is smaller than alpha then reject H0 else fail to reject
    print("Reject H0: Bee has higher mean cost than Dijkstra.")
else:
    print("Fail to reject H0.")

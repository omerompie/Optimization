# Statistical test Wilcoxen

import pandas as pd

bee = pd.read_csv("sample_ac1.csv")
dij = pd.read_csv("batch_statistics_results.csv")

bee["Start_Hour"] = bee["t_start"].str.replace("t_start_", "", regex=False).astype(float).astype(int)

dij = dij[["Start_Hour", "Total_Cost_Euro"]]

df = bee.merge(dij, on="Start_Hour", how="inner")

df["gap_median_pct"] = (
    (df["median_cost_eur"] - df["Total_Cost_Euro"])
    / df["Total_Cost_Euro"]
) * 100

df.to_csv("ac1_gap_only.csv", index=False)

print(df[["Start_Hour", "median_cost_eur", "Total_Cost_Euro", "gap_median_pct"]])

#For Aircraft 1, the Bee algorithm achieves a median cost
# approximately 1% above the Dijkstra optimum across the tested start times.

from scipy.stats import wilcoxon, ttest_1samp

# Wilcoxon: is gap > 0 ?
stat_w, p_w = wilcoxon(df["gap_median_pct"], alternative="greater")
print("Wilcoxon (gap > 0) p-value:", p_w)

# t-test tegen threshold 2%: is gemiddelde gap > 2% ?
t_stat, p_t = ttest_1samp(df["gap_median_pct"], popmean=2.0, alternative="greater")
print("t-test (mean gap > 2%) p-value:", p_t)

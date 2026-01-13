import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('abc_costs_tstart_0.0.csv')
df2 = pd.read_csv('abc_costs_tstart_0.1.csv')
df3 = pd.read_csv('abc_costs_tstart_0.2.csv')
df4 = pd.read_csv('abc_costs_tstart_0.3.csv')
df5 = pd.read_csv('abc_costs_tstart_0.4.csv')
df6 = pd.read_csv('abc_costs_tstart_0.5.csv')
df7 = pd.read_csv('abc_costs_tstart_0.6.csv')
df8 = pd.read_csv('abc_costs_tstart_0.7.csv')
df9 = pd.read_csv('abc_costs_tstart_0.8.csv')
df10 = pd.read_csv('abc_costs_tstart_0.9.csv')
df11 = pd.read_csv('abc_costs_tstart_1.0.csv')

mean_ac_1_1 = float(df['total_cost_eur'].median())
mean_ac_1_2 = float(df2['total_cost_eur'].median())
mean_ac_1_3 = float(df3['total_cost_eur'].median())
mean_ac_1_4 = float(df4['total_cost_eur'].median())
mean_ac_1_5 = float(df5['total_cost_eur'].median())
mean_ac_1_6 = float(df6['total_cost_eur'].median())
mean_ac_1_7 = float(df7['total_cost_eur'].median())
mean_ac_1_8 = float(df8['total_cost_eur'].median())
mean_ac_1_9 = float(df9['total_cost_eur'].median())
mean_ac_1_10 = float(df10['total_cost_eur'].median())
mean_ac_1_11 = float(df11['total_cost_eur'].median())

medians_ac1 = {
    "t_start_0.0": mean_ac_1_1,
    "t_start_0.1": mean_ac_1_2,
    "t_start_0.2": mean_ac_1_3,
    "t_start_0.3": mean_ac_1_4,
    "t_start_0.4": mean_ac_1_5,
    "t_start_0.5": mean_ac_1_6,
    "t_start_0.6": mean_ac_1_7,
    "t_start_0.7": mean_ac_1_8,
    "t_start_0.8": mean_ac_1_9,
    "t_start_0.9": mean_ac_1_10,
    "t_start_1.0": mean_ac_1_11,
}


from scipy import stats

values = np.array(list(medians_ac1.values()), dtype=float)

mu, sigma = values.mean(), values.std(ddof=1)
#make a histogram
plt.hist(values, bins=11, density=True, alpha=0.7, edgecolor="black")
x = np.linspace(values.min(), values.max(), 400)
plt.plot(x, stats.norm.pdf(x, mu, sigma), linewidth=2)

plt.title("Histogram + normal distribution")
plt.xlabel("value")
plt.ylabel("density")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()



fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)

stats.probplot(values, dist="norm", plot=ax)  # Q–Q plot
ax.set_title("Q–Q plot vs normaal")
ax.grid(True, alpha=0.3)

plt.show()

stat, p = stats.shapiro(values)
print(f"Shapiro-Wilk p-value = {p:.4f}")


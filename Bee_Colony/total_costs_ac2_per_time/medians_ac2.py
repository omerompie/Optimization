import pandas as pd
df = pd.read_csv('abc_costs_ac2_tstart_0.0.csv')
df2 = pd.read_csv('abc_costs_ac2_tstart_0.1.csv')
df3 = pd.read_csv('abc_costs_ac2_tstart_0.2.csv')
df4 = pd.read_csv('abc_costs_ac2_tstart_0.3.csv')
df5 = pd.read_csv('abc_costs_ac2_tstart_0.4.csv')
df6 = pd.read_csv('abc_costs_ac2_tstart_0.5.csv')
df7 = pd.read_csv('abc_costs_ac2_tstart_0.6.csv')
df8 = pd.read_csv('abc_costs_ac2_tstart_0.7.csv')
df9 = pd.read_csv('abc_costs_ac2_tstart_0.8.csv')
df10 = pd.read_csv('abc_costs_ac2_tstart_0.9.csv')
df11 = pd.read_csv('abc_costs_ac2_tstart_1.0.csv')

mean_ac_2_1 = float(df['total_cost_eur'].median())
mean_ac_2_2 = float(df2['total_cost_eur'].median())
mean_ac_2_3 = float(df3['total_cost_eur'].median())
mean_ac_2_4 = float(df4['total_cost_eur'].median())
mean_ac_2_5 = float(df5['total_cost_eur'].median())
mean_ac_2_6 = float(df6['total_cost_eur'].median())
mean_ac_2_7 = float(df7['total_cost_eur'].median())
mean_ac_2_8 = float(df8['total_cost_eur'].median())
mean_ac_2_9 = float(df9['total_cost_eur'].median())
mean_ac_2_10 = float(df10['total_cost_eur'].median())
mean_ac_2_11 = float(df11['total_cost_eur'].median())

medians_ac2 = {
    "t_start_0.0": mean_ac_2_1,
    "t_start_0.1": mean_ac_2_2,
    "t_start_0.2": mean_ac_2_3,
    "t_start_0.3": mean_ac_2_4,
    "t_start_0.4": mean_ac_2_5,
    "t_start_0.5": mean_ac_2_6,
    "t_start_0.6": mean_ac_2_7,
    "t_start_0.7": mean_ac_2_8,
    "t_start_0.8": mean_ac_2_9,
    "t_start_0.9": mean_ac_2_10,
    "t_start_1.0": mean_ac_2_11,
}
print(medians_ac2)




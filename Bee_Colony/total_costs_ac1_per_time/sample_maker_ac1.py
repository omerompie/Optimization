"""
this file makes a sample for ac 1 bee colony
For every scenario, it calculates the median costs, median fuel burn, mean computation time, best costs, worst cost
"""



import pandas as pd

#read all the csvs
df = pd.read_csv('abc_costs_tstart_0.0.csv')
df2 = pd.read_csv('abc_costs_tstart_1.0.csv')
df3 = pd.read_csv('abc_costs_tstart_2.0.csv')
df4 = pd.read_csv('abc_costs_tstart_3.0.csv')
df5 = pd.read_csv('abc_costs_tstart_4.0.csv')
df6 = pd.read_csv('abc_costs_tstart_5.0.csv')
df7 = pd.read_csv('abc_costs_tstart_6.0.csv')
df8 = pd.read_csv('abc_costs_tstart_7.0.csv')
df9 = pd.read_csv('abc_costs_tstart_8.0.csv')
df10 = pd.read_csv('abc_costs_tstart_9.0.csv')
df11 = pd.read_csv('abc_costs_tstart_10.0.csv')
df12 = pd.read_csv('abc_costs_tstart_11.0.csv')
df13 = pd.read_csv('abc_costs_tstart_12.0.csv')
df14 = pd.read_csv('abc_costs_tstart_13.0.csv')
df15 = pd.read_csv('abc_costs_tstart_14.0.csv')
df16 = pd.read_csv('abc_costs_tstart_15.0.csv')
df17 = pd.read_csv('abc_costs_tstart_16.0.csv')
df18 = pd.read_csv('abc_costs_tstart_17.0.csv')
df19 = pd.read_csv('abc_costs_tstart_18.0.csv')
df20 = pd.read_csv('abc_costs_tstart_19.0.csv')
df21 = pd.read_csv('abc_costs_tstart_20.0.csv')
df22 = pd.read_csv('abc_costs_tstart_21.0.csv')
df23 = pd.read_csv('abc_costs_tstart_22.0.csv')
df24 = pd.read_csv('abc_costs_tstart_23.0.csv')
df25 = pd.read_csv('abc_costs_tstart_24.0.csv')
df26 = pd.read_csv('abc_costs_tstart_25.0.csv')
df27 = pd.read_csv('abc_costs_tstart_26.0.csv')
df28 = pd.read_csv('abc_costs_tstart_27.0.csv')
df29 = pd.read_csv('abc_costs_tstart_28.0.csv')
df30 = pd.read_csv('abc_costs_tstart_29.0.csv')
df31 = pd.read_csv('abc_costs_tstart_30.0.csv')

#calculate all the median costs for every scenario
median_ac_1_1 = float(df['total_cost_eur'].median())
median_ac_1_2 = float(df2['total_cost_eur'].median())
median_ac_1_3 = float(df3['total_cost_eur'].median())
median_ac_1_4 = float(df4['total_cost_eur'].median())
median_ac_1_5 = float(df5['total_cost_eur'].median())
median_ac_1_6 = float(df6['total_cost_eur'].median())
median_ac_1_7 = float(df7['total_cost_eur'].median())
median_ac_1_8 = float(df8['total_cost_eur'].median())
median_ac_1_9 = float(df9['total_cost_eur'].median())
median_ac_1_10 = float(df10['total_cost_eur'].median())
median_ac_1_11 = float(df11['total_cost_eur'].median())
median_ac_1_12 = float(df12['total_cost_eur'].median())
median_ac_1_13 = float(df13['total_cost_eur'].median())
median_ac_1_14 = float(df14['total_cost_eur'].median())
median_ac_1_15 = float(df15['total_cost_eur'].median())
median_ac_1_16 = float(df16['total_cost_eur'].median())
median_ac_1_17 = float(df17['total_cost_eur'].median())
median_ac_1_18 = float(df18['total_cost_eur'].median())
median_ac_1_19 = float(df19['total_cost_eur'].median())
median_ac_1_20 = float(df20['total_cost_eur'].median())
median_ac_1_21 = float(df21['total_cost_eur'].median())
median_ac_1_22 = float(df22['total_cost_eur'].median())
median_ac_1_23 = float(df23['total_cost_eur'].median())
median_ac_1_24 = float(df24['total_cost_eur'].median())
median_ac_1_25 = float(df25['total_cost_eur'].median())
median_ac_1_26 = float(df26['total_cost_eur'].median())
median_ac_1_27 = float(df27['total_cost_eur'].median())
median_ac_1_28 = float(df28['total_cost_eur'].median())
median_ac_1_29 = float(df29['total_cost_eur'].median())
median_ac_1_30 = float(df30['total_cost_eur'].median())
median_ac_1_31 = float(df31['total_cost_eur'].median())

#make a dictionary of all medians
medians_ac1 = {
    "t_start_0.0": median_ac_1_1,
    "t_start_1.0": median_ac_1_2,
    "t_start_2.0": median_ac_1_3,
    "t_start_3.0": median_ac_1_4,
    "t_start_4.0": median_ac_1_5,
    "t_start_5.0": median_ac_1_6,
    "t_start_6.0": median_ac_1_7,
    "t_start_7.0": median_ac_1_8,
    "t_start_8.0": median_ac_1_9,
    "t_start_9.0": median_ac_1_10,
    "t_start_10.0": median_ac_1_11,
    "t_start_11.0": median_ac_1_12,
    "t_start_12.0": median_ac_1_13,
    "t_start_13.0": median_ac_1_14,
    "t_start_14.0": median_ac_1_15,
    "t_start_15.0": median_ac_1_16,
    "t_start_16.0": median_ac_1_17,
    "t_start_17.0": median_ac_1_18,
    "t_start_18.0": median_ac_1_19,
    "t_start_19.0": median_ac_1_20,
    "t_start_20.0": median_ac_1_21,
    "t_start_21.0": median_ac_1_22,
    "t_start_22.0": median_ac_1_23,
    "t_start_23.0": median_ac_1_24,
    "t_start_24.0": median_ac_1_25,
    "t_start_25.0": median_ac_1_26,
    "t_start_26.0": median_ac_1_27,
    "t_start_27.0": median_ac_1_28,
    "t_start_28.0": median_ac_1_29,
    "t_start_29.0": median_ac_1_30,
    "t_start_30.0": median_ac_1_31,
}
print(medians_ac1)

#for every scenario, calculate average runtime for each run.
avg_runtime_ac1_1 = float(df['runtime_sec'].mean())
avg_runtime_ac1_2 = float(df2['runtime_sec'].mean())
avg_runtime_ac1_3 = float(df3['runtime_sec'].mean())
avg_runtime_ac1_4 = float(df4['runtime_sec'].mean())
avg_runtime_ac1_5 = float(df5['runtime_sec'].mean())
avg_runtime_ac1_6 = float(df6['runtime_sec'].mean())
avg_runtime_ac1_7 = float(df7['runtime_sec'].mean())
avg_runtime_ac1_8 = float(df8['runtime_sec'].mean())
avg_runtime_ac1_9 = float(df9['runtime_sec'].mean())
avg_runtime_ac1_10 = float(df10['runtime_sec'].mean())
avg_runtime_ac1_11 = float(df11['runtime_sec'].mean())
avg_runtime_ac1_12 = float(df12['runtime_sec'].mean())
avg_runtime_ac1_13 = float(df13['runtime_sec'].mean())
avg_runtime_ac1_14 = float(df14['runtime_sec'].mean())
avg_runtime_ac1_15 = float(df15['runtime_sec'].mean())
avg_runtime_ac1_16 = float(df16['runtime_sec'].mean())
avg_runtime_ac1_17 = float(df17['runtime_sec'].mean())
avg_runtime_ac1_18 = float(df18['runtime_sec'].mean())
avg_runtime_ac1_19 = float(df19['runtime_sec'].mean())
avg_runtime_ac1_20 = float(df20['runtime_sec'].mean())
avg_runtime_ac1_21 = float(df21['runtime_sec'].mean())
avg_runtime_ac1_22 = float(df22['runtime_sec'].mean())
avg_runtime_ac1_23 = float(df23['runtime_sec'].mean())
avg_runtime_ac1_24 = float(df24['runtime_sec'].mean())
avg_runtime_ac1_25 = float(df25['runtime_sec'].mean())
avg_runtime_ac1_26 = float(df26['runtime_sec'].mean())
avg_runtime_ac1_27 = float(df27['runtime_sec'].mean())
avg_runtime_ac1_28 = float(df28['runtime_sec'].mean())
avg_runtime_ac1_29 = float(df29['runtime_sec'].mean())
avg_runtime_ac1_30 = float(df30['runtime_sec'].mean())
avg_runtime_ac1_31 = float(df31['runtime_sec'].mean())

#store at in a dictionary
avg_runtimes_ac1 = {
    "t_start_0.0": avg_runtime_ac1_1,
    "t_start_1.0": avg_runtime_ac1_2,
    "t_start_2.0": avg_runtime_ac1_3,
    "t_start_3.0": avg_runtime_ac1_4,
    "t_start_4.0": avg_runtime_ac1_5,
    "t_start_5.0": avg_runtime_ac1_6,
    "t_start_6.0": avg_runtime_ac1_7,
    "t_start_7.0": avg_runtime_ac1_8,
    "t_start_8.0": avg_runtime_ac1_9,
    "t_start_9.0": avg_runtime_ac1_10,
    "t_start_10.0": avg_runtime_ac1_11,
    "t_start_11.0": avg_runtime_ac1_12,
    "t_start_12.0": avg_runtime_ac1_13,
    "t_start_13.0": avg_runtime_ac1_14,
    "t_start_14.0": avg_runtime_ac1_15,
    "t_start_15.0": avg_runtime_ac1_16,
    "t_start_16.0": avg_runtime_ac1_17,
    "t_start_17.0": avg_runtime_ac1_18,
    "t_start_18.0": avg_runtime_ac1_19,
    "t_start_19.0": avg_runtime_ac1_20,
    "t_start_20.0": avg_runtime_ac1_21,
    "t_start_21.0": avg_runtime_ac1_22,
    "t_start_22.0": avg_runtime_ac1_23,
    "t_start_23.0": avg_runtime_ac1_24,
    "t_start_24.0": avg_runtime_ac1_25,
    "t_start_25.0": avg_runtime_ac1_26,
    "t_start_26.0": avg_runtime_ac1_27,
    "t_start_27.0": avg_runtime_ac1_28,
    "t_start_28.0": avg_runtime_ac1_29,
    "t_start_29.0": avg_runtime_ac1_30,
    "t_start_30.0": avg_runtime_ac1_31,
}

print(avg_runtimes_ac1)

#for every scenario, calculate best costs
best_cost_ac1_1 = float(df['total_cost_eur'].min())
best_cost_ac1_2 = float(df2['total_cost_eur'].min())
best_cost_ac1_3 = float(df3['total_cost_eur'].min())
best_cost_ac1_4 = float(df4['total_cost_eur'].min())
best_cost_ac1_5 = float(df5['total_cost_eur'].min())
best_cost_ac1_6 = float(df6['total_cost_eur'].min())
best_cost_ac1_7 = float(df7['total_cost_eur'].min())
best_cost_ac1_8 = float(df8['total_cost_eur'].min())
best_cost_ac1_9 = float(df9['total_cost_eur'].min())
best_cost_ac1_10 = float(df10['total_cost_eur'].min())
best_cost_ac1_11 = float(df11['total_cost_eur'].min())
best_cost_ac1_12 = float(df12['total_cost_eur'].min())
best_cost_ac1_13 = float(df13['total_cost_eur'].min())
best_cost_ac1_14 = float(df14['total_cost_eur'].min())
best_cost_ac1_15 = float(df15['total_cost_eur'].min())
best_cost_ac1_16 = float(df16['total_cost_eur'].min())
best_cost_ac1_17 = float(df17['total_cost_eur'].min())
best_cost_ac1_18 = float(df18['total_cost_eur'].min())
best_cost_ac1_19 = float(df19['total_cost_eur'].min())
best_cost_ac1_20 = float(df20['total_cost_eur'].min())
best_cost_ac1_21 = float(df21['total_cost_eur'].min())
best_cost_ac1_22 = float(df22['total_cost_eur'].min())
best_cost_ac1_23 = float(df23['total_cost_eur'].min())
best_cost_ac1_24 = float(df24['total_cost_eur'].min())
best_cost_ac1_25 = float(df25['total_cost_eur'].min())
best_cost_ac1_26 = float(df26['total_cost_eur'].min())
best_cost_ac1_27 = float(df27['total_cost_eur'].min())
best_cost_ac1_28 = float(df28['total_cost_eur'].min())
best_cost_ac1_29 = float(df29['total_cost_eur'].min())
best_cost_ac1_30 = float(df30['total_cost_eur'].min())
best_cost_ac1_31 = float(df31['total_cost_eur'].min())

#store them in a dictionary
best_costs_ac1 = {
    "t_start_0.0": best_cost_ac1_1,
    "t_start_1.0": best_cost_ac1_2,
    "t_start_2.0": best_cost_ac1_3,
    "t_start_3.0": best_cost_ac1_4,
    "t_start_4.0": best_cost_ac1_5,
    "t_start_5.0": best_cost_ac1_6,
    "t_start_6.0": best_cost_ac1_7,
    "t_start_7.0": best_cost_ac1_8,
    "t_start_8.0": best_cost_ac1_9,
    "t_start_9.0": best_cost_ac1_10,
    "t_start_10.0": best_cost_ac1_11,
    "t_start_11.0": best_cost_ac1_12,
    "t_start_12.0": best_cost_ac1_13,
    "t_start_13.0": best_cost_ac1_14,
    "t_start_14.0": best_cost_ac1_15,
    "t_start_15.0": best_cost_ac1_16,
    "t_start_16.0": best_cost_ac1_17,
    "t_start_17.0": best_cost_ac1_18,
    "t_start_18.0": best_cost_ac1_19,
    "t_start_19.0": best_cost_ac1_20,
    "t_start_20.0": best_cost_ac1_21,
    "t_start_21.0": best_cost_ac1_22,
    "t_start_22.0": best_cost_ac1_23,
    "t_start_23.0": best_cost_ac1_24,
    "t_start_24.0": best_cost_ac1_25,
    "t_start_25.0": best_cost_ac1_26,
    "t_start_26.0": best_cost_ac1_27,
    "t_start_27.0": best_cost_ac1_28,
    "t_start_28.0": best_cost_ac1_29,
    "t_start_29.0": best_cost_ac1_30,
    "t_start_30.0": best_cost_ac1_31,
}
print(best_costs_ac1)

#for every scenario, determine the worst cost
worst_cost_ac1_1 = float(df['total_cost_eur'].max())
worst_cost_ac1_2 = float(df2['total_cost_eur'].max())
worst_cost_ac1_3 = float(df3['total_cost_eur'].max())
worst_cost_ac1_4 = float(df4['total_cost_eur'].max())
worst_cost_ac1_5 = float(df5['total_cost_eur'].max())
worst_cost_ac1_6 = float(df6['total_cost_eur'].max())
worst_cost_ac1_7 = float(df7['total_cost_eur'].max())
worst_cost_ac1_8 = float(df8['total_cost_eur'].max())
worst_cost_ac1_9 = float(df9['total_cost_eur'].max())
worst_cost_ac1_10 = float(df10['total_cost_eur'].max())
worst_cost_ac1_11 = float(df11['total_cost_eur'].max())
worst_cost_ac1_12 = float(df12['total_cost_eur'].max())
worst_cost_ac1_13 = float(df13['total_cost_eur'].max())
worst_cost_ac1_14 = float(df14['total_cost_eur'].max())
worst_cost_ac1_15 = float(df15['total_cost_eur'].max())
worst_cost_ac1_16 = float(df16['total_cost_eur'].max())
worst_cost_ac1_17 = float(df17['total_cost_eur'].max())
worst_cost_ac1_18 = float(df18['total_cost_eur'].max())
worst_cost_ac1_19 = float(df19['total_cost_eur'].max())
worst_cost_ac1_20 = float(df20['total_cost_eur'].max())
worst_cost_ac1_21 = float(df21['total_cost_eur'].max())
worst_cost_ac1_22 = float(df22['total_cost_eur'].max())
worst_cost_ac1_23 = float(df23['total_cost_eur'].max())
worst_cost_ac1_24 = float(df24['total_cost_eur'].max())
worst_cost_ac1_25 = float(df25['total_cost_eur'].max())
worst_cost_ac1_26 = float(df26['total_cost_eur'].max())
worst_cost_ac1_27 = float(df27['total_cost_eur'].max())
worst_cost_ac1_28 = float(df28['total_cost_eur'].max())
worst_cost_ac1_29 = float(df29['total_cost_eur'].max())
worst_cost_ac1_30 = float(df30['total_cost_eur'].max())
worst_cost_ac1_31 = float(df31['total_cost_eur'].max())

#put it in a dictionary
worst_costs_ac1 = {
    "t_start_0.0": worst_cost_ac1_1,
    "t_start_1.0": worst_cost_ac1_2,
    "t_start_2.0": worst_cost_ac1_3,
    "t_start_3.0": worst_cost_ac1_4,
    "t_start_4.0": worst_cost_ac1_5,
    "t_start_5.0": worst_cost_ac1_6,
    "t_start_6.0": worst_cost_ac1_7,
    "t_start_7.0": worst_cost_ac1_8,
    "t_start_8.0": worst_cost_ac1_9,
    "t_start_9.0": worst_cost_ac1_10,
    "t_start_10.0": worst_cost_ac1_11,
    "t_start_11.0": worst_cost_ac1_12,
    "t_start_12.0": worst_cost_ac1_13,
    "t_start_13.0": worst_cost_ac1_14,
    "t_start_14.0": worst_cost_ac1_15,
    "t_start_15.0": worst_cost_ac1_16,
    "t_start_16.0": worst_cost_ac1_17,
    "t_start_17.0": worst_cost_ac1_18,
    "t_start_18.0": worst_cost_ac1_19,
    "t_start_19.0": worst_cost_ac1_20,
    "t_start_20.0": worst_cost_ac1_21,
    "t_start_21.0": worst_cost_ac1_22,
    "t_start_22.0": worst_cost_ac1_23,
    "t_start_23.0": worst_cost_ac1_24,
    "t_start_24.0": worst_cost_ac1_25,
    "t_start_25.0": worst_cost_ac1_26,
    "t_start_26.0": worst_cost_ac1_27,
    "t_start_27.0": worst_cost_ac1_28,
    "t_start_28.0": worst_cost_ac1_29,
    "t_start_29.0": worst_cost_ac1_30,
    "t_start_30.0": worst_cost_ac1_31,
}
print(worst_costs_ac1)

#for every scenario, determine the median fuel burn

median_fuel_ac_1_1  = float(df['total_fuel_burn_kg'].median())
median_fuel_ac_1_2  = float(df2['total_fuel_burn_kg'].median())
median_fuel_ac_1_3  = float(df3['total_fuel_burn_kg'].median())
median_fuel_ac_1_4  = float(df4['total_fuel_burn_kg'].median())
median_fuel_ac_1_5  = float(df5['total_fuel_burn_kg'].median())
median_fuel_ac_1_6  = float(df6['total_fuel_burn_kg'].median())
median_fuel_ac_1_7  = float(df7['total_fuel_burn_kg'].median())
median_fuel_ac_1_8  = float(df8['total_fuel_burn_kg'].median())
median_fuel_ac_1_9  = float(df9['total_fuel_burn_kg'].median())
median_fuel_ac_1_10 = float(df10['total_fuel_burn_kg'].median())
median_fuel_ac_1_11 = float(df11['total_fuel_burn_kg'].median())
median_fuel_ac_1_12 = float(df12['total_fuel_burn_kg'].median())
median_fuel_ac_1_13 = float(df13['total_fuel_burn_kg'].median())
median_fuel_ac_1_14 = float(df14['total_fuel_burn_kg'].median())
median_fuel_ac_1_15 = float(df15['total_fuel_burn_kg'].median())
median_fuel_ac_1_16 = float(df16['total_fuel_burn_kg'].median())
median_fuel_ac_1_17 = float(df17['total_fuel_burn_kg'].median())
median_fuel_ac_1_18 = float(df18['total_fuel_burn_kg'].median())
median_fuel_ac_1_19 = float(df19['total_fuel_burn_kg'].median())
median_fuel_ac_1_20 = float(df20['total_fuel_burn_kg'].median())
median_fuel_ac_1_21 = float(df21['total_fuel_burn_kg'].median())
median_fuel_ac_1_22 = float(df22['total_fuel_burn_kg'].median())
median_fuel_ac_1_23 = float(df23['total_fuel_burn_kg'].median())
median_fuel_ac_1_24 = float(df24['total_fuel_burn_kg'].median())
median_fuel_ac_1_25 = float(df25['total_fuel_burn_kg'].median())
median_fuel_ac_1_26 = float(df26['total_fuel_burn_kg'].median())
median_fuel_ac_1_27 = float(df27['total_fuel_burn_kg'].median())
median_fuel_ac_1_28 = float(df28['total_fuel_burn_kg'].median())
median_fuel_ac_1_29 = float(df29['total_fuel_burn_kg'].median())
median_fuel_ac_1_30 = float(df30['total_fuel_burn_kg'].median())
median_fuel_ac_1_31 = float(df31['total_fuel_burn_kg'].median())

#put it in a dictionary
medians_fuel_ac1 = {
    "t_start_0.0":  median_fuel_ac_1_1,
    "t_start_1.0":  median_fuel_ac_1_2,
    "t_start_2.0":  median_fuel_ac_1_3,
    "t_start_3.0":  median_fuel_ac_1_4,
    "t_start_4.0":  median_fuel_ac_1_5,
    "t_start_5.0":  median_fuel_ac_1_6,
    "t_start_6.0":  median_fuel_ac_1_7,
    "t_start_7.0":  median_fuel_ac_1_8,
    "t_start_8.0":  median_fuel_ac_1_9,
    "t_start_9.0":  median_fuel_ac_1_10,
    "t_start_10.0": median_fuel_ac_1_11,
    "t_start_11.0": median_fuel_ac_1_12,
    "t_start_12.0": median_fuel_ac_1_13,
    "t_start_13.0": median_fuel_ac_1_14,
    "t_start_14.0": median_fuel_ac_1_15,
    "t_start_15.0": median_fuel_ac_1_16,
    "t_start_16.0": median_fuel_ac_1_17,
    "t_start_17.0": median_fuel_ac_1_18,
    "t_start_18.0": median_fuel_ac_1_19,
    "t_start_19.0": median_fuel_ac_1_20,
    "t_start_20.0": median_fuel_ac_1_21,
    "t_start_21.0": median_fuel_ac_1_22,
    "t_start_22.0": median_fuel_ac_1_23,
    "t_start_23.0": median_fuel_ac_1_24,
    "t_start_24.0": median_fuel_ac_1_25,
    "t_start_25.0": median_fuel_ac_1_26,
    "t_start_26.0": median_fuel_ac_1_27,
    "t_start_27.0": median_fuel_ac_1_28,
    "t_start_28.0": median_fuel_ac_1_29,
    "t_start_29.0": median_fuel_ac_1_30,
    "t_start_30.0": median_fuel_ac_1_31,
}


sample_ac1 = pd.DataFrame({
    "median_cost_eur": medians_ac1,
    "mean_runtime_sec": avg_runtimes_ac1,
    "best_cost_eur": best_costs_ac1,
    "worst_cost_eur": worst_costs_ac1,
    "median_fuel_burn_kg": medians_fuel_ac1,
}) #put all the dictionaries in one dataframe
print(medians_fuel_ac1)
sample_ac1.to_csv("sample_ac1.csv", index=True, index_label="t_start") #without the last statement, the column t start was named 'anonymus'. export the sample

import pandas as pd

df = pd.read_csv(
    'Aircraft_1.txt',
    sep=r'\s+',       # één of meer spaties als scheiding
    engine='python',  # nodig voor regex-separator
)

"""
Ik ga nu filteren op FL 340. dit is de gemiddelde vlieghoogte van amsterdam naar new york toe
"""
df_340 = df[df["altitude"] == 34000]
#print(df_340.info())

h_ft = 34000 #dit is de hoogte waarop we vliegen. deze moeten we nog bepalen uit aircraft data. ik heb voor nu 34000 ft ingevuld
h_meter = h_ft * 0.3048
T_height = 288.15 - (0.0065*h_meter)


import math
grouped = df_340.groupby("Mach")

# Berekenen van gemiddelde fuel flow
avg_fuel_flow = grouped["fuel_flow"].mean()

def tas_kmh(M):
    return M * math.sqrt(T_height * 287 * 1.4) * 3.6

# Specific range berekenen
zuinigheid = avg_fuel_flow.copy()
for M in avg_fuel_flow.index:
    GS = tas_kmh(M)
    FF = avg_fuel_flow[M]
    zuinigheid[M] = GS / FF    # km per kg brandstof

#print(zuinigheid.sort_values(ascending=False))

"""
Nu weten we dat mach = 0.82 de zuinigste is, dus ik ga de dataframe aanpassen naar mach is 0.82 en altitude is FL340
"""
df_aircraft = df[(df["altitude"] == 34000) & (df["Mach"] == 0.82)]


print(df_aircraft.info())

df_aircraft.to_csv("Aircraft_1_filtered.csv", index=False)







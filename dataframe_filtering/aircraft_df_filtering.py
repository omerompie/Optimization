import pandas as pd

df = pd.read_csv( #make a dataframe from the aircraft PDB
    'Aircraft_1.txt',
    sep=r'\s+',       # the txt is formatted with spaces between the values, not commas. Pandas will not read it correctly without this line
    engine='python',  # this is needed to make a dataframe because there are no commas between the values
)

"""
An average flight level from AMS to NY is FL340. So the dataframe will be filtered on this below.
"""
df_340 = df[df["altitude"] == 34000]
#print(df_340.info()) #check if data is clean
#print(df_340.isnull().sum()) #check if data is clean

"""
We are going to keep speed constant. In the lines below, we calculated the Mach at which the aircraft flies most economical
"""

h_ft = 34000
h_meter = h_ft * 0.3048
T_height = 288.15 - (0.0065*h_meter) #calculate the temperature at height


import math
grouped = df_340.groupby("Mach") #group the dataframe by every Mach value


avg_fuel_flow = grouped["fuel_flow"].mean() #calculate the average fuel flow for every mach value

def tas_kmh(M):
    return M * math.sqrt(T_height * 287 * 1.4) * 3.6 #make a function which calculates Mach out of the speed of sound, derived from the temperature at height


economics = avg_fuel_flow.copy() #copy the average fuel flows to prevent overwriting the original values
for M in avg_fuel_flow.index: #for every average fuel flow value
    TAS = tas_kmh(M) #note the TAS
    FF = avg_fuel_flow[M] #note the fuel flow
    economics[M] = TAS / FF    # for every speed, calculate the amount of kilometers flown per kilogram burned fuel

#print(economics.sort_values(ascending=False)) #see what speed has the most amount of kilometers per kg burned fuel. this is the most economic speed

"""
Mach 0.82 turned out to be the most economic one. we now make a separate df for this speed and altitude. We then have our filtered aircraft PDB
"""
df_aircraft = df[(df["altitude"] == 34000) & (df["Mach"] == 0.82)]




df_aircraft.to_csv("Aircraft_1_filtered.csv", index=False) #export the dataframe to be used in other python files







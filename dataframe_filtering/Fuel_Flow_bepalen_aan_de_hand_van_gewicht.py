import pandas as pd


import pandas as pd
import os

# FIX: Get directory of THIS file (dataframe_filtering/)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Target CSV in 'Trajectory' (Up one level, then into Trajectory)
ac2_path = os.path.join(current_dir, '..', 'Trajectory', 'Aircraft_2_filtered.csv')

# If the code also reads Aircraft 1, fix that path too:
# ac1_path = os.path.join(current_dir, '..', 'Trajectory', 'Aircraft_1_filtered.csv')

df2 = pd.read_csv(ac2_path)

df = pd.read_csv('Aircraft_1_filtered.csv')
#df2 = pd.read_csv('Aircraft_2_filtered.csv')

weight_table = df["Gross_Weight"].tolist() #for interpolation and extrapolation
ff_table = df["fuel_flow"].tolist() #for interpolation and extrapolation

weight_table2 = df2['weight'].tolist()
ff_table2 = df2['FF'].tolist()

def get_fuel_flow(weight, weight_table, ff_table):

    pairs = sorted(zip(weight_table, ff_table))
    weight_table = [p[0] for p in pairs]
    ff_table = [p[1] for p in pairs]  #this code ensures that the values are sorted from low to high in the list

    if weight in weight_table:
        return ff_table[weight_table.index(weight)] #for the magic coincidence that the exact weight is listed in the data

    Wmin = weight_table[0]
    Wmax = weight_table[-1] #boundaries of the table

    if weight < Wmin:
        Wa, Wb = weight_table[0], weight_table[1]
        FFa, FFb = ff_table[0], ff_table[1] #this is for extrapolation

    elif weight > Wmax:
        Wa, Wb = weight_table[-2], weight_table[-1]
        FFa, FFb = ff_table[-2], ff_table[-1]

    else:
        for i in range(len(weight_table) - 1): #this is the interpolation
            Wa = weight_table[i]
            Wb = weight_table[i + 1]
            if Wa <= weight <= Wb:
                FFa = ff_table[i]
                FFb = ff_table[i + 1]
                break
    FF = ((weight - Wb) / (Wa - Wb)) * FFa + \
         ((weight - Wa) / (Wb - Wa)) * FFb

    return FF

current_weight = 260080 #dit moet dus een variabele worden voor elke edge, ik doe het nu voor W0




"""
De fuel flow voor Wo is 7898.40 kg / hour. dit komt overeen met mijn handmatige berekening. de functie is dus juist
"""


def get_fuel_flow_ac2(weight, weight_table2, ff_table2):

    pairs = sorted(zip(weight_table2, ff_table2))
    weight_table2 = [p[0] for p in pairs]
    ff_table2 = [p[1] for p in pairs]  #this code ensures that the values are sorted from low to high in the list

    if weight in weight_table2:
        return ff_table2[weight_table2.index(weight)] #for the magic coincidence that the exact weight is listed in the data

    Wmin = weight_table2[0]
    Wmax = weight_table2[-1] #boundaries of the table

    if weight < Wmin:
        Wa, Wb = weight_table2[0], weight_table2[1]
        FFa, FFb = ff_table2[0], ff_table2[1] #this is for extrapolation

    elif weight > Wmax:
        Wa, Wb = weight_table2[-2], weight_table2[-1]
        FFa, FFb = ff_table2[-2], ff_table2[-1]

    else:
        for i in range(len(weight_table2) - 1): #this is the interpolation
            Wa = weight_table2[i]
            Wb = weight_table2[i + 1]
            if Wa <= weight <= Wb:
                FFa = ff_table2[i]
                FFb = ff_table2[i + 1]
                break
    FF = ((weight - Wb) / (Wa - Wb)) * FFa + \
         ((weight - Wa) / (Wb - Wa)) * FFb

    return FF


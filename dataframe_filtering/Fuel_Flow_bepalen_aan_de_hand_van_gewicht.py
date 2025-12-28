import pandas as pd
import os

# --- PATH FIX: ALWAYS LOOK IN TRAJECTORY FOLDER ---
# 1. Get the folder where THIS python file lives
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Construct the path to the CSVs (Go up one level, then down into Trajectory)
path_ac1 = os.path.join(current_dir, '..', 'Trajectory', 'Aircraft_1_filtered.csv')
path_ac2 = os.path.join(current_dir, '..', 'Trajectory', 'Aircraft_2_filtered.csv')

# 3. Read using the absolute paths
df = pd.read_csv(path_ac1)
df2 = pd.read_csv(path_ac2)

weight_table = df["Gross_Weight"].tolist()
ff_table = df["fuel_flow"].tolist()

weight_table2 = df2['weight'].tolist()
ff_table2 = df2['FF'].tolist()

# ... (Keep the rest of the functions below as they are) ...

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


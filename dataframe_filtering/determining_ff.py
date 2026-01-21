import pandas as pd

df = pd.read_csv('Aircraft_1_filtered.csv')
df2 = pd.read_csv('Aircraft_2_filtered.csv') #read the filtered csv files produced

weight_table = df["Gross_Weight"].tolist() # make a table for interpolation and extrapolation
ff_table = df["fuel_flow"].tolist() #make a table for interpolation and extrapolation

weight_table2 = df2['weight'].tolist() #the same for ac 2
ff_table2 = df2['FF'].tolist()

def get_fuel_flow(weight, weight_table, ff_table): #make a function which calculates fuel flow by the interpolation by weights

    pairs = sorted(zip(weight_table, ff_table)) #make every index of weight and fuel flow table pairs (stores them in tuples). Then it sorts the values so that the weights are ascending
    weight_table = [p[0] for p in pairs] #now that it is ensured that the weights are ascending, we are going to reconstruct the weight table
    ff_table = [p[1] for p in pairs]  #now that it is ensured that the weights are ascending, we are going to reconstruct the FF table

    if weight in weight_table:
        return ff_table[weight_table.index(weight)] #for the magic coincidence that the exact weight is listed in the data
    """
    now the inter/extrapolation begins wth first defining the variables
    """

    Wmin = weight_table[0]
    Wmax = weight_table[-1] #boundaries of the table

    if weight < Wmin:
        Wa, Wb = weight_table[0], weight_table[1]
        FFa, FFb = ff_table[0], ff_table[1] #this is for extrapolation if the weight falls outside the datapoints

    elif weight > Wmax:
        Wa, Wb = weight_table[-2], weight_table[-1]
        FFa, FFb = ff_table[-2], ff_table[-1] #this is for extrapolation if the weight falls outside the datapoints

    else:
        for i in range(len(weight_table) - 1): #start of the loop to create weight intervals
            Wa = weight_table[i]
            Wb = weight_table[i + 1]
            if Wa <= weight <= Wb: #is the weight in interval i?
                FFa = ff_table[i] #if yes, give the FFa which corresponds to Wa
                FFb = ff_table[i + 1] #if yes, give the FFv which corresponds to Wb
                break #if yes, stop the loop. if weight is not in interval, go to the next index
    FF = ((weight - Wb) / (Wa - Wb)) * FFa + ((weight - Wa) / (Wb - Wa)) * FFb #this is the linear interpolation formula

    return FF






"""
The code below does exactly the same for aircraft 2 so i'm not going to comment that again
"""


def get_fuel_flow_ac2(weight, weight_table2, ff_table2):

    pairs = sorted(zip(weight_table2, ff_table2))
    weight_table2 = [p[0] for p in pairs]
    ff_table2 = [p[1] for p in pairs]

    if weight in weight_table2:
        return ff_table2[weight_table2.index(weight)]

    Wmin = weight_table2[0]
    Wmax = weight_table2[-1]

    if weight < Wmin:
        Wa, Wb = weight_table2[0], weight_table2[1]
        FFa, FFb = ff_table2[0], ff_table2[1]

    elif weight > Wmax:
        Wa, Wb = weight_table2[-2], weight_table2[-1]
        FFa, FFb = ff_table2[-2], ff_table2[-1]

    else:
        for i in range(len(weight_table2) - 1):
            Wa = weight_table2[i]
            Wb = weight_table2[i + 1]
            if Wa <= weight <= Wb:
                FFa = ff_table2[i]
                FFb = ff_table2[i + 1]
                break
    FF = ((weight - Wb) / (Wa - Wb)) * FFa + ((weight - Wa) / (Wb - Wa)) * FFb

    return FF


"""
Temperatuur op hoogte berekening. Dit is nog zonder dynamische temperatuur, gebaseerd op ISA conditions
"""


h_ft = 34000 #dit is de hoogte waarop we vliegen. deze moeten we nog bepalen uit aircraft data. ik heb voor nu 34000 ft ingevuld
h_meter = h_ft * 0.3048
T_height = 288.15 - (0.0065*h_meter)

"""
Berekening wind speed
Ik heb het zo neergezet dat headwind een negatief getal is en tailwind positief
"""
from vinc import v_direct
from vinc import v_inverse

n1 = (52.308056, 4.764167) #heb hiervoor even ams en jfk gepakt om te testen. in het algortime moeten de edges komen.
n2 = (40.641766, -73.780968)
def heading_calculation(n1, n2):

    _, heading = v_direct(n1, n2)   #geeft de heading
    return heading

heading = heading_calculation(n1, n2)

wind_heading = 90 #random wind heading. moet uit die dat komen en rishaad moet nog even kijken hoe we de waardes voor elke node moeten krijgen
wind_speed_kts = 55
import math

def head_tail_wind_calculation(heading, wind_heading, wind_speed_kts):
    # signed angle difference between heading and wind_FROM
    wind_to_deg = (wind_heading + 180) % 360
    diff = (wind_to_deg - heading + 180) % 360 - 180 #berekening wind angle
    return (wind_speed_kts*1.852) * math.cos(math.radians(diff)) #berekening wind speed met headwind als negatief component
head_tail_wind_kmh = head_tail_wind_calculation(heading, wind_heading, wind_speed_kts)


"""
Berekening ground speed
"""
TAS_M = 0.83 #moet uit aircraft data komen, heb nu even dit neergezet.

def ground_speed_calculation(TAS_M, T_height, head_tail_wind_kmh):
    TAS_kmh = TAS_M * math.sqrt(T_height*287*1.4) * 3.6 #berekening van mach naar km/h
    return (TAS_kmh + head_tail_wind_kmh) #berekening ground speed

GS_kmh = ground_speed_calculation(TAS_M, T_height, head_tail_wind_kmh)


#Step 4 Rishaad
# Calculation of time from node to node ; moet nog kijken met omer voor de juiste distances want die verschillen per node

Distance = 200 # voor nu even op 200 gezet maar we moeten kijken.

Time = Distance/GS_kmh
print("The time is",Time)

#Step 5 Rishaad fuel calculation
#Fuel flow moeten we kijken of we dat constant willen houden of juist niet, dit moet nog besproken worden.

Fuel_flow = 0.025 # voor nu een random getal ingevuld als test

Fuel_burned = Fuel_flow * Time
print("The burned fuel is",Fuel_burned)

#Step 6 calculate fuel cost Rishaad fuel cost

Fuel_costs = Fuel_burned * 0.683125 # kosten van fuel per kg
print("The cost of the fuel is",Fuel_costs)

#Calculation of cost of time

Cost_Of_Time = Time * 35 * 0.683125
print("the cost of time is", Cost_Of_Time)

#Code werkt

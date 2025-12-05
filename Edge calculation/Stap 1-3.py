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
print(heading)

wind_heading = 90 #random wind heading. moet uit die dat komen en rishaad moet nog even kijken hoe we de waardes voor elke node moeten krijgen
wind_speed_kts = 55
import math

def head_tail_wind_calculation(heading, wind_heading, wind_speed_kts):
    # signed angle difference between heading and wind_FROM
    wind_to_deg = (wind_heading + 180) % 360
    diff = (wind_to_deg - heading + 180) % 360 - 180
    return (wind_speed_kts*1.852) * math.cos(math.radians(diff))
head_tail_wind_kmh = head_tail_wind_calculation(heading, wind_heading, wind_speed_kts)
print(head_tail_wind_kmh)

"""
Berekening ground speed
"""
TAS_M = 0.83 #moet uit aircraft data komen, heb nu even dit neergezet.

def ground_speed_calculation(TAS_M, T_height, head_tail_wind_kmh):
    TAS_kmh = TAS_M * math.sqrt(T_height*287*1.4) * 3.6
    return (TAS_kmh + head_tail_wind_kmh)

GS_kmh = ground_speed_calculation(TAS_M, T_height, head_tail_wind_kmh)
print(GS_kmh)










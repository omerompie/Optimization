"""
Indeling document:
Eerst worden alle individuele stappen berekend en defined in een functie
Dan wordt de kost of time berekend
Als laatste is er de functie get_edge_costs. Dit is 1 functie waarbij alle vorige functies verwerkt zitten om
de kosten van 1 edge te berekenen. Dit is handiger want zo hoef je maar in de trajectory costs berekening
naar 1 functie uit dit bestand te callen.
"""

from Edge_calculation.vinc import v_direct
import math
from dataframe_filtering.Fuel_Flow_bepalen_aan_de_hand_van_gewicht import get_fuel_flow
import pandas as pd
from src.ansp import get_ansp_cost_for_edge
from weather.weather_model import get_wind_kmh

df = pd.read_csv('wind_for_coordinates.csv')


u_table = df.pivot(index='time_hours', columns='waypoint_id', values='u_speed_ms').sort_index() #make a table for the x wind on every hour
v_table = df.pivot(index='time_hours', columns='waypoint_id', values='v_speed_ms').sort_index() #make a table for the y wind on every hour




"""
Our fixed variables are listed below
"""

TEMPERATURE_HEIGHT = 288.15 - ((34000 * 0.3048) * 0.0065) #temperature at our fixed flight altitude of 34,0000 feet
COST_OF_TIME_INDEX = 35 #associated operating costs, expressed in kg fuel burn per hour
MACH_AIRCRAFT_1 = 0.82 #the speed at which aircraft 1 flies with maximum efficiency
MACH_AIRCRAFT_2 = 0.81 #the speed at which aircraft 2 flies with maximum efficiency
FUEL_COSTS_PER_KG = 0.683125 #fuel kosts for 1 kg fuel burn
WEIGHT_START_CRUISE = 257743 #weight in kilos at the start of the cruise
T_MAX = 39.0
t_max = T_MAX
"""
Our aircraft Performance database with weight and fuel flow converted into a list
"""
df = pd.read_csv('Aircraft_1_filtered.csv')
weight_table = df["Gross_Weight"].tolist()
ff_table = df["fuel_flow"].tolist()



"""
Berekening headind en wind speed
Ik heb het zo neergezet dat headwind een negatief getal is en tailwind positief
"""



def get_heading(waypoint_i, waypoint_j):

    _, heading = v_direct(waypoint_i, waypoint_j)   #geeft de heading
    return heading



"""
Berekening ground speed
"""

def get_ground_speed(TAS_MACH, Temperature_height, head_tail_wind_kmh):
    TAS_kmh = TAS_MACH * math.sqrt(Temperature_height*287*1.4) * 3.6 #berekening van mach naar km/h
    return (TAS_kmh + head_tail_wind_kmh) #berekening ground speed

"""
Step 4 Rishaad
Calculation of distance and time from node to node 
"""
def get_distance(waypoint_i, waypoint_j):
    distance_meter, _ = v_direct(waypoint_i, waypoint_j)
    distance_km = distance_meter/1000
    return (distance_km)


def get_time(distance_nodes,GS_kmh): # We moeten de afstanden ook in uren krijgen
    time_nodes = distance_nodes/GS_kmh #berekening van de tijd in uren van node to node
    return time_nodes #Tijd in uren

"""
Step 5 Rishaad fuel calculation
"""

def get_fuel_burn(fuel_flow,time_nodes):
    fuel_burn = fuel_flow * time_nodes
    return fuel_burn

"""
Step 6 calculate fuel cost Rishaad fuel cost
"""

def get_fuel_costs(fuel_burned, fuel_costs_kg):
    fuel_cost = fuel_burned * fuel_costs_kg # kosten van fuel per kg
    return fuel_cost

"""
Calculation of cost of time
"""

def get_cost_of_time(time_nodes, CI, fuel_costs_kg):
    cost_of_time = time_nodes * CI * fuel_costs_kg
    return cost_of_time

"""
Now we combine the previous functions
"""

def get_edge_cost(
    waypoint_i, #the first waypoint
    waypoint_j, #the second waypoint
    waypoint_i_id,
    current_weight_kg, #the current weight. Later used in trajectory costs. at the start of the cruise this is 257743
    current_time=None, #set a default for calculating examples of random edges where there is no current time. in the trajectory costs there is a variable current time and then this statement expires

#Rishaad has to create the wind model. we have to make a function which gives the speed and direction of
#the wind for node i. Now I made a code that states if wind_model=none that there is no wind speed.
#So the code works, but we have to create a wind model function


):
    distance_km = get_distance(waypoint_i, waypoint_j) #calculate the distance with the function

    heading_deg = get_heading(waypoint_i, waypoint_j) #calculate the heading with the function

    head_tail_kmh = get_wind_kmh(waypoint_i_id, current_time, heading_deg) #calculate the head or tail wind with the function

    ground_speed_kmh = get_ground_speed(MACH_AIRCRAFT_1, TEMPERATURE_HEIGHT, head_tail_kmh)
    #calculate the ground speed with the function
    time_h = get_time(distance_km, ground_speed_kmh) #calculate the time with the function

    fuel_flow_kg_per_h = get_fuel_flow(current_weight_kg, weight_table, ff_table)
    #calculate the fuel flow by the interpolation function
    fuel_burn_kg = get_fuel_burn(fuel_flow_kg_per_h, time_h)
    #calculate the fuel burn with the function

    fuel_cost = get_fuel_costs(fuel_burn_kg, FUEL_COSTS_PER_KG) #calculate the fuel costs of the edge with the function
    time_cost = get_cost_of_time(time_h, COST_OF_TIME_INDEX, FUEL_COSTS_PER_KG) #calculate the cost of time with the function

    ansp_cost = get_ansp_cost_for_edge(waypoint_i, waypoint_j)

    total_cost_edge = fuel_cost + time_cost + ansp_cost
    #Total cost of the edge. Here, the ANSP costs is missing. omer is still performing research on the topic.
    return fuel_burn_kg, time_h, total_cost_edge

"""
als jullie willen testen boys heb ik hier random variabelen opgeschreven. heb zelf al getest en hij werkt


waypoint_i = (52.308056, 4.764167)
waypoint_j = (52.57845370868331, 1.856151430826293)
waypoint_i_id = 0
current_weight_kg = WEIGHT_START_CRUISE

fuel_burn_kg, time_h, cost_eur, headwind = get_edge_cost(waypoint_i, waypoint_j, waypoint_i_id, current_weight_kg)

print(f'The total fuel burn on this edge is {fuel_burn_kg:.0f} kg')
print(f'The total time for this edge is {time_h:.2f} hours')
print(f'The total costs for this is edge are {cost_eur:.0f} euros')
print(f'The headwind is {headwind} kmh')
"""

"""
Literally everything is the same as for aircraft 1, only a different PDB and Mach is used.
So im not commenting this code.
"""

from vinc.vinc import v_direct
import math
from dataframe_filtering.determining_ff import get_fuel_flow_ac2
import pandas as pd
from src.ansp import get_ansp_cost_for_edge
from weather.weather_model import get_wind_kmh




TEMPERATURE_HEIGHT = 288.15 - ((34000 * 0.3048) * 0.0065) #temperature at our fixed flight altitude of 34,0000 feet
COST_OF_TIME_INDEX = 35 #associated operating costs, expressed in kg fuel burn per hour
MACH_AIRCRAFT_1 = 0.82 #the speed at which aircraft 1 flies with maximum efficiency
MACH_AIRCRAFT_2 = 0.81 #the speed at which aircraft 2 flies with maximum efficiency
FUEL_COSTS_PER_KG = 0.683125 #fuel kosts for 1 kg fuel burn (€). adapted from jet-a1-fuel.com. to convert the price of liters into price per kilogram, we used 0.804 kg/L adated from Air BP
WEIGHT_START_CRUISE = 257743 #weight in kilos at the start of the cruise, retrieved from simbrief
FUEL_BURN_MAX = 62600 #maximum amount of fuel burn for the cruise based on aircraft data from simbrief
T_MAX = 39.0 #this is as far as the weather data goes. if T_MAX is reached, the weather model uses the weather at T_MAX
t_max = T_MAX
TIME_MAX = 7.5 #this is the time window for the aircraft. this is the maximum flight time
TIME_MIN = 7.0 #this is the time window for the aircraft. this is the minimum flight time
TIME_MAX_AC2 = 7.85 #this is the time window for the aircraft 2. this is the maximum flight time. it is later than for ac1 because ac 2 has a lower TAS
TIME_MIN_AC2 = 7.35 #this is the time window for the aircraft 2. this is the minimum flight time


df = pd.read_csv('Aircraft_1_filtered.csv')
weight_table = df["Gross_Weight"].tolist()
ff_table = df["fuel_flow"].tolist()





def get_heading(waypoint_i, waypoint_j):

    _, heading = v_direct(waypoint_i, waypoint_j)
    return heading

wind_heading = 90
wind_speed_kts = 55


def get_wind(heading, wind_heading, wind_speed_kts):
    wind_to_deg = (wind_heading + 180) % 360
    diff = (wind_to_deg - heading + 180) % 360 - 180
    return (wind_speed_kts*1.852) * math.cos(math.radians(diff))



def get_ground_speed(TAS_MACH, Temperature_height, head_tail_wind_kmh):
    TAS_kmh = TAS_MACH * math.sqrt(Temperature_height*287*1.4) * 3.6
    return (TAS_kmh + head_tail_wind_kmh)


def get_distance(waypoint_i, waypoint_j):
    distance_meter, _ = v_direct(waypoint_i, waypoint_j)
    distance_km = distance_meter/1000
    return (distance_km)


def get_time(distance_nodes,GS_kmh):
    time_nodes = distance_nodes/GS_kmh
    return time_nodes


def get_fuel_burn(fuel_flow,time_nodes):
    fuel_burn = fuel_flow * time_nodes
    return fuel_burn


def get_fuel_costs(fuel_burned, fuel_costs_kg):
    fuel_cost = fuel_burned * fuel_costs_kg
    return fuel_cost



def get_cost_of_time(time_nodes, CI, fuel_costs_kg):
    cost_of_time = time_nodes * CI * fuel_costs_kg
    return cost_of_time



def get_edge_cost_ac2(
    waypoint_i,
    waypoint_j,
    waypoint_i_id,
    current_weight_kg,
    current_time,

):
    distance_km = get_distance(waypoint_i, waypoint_j)

    heading_deg = get_heading(waypoint_i, waypoint_j)

    head_tail_kmh = get_wind_kmh(waypoint_i_id, current_time, heading_deg)

    ground_speed_kmh = get_ground_speed(MACH_AIRCRAFT_2, TEMPERATURE_HEIGHT, head_tail_kmh)

    time_h = get_time(distance_km, ground_speed_kmh)

    fuel_flow_kg_per_h = get_fuel_flow_ac2(current_weight_kg, weight_table, ff_table)

    fuel_burn_kg = get_fuel_burn(fuel_flow_kg_per_h, time_h)


    fuel_cost = get_fuel_costs(fuel_burn_kg, FUEL_COSTS_PER_KG)
    time_cost = get_cost_of_time(time_h, COST_OF_TIME_INDEX, FUEL_COSTS_PER_KG)

    ansp_cost = get_ansp_cost_for_edge(waypoint_i, waypoint_j)

    total_cost_edge = fuel_cost + time_cost + ansp_cost

    return fuel_burn_kg, time_h, total_cost_edge

"""
To see if it works, here is a sample


waypoint_i = (52.308056, 4.764167)
waypoint_j = (52.57845370868331, 1.856151430826293)
waypoint_i_id = 0
current_weight_kg = WEIGHT_START_CRUISE
current_time = 0.0

fuel_burn_kg, time_h, cost_eur = get_edge_cost_ac2(waypoint_i, waypoint_j, waypoint_i_id, current_weight_kg, current_time)

print(f'The total fuel burn on this edge is {fuel_burn_kg:.0f} kg')
print(f'The total time for this edge is {time_h:.2f} hours')
print(f'The total costs for this edge are {cost_eur:.0f} euros')
"""
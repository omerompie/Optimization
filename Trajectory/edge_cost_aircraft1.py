"""
Indeling document:
First all the individual steps will be computed into a function.
Then, the function get edge costs combines all this to determine the cost of an edge
"""

from vinc.vinc import v_direct
import math
from dataframe_filtering.determining_ff import get_fuel_flow
import pandas as pd
from src.ansp import get_ansp_cost_for_edge
from weather.weather_model import get_wind_kmh

"""
Our fixed variables are listed below
"""

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

df = pd.read_csv('wind_for_coordinates.csv') #read the dataframe of the wind. later used by the weather model


u_table = df.pivot(index='time_hours', columns='waypoint_id', values='u_speed_ms').sort_index() #make a table for the u wind on every hour. now, the time are the rows and the waypoint IDs are the columns
v_table = df.pivot(index='time_hours', columns='waypoint_id', values='v_speed_ms').sort_index() #make a table for the v wind on every hour. now, the time are the rows and the waypoint IDs are the columns






"""
Below is uur aircraft Performance database with weight and fuel flow converted into a list
"""

df = pd.read_csv('Aircraft_1_filtered.csv')
weight_table = df["Gross_Weight"].tolist()
ff_table = df["fuel_flow"].tolist() #create the tables again because the fuel flow function uses weight and fuel flow tables.



"""
Calculation of the heading of the aircraft is listed below
"""

def get_heading(waypoint_i, waypoint_j): #make the function with the two waypoints as variables

    _, heading = v_direct(waypoint_i, waypoint_j)   #v_direct gives the distance and azimuth (initial heading). we only want the azimuth, so that's why the _ is there
    return heading

"""
calculation ground speed
"""

def get_ground_speed(TAS_MACH, Temperature_height, head_tail_wind_kmh): #make a function
    TAS_kmh = TAS_MACH * math.sqrt(Temperature_height*287*1.4) * 3.6 #calculation of  mach to km/h
    return (TAS_kmh + head_tail_wind_kmh) #calculation of ground speed. head_tail_wind_kmh is calculated in the weather model in the directory weather.

"""
Calculation of distance and time from node to node 
"""

def get_distance(waypoint_i, waypoint_j): #make the function
    distance_meter, _ = v_direct(waypoint_i, waypoint_j) #we only want the distance between two waypoints, so _ for azimuth
    distance_km = distance_meter/1000 #convert into km
    return (distance_km)


def get_time(distance_nodes,GS_kmh): #make a function
    time_nodes = distance_nodes/GS_kmh #calculate the time by dividing the distance between the nodes by the groundspeed
    return time_nodes #return the time in hours

"""
Calculation of fuel flow
"""

def get_fuel_burn(fuel_flow,time_nodes): #make the function
    fuel_burn = fuel_flow * time_nodes #calculate fuel burn by multiplying fuel flow with the time.
    return fuel_burn

"""
Calculate fuel cost
"""

def get_fuel_costs(fuel_burned, fuel_costs_kg): #make the function
    fuel_cost = fuel_burned * fuel_costs_kg #calculate the costs of burning x kilograms of fuel
    return fuel_cost

"""
Calculation of cost of time
"""

def get_cost_of_time(time_nodes, CI, fuel_costs_kg): #make the function
    cost_of_time = time_nodes * CI * fuel_costs_kg #cost of time is expressed in fuel burn. So the cost in euros is calculated by mulitplying the cost index with the time and fuel price
    return cost_of_time

"""
Now we combine the previous functions
"""

def get_edge_cost(
    waypoint_i, #the first waypoint
    waypoint_j, #the second waypoint
    waypoint_i_id, #the id of the waypoint
    current_weight_kg, #current weight of the aircraft somewhere in the graph
    current_time, #the time. expressed in hours from 1-13-2026 18.00 UTC. used by the weather model
): #create the function

    distance_km = get_distance(waypoint_i, waypoint_j) #calculate the distance with the function

    heading_deg = get_heading(waypoint_i, waypoint_j) #calculate the heading with the function

    head_tail_kmh = get_wind_kmh(waypoint_i_id, current_time, heading_deg) #calculate the head or tail wind with the weather model in the weather directory

    ground_speed_kmh = get_ground_speed(MACH_AIRCRAFT_1, TEMPERATURE_HEIGHT, head_tail_kmh)
    #calculate the ground speed with the function
    time_h = get_time(distance_km, ground_speed_kmh) #calculate the time with the function

    fuel_flow_kg_per_h = get_fuel_flow(current_weight_kg, weight_table, ff_table)
    #calculate the fuel flow by the interpolation function in te dataframe_filtering directory
    fuel_burn_kg = get_fuel_burn(fuel_flow_kg_per_h, time_h)
    #calculate the fuel burn with the function

    fuel_cost = get_fuel_costs(fuel_burn_kg, FUEL_COSTS_PER_KG) #calculate the fuel costs of the edge with the function
    time_cost = get_cost_of_time(time_h, COST_OF_TIME_INDEX, FUEL_COSTS_PER_KG) #calculate the cost of time with the function

    ansp_cost = get_ansp_cost_for_edge(waypoint_i, waypoint_j) #calcultate the ansp costs with the function defined in the src directory

    total_cost_edge = fuel_cost + time_cost + ansp_cost
    #Total cost of the edge. Here, the ANSP costs is missing. omer is still performing research on the topic.
    return fuel_burn_kg, time_h, total_cost_edge

"""
To see if it works, here is a sample, remove the quotes at the end


waypoint_i = (52.308056, 4.764167)
waypoint_j = (52.57845370868331, 1.856151430826293)
waypoint_i_id = 0
current_weight_kg = WEIGHT_START_CRUISE
current_time = 0.0

fuel_burn_kg, time_h, cost_eur = get_edge_cost(waypoint_i, waypoint_j, waypoint_i_id, current_weight_kg, current_time)

print(f'The total fuel burn on this edge is {fuel_burn_kg:.0f} kg')
print(f'The total time for this edge is {time_h:.2f} hours')
print(f'The total costs for this edge are {cost_eur:.0f} euros')
"""


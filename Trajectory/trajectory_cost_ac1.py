from Trajectory.edge_cost_aircraft1 import get_edge_cost

"""
Our fixed variables are listed below again
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

"""
Now it's time to calculate the cost of a whole trajectory 
"""

def get_trajectory_cost(
    trajectory, #this is a list of all the node (waypoint) IDs
    node_coordinates, #this is a dictionary with all the node IDs as keys and coordinates (in a tuple) as value
    t_start = 0.0, #the starting time in hours from 1-13-2026 18.00 UTC. this is used for different starting times in different scenarios for the algorithm. if no t_start is given, 0.0 is used
): #define the function

    weight = WEIGHT_START_CRUISE #The beginning weight
    total_cost = 0.0
    total_fuel = 0.0
    total_time = 0.0 #set all the end variables we want to know at zero.
    current_time = t_start #the current time at the start is the same as t_start

    for i in range(len(trajectory) - 1): #the loop is created to calculate the costs for all edges in the trajectory
        node_i = trajectory[i] #define node_i by node identification out of the trajectory list
        node_j = trajectory[i + 1] #define node_j by node identification out of the trajectory list

        wp_i = node_coordinates[node_i]  #get the coordinates of i out of the dictionary based on the ID
        wp_j = node_coordinates[node_j]  #get the coordinates of j out of the dictionary based on the ID

        fuel_ij, time_ij, cost_ij = get_edge_cost( #store the return of the function in fuel_ij, time_ij and cost_ij
            waypoint_i=wp_i,
            waypoint_j=wp_j,
            waypoint_i_id=node_i,
            current_weight_kg=weight,
            current_time=current_time, #link the variables needed for get_edge_cost to the right variables in this function
        ) #This is the edge calculation with the get_edge_cost. It does this for every edge by using the for loop


        total_fuel += fuel_ij #for every iteration, add the fuel burn to the previous value
        total_time += time_ij #for every iteration, add the time to the previous value
        total_cost += cost_ij #for every iteration, add the total costs to the previous value

        weight -= fuel_ij #for every iteration, substract the fuel burn from the weight so that the next iteration uses an updated weight
        current_time += time_ij #update the local time. The difference with total time is that total time is the duration of the flight and current time is the local time in hours from 1-13-2026 18.00 UTC. this is for the weather model.
    if total_fuel > FUEL_BURN_MAX:
        total_cost += 1e12 #penalty for burning too much fuel.

    if total_time < TIME_MIN:
        total_cost += 1e12  #penalty for arriving too soon
    if total_time > TIME_MAX:
        total_cost += 1e12 #penalty for arriving too late

    return (total_cost, total_fuel, total_time, weight) #return the total costs, total fuel, total flight time and the weight at the end of the cruise

"""
If you want to run this, I put a sample below. it is the great circle trajectory of AMS-NY. Just remove the quotes. 

from graph_build_for_bee.build_graph_function import build_graph

nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()

great_circle_trajectory = [0, 11, 32, 53, 74, 95, 116, 137, 158, 179, 200, 221, 242, 263, 284, 305, 326, 347, 368, 389, 410, 431, 452, 473, 494, 515, 536, 557, 578, 610]

cost_gc, fuel_gc, time_gc, _ = get_trajectory_cost(great_circle_trajectory, node_coords)

print(f'The total costs of the great circle trajectory are: {cost_gc:.0f} euros')
print(f'the total fuel burn on this route is equal to {fuel_gc:.0f} kg')
print(f'the total time for this route is equal to {time_gc:.2f} hours')
"""
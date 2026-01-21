from Trajectory.edge_cost_aircraft2 import get_edge_cost_ac2

"""
The code is again exactly the same as for the trajectory costs of aircraft 1, except from the used function. 
So, I'm not commenting this again.
"""

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


"""
Now it's time to calculate the cost of a whole trajectory 
"""

def get_trajectory_cost_ac2(
    trajectory,
    node_coordinates,
    t_start = 0.0,
):

    weight = WEIGHT_START_CRUISE
    total_cost = 0.0
    total_fuel = 0.0
    total_time = 0.0
    current_time = t_start

    for i in range(len(trajectory) - 1):
        node_i = trajectory[i]
        node_j = trajectory[i + 1]

        wp_i = node_coordinates[node_i]
        wp_j = node_coordinates[node_j]

        fuel_ij, time_ij, cost_ij = get_edge_cost_ac2(
            waypoint_i=wp_i,
            waypoint_j=wp_j,
            waypoint_i_id=node_i,
            current_weight_kg=weight,
            current_time=current_time,
        )


        total_fuel += fuel_ij
        total_time += time_ij
        total_cost += cost_ij

        weight -= fuel_ij
        current_time += time_ij
    if total_fuel > FUEL_BURN_MAX:
        total_cost += 1e12 * (total_fuel - FUEL_BURN_MAX)

    if total_time < TIME_MIN_AC2:
        total_cost += 1e12 * (TIME_MIN - total_time)
    if total_time > TIME_MAX_AC2:
        total_cost += 1e12 * (total_time - TIME_MAX)

    return (total_cost, total_fuel, total_time, weight)

"""
If you want to run this, I put a sample below. it is the great circle trajectory of AMS-NY. Just remove the quotes. 


from graph_build_for_bee.build_graph_function import build_graph

nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()

great_circle_trajectory = [0, 11, 32, 53, 74, 95, 116, 137, 158, 179, 200, 221, 242, 263, 284, 305, 326, 347, 368, 389, 410, 431, 452, 473, 494, 515, 536, 557, 578, 610]

cost_gc, fuel_gc, time_gc, _ = get_trajectory_cost_ac2(great_circle_trajectory, node_coords)

print(f'The total costs of the great circle trajectory are: {cost_gc:.0f} euros')
print(f'the total fuel burn on this route is equal to {fuel_gc:.0f} kg')
print(f'the total time for this route is equal to {time_gc:.2f} hours')
"""

from Trajectory.edge_cost_aircraft2 import get_edge_cost_ac2


"""
Our fixed variables are listed below
"""

TEMPERATURE_HEIGHT = 288.15 - ((34000 * 0.3048) * 0.0065) #temperature at our fixed flight altitude of 34,0000 feet
COST_OF_TIME_INDEX = 35 #associated operating costs, expressed in kg fuel burn per hour
MACH_AIRCRAFT_1 = 0.82 #the speed at which aircraft 1 flies with maximum efficiency
MACH_AIRCRAFT_2 = 0.81 #the speed at which aircraft 2 flies with maximum efficiency
FUEL_COSTS_PER_KG = 0.683125 #fuel kosts for 1 kg fuel burn
WEIGHT_START_CRUISE = 257743 #weight in kilos at the start of the cruise
FUEL_BURN_MAX = 62600 #maximum amount of fuel burn for the cruise based on aircraft data
TIME_MAX = 8.0
TIME_MIN = 7.0

"""
Now it's time to calculate the cost of a whole trajectory 
"""

def get_trajectory_cost_ac2(
    trajectory, #dit moet een lijst zijn van alle nodes. elke node moet een 'identificatie' hebben
    node_coordinates, #dit moet een dictionary zijn met alle node identificaties met hun bijbehorende coordinaten
    wind_model=None, #omdat we nu nog geen wind model hebben zet ik hem op none
    t_start = 0.0, #we start the cruise at t = 0 hours of course
):

    weight = WEIGHT_START_CRUISE #The beginning weight is predefined
    total_cost = 0.0
    total_fuel = 0.0
    total_time = 0.0 #set all the end variables we want to know at zero. ANSP costs should be included here as well but Omer is still investigating it
    current_time = t_start #we start from 0

    for i in range(len(trajectory) - 1): #the loop is created to calculate the costs for all edges in the trajectory
        node_i = trajectory[i] #define node_i by node identification out of the trajectory list
        node_j = trajectory[i + 1] #define node_j by node identification out of the trajectory list

        wp_i = node_coordinates[node_i]  #get the coordinates of i out of the dictionary based on the ID
        wp_j = node_coordinates[node_j]  #get the coordinates of i out of the dictionary based on the ID

        fuel_ij, time_ij, cost_ij = get_edge_cost_ac2( #store the return of the function in fuel_ij, time_ij and cost_ij
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
        current_time += time_ij #actually the same as th total time, but this variable will be used for the weather model to define the weather at that exact timestamp
    if total_fuel > FUEL_BURN_MAX:
        total_cost += 1e12 * (total_fuel - FUEL_BURN_MAX) #penaly relative to how much you are above your maximum fuel burn

    if total_time < TIME_MIN:
        total_cost += 1e12 * (TIME_MIN - total_time) #penaly relative to how much you are under your minimum time
    if total_time > TIME_MAX:
        total_cost += 1e12 * (total_time - TIME_MAX) #penaly relative to how much you are above your maximum time

    return (total_cost, total_fuel, total_time, weight)





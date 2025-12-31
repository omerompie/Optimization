
TEMPERATURE_HEIGHT = 288.15 - ((34000 * 0.3048) * 0.0065) #temperature at our fixed flight altitude of 34,0000 feet
COST_OF_TIME_INDEX = 35 #associated operating costs, expressed in kg fuel burn per hour
MACH_AIRCRAFT_1 = 0.82 #the speed at which aircraft 1 flies with maximum efficiency
MACH_AIRCRAFT_2 = 0.81 #the speed at which aircraft 2 flies with maximum efficiency
FUEL_COSTS_PER_KG = 0.683125 #fuel kosts for 1 kg fuel burn
WEIGHT_START_CRUISE = 257743 #weight in kilos at the start of the cruise
FUEL_BURN_MAX = 62600 #maximum amount of fuel burn for the cruise based on aircraft data
MIN_WEIGHT = 195143
T_MAX = 7.5
T_MIN = 7.0
t_max = 9.0 #this is for interpolation of weather


from Bee_Colony.random_or_mutate_trajectory import RandomTrajectory
from Bee_Colony.random_or_mutate_trajectory import MutateSolution
from main_tryout import build_graph
from Trajectory.Total_costs_trajectory import get_trajectory_cost
from Bee_Colony.random_or_mutate_trajectory import select_index_by_probability

nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()
Node_coordinates = node_coords

trajectory = [0, 11, 32, 53, 74, 95, 116, 137, 158, 179, 200, 221, 242, 263, 284, 305, 326, 347, 368, 389, 410, 431, 452, 473, 494, 515, 536, 557, 578, 610]

cost_great_circle, total_fuel, total_time, _ = get_trajectory_cost(trajectory, Node_coordinates)

print(f'The total costs of the great circle route are ${cost_great_circle:.0f}.')
print(f'The total fuel consumption for the great circle route is {total_fuel:.0f} kg.')
print(f'The great circle route takes {total_time:.1f} hours')




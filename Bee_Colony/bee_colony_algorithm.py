POPULATION_SIZE = 20 #voor nu klein zodat we snel antwoord krijgen, kan opgeschaald worden
MAX_ITERATIONS = 100 #zelfde als voor pupulation: klein voor nu
LIMIT = 15 #zelfde als voor population: klein voor nu
TEMPERATURE_HEIGHT = 288.15 - ((34000 * 0.3048) * 0.0065) #temperature at our fixed flight altitude of 34,0000 feet
COST_OF_TIME_INDEX = 35 #associated operating costs, expressed in kg fuel burn per hour
MACH_AIRCRAFT_1 = 0.82 #the speed at which aircraft 1 flies with maximum efficiency
MACH_AIRCRAFT_2 = 0.81 #the speed at which aircraft 2 flies with maximum efficiency
FUEL_COSTS_PER_KG = 0.683125 #fuel kosts for 1 kg fuel burn
WEIGHT_START_CRUISE = 257743 #weight in kilos at the start of the cruise
FUEL_BURN_MAX = 62600 #maximum amount of fuel burn for the cruise based on aircraft data
#TIME_MAX = TO BE DETERMINED

from Bee_Colony.random_or_mutate_trajectory import RandomTrajectory
from Bee_Colony.random_or_mutate_trajectory import MutateSolution
from main_tryout import build_graph
from Trajectory.Total_costs_trajectory import get_trajectory_cost


nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()
Node_coordinates = node_coords

"""
Input variables
"""

NP = POPULATION_SIZE
NumIter = MAX_ITERATIONS
Limit = LIMIT
start_node = 0
goal_node = 610

"""
Initialization
"""

Solutions = [None] * NP #make a list with the length of NP. All the values of solutions will come into this list
Costs = [None] * NP #make a list with the length of NP. All the values of Costs will come into this list
Trials = [0] * NP #make a list with the length of NP. All the values of Trials will come into this list
Prob = [0.0] * NP #make a list with the length of NP. All the Prob of solutions will come into this list

for i in range(NP):
    Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS)
    cost_euro, fuel_burn, time_s, weight = get_trajectory_cost(Solutions[i], Node_coordinates) #when we have the wind model, insert it between the brackets)
    Costs[i] = cost_euro
    Trials[i] = 0

min_cost = min(Costs) #finds the minimum value of all costs
b = Costs.index(min_cost) #Gives the index of the best solution and name it b
BestSolution = Solutions[b].copy() #to avoid accidentally overwriting it later
BestCost = Costs[b]

iteration = 0

while iteration < NumIter: #start of the headloop
    """
    Employed bee phase
    """


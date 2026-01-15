POPULATION_SIZE = 20 #voor nu klein zodat we snel antwoord krijgen, kan opgeschaald worden
MAX_ITERATIONS = 100 #zelfde als voor pupulation: klein voor nu
LIMIT = 20 #zelfde als voor population: klein voor nu
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
t_max = 39.0 #this is for interpolation of weather
T_START = 30.0


from Bee_Colony.random_or_mutate_trajectory import RandomTrajectory
from Bee_Colony.random_or_mutate_trajectory import MutateSolution
from main_tryout import build_graph
from Trajectory.Total_costs_trajectory import get_trajectory_cost
from Bee_Colony.random_or_mutate_trajectory import select_index_by_probability
import numpy as np






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
rng = np.random.default_rng(123) #this is a seed
"""
Initialization
"""

Solutions = [None] * NP #make a list with the length of NP. All the values of solutions will come into this list
Costs = [None] * NP #make a list with the length of NP. All the values of Costs will come into this list
Trials = [0] * NP #make a list with the length of NP. All the values of Trials will come into this list
Prob = [0.0] * NP #make a list with the length of NP. All the Prob of solutions will come into this list

for i in range(NP):
    Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS, rng=rng)
    cost_euro, fuel_burn, time_s, weight = get_trajectory_cost(Solutions[i], Node_coordinates) #when we have the wind model, insert it between the brackets)
    Costs[i] = cost_euro
    Trials[i] = 0

min_cost = min(Costs) #finds the minimum value of all costs
b = Costs.index(min_cost) #Gives the index of the best solution and name it b
BestSolution = Solutions[b].copy() #to avoid accidentally overwriting it later
BestCost = Costs[b]

iteration = 0



best_history = []   #for the animation
cost_history = []

while iteration < NumIter: #start of the headloop

    """
    Employed bee phase
    """

    for i in range(NP):
        current_solution = Solutions[i]
        current_costs = Costs[i]

        candidate_solution = MutateSolution(current_solution, graph, n_rings=N_RINGS, rng=rng)
        candidate_costs, _, _, _ = get_trajectory_cost(candidate_solution, Node_coordinates)

        if candidate_costs < current_costs:
            Solutions[i] = candidate_solution
            Costs[i] = candidate_costs
            Trials[i] = 0

        else:
            Trials[i] += 1

    min_cost = min(Costs)
    b = Costs.index(min_cost)

    if min_cost < BestCost:
        BestCost = min_cost
        BestSolution = Solutions[b].copy()

    """
    Onlooker bee phase
    """
    a = [0] * NP #make a list of all ranking scores a
    for i in range(NP):
        for j in range(NP):
            if Costs[i] <= Costs[j]:
                a[i] += 1 #compare all trajectories. if one trajectory is better, it gets a plus 1 score

    SumA = sum(a) #sum of the a scores
    if SumA == 0:
        Prob = [1.0 / NP] * NP #for debugging, in the very low chance that sumA is zero, make every prob the same
    else:
        Prob = [ai / SumA for ai in a] #divide every a ranking by the sum to get the probability and store them in a list

    for onlooker in range(NP):
        k = select_index_by_probability(Prob, rng=rng) #the function returns the index based on the roulette wheel and is a random tajectory

        base_solution = Solutions[k] #this is the trajectory with index k
        base_cost = Costs[k] #associated costs

        candidate_solution = MutateSolution(base_solution, graph, n_rings=N_RINGS, rng=rng) #make a mutation
        candidate_cost, _, _, _ = get_trajectory_cost(candidate_solution, Node_coordinates) #calculate the costs of this mutation

        if candidate_cost < base_cost:
            Solutions[k] = candidate_solution
            Costs[k] = candidate_cost #same as for employed. if the mutation is a success, replace the new trajectory with the old
            Trials[k] = 0 #if the mutation is a success, do not add a trial, else, add a trial.
        else:
            Trials[k] += 1

    min_cost = min(Costs) #update global costs, againn!!!
    b = Costs.index(min_cost)

    if min_cost < BestCost:
        BestCost = min_cost
        BestSolution = Solutions[b].copy()

    """
    Scout bee phase
    """
    best_index = Costs.index(min(Costs)) #store the index of the best solution in best_index
    for i in range(NP):
        if i == best_index:
            continue #this line prevents the best solution until now to be replaced by a random trajectory by the scout
            #it is possible that the best trajectory until now can't be improved but it is still the global best
            #so I don't want that to be thrown away

        if Trials[i] > LIMIT:
            Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS, rng=rng) #make a new random trajectory
            new_costs, _, _, _ = get_trajectory_cost(Solutions[i], Node_coordinates)
            Costs[i] = new_costs
            Trials[i] = 0

    min_cost = min(Costs) #again, find the new costs
    b = Costs.index(min_cost)

    if min_cost < BestCost:
        BestCost = min_cost
        BestSolution = Solutions[b].copy()

    best_history.append(BestSolution.copy()) #for the animation
    cost_history.append(BestCost)

    iteration += 1 #add 1 iteration

print(f'The best trajectory are the following waypoint: {BestSolution}')


_, total_fuel, total_time, total_weight = get_trajectory_cost(BestSolution, Node_coordinates)

remaining_weight = total_weight - MIN_WEIGHT


print(f'The total fuel burn on this trajectory is {total_fuel:.0f} kg')
print(f'The total time for this trajectory is {total_time:.2f} hours')
print(f'The total costs for this is trajectory are {BestCost:.0f} euros')
print(f'The total weight of the aircraft is {total_weight:.0f} kilos. This is {remaining_weight:.0f} kilos above the minimum weight')

"""
To be honest, the following has been made by chat gpt because i couldn't figure out how to make
this kind of animation.
"""


import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_bees(best_history, cost_history, node_coords):
    # 1) grid points (lon=x, lat=y)
    lons = [lon for (lat, lon) in node_coords.values()]
    lats = [lat for (lat, lon) in node_coords.values()]

    fig, ax = plt.subplots()
    ax.set_title("ABC Optimization Replay")
    ax.scatter(lons, lats, s=10)  # groen/kleuren kun je zelf zetten als je wil
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # 2) lijn-object voor het beste pad (wordt elke frame geupdate)
    (best_line,) = ax.plot([], [], linewidth=2)  # rood kun je met set_color

    # 3) tekst overlay
    txt = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top")

    def traj_to_xy(traj):
        xs, ys = [], []
        for nid in traj:
            lat, lon = node_coords[nid]
            xs.append(lon)
            ys.append(lat)
        return xs, ys

    def init():
        best_line.set_data([], [])
        txt.set_text("")
        return best_line, txt

    def update(frame):
        traj = best_history[frame]
        xs, ys = traj_to_xy(traj)
        best_line.set_data(xs, ys)
        txt.set_text(f"iter={frame}  best_cost={cost_history[frame]:.2f}")
        return best_line, txt

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(best_history),
        init_func=init,
        interval=100,   # ms per frame
        blit=True,
        repeat = False
    )

    plt.show()
animate_bees(best_history, cost_history, Node_coordinates)





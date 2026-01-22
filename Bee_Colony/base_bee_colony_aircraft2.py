"""
This file makes the code for the bee colony algorithm to run once.
This is the base file in which we are going to test it before putting it into a function for different
scenarios.

As it is the same as for aircraft 1, but with another speed and performance database input,
I will not comment the code again. refer to base bee colony ac 1
"""


POPULATION_SIZE = 50
MAX_ITERATIONS = 150
LIMIT = 50
TEMPERATURE_HEIGHT = 288.15 - ((34000 * 0.3048) * 0.0065) #temperature at our fixed flight altitude of 34,0000 feet
COST_OF_TIME_INDEX = 35 #associated operating costs, expressed in kg fuel burn per hour
MACH_AIRCRAFT_1 = 0.82 #the speed at which aircraft 1 flies with maximum efficiency
MACH_AIRCRAFT_2 = 0.81 #the speed at which aircraft 2 flies with maximum efficiency
FUEL_COSTS_PER_KG = 0.683125 #fuel kosts for 1 kg fuel burn
WEIGHT_START_CRUISE = 257743 #weight in kilos at the start of the cruise
FUEL_BURN_MAX = 62600 #maximum amount of fuel burn for the cruise based on aircraft data
MIN_WEIGHT = 195143
T_MAX = 7.0
T_MIN = 8.0
TIME_MAX_AC2 = 7.85 #this is the time window for the aircraft 2. this is the maximum flight time. it is later than for ac1 because ac 2 has a lower TAS
TIME_MIN_AC2 = 7.35
t_max = 39.0 #this is for interpolation of weather
T_START = 0.0

from Bee_Colony.random_or_mutate_trajectory_and_roulette_wheel import RandomTrajectory
from Bee_Colony.random_or_mutate_trajectory_and_roulette_wheel import MutateSolution
from graph_build_for_bee.build_graph_function import build_graph
from Trajectory.trajectory_cost_ac2 import get_trajectory_cost_ac2
from Bee_Colony.random_or_mutate_trajectory_and_roulette_wheel import select_index_by_probability





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

Solutions = [None] * NP
Costs = [None] * NP
Trials = [0] * NP
Prob = [0.0] * NP

for i in range(NP):
    Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS)
    cost_euro, fuel_burn, time_s, weight = get_trajectory_cost_ac2(Solutions[i], Node_coordinates, t_start=T_START)
    Costs[i] = cost_euro

min_cost = min(Costs)
b = Costs.index(min_cost)
BestSolution = Solutions[b].copy()
BestCost = Costs[b]

iteration = 0



best_history = []
cost_history = []

while iteration < NumIter:

    """
    Employed bee phase
    """

    for i in range(NP):
        current_solution = Solutions[i]
        current_costs = Costs[i]

        candidate_solution = MutateSolution(current_solution, graph, n_rings=N_RINGS)
        candidate_costs, _, _, _ = get_trajectory_cost_ac2(candidate_solution, Node_coordinates, t_start=T_START)

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
    a = [0] * NP
    for i in range(NP):
        for j in range(NP):
            if Costs[i] <= Costs[j]:
                a[i] += 1

    SumA = sum(a)
    if SumA == 0:
        Prob = [1.0 / NP] * NP
    else:
        Prob = [ai / SumA for ai in a]

    for onlooker in range(NP):
        k = select_index_by_probability(Prob)

        base_solution = Solutions[k]
        base_cost = Costs[k]

        candidate_solution = MutateSolution(base_solution, graph, n_rings=N_RINGS)
        candidate_cost, _, _, _ = get_trajectory_cost_ac2(candidate_solution, Node_coordinates, t_start=T_START)

        if candidate_cost < base_cost:
            Solutions[k] = candidate_solution
            Costs[k] = candidate_cost
            Trials[k] = 0
        else:
            Trials[k] += 1

    min_cost = min(Costs)
    b = Costs.index(min_cost)

    if min_cost < BestCost:
        BestCost = min_cost
        BestSolution = Solutions[b].copy()

    """
    Scout bee phase
    """
    best_index = Costs.index(min(Costs))
    for i in range(NP):
        if i == best_index:
            continue

        if Trials[i] > LIMIT:
            Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS) #make a new random trajectory
            new_costs, _, _, _ = get_trajectory_cost_ac2(Solutions[i], Node_coordinates, t_start=T_START)
            Costs[i] = new_costs
            Trials[i] = 0

    min_cost = min(Costs)
    b = Costs.index(min_cost)

    if min_cost < BestCost:
        BestCost = min_cost
        BestSolution = Solutions[b].copy()

    best_history.append(BestSolution.copy())
    cost_history.append(BestCost)

    iteration += 1 #add 1 iteration

print(f'The best trajectory are the following waypoints: {BestSolution}')


_, total_fuel, total_time, _ = get_trajectory_cost_ac2(BestSolution, Node_coordinates, t_start=T_START)




print(f'The total fuel burn on this trajectory is {total_fuel:.0f} kg')
print(f'The total time for this trajectory is {total_time:.2f} hours')
print(f'The total costs for this is trajectory are {BestCost:.0f} euros')

"""
for animation, refer to AI disclosure
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





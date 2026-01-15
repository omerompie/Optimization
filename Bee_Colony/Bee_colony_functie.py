POPULATION_SIZE = 10 #voor nu klein zodat we snel antwoord krijgen, kan opgeschaald worden
MAX_ITERATIONS = 50 #zelfde als voor pupulation: klein voor nu
LIMIT = 10
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
T_START = 0.0


from Bee_Colony.random_or_mutate_trajectory import RandomTrajectory
from Bee_Colony.random_or_mutate_trajectory import MutateSolution
from main_tryout import build_graph
from Trajectory.Total_costs_trajectory import get_trajectory_cost
from Bee_Colony.random_or_mutate_trajectory import select_index_by_probability
import pandas as pd
from pathlib import Path
import numpy as np
import time



def run_abc_once(
    graph,
    node_coords,
    N_RINGS,
    t_start,
    start_node=0,
    goal_node=610,
    NP=POPULATION_SIZE,
    NumIter=MAX_ITERATIONS,
    Limit=LIMIT,
    seed=None
):
    rng = np.random.default_rng(seed) #this is the seed

    # ----------------------------
    # Initialization
    # ----------------------------
    Solutions = [None] * NP
    Costs = [None] * NP
    Trials = [0] * NP
    Prob = [0.0] * NP  # wordt later gevuld

    # Maak NP random trajectories + cost evaluatie
    for i in range(NP):
        Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS, rng=rng)
        cost_euro, fuel_burn, time_h, weight_end = get_trajectory_cost(Solutions[i], node_coords, t_start=t_start)
        Costs[i] = cost_euro
        Trials[i] = 0

    # Global best
    min_cost = min(Costs)
    b = Costs.index(min_cost)
    BestSolution = Solutions[b].copy()
    BestCost = Costs[b]

    # ----------------------------
    # Main loop
    # ----------------------------
    iteration = 0
    while iteration < NumIter:

        # -------- Employed bees phase --------
        for i in range(NP):
            current_solution = Solutions[i]
            current_cost = Costs[i]

            candidate_solution = MutateSolution(current_solution, graph, n_rings=N_RINGS, rng=rng)
            candidate_cost, _, _, _ = get_trajectory_cost(candidate_solution, node_coords, t_start=t_start)

            if candidate_cost < current_cost:
                Solutions[i] = candidate_solution
                Costs[i] = candidate_cost
                Trials[i] = 0
            else:
                Trials[i] += 1

        # update global best
        min_cost = min(Costs)
        b = Costs.index(min_cost)
        if min_cost < BestCost:
            BestCost = min_cost
            BestSolution = Solutions[b].copy()

        # -------- Onlooker bees phase --------
        # ranking scores a[i]
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

        for _ in range(NP):
            k = select_index_by_probability(Prob, rng=rng)

            base_solution = Solutions[k]
            base_cost = Costs[k]

            candidate_solution = MutateSolution(base_solution, graph, n_rings=N_RINGS, rng=rng)
            candidate_cost, _, _, _ = get_trajectory_cost(candidate_solution, node_coords, t_start=t_start)

            if candidate_cost < base_cost:
                Solutions[k] = candidate_solution
                Costs[k] = candidate_cost
                Trials[k] = 0
            else:
                Trials[k] += 1

        # update global best
        min_cost = min(Costs)
        b = Costs.index(min_cost)
        if min_cost < BestCost:
            BestCost = min_cost
            BestSolution = Solutions[b].copy()

        # -------- Scout bees phase --------
        best_index = Costs.index(min(Costs))
        for i in range(NP):
            if i == best_index:
                continue

            if Trials[i] > Limit:
                Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS, rng=rng)
                new_cost, _, _, _ = get_trajectory_cost(Solutions[i], node_coords, t_start=t_start)
                Costs[i] = new_cost
                Trials[i] = 0

        # update global best
        min_cost = min(Costs)
        b = Costs.index(min_cost)
        if min_cost < BestCost:
            BestCost = min_cost
            BestSolution = Solutions[b].copy()

        iteration += 1

    # ----------------------------
    # Final metrics for BestSolution
    # ----------------------------
    best_cost_eur, best_fuel_kg, best_time_h, best_weight_end = get_trajectory_cost(BestSolution, node_coords, t_start=t_start)

    return BestSolution, float(best_cost_eur), float(best_fuel_kg), float(best_time_h), float(best_weight_end)


def main():
    nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()

    # Jouw Optie A: map in huidige directory (Bee_Colony/total_costs_ac1_per_time)
    OUT_DIR = Path("total_costs_ac1_per_time")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    N_RUNS = 30
    BASE_SEED = 10000
    t_starts = [float(i) for i in range(31)] #this is for the different scenarios. Each scenario is 1 hour later. so the wind changes

    for t_start in t_starts:
        results = []

        for run_id in range(1, N_RUNS + 1):
            seed = BASE_SEED + run_id #these are seeds. this line ensures that every run in different scenarios have the same seed. So run 1 in scenario 1 has the same seed as run 1 in scenario 2
            t0 = time.perf_counter()
            _, cost_eur, _, _, _ = run_abc_once(
                graph=graph,
                node_coords=node_coords,
                N_RINGS=N_RINGS,
                t_start=t_start,              # <-- hier komt scenario binnen
                start_node=0,
                goal_node=610,
                NP=POPULATION_SIZE,
                NumIter=MAX_ITERATIONS,
                Limit=LIMIT,
                seed=seed
            )
            runtime_sec = time.perf_counter() - t0 # seconds to run the abc once

            results.append({
                "run": run_id,
                "seed": seed,
                "t_start": t_start,
                "total_cost_eur": float(cost_eur),
                "runtime_sec": runtime_sec,
            })

        df = pd.DataFrame(results)

        csv_name = f"abc_costs_tstart_{t_start:.1f}.csv"
        out_path = OUT_DIR / csv_name
        df.to_csv(out_path, index=False)

        print(f"Created: {csv_name}")

if __name__ == "__main__":
    main()

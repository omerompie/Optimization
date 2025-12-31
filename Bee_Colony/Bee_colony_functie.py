POPULATION_SIZE = 10 #voor nu klein zodat we snel antwoord krijgen, kan opgeschaald worden
MAX_ITERATIONS = 150 #zelfde als voor pupulation: klein voor nu
LIMIT = 50 #zelfde als voor population: klein voor nu
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
import pandas as pd



def run_abc_once(
    graph,
    node_coords,
    N_RINGS,
    start_node=0,
    goal_node=610,
    NP=10,
    NumIter=50,
    Limit=50,
):
    """
    Doet 1 run van jouw Artificial Bee Colony (ABC).
    Retourneert:
      best_solution (list),
      best_cost_eur (float),
      best_fuel_kg (float),
      best_time_h (float),
      best_end_weight_kg (float)
    """

    # ----------------------------
    # Initialization
    # ----------------------------
    Solutions = [None] * NP
    Costs = [None] * NP
    Trials = [0] * NP
    Prob = [0.0] * NP  # wordt later gevuld

    # Maak NP random trajectories + cost evaluatie
    for i in range(NP):
        Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS)
        cost_euro, fuel_burn, time_h, weight_end = get_trajectory_cost(Solutions[i], node_coords)
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

            candidate_solution = MutateSolution(current_solution, graph, n_rings=N_RINGS)
            candidate_cost, _, _, _ = get_trajectory_cost(candidate_solution, node_coords)

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
            k = select_index_by_probability(Prob)

            base_solution = Solutions[k]
            base_cost = Costs[k]

            candidate_solution = MutateSolution(base_solution, graph, n_rings=N_RINGS)
            candidate_cost, _, _, _ = get_trajectory_cost(candidate_solution, node_coords)

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
                Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS)
                new_cost, _, _, _ = get_trajectory_cost(Solutions[i], node_coords)
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
    best_cost_eur, best_fuel_kg, best_time_h, best_weight_end = get_trajectory_cost(BestSolution, node_coords)

    return BestSolution, float(best_cost_eur), float(best_fuel_kg), float(best_time_h), float(best_weight_end)


def main():
    # 1) Build graph maar 1 keer
    nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()

    # 2) Run 1200 keer
    results = []
    N_RUNS = 500

    for run_id in range(N_RUNS):
        best_solution, cost_eur, fuel_kg, time_h, weight_end = run_abc_once(
            graph=graph,
            node_coords=node_coords,
            N_RINGS=N_RINGS,
            start_node=0,
            goal_node=610,
            NP=10,
            NumIter=50,
            Limit=50,
        )

        results.append({
            "run": run_id,
            "total_cost_eur": cost_eur,
            "total_fuel_kg": fuel_kg,
            "total_time_h": time_h,
            "end_weight_kg": weight_end,
            "trajectory_len": len(best_solution),
            "best_solution": best_solution,   # dit is een list -> kan in DataFrame
        })

        if run_id % 50 == 0:
            print("Finished run", run_id)

    # 3) DataFrame
    df = pd.DataFrame(results)

    print(df.head())
    print(df[["total_cost_eur", "total_fuel_kg", "total_time_h"]].describe())

    # 4) Opslaan
    # JSON is het fijnst omdat best_solution echt een list blijft
    df.to_json("abc_runs_1200.json", orient="records", lines=True)

    # CSV kan ook, maar best_solution wordt dan tekst
    df.to_csv("abc_runs_1200.csv", index=False)

    print("Saved: abc_runs_1200.json and abc_runs_1200.csv")


if __name__ == "__main__":
    main()
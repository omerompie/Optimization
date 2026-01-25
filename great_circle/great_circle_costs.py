""""
This file calculates the fuel burn, time and costs of the great circle route for each scenario. this is for comparison with the algorithms
"""
from Trajectory.trajectory_cost_ac1 import get_trajectory_cost
from graph_build_for_bee.build_graph_function import build_graph
import pandas as pd

nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()

great_circle_trajectory = [0, 11, 32, 53, 74, 95, 116, 137, 158, 179, 200, 221, 242, 263, 284, 305, 326, 347, 368, 389, 410, 431, 452, 473, 494, 515, 536, 557, 578, 610] #all the node IDs


t_starts = [float(i) for i in range(31)] #there are 31 t_starts. Every start is exactly 1.0 hours later

results = [] #make a list in which dictionaries are put for every t start
for t_start in t_starts: #start the loop
    total_cost, total_fuel, total_time, _ = get_trajectory_cost(
        great_circle_trajectory,
        node_coords,
        t_start=t_start
    ) #calculate the costs, fuel, and time for the great circle trajectory for a given t_start

    results.append({
        "t_start_h": t_start,
        "total_cost": total_cost,
        "total_fuel_kg": total_fuel,
        "total_time_h": total_time,
    }) #store the outcomes in a dictionary and add it to results

df = pd.DataFrame(results).sort_values("t_start_h").reset_index(drop=True) #make a dataframe from the list. make the times ascending (if this was not already the case). probably unnecessary
df.to_csv("great_circle.csv", index=False) #export it to a csv





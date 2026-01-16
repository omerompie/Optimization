from Trajectory.Total_costs_trajectory import get_trajectory_cost
from main_tryout import build_graph
import pandas as pd

nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()

great_circle_trajectory = [0, 11, 32, 53, 74, 95, 116, 137, 158, 179, 200, 221, 242, 263, 284, 305, 326, 347, 368, 389, 410, 431, 452, 473, 494, 515, 536, 557, 578, 610]

cost_gc, fuel_gc, time_gc, _ = get_trajectory_cost(great_circle_trajectory, node_coords, t_start = 0.0)


t_starts = [float(i) for i in range(31)]

results = []
for t_start in t_starts:
    total_cost, total_fuel, total_time, _ = get_trajectory_cost(
        great_circle_trajectory,
        node_coords,
        t_start=t_start
    )

    results.append({
        "t_start_h": t_start,
        "total_cost": total_cost,
        "total_fuel_kg": total_fuel,
        "total_time_h": total_time,
    })

df = pd.DataFrame(results).sort_values("t_start_h").reset_index(drop=True)
df.to_csv("great_circle.csv", index=False)
print(df.head())




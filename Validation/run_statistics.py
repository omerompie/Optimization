import sys
import os
import time
import pandas as pd
import numpy as np

# --- 1. SETUP PATHS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.grid import generate_grid, build_adjacency_list
from src.solver import solve_dynamic_dijkstra
from Trajectory.Total_costs_edge import get_edge_cost

# ==========================================
#        CONFIGURATION FOR BATCH RUN
# ==========================================
SCHIPHOL = (52.308056, 4.764167)
JFK = (40.641766, -73.780968)

# Grid Settings
N_RINGS = 29
N_ANGLES = 21
RING_SPACING_KM = 200.0
MAX_WIDTH_KM = 1800.0
BASE_WIDTH_M = 40000.0

# Solver Settings
INITIAL_WEIGHT_KG = 257743.0
TIME_BIN_SEC = 100.0

# Time Settings (Start Times to test)
# From t=0 to t=30 (31 data points)
HOURS_TO_TEST = list(range(0, 31))

# --- DURATION CONSTRAINTS ---
ENABLE_TOA_CONSTRAINT = True
MIN_FLIGHT_DURATION_HOURS = 7.00
MAX_FLIGHT_DURATION_HOURS = 7.50


# Physics Adapter
def physics_adapter(u_id, waypoint_i, waypoint_j, current_weight_kg, current_time):
    return get_edge_cost(waypoint_i, waypoint_j, u_id, current_weight_kg, current_time)


# ==========================================
#        MAIN BATCH LOOP
# ==========================================
def main():
    print(f"--- STARTING BATCH STATISTICS (t=0 to t={HOURS_TO_TEST[-1]}) ---")

    print("Generating Grid...")
    nodes, node_coords = generate_grid(SCHIPHOL, JFK, N_RINGS, N_ANGLES, RING_SPACING_KM, MAX_WIDTH_KM, BASE_WIDTH_M)
    graph = build_adjacency_list(node_coords, N_RINGS, N_ANGLES, lambda a, b: 0.0)
    end_node_id = len(nodes) - 1

    results_list = []

    for start_hour in HOURS_TO_TEST:
        print(f"\nProcessing Start Time: t = {start_hour} hours...")

        start_time_sec = start_hour * 3600.0

        # Calculate Window
        if ENABLE_TOA_CONSTRAINT:
            min_arrival_sec = start_time_sec + (MIN_FLIGHT_DURATION_HOURS * 3600.0)
            max_arrival_sec = start_time_sec + (MAX_FLIGHT_DURATION_HOURS * 3600.0)
            time_range = (min_arrival_sec, max_arrival_sec)
        else:
            time_range = None

        t0 = time.time()

        # *** UNPACK 3 VALUES NOW ***
        path, cost, states_visited = solve_dynamic_dijkstra(
            adjacency_list=graph,
            node_coords=node_coords,
            start_node_id=0,
            end_node_id=end_node_id,
            initial_weight_kg=INITIAL_WEIGHT_KG,
            start_time_sec=start_time_sec,
            physics_engine_fn=physics_adapter,
            time_bin_sec=TIME_BIN_SEC,
            target_time_range_sec=time_range
        )

        t1 = time.time()
        runtime = t1 - t0

        if path:
            # Recalculate specifics (Fuel vs Time)
            sim_weight = INITIAL_WEIGHT_KG
            sim_time = start_time_sec
            for i in range(len(path) - 1):
                f, t, c = physics_adapter(path[i], node_coords[path[i]], node_coords[path[i + 1]], sim_weight, sim_time)
                sim_weight -= f
                sim_time += t * 3600.0

            final_fuel_burn = INITIAL_WEIGHT_KG - sim_weight
            final_flight_time_h = (sim_time - start_time_sec) / 3600.0

            print(f"  -> Solved! Cost: €{cost:.0f} | Time: {final_flight_time_h:.2f}h | States: {states_visited}")

            results_list.append({
                "Start_Hour": start_hour,
                "Total_Cost_Euro": cost,
                "Fuel_Burn_Kg": final_fuel_burn,
                "Flight_Time_Hours": final_flight_time_h,
                "States_Checked": states_visited,
                "Computation_Time_Sec": runtime,
                "Status": "Optimal"
            })
        else:
            print(f"  -> No Path Found!")
            results_list.append({
                "Start_Hour": start_hour,
                "States_Checked": states_visited,
                "Computation_Time_Sec": runtime,
                "Status": "Failed"
            })

    # Save to CSV
    df = pd.DataFrame(results_list)
    output_file = "batch_statistics_results.csv"
    df.to_csv(output_file, index=False)

    print(f"\nBATCH RUN COMPLETE. Results saved to: {output_file}")


if __name__ == "__main__":
    main()
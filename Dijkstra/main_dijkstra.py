import sys
import os
import time

"""
main_dijkstra.py is the main script to run the Dijkstra algorithm.

it generates the grid, builds the graph and calls the dijkstra algorithm.
the output is a solution path and the total cost.
"""

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import
from src.grid import generate_grid, build_adjacency_list
from src.solver_1 import solve_dynamic_dijkstra
from Trajectory.edge_cost_aircraft1 import get_edge_cost

# Global variables

# A - Location
SCHIPHOL = (52.308056, 4.764167)
JFK = (40.641766, -73.780968)

# B - Grid Settings
N_RINGS = 29 # Vertical slices between AMS and JFK.
N_ANGLES = 21 # Lateral options per slice (how far left/right we can go).
RING_SPACING_KM = 200.0 # Resolution: how often we check for a new heading.
MAX_WIDTH_KM = 1800.0 # Limits how far the route can deviate (the 'search funnel').
BASE_WIDTH_M = 40000.0 # Minimum width near the start/end points.

# C - Dijkstra settings
INITIAL_WEIGHT_KG = 257743.0 # Starting weight
START_TIME_SEC = 0.0 # Reference time for weather interpolation
TIME_BIN_SEC = 100.0 # Pareto Pruning resolution (groups similar arrival times)

# D - Time of Arrival (ToA)
ENABLE_TOA_CONSTRAINT = True

# Exact min max allowed time
MIN_ARRIVAL_HOURS = 7.0
MAX_ARRIVAL_HOURS = 7.50


# Pysics adapter
def physics_adapter(u_id, waypoint_i, waypoint_j, current_weight_kg, current_time):
    """
    For every possible edge we calculate:
        1. Fuel used (based on weight/wind).
        2. Time taken (Distance / Groundspeed).
        3. Financial cost.
    """
    fuel_burn, time_h, total_cost = get_edge_cost(
        waypoint_i=waypoint_i,
        waypoint_j=waypoint_j,
        waypoint_i_id=u_id,
        current_weight_kg=current_weight_kg,
        current_time=current_time
    )
    return fuel_burn, time_h, total_cost


# Main script
def main():
    print(f"INITIALIZING DIJKSTRA OPTIMIZATION")

    # 0. Setup time constraints
    if ENABLE_TOA_CONSTRAINT:
        min_time_sec = MIN_ARRIVAL_HOURS * 3600.0 # Convert hours to seconds for the math solver
        max_time_sec = MAX_ARRIVAL_HOURS * 3600.0
        final_time_range = (min_time_sec, max_time_sec)

        print(f"ToA Active")
        print(f"{MIN_ARRIVAL_HOURS:.3f}h to {MAX_ARRIVAL_HOURS:.3f}h")
    else:
        print(f"ToA Not active")
        final_time_range = None

    # 1. Generate the grid
    print("\nGenerating the grid...")
    nodes, node_coords = generate_grid(
        origin=SCHIPHOL,
        destination=JFK,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        ring_spacing_km=RING_SPACING_KM,
        max_width_km=MAX_WIDTH_KM,
        base_width_m=BASE_WIDTH_M
    )
    print(f"Grid Generated: {len(nodes)} nodes.")

    # 2. Build the graph
    print("Building the adjacency List...")
    graph = build_adjacency_list(
        # We define which dots are reachable from the current dot.
        node_coords=node_coords,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        edge_cost_fn=lambda a, b: 0.0 # for now we are only concerned with the actual connections between the nodes this
        # is just a placeholder
    )
    # some error handling (check if the graph is empty)
    if len(graph) == 0:
        print("Error: Graph is empty.")
        return


    print("\n Starting Dijkstra")
    t_start = time.time() # for timing

    # 3. Call dijkstra
    path, cost, states_visited = solve_dynamic_dijkstra(
        adjacency_list=graph,
        node_coords=node_coords,
        start_node_id=0,
        end_node_id=len(nodes) - 1,
        initial_weight_kg=INITIAL_WEIGHT_KG,
        start_time_sec=START_TIME_SEC,
        physics_engine_fn=physics_adapter,
        time_bin_sec=TIME_BIN_SEC,
        target_time_range_sec=final_time_range
    )

    #stop the time
    t_end = time.time()
    runtime = t_end - t_start
    print(f"Computation Time: {runtime:.4f} seconds")
    print(f"States visited: {states_visited}")

    # 4. Save results for further analysis en visualization some are for specefic website to visualize the grid
    if path:
        with open("grid_waypoints_lonlat.txt", "w") as f:
            for nid in sorted(node_coords.keys()):
                lat, lon = node_coords[nid]
                f.write(f"{lat}, {lon}\n")

        with open("solution_path.txt", "w") as f:
            for nid in path:
                lat, lon = node_coords[nid]
                f.write(f"{lat}, {lon}\n")

        with open("solution_path_ids.txt", "w") as f:
            for nid in path:
                f.write(f"{nid}\n")

        print("Results saved.")
    else:
        print("\nOptimization Failed: No path found.")


if __name__ == "__main__":
    main()
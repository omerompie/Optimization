import sys
import os

# --- 1. SETUP PATHS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.grid import generate_grid, build_adjacency_list
from src.solver import solve_dynamic_dijkstra
from Trajectory.edge_cost_aircraft1 import get_edge_cost

# ==========================================
#        GLOBAL CONFIGURATION
# ==========================================

# --- A. LOCATION SETTINGS ---
SCHIPHOL = (52.308056, 4.764167)
JFK = (40.641766, -73.780968)

# --- B. GRID SETTINGS ---
N_RINGS = 29
N_ANGLES = 21
RING_SPACING_KM = 200.0
MAX_WIDTH_KM = 1800.0
BASE_WIDTH_M = 40000.0

# --- C. SOLVER SETTINGS ---
INITIAL_WEIGHT_KG = 257743.0
START_TIME_SEC = 0.0
TIME_BIN_SEC = 100.0

# --- D. TIME OF ARRIVAL (ToA) CONSTRAINTS ---
# Set this to FALSE if you want pure cheapest/fastest route without penalty
ENABLE_TOA_PENALTY = False

SCHEDULED_TIME_HOURS = 8.0  # Target: Arrive in exactly 8.00 hours
PENALTY_COST_PER_HOUR = 50000.0

# Calculate Seconds (Internal use)
SCHEDULED_TIME_SEC = SCHEDULED_TIME_HOURS * 3600.0


# ==========================================
#        PHYSICS ADAPTER
# ==========================================
def physics_adapter(u_id, waypoint_i, waypoint_j, current_weight_kg, current_time):
    fuel_burn, time_h, total_cost = get_edge_cost(
        waypoint_i=waypoint_i,
        waypoint_j=waypoint_j,
        waypoint_i_id=u_id,
        current_weight_kg=current_weight_kg,
        current_time=current_time
    )
    return fuel_burn, time_h, total_cost


# ==========================================
#             MAIN EXECUTION
# ==========================================
def main():
    print(f"--- INITIALIZING DIJKSTRA OPTIMIZATION ---")

    # 0. SETUP PENALTY LOGIC
    if ENABLE_TOA_PENALTY:
        print(f"ToA CONSTRAINT ACTIVE: Target {SCHEDULED_TIME_HOURS:.2f}h")
        print(f"    Penalty: €{PENALTY_COST_PER_HOUR:.0f} per hour deviation")
        final_target_time = SCHEDULED_TIME_SEC
        final_penalty_rate = PENALTY_COST_PER_HOUR
    else:
        print(f"ToA CONSTRAINT OFF: Optimizing for lowest base cost only.")
        final_target_time = None
        final_penalty_rate = 0.0

    # 1. GENERATE GRID
    print("\nGenerating Grid...")
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

    # 2. BUILD GRAPH
    print("Building Adjacency List...")
    graph = build_adjacency_list(
        node_coords=node_coords,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        edge_cost_fn=lambda a, b: 0.0
    )

    if len(graph) == 0:
        print("Error: Graph is empty.")
        return

    # 3. RUN DYNAMIC SOLVER
    print("\n--- Starting Dynamic Optimization ---")

    path, cost = solve_dynamic_dijkstra(
        adjacency_list=graph,
        node_coords=node_coords,
        start_node_id=0,
        end_node_id=len(nodes) - 1,
        initial_weight_kg=INITIAL_WEIGHT_KG,
        start_time_sec=START_TIME_SEC,
        physics_engine_fn=physics_adapter,
        time_bin_sec=TIME_BIN_SEC,

        # --- PASSING THE CONFIGURABLE VARIABLES ---
        target_time_sec=final_target_time,
        penalty_per_hour=final_penalty_rate
    )

    # 4. SAVE RESULTS
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
import sys
import os

# --- 1. SETUP PATHS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.grid import generate_grid, build_adjacency_list
from src.solver import solve_dynamic_dijkstra

# Import Team Physics
# After merge, this file will have the new signature with weather inside
from Trajectory.Total_costs_edge import get_edge_cost

# ==========================================
#        GLOBAL CONFIGURATION
# ==========================================
SCHIPHOL = (52.308056, 4.764167)
JFK = (40.641766, -73.780968)

N_RINGS = 29
N_ANGLES = 21
RING_SPACING_KM = 200.0
MAX_WIDTH_KM = 1800.0
BASE_WIDTH_M = 40000.0

INITIAL_WEIGHT_KG = 257743.0
START_TIME_SEC = 0.0
TIME_BIN_SEC = 100.0


# ==========================================
#        PHYSICS ADAPTER
# ==========================================

def physics_adapter(u_id, waypoint_i, waypoint_j, current_weight_kg, current_time):
    """
    Bridges the gap between Solver and Team Code.
    Now supports the "Merged" logic where Weather and ANSP are internal.
    """

    # CALL TEAMMATE'S FUNCTION
    # His signature: get_edge_cost(waypoint_i, waypoint_j, waypoint_i_id, current_weight_kg, current_time)

    fuel_burn, time_h, total_cost = get_edge_cost(
        waypoint_i=waypoint_i,
        waypoint_j=waypoint_j,
        waypoint_i_id=u_id,  # <--- PASSING THE ID FOR CSV LOOKUP
        current_weight_kg=current_weight_kg,
        current_time=current_time  # <--- PASSING EXACT TIME FOR INTERPOLATION
    )

    # Note: We do NOT add ANSP cost here anymore.
    # Your teammate added "ansp_cost = get_ansp_cost_for_edge" inside get_edge_cost.
    # We do NOT pass a wind model here.
    # Your teammate imports "get_wind_kmh" inside Total_costs_edge.py.

    return fuel_burn, time_h, total_cost


# ==========================================
#             MAIN EXECUTION
# ==========================================

def main():
    print(f"--- INITIALIZING DIJKSTRA OPTIMIZATION (MERGED WEATHER) ---")

    # 1. GENERATE GRID
    print("Generating Grid...")
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

    if len(graph) > 0:
        print(f"Graph built. Edges from AMS: {len(graph[0])}")
    else:
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
        # wind_model_fn is removed here
        time_bin_sec=TIME_BIN_SEC
    )

    # 4. SAVE RESULTS
    if path:
        print(f"\nOptimization Successful! Optimal Cost: €{cost:.2f}")

        # Save Waypoints
        with open("grid_waypoints_lonlat.txt", "w") as f:
            for nid in sorted(node_coords.keys()):
                lat, lon = node_coords[nid]
                f.write(f"{lat}, {lon}\n")

        # Save Solution Path
        with open("solution_path.txt", "w") as f:
            for nid in path:
                lat, lon = node_coords[nid]
                f.write(f"{lat}, {lon}\n")

        print("Results saved.")
    else:
        print("\nOptimization Failed: No path found.")


if __name__ == "__main__":
    main()
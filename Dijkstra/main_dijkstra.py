import sys
import os

# --- 1. SETUP PATHS ---
# This allows 'main_dijkstra.py' (inside Dijkstra folder) to import 'src' & 'Trajectory' (from parent)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.grid import generate_grid, build_adjacency_list
from src.solver import solve_dynamic_dijkstra
from src.ansp import get_ansp_cost_for_edge

# Import Team Physics
from Trajectory.Total_costs_edge import get_edge_cost

# ==========================================
#        GLOBAL CONFIGURATION
# ==========================================

# --- A. LOCATION SETTINGS ---
SCHIPHOL = (52.308056, 4.764167)
JFK = (40.641766, -73.780968)

# --- B. GRID SETTINGS (The "Chassis") ---
# Validated High-Res Config: 87 rings * 70km = ~6000km range
N_RINGS = 29
N_ANGLES = 21
RING_SPACING_KM = 200.0
MAX_WIDTH_KM = 1800.0
BASE_WIDTH_M = 40000.0

# --- C. SOLVER SETTINGS (The "Engine") ---
INITIAL_WEIGHT_KG = 257743.0  # Start Weight
START_TIME_SEC = 0.0  # Simulation Start
TIME_BIN_SEC = 100.0  # Pruning Bucket Size (Smaller = Slower & More Precise)


# ==========================================
#        WIND MODELS & PHYSICS
# ==========================================

def wavy_wind_model(position, time_hr):
    """
    A sophisticated "Wavy" Wind Model.
    Creates a series of headwind walls and tailwind corridors to force
    the aircraft to fly a North -> South -> North wave pattern.
    """
    lat, lon = position

    # Base Wind: A moderate headwind everywhere (25 kts from West)
    wind_dir = 270.0
    wind_spd = 25.0

    # PHASE 1: FORCE NORTH (East Atlantic)
    # Block 48N-53N with strong headwind
    if -20.0 < lon <= 5.0:
        if 48.0 < lat < 53.0:
            wind_spd = 130.0
            wind_dir = 270.0

    # PHASE 2: FORCE SOUTH-WEST (Mid-Atlantic)
    # Block Northern path >54N, open Southern tunnel
    elif -50.0 < lon <= -20.0:
        if lat > 54.0:
            wind_spd = 160.0  # Wall
            wind_dir = 270.0
        else:
            wind_spd = 80.0  # Tunnel
            wind_dir = 45.0  # From North-East

    # PHASE 3: FORCE NORTH TO JFK (West Atlantic)
    # Block Southern approach <45N
    elif lon <= -50.0:
        if lat < 45.0:
            wind_spd = 120.0  # Wall
            wind_dir = 270.0
        else:
            wind_spd = 40.0
            wind_dir = 135.0

    return (wind_dir, wind_spd)


def physics_adapter(waypoint_i, waypoint_j, current_weight_kg, wind_model, current_time):
    """
    Bridges the gap between Solver (Total Cost) and Team Code (Fuel/Time).
    Adds ANSP costs to the Fuel/Time costs.
    """
    # 1. Get Fuel & Time from Team Code
    fuel_burn, time_h, partial_cost = get_edge_cost(
        waypoint_i,
        waypoint_j,
        current_weight_kg,
        wind_model,
        current_time
    )

    # 2. Add the missing ANSP cost
    ansp_cost = get_ansp_cost_for_edge(waypoint_i, waypoint_j)

    # 3. Sum it up
    total_cost = partial_cost + ansp_cost

    return fuel_burn, time_h, total_cost


# ==========================================
#             MAIN EXECUTION
# ==========================================

def main():
    print(f"--- INITIALIZING DIJKSTRA OPTIMIZATION ---")
    print(f"Grid: {N_RINGS} Rings x {N_ANGLES} Angles | Spacing: {RING_SPACING_KM}km")

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

    # 2. BUILD GRAPH (Topology)
    print("Building Adjacency List...")
    graph = build_adjacency_list(
        node_coords=node_coords,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        # Pass dummy lambda because Solver calculates real cost dynamically
        edge_cost_fn=lambda a, b: 0.0
    )

    # Simple connectivity check
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
        end_node_id=len(nodes) - 1,  # JFK is the last node
        initial_weight_kg=INITIAL_WEIGHT_KG,
        start_time_sec=START_TIME_SEC,
        physics_engine_fn=physics_adapter,
        wind_model_fn=wavy_wind_model,
        time_bin_sec=TIME_BIN_SEC  # Passing the global setting
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

        print("Results saved to 'grid_waypoints_lonlat.txt' and 'solution_path.txt'")
    else:
        print("\nOptimization Failed: No path found.")


if __name__ == "__main__":
    main()
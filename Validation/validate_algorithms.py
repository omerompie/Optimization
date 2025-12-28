import sys
import os

# --- PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.grid import generate_grid, build_adjacency_list
from Trajectory.Total_costs_edge import get_edge_cost

# ==========================================
#      1. CONFIGURATION (MICRO-WORLD)
# ==========================================
SCHIPHOL = (52.308056, 4.764167)
JFK = (40.641766, -73.780968)

N_RINGS = 8  # Small grid for Brute Force
N_ANGLES = 3 # 3 Options: Left, Straight, Right
RING_SPACING_KM = 200.0
MAX_WIDTH_KM = 500.0
BASE_WIDTH_M = 40000.0
INITIAL_WEIGHT_KG = 257743.0


# ==========================================
#      2. PHYSICS ADAPTER
# ==========================================
def calculate_physics(u, v, node_coords, current_weight, current_time):
    """
    Simple wrapper to call your team's physics engine.
    """
    return get_edge_cost(
        waypoint_i=node_coords[u],
        waypoint_j=node_coords[v],
        waypoint_i_id=u,
        current_weight_kg=current_weight,
        current_time=current_time
    )


# ==========================================
#      3. BRUTE FORCE SOLVER
# ==========================================
def solve_brute_force(graph, node_coords, start_node, end_node):
    """
    Recursively explores EVERY possible path.
    """
    global total_paths_checked
    total_paths_checked = 0

    best_cost = float('inf')
    best_path = []

    def explore(current_node, current_cost, current_weight, current_time, path_history):
        nonlocal best_cost, best_path
        global total_paths_checked

        # A. BASE CASE: Reached Destination
        if current_node == end_node:
            total_paths_checked += 1
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = list(path_history)
            return

        # B. RECURSIVE STEP: Explore Neighbors
        if current_node not in graph:
            return

        for neighbor_info in graph[current_node]:
            # Handle format (neighbor_id, distance_cost)
            neighbor = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info

            # Calculate Physics for this segment
            burn, time_h, segment_cost = calculate_physics(
                current_node, neighbor, node_coords,
                current_weight, (current_time / 3600.0)
            )

            new_weight = current_weight - burn
            if new_weight < 0: continue  # Invalid path (out of fuel)

            explore(
                neighbor,
                current_cost + segment_cost,
                new_weight,
                current_time + (time_h * 3600.0),
                path_history + [neighbor]
            )

    # Start Recursion
    explore(start_node, 0.0, INITIAL_WEIGHT_KG, 0.0, [start_node])
    return best_path, best_cost


# ==========================================
#      4. MAIN EXECUTION
# ==========================================
def main():
    print(f"\n--- BRUTE FORCE VALIDATION ---")
    print(f"Grid Settings: {N_RINGS} Rings x {N_ANGLES} Angles")

    # 1. Generate Mini Grid
    nodes, node_coords = generate_grid(SCHIPHOL, JFK, N_RINGS, N_ANGLES, RING_SPACING_KM, MAX_WIDTH_KM, BASE_WIDTH_M)
    graph = build_adjacency_list(node_coords, N_RINGS, N_ANGLES, lambda a, b: 0.0)
    end_node_id = len(nodes) - 1

    print(f"Graph Built: {len(nodes)} nodes total.")
    print("Calculating absolute optimal path (this may take a moment)...")

    # 2. Run Solver
    optimal_path, optimal_cost = solve_brute_force(graph, node_coords, 0, end_node_id)

    # 3. Report Results
    print("\n" + "=" * 40)
    print("       BRUTE FORCE RESULTS       ")
    print("=" * 40)
    print(f"Total Paths Checked:   {total_paths_checked}")
    print(f"Optimal Total Cost:    €{optimal_cost:,.2f}")
    print(f"Optimal Path Nodes:    {optimal_path}")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    main()
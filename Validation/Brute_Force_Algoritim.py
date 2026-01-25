import sys
import os

# PATH SETUP
# Determine the directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
parent_dir = os.path.dirname(current_dir)
# Add project root to Python path so imports work
sys.path.append(parent_dir)

from src.grid import generate_grid, build_adjacency_list
from Trajectory.edge_cost_aircraft1 import get_edge_cost

# 1. Config
SCHIPHOL = (52.308056, 4.764167)
JFK = (40.641766, -73.780968)

N_RINGS = 8  # Small grid for Brute Force
N_ANGLES = 3 # 3 Options: Left, Straight, Right
RING_SPACING_KM = 200.0
MAX_WIDTH_KM = 500.0
BASE_WIDTH_M = 40000.0
INITIAL_WEIGHT_KG = 257743.0

# 2. Physics Engine
def calculate_physics(u, v, node_coords, current_weight, current_time):
    """
    Simple wrapper to call physics engine.
    """
    return get_edge_cost(
        waypoint_i=node_coords[u],
        waypoint_j=node_coords[v],
        waypoint_i_id=u,
        current_weight_kg=current_weight,
        current_time=current_time
    )

# 3. Brute force solver
def solve_brute_force(graph, node_coords, start_node, end_node):
    """
    Recursively explores EVERY possible path.
    """
    # Global counter to measure how many complete paths were evaluated
    global total_paths_checked
    total_paths_checked = 0

    # Store the best solution found so far
    best = {
        "cost": float("inf"),
        "path": []
    }

    def explore(current_node, current_cost, current_weight, current_time, path_history):
        """
        Recursive depth-first search through all possible paths.
        """
        global total_paths_checked

        # A. Destination reached
        if current_node == end_node:
            total_paths_checked += 1
            # Update best solution if this path is cheaper
            if current_cost < best["cost"]:
                best["cost"] = current_cost
                best["path"] = list(path_history)
            return

        # B. Explore all outgoing edges
        for neighbor_info in graph.get(current_node, []):
            # Extract neighbor node ID (edge stored as (node, cost))
            neighbor = neighbor_info[0]

            # Compute physics for this flight segment
            burn, time_h, segment_cost = calculate_physics(
                current_node, neighbor, node_coords,
                current_weight, current_time / 3600.0  # Convert seconds to hours
            )

            # Update aircraft weight after fuel burn
            new_weight = current_weight - burn
            # Discard invalid paths that run out of fuel
            if new_weight < 0:
                continue

            # Go deeper into the path
            explore(
                neighbor,
                current_cost + segment_cost,
                new_weight,
                current_time + time_h * 3600.0,
                path_history + [neighbor]
            )
    # Start recursive exploration from the origin
    explore(start_node, 0.0, INITIAL_WEIGHT_KG, 0.0, [start_node])
    # Return the globally optimal path and cost
    return best["path"], best["cost"]



# 4. Main
def main():
    print(f"\nBrute force")
    print(f"Grid: {N_RINGS} Rings x {N_ANGLES} Angles")

    # 1. Generate Mini Grid
    nodes, node_coords = generate_grid(
        SCHIPHOL,
        JFK,
        N_RINGS,
        N_ANGLES,
        RING_SPACING_KM,
        MAX_WIDTH_KM,
        BASE_WIDTH_M
    )
    # Build adjacency list (edge cost ignored here)
    graph = build_adjacency_list(node_coords, N_RINGS, N_ANGLES, lambda a, b: 0.0)
    # Destination node is always the last node
    end_node_id = len(nodes) - 1

    print(f"Graph done: {len(nodes)} nodes total.")
    print("Calculating absolute optimal path (this may take a moment)...")

    # 2. Run Solver
    optimal_path, optimal_cost = solve_brute_force(graph, node_coords, 0, end_node_id)

    # 3. Report Results
    print("Brute Force")
    print(f"Total Paths:   {total_paths_checked}")
    print(f"Optimal Total Cost:    €{optimal_cost:,.2f}")
    print(f"Optimal Path Nodes:    {optimal_path}")

# Standard Python entry point
if __name__ == "__main__":
    main()
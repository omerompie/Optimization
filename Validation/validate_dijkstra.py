import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.grid import generate_grid, build_adjacency_list
from src.solver_1 import solve_dynamic_dijkstra
from Trajectory.edge_cost_aircraft1 import get_edge_cost


SCHIPHOL = (52.308056, 4.764167)
JFK = (40.641766, -73.780968)

N_RINGS = 8
N_ANGLES = 3
RING_SPACING_KM = 200.0
MAX_WIDTH_KM = 500.0
BASE_WIDTH_M = 40000.0
INITIAL_WEIGHT_KG = 257743.0
START_TIME_SEC = 0.0

def physics_adapter(u_id, waypoint_i, waypoint_j, current_weight_kg, current_time):
    return get_edge_cost(
        waypoint_i=waypoint_i,
        waypoint_j=waypoint_j,
        waypoint_i_id=u_id,
        current_weight_kg=current_weight_kg,
        current_time=current_time
    )

# Main
def main():
    print(f"\n--- DIJKSTRA VALIDATION (MICRO-WORLD) ---")
    print(f"Grid Settings: {N_RINGS} Rings x {N_ANGLES} Angles")

    # 1. Generate Mini Grid
    nodes, node_coords = generate_grid(SCHIPHOL, JFK, N_RINGS, N_ANGLES, RING_SPACING_KM, MAX_WIDTH_KM, BASE_WIDTH_M)
    graph = build_adjacency_list(node_coords, N_RINGS, N_ANGLES, lambda a, b: 0.0)
    end_node_id = len(nodes) - 1

    print(f"Graph Built: {len(nodes)} nodes total.")
    print("Running Dijkstra Solver...")

    # 2. Run Solver
    path, cost, _ = solve_dynamic_dijkstra(
        adjacency_list=graph,
        node_coords=node_coords,
        start_node_id=0,
        end_node_id=end_node_id,
        initial_weight_kg=INITIAL_WEIGHT_KG,
        start_time_sec=START_TIME_SEC,
        physics_engine_fn=physics_adapter,
        time_bin_sec=100.0,
        target_time_range_sec=None
    )

    # 3. Report Results
    print("\n" + "=" * 40)
    print("DIJKSTRA RESULTS")
    print(f"Optimal Total Cost: €{cost:,.2f}")
    print(f"Optimal Path Nodes: {path}")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    main()
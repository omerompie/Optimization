import math
from src.grid import generate_grid, build_adjacency_list
from src.solver import solve_dynamic_dijkstra
from src.ansp import get_ansp_cost_for_edge

# --- IMPORT YOUR TEAM'S PHYSICS ---
# Importing directly from the Trajectory folder as requested
from Trajectory.Total_costs_edge import get_edge_cost


def dummy_wind_model(position, time_hr):
    """
    A sophisticated "Wavy" Wind Model.
    Creates a series of headwind walls and tailwind corridors to force
    the aircraft to fly a North -> South -> North wave pattern.
    """
    lat, lon = position

    # Base Wind: A moderate headwind everywhere (25 kts from West)
    wind_dir = 270.0
    wind_spd = 25.0

    # --- PHASE 1: FORCE NORTH (East Atlantic) ---
    # Region: 0 to -20 Longitude
    # Block the direct path (48N-53N) with strong headwind.
    # Leave the north (>53N) with base wind.
    if -20.0 < lon <= 5.0:
        if 48.0 < lat < 53.0:
            wind_spd = 130.0  # Strong Headwind Wall
            wind_dir = 270.0

    # --- PHASE 2: FORCE SOUTH-WEST (Mid-Atlantic) ---
    # Region: -20 to -50 Longitude
    # Block the northern path (>54N) with a massive headwind.
    # Create a tailwind "tunnel" in the south (<54N).
    elif -50.0 < lon <= -20.0:
        if lat > 54.0:
            wind_spd = 160.0  # Massive Northern Headwind Wall
            wind_dir = 270.0
        else:
            # Southern Corridor: Tailwind from North-East
            wind_spd = 80.0  # Strong Tailwind
            wind_dir = 45.0  # From North-East (pushes South-West)

    # --- PHASE 3: FORCE NORTH TO JFK (West Atlantic) ---
    # Region: -50 to -75 Longitude
    # Block the southern approach (<45N) with a headwind.
    # Make the northern approach favorable.
    elif lon <= -50.0:
        if lat < 45.0:
            wind_spd = 120.0  # Southern Headwind Wall
            wind_dir = 270.0
        else:
            # Northern approach: Lighter tailwind/crosswind
            wind_spd = 40.0
            wind_dir = 135.0  # From South-East (pushes North-West)

    return (wind_dir, wind_spd)


# --- PHYSICS ADAPTER ---
# This bridges the gap between the Solver (which needs Total Cost)
# and your Team's Code (which currently misses ANSP).
def physics_adapter(waypoint_i, waypoint_j, current_weight_kg, wind_model, current_time):
    # 1. Call the existing function from Trajectory/Total_costs_edge.py
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


# --- MAIN EXECUTION ---
def main():
    # 1. CONFIGURATION
    SCHIPHOL = (52.308056, 4.764167)
    JFK = (40.641766, -73.780968)

    N_RINGS = 29
    N_ANGLES = 21
    RING_SPACING_KM = 200.0
    MAX_WIDTH_KM = 1800.0
    BASE_WIDTH_M = 40000.0

    # 2. GENERATE GRID
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

    # 3. BUILD GRAPH (Topology Only)
    print("Building Adjacency List...")
    graph = build_adjacency_list(
        node_coords=node_coords,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        # Pass dummy lambda because Solver calculates real cost dynamically
        edge_cost_fn=lambda a, b: 0.0
    )
    print(f"Graph built. Edges from AMS: {len(graph[0])}")

    # 4. RUN DYNAMIC SOLVER
    print("\n--- Starting Dynamic Optimization ---")

    path, cost = solve_dynamic_dijkstra(
        adjacency_list=graph,
        node_coords=node_coords,
        start_node_id=0,
        end_node_id=len(nodes) - 1,  # JFK is the last node
        initial_weight_kg=257743.0,  # WEIGHT_START_CRUISE
        start_time_sec=0.0,
        physics_engine_fn=physics_adapter,  # Use the adapter!
        wind_model_fn=dummy_wind_model
    )

    # 5. SAVE RESULTS
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
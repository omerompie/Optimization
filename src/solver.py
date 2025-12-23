import heapq
import math


def solve_dynamic_dijkstra(
        adjacency_list,
        node_coords,
        start_node_id,
        end_node_id,
        initial_weight_kg,
        start_time_sec,
        physics_engine_fn,
        wind_model_fn,
        time_bin_sec=100.0  # <--- Now a parameter (Default 100s)
):
    """
    Solves the trajectory using Implicit Dijkstra with Pareto Dominance Pruning.

    Args:
        time_bin_sec (float): Pruning bucket size.
                              Smaller = More accuracy, slower.
                              Larger = Faster, but might prune valid paths.
    """

    # 1. INITIALIZATION
    # Priority Queue stores: (Total Cost, Node ID, Time, Weight)
    # Ordered by Cost (Lowest first)
    priority_queue = []
    heapq.heappush(priority_queue, (0.0, start_node_id, start_time_sec, initial_weight_kg))

    # Best States Registry: Used for pruning
    # Key: (Node_ID, Time_Bin) -> Value: List of [(Cost, Weight)]
    best_states = {}

    # Path Reconstruction Registry
    # Key: (Node, Time, Weight) -> Value: Parent State
    came_from = {}
    came_from[(start_node_id, start_time_sec, initial_weight_kg)] = None

    nodes_visited = 0

    print("Starting Implicit Dijkstra Search (logging history)...")

    # Open file to log the search pattern for visualization
    with open("search_history.txt", "w") as history_file:

        while priority_queue:
            # Pop the cheapest path found so far
            current_cost, u, current_time, current_weight = heapq.heappop(priority_queue)
            nodes_visited += 1

            # Log for animation
            history_file.write(f"{u}\n")

            # --- STEP A: GOAL CHECK ---
            if u == end_node_id:
                print(f"Path found! Checked {nodes_visited} states.")
                print(
                    f"Final Cost: €{current_cost:.2f}, Time: {current_time / 3600:.2f}h, Fuel Left: {current_weight:.0f}kg")
                return reconstruct_path(came_from, (u, current_time, current_weight)), current_cost

            # --- STEP B: PARETO PRUNING ---
            # We group similar arrivals into "Time Bins".
            # Inside a bin, if a previous path was Cheaper AND had More Fuel,
            # then this current path is useless (dominated). We discard it.

            t_bin = int(current_time / time_bin_sec)
            state_key = (u, t_bin)

            if state_key not in best_states:
                best_states[state_key] = []

            # Check for dominance
            is_dominated = False
            for (exist_cost, exist_weight) in best_states[state_key]:
                if exist_cost <= current_cost and exist_weight >= current_weight:
                    is_dominated = True
                    break

            if is_dominated:
                continue

                # If not dominated, add ourselves to the list
            # And remove any old paths that *we* now dominate
            new_list = []
            for (exist_cost, exist_weight) in best_states[state_key]:
                # Keep existing path only if it is NOT dominated by current
                if not (current_cost <= exist_cost and current_weight >= exist_weight):
                    new_list.append((exist_cost, exist_weight))

            new_list.append((current_cost, current_weight))
            best_states[state_key] = new_list

            # --- STEP C: EXPAND NEIGHBORS ---
            if u not in adjacency_list:
                continue

            for neighbor_info in adjacency_list[u]:
                # Handle adjacency formats: (v, cost) or just v
                v = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info

                # CALCULATE PHYSICS
                # We ask the physics engine: "If I fly u->v now, what happens?"
                fuel_burn, segment_time_h, segment_cost = physics_engine_fn(
                    waypoint_i=node_coords[u],
                    waypoint_j=node_coords[v],
                    current_weight_kg=current_weight,
                    wind_model=wind_model_fn,
                    current_time=(current_time / 3600.0)  # Convert to hours for physics
                )

                new_cost = current_cost + segment_cost
                new_weight = current_weight - fuel_burn
                new_time = current_time + (segment_time_h * 3600.0)

                # CONSTRAINT: Cannot fly with negative fuel
                if new_weight < 0:
                    continue

                # Add valid neighbor to queue
                new_state_id = (v, new_time, new_weight)
                current_state_id = (u, current_time, current_weight)
                came_from[new_state_id] = current_state_id

                heapq.heappush(priority_queue, (new_cost, v, new_time, new_weight))

    print(f"No path found. Visited {nodes_visited} states.")
    return [], 0.0


def reconstruct_path(came_from, final_state):
    """
    Backtracks from the goal to the start to rebuild the optimal path.
    """
    path = []
    curr = final_state
    while curr:
        node_id = curr[0]
        path.append(node_id)
        # Move to parent
        curr = came_from.get(curr)
    return path[::-1]  # Reverse list to get Start -> End
import heapq
import math

# --- CONFIGURATION ---
# Time Bin: Group arrivals within this window (seconds) for comparison.
# Smaller bin = More accuracy, slower runtime.
TIME_BIN_SIZE_SEC = 150.0


def solve_dynamic_dijkstra(
        adjacency_list,
        node_coords,
        start_node_id,
        end_node_id,
        initial_weight_kg,
        start_time_sec,
        physics_engine_fn,
        wind_model_fn,
):
    """
    Solves the trajectory using Implicit Dijkstra with Pareto Dominance Pruning.
    Generates 'search_history.txt' for visualization.
    """

    # 1. PRIORITY QUEUE (Cost, Node, Time, Weight)
    pq = []
    heapq.heappush(pq, (0.0, start_node_id, start_time_sec, initial_weight_kg))

    # 2. BEST STATES (Key: Node, TimeBin)
    best_states = {}

    # 3. PATH RECONSTRUCTION
    came_from = {}
    came_from[(start_node_id, start_time_sec, initial_weight_kg)] = None

    nodes_visited = 0

    print("Starting Implicit Dijkstra Search (logging history)...")

    # Open file to record the search order for animation
    # Using 'with' ensures it closes automatically when we return
    with open("search_history.txt", "w") as history_file:

        while pq:
            current_cost, u, current_time, current_weight = heapq.heappop(pq)
            nodes_visited += 1

            # --- LOG HISTORY ---
            # Record which node we are currently visiting
            history_file.write(f"{u}\n")

            # --- GOAL CHECK ---
            if u == end_node_id:
                print(f"Path found! Checked {nodes_visited} states.")
                print(
                    f"Final Cost: €{current_cost:.2f}, Time: {current_time / 3600:.2f}h, Fuel Left: {current_weight:.0f}kg")
                return reconstruct_path(came_from, (u, current_time, current_weight)), current_cost

            # --- PRUNING / DOMINANCE CHECK ---
            t_bin = int(current_time / TIME_BIN_SIZE_SEC)
            state_key = (u, t_bin)

            if state_key not in best_states:
                best_states[state_key] = []

            is_dominated = False
            for (exist_cost, exist_weight) in best_states[state_key]:
                # DOMINANCE RULE: Cheaper AND More Fuel = Dominated
                if exist_cost <= current_cost and exist_weight >= current_weight:
                    is_dominated = True
                    break

            if is_dominated:
                continue

            # Update best_states with current path
            new_list = []
            for (exist_cost, exist_weight) in best_states[state_key]:
                if not (current_cost <= exist_cost and current_weight >= exist_weight):
                    new_list.append((exist_cost, exist_weight))

            new_list.append((current_cost, current_weight))
            best_states[state_key] = new_list

            # --- EXPAND NEIGHBORS ---
            if u not in adjacency_list:
                continue

            for neighbor_info in adjacency_list[u]:
                v = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info

                fuel_burn, segment_time_h, segment_cost = physics_engine_fn(
                    waypoint_i=node_coords[u],
                    waypoint_j=node_coords[v],
                    current_weight_kg=current_weight,
                    wind_model=wind_model_fn,
                    current_time=(current_time / 3600.0)
                )

                new_cost = current_cost + segment_cost
                new_weight = current_weight - fuel_burn
                new_time = current_time + (segment_time_h * 3600.0)

                # Physics Constraint: Cannot fly with negative fuel
                if new_weight < 0:
                    continue

                new_state_id = (v, new_time, new_weight)
                current_state_id = (u, current_time, current_weight)
                came_from[new_state_id] = current_state_id

                heapq.heappush(pq, (new_cost, v, new_time, new_weight))

    print(f"No path found. Visited {nodes_visited} states.")
    return [], 0.0


def reconstruct_path(came_from, final_state):
    path = []
    curr = final_state
    while curr:
        node_id = curr[0]
        path.append(node_id)
        curr = came_from.get(curr)
    return path[::-1]
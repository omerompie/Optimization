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
        time_bin_sec=100.0,
        target_time_range_sec=None
):
    """
    Solves trajectory using Implicit Dynamic Dijkstra.
    Returns: (path, total_cost, nodes_visited_count)
    """

    # 1. INITIALIZATION
    priority_queue = []
    # (Cost, Node, Time, Weight)
    heapq.heappush(priority_queue, (0.0, start_node_id, start_time_sec, initial_weight_kg))

    best_states = {}
    came_from = {}
    came_from[(start_node_id, start_time_sec, initial_weight_kg)] = None

    nodes_visited = 0

    print(f"Starting Implicit Dijkstra Search (Start t={start_time_sec / 3600:.1f}h)...")

    with open("search_history.txt", "w") as history_file:

        while priority_queue:
            current_cost, u, current_time, current_weight = heapq.heappop(priority_queue)
            nodes_visited += 1
            history_file.write(f"{u}\n")

            # --- STEP A: GOAL CHECK ---
            if u == end_node_id:
                # 1. CHECK LOWER BOUND (Too Early?)
                if target_time_range_sec:
                    min_t, max_t = target_time_range_sec
                    if current_time < min_t:
                        # Arrived too early. Discard this path.
                        continue

                        # --- RESTORED PRINTING BLOCK ---
                actual_hours = current_time / 3600.0
                print("-" * 40)
                print(f"PATH FOUND! (Checked {nodes_visited} states)")
                print("-" * 40)
                print(f"Actual Flight Time: {actual_hours:.4f} hours")

                if target_time_range_sec:
                    min_h = target_time_range_sec[0] / 3600.0
                    max_h = target_time_range_sec[1] / 3600.0
                    print(f"Target Range:       {min_h:.4f}h - {max_h:.4f}h")
                    print("Constraint:         PASSED (Within Range)")

                print("-" * 40)
                print(f"FINAL TOTAL COST:   €{current_cost:.2f}")
                print(f"Fuel Remaining:     {current_weight:.0f} kg")
                print("-" * 40)

                # Return Path, Cost, AND nodes_visited
                return reconstruct_path(came_from, (u, current_time, current_weight)), current_cost, nodes_visited

            # --- STEP B: PRUNING (Pareto) ---
            t_bin = int(current_time / time_bin_sec)
            state_key = (u, t_bin)

            if state_key not in best_states:
                best_states[state_key] = []

            is_dominated = False
            for (exist_cost, exist_weight) in best_states[state_key]:
                if exist_cost <= current_cost and exist_weight >= current_weight:
                    is_dominated = True
                    break

            if is_dominated:
                continue

            new_list = []
            for (exist_cost, exist_weight) in best_states[state_key]:
                if not (current_cost <= exist_cost and current_weight >= exist_weight):
                    new_list.append((exist_cost, exist_weight))

            new_list.append((current_cost, current_weight))
            best_states[state_key] = new_list

            # --- STEP C: EXPAND NEIGHBORS ---
            if u not in adjacency_list:
                continue

            for neighbor_info in adjacency_list[u]:
                v = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info

                # 1. CALCULATE PHYSICS
                fuel_burn, segment_time_h, segment_cost = physics_engine_fn(
                    u_id=u,
                    waypoint_i=node_coords[u],
                    waypoint_j=node_coords[v],
                    current_weight_kg=current_weight,
                    current_time=(current_time / 3600.0)
                )

                new_cost = current_cost + segment_cost
                new_weight = current_weight - fuel_burn
                new_time = current_time + (segment_time_h * 3600.0)

                # 2. CHECK VALIDITY (Fuel)
                if new_weight < 0:
                    continue

                    # 3. CHECK VALIDITY (Time Upper Bound)
                if target_time_range_sec:
                    min_t, max_t = target_time_range_sec
                    if new_time > max_t:
                        continue

                        # 4. PUSH TO QUEUE
                new_state_id = (v, new_time, new_weight)
                current_state_id = (u, current_time, current_weight)
                came_from[new_state_id] = current_state_id

                heapq.heappush(priority_queue, (new_cost, v, new_time, new_weight))

    print(f"No path found. Visited {nodes_visited} states.")
    return [], 0.0, nodes_visited


def reconstruct_path(came_from, final_state):
    path = []
    curr = final_state
    while curr:
        node_id = curr[0]
        path.append(node_id)
        curr = came_from.get(curr)
    return path[::-1]
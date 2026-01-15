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
        target_time_sec=None,  # Optional: Scheduled Time of Arrival
        penalty_per_hour=0.0  # Optional: Cost per hour deviation
):
    """
    Solves trajectory with optional Time of Arrival (ToA) Penalty.
    """

    # 1. INITIALIZATION
    priority_queue = []
    # (Cost, Node, Time, Weight)
    heapq.heappush(priority_queue, (0.0, start_node_id, start_time_sec, initial_weight_kg))

    best_states = {}
    came_from = {}
    came_from[(start_node_id, start_time_sec, initial_weight_kg)] = None

    nodes_visited = 0

    print("Starting Implicit Dijkstra Search...")

    with open("search_history.txt", "w") as history_file:

        while priority_queue:
            current_cost, u, current_time, current_weight = heapq.heappop(priority_queue)
            nodes_visited += 1
            history_file.write(f"{u}\n")

            # --- STEP A: GOAL CHECK ---
            if u == end_node_id:
                actual_hours = current_time / 3600.0

                print("-" * 40)
                print(f"PATH FOUND! (Checked {nodes_visited} states)")
                print("-" * 40)
                print(f"Actual Flight Time: {actual_hours:.4f} hours")

                # Detailed Report if Penalty was active
                if target_time_sec:
                    target_hours = target_time_sec / 3600.0
                    diff_hours = actual_hours - target_hours
                    penalty_amount = abs(diff_hours) * penalty_per_hour

                    print(f"Target Flight Time: {target_hours:.4f} hours")
                    print(f"Deviation:          {diff_hours:+.4f} hours")
                    print(f"Penalty Applied:    €{penalty_amount:.2f}")
                else:
                    print("Constraint:         None (Fastest/Cheapest found)")

                print("-" * 40)
                print(f"FINAL TOTAL COST:   €{current_cost:.2f}")
                print(f"Fuel Remaining:     {current_weight:.0f} kg")
                print("-" * 40)

                return reconstruct_path(came_from, (u, current_time, current_weight)), current_cost

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

                if new_weight < 0:   # Fix this. (Not good assumption).
                    continue

                # 2. APPLY TOA PENALTY (Only if entering the Goal Node)
                if v == end_node_id and target_time_sec is not None:
                    diff_hours = abs(new_time - target_time_sec) / 3600.0
                    penalty = diff_hours * penalty_per_hour
                    new_cost += penalty

                # 3. PUSH TO QUEUE
                new_state_id = (v, new_time, new_weight)
                current_state_id = (u, current_time, current_weight)
                came_from[new_state_id] = current_state_id

                heapq.heappush(priority_queue, (new_cost, v, new_time, new_weight))

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
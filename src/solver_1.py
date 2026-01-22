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
    Finds the optimal flight path using a constrained Dijkstra search.

    This uses an implicit graph approach: states are expanded dynamically.
    To ensure efficiency, we use Pareto Pruning (keeping only the best states
    per time-bin) rather than visiting every possible permutation.

    Returns:
        Tuple: (List of Node IDs in path, Total Cost, Total States Visited)
    """

    # --- CONSTANTS ---
    # The weight of the aircraft when empty (Zero Fuel Weight).
    # If current_weight drops below this, we have run out of fuel.
    MIN_DRY_WEIGHT_KG = 160000.0

    # --- 1. INITIALIZATION ---

    # Priority Queue: The "To-Do" list, sorted by lowest Cost.
    # Structure: (Total Cost, Node ID, Current Time, Current Weight)
    priority_queue = []
    heapq.heappush(priority_queue, (0.0, start_node_id, start_time_sec, initial_weight_kg))

    # Pruning Storage ('best_states'):
    # Key: (Node ID, Time Bin) -> Value: List of [Cost, Weight] pairs.
    # Used to discard paths that are strictly worse than ones we've already found.
    best_states = {}

    # Path Reconstruction ('came_from'):
    # Maps a State -> Previous State, allowing us to backtrack the path at the end.
    came_from = {}
    came_from[(start_node_id, start_time_sec, initial_weight_kg)] = None

    nodes_visited = 0
    print(f"Starting Search... (Start Time: {start_time_sec / 3600:.2f}h)")

    with open("search_history.txt", "w") as history_file:

        # --- 2. MAIN LOOP ---
        while priority_queue:
            # Pop the state with the lowest cost
            current_cost, u, current_time, current_weight = heapq.heappop(priority_queue)
            nodes_visited += 1
            history_file.write(f"{u}\n")

            # --- A. GOAL CHECK (Did we reach JFK?) ---
            if u == end_node_id:

                # Check Time Window (Hard Constraint)
                if target_time_range_sec:
                    min_arrival, max_arrival = target_time_range_sec
                    # If we arrived too early, we discard this path and keep searching
                    # for a slower (and likely cheaper) one in the queue.
                    if current_time < min_arrival:
                        continue

                        # Success! Print report and return.
                fuel_burned = initial_weight_kg - current_weight
                print("-" * 40)
                print(f"PATH FOUND! (Explored {nodes_visited} states)")
                print("-" * 40)
                print(f"Arrival Time:   {current_time / 3600.0:.4f} hours")
                print(f"Total Cost:     €{current_cost:.2f}")
                print(f"Total Fuel:     {fuel_burned:.0f} kg")
                print("-" * 40)

                final_state = (u, current_time, current_weight)
                path = reconstruct_path(came_from, final_state)
                return path, current_cost, nodes_visited

            # --- B. PARETO PRUNING (Optimization) ---
            # We discretize time into 'bins' (e.g., 100 seconds) to group similar states.
            t_bin = int(current_time / time_bin_sec)
            state_key = (u, t_bin)

            if state_key not in best_states:
                best_states[state_key] = []

            # Check for Dominance:
            # Is there an existing path to this node (in this time bin) that is
            # BOTH Cheaper AND has More Fuel? If yes, this current path is useless.
            is_dominated = False
            for (exist_cost, exist_weight) in best_states[state_key]:
                if exist_cost <= current_cost and exist_weight >= current_weight:
                    is_dominated = True
                    break

            if is_dominated:
                continue

                # Update the Pareto Frontier:
            # Add the current state, and remove any old states that are now dominated by this one.
            new_list = []
            for (exist_cost, exist_weight) in best_states[state_key]:
                if not (current_cost <= exist_cost and current_weight >= exist_weight):
                    new_list.append((exist_cost, exist_weight))

            new_list.append((current_cost, current_weight))
            best_states[state_key] = new_list

            # --- C. EXPAND NEIGHBORS (Next Steps) ---
            if u not in adjacency_list:
                continue

            for neighbor_info in adjacency_list[u]:
                v = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info

                # 1. Physics Engine Calculation
                # Calculate cost/fuel/time to fly from U to V
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

                # 2. Safety Check: Out of Fuel?
                # We crash if weight drops below the empty aircraft weight.
                if new_weight < MIN_DRY_WEIGHT_KG:
                    continue

                    # 3. Constraint Check: Too Late?
                # Stop exploring if we have already exceeded the latest arrival time.
                if target_time_range_sec:
                    _, max_arrival = target_time_range_sec
                    if new_time > max_arrival:
                        continue

                        # 4. Add valid neighbor to Queue
                new_state_id = (v, new_time, new_weight)
                current_state_id = (u, current_time, current_weight)
                came_from[new_state_id] = current_state_id

                heapq.heappush(priority_queue, (new_cost, v, new_time, new_weight))

    print(f"Optimization Failed. Visited {nodes_visited} states.")
    return [], 0.0, nodes_visited


def reconstruct_path(came_from, final_state):
    """
    Rebuilds the path by backtracking from the destination to the start.
    """
    path = []
    curr = final_state
    while curr:
        node_id = curr[0]
        path.append(node_id)
        curr = came_from.get(curr)
    return path[::-1]
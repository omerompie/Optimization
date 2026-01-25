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
    this is the modified Dijkstra algorithm.

    Implicit graph approach: states are expanded dynamically.
    For Efficiency, we use Pareto Pruning (keeping only the best states
    per time-bin) rather than visiting every possible permutation.

    Returns: List of Node IDs in path, Total Cost, Total States Visited)
    """

    # Constants
    # Zero Fuel Weight
    # If the aircraft weight drops below this, it means we ran out of fuel.
    MIN_DRY_WEIGHT_KG = 160000.0

    # 1. Initialization

    # Priority queue for Dijkstra search.
    # Each entry represents a "state" of the aircraft.
    # Stored as: (total_cost, current_node, current_time_seconds, current_weight_kg)
    priority_queue = []
    heapq.heappush(priority_queue, (0.0, start_node_id, start_time_sec, initial_weight_kg))

    # Dictionary used for Pareto pruning.
    # Key: (node_id, discretized_time_bin)
    # Used to discard paths that are strictly worse than ones we've already found.
    best_states = {}

    # Dictionary used to reconstruct the final path.
    # Each state maps to the state that led to it.
    came_from = {}
    came_from[(start_node_id, start_time_sec, initial_weight_kg)] = None

    # Counter to track how many states were explored
    nodes_visited = 0
    print(f"Starting Search (Start Time: {start_time_sec / 3600:.2f}h)")

    # Open a file to gather the visited nodes
    with open("search_history.txt", "w") as history_file:

        # 2. The main loop
        # Continue until there are no more states to explore
        while priority_queue:
            # Pop the state with the lowest cost
            current_cost, u, current_time, current_weight = heapq.heappop(priority_queue)
            nodes_visited += 1
            # Log the visited node
            history_file.write(f"{u}\n")

            # A - checking if we reached the goal
            if u == end_node_id:

                # If a ToA is active, enforce it
                if target_time_range_sec:
                    min_arrival, max_arrival = target_time_range_sec
                    # If we arrived too early, we discard this path and keep searching
                    if current_time < min_arrival:
                        continue

                        # Success! Print report and return.
                fuel_burned = initial_weight_kg - current_weight
                print(f"Path found (searched {nodes_visited} states)")
                print(f"Arrival Time:   {current_time / 3600.0:.3f} hours")
                print(f"Total Cost:     €{current_cost:.2f}")
                print(f"Total Fuel:     {fuel_burned:.0f} kg")
                print("-" * 40)

                # Reconstruct and return the path
                final_state = (u, current_time, current_weight)
                path = reconstruct_path(came_from, final_state)
                return path, current_cost, nodes_visited

            # --- B. PARETO PRUNING (Optimization) ---
            # We discretize time into 'bins' (e.g., 100 seconds) to group similar states.
            t_bin = int(current_time / time_bin_sec)
            state_key = (u, t_bin)

            # Initialize the Pareto list if this state hasn't been visited before
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

            # If it is worse, just discard this state
            if is_dominated:
                continue

                # Update
            # Add the current state, and remove any old states that are now dominated by this one.
            new_list = []
            for (exist_cost, exist_weight) in best_states[state_key]:
                if not (current_cost <= exist_cost and current_weight >= exist_weight):
                    new_list.append((exist_cost, exist_weight))

            # Add the current state
            new_list.append((current_cost, current_weight))
            best_states[state_key] = new_list

            # C - Look at the neighbors of this node
            if u not in adjacency_list:
                continue

            # Loop over all neighboring nodes
            for neighbor_info in adjacency_list[u]:
                #get the tuple of the neighbor
                v = neighbor_info[0]

                # 1. Physics Engine Calculation
                # Compute fuel burn, flight time, and cost for this segment
                fuel_burn, segment_time_h, segment_cost = physics_engine_fn(
                    u_id=u,
                    waypoint_i=node_coords[u],
                    waypoint_j=node_coords[v],
                    current_weight_kg=current_weight,
                    current_time=(current_time / 3600.0)
                )

                # Update cumulative values
                new_cost = current_cost + segment_cost
                new_weight = current_weight - fuel_burn
                new_time = current_time + (segment_time_h * 3600.0)

                # 2. Safety Check: Out of Fuel?
                # Discard paths that run out of fuel
                if new_weight < MIN_DRY_WEIGHT_KG:
                    continue

                # 3. Constraint Check: Too Late?
                # Discard paths that arrive too late
                if target_time_range_sec:
                    _, max_arrival = target_time_range_sec
                    if new_time > max_arrival:
                        continue

                # 4. Add valid neighbor to Queue
                new_state_id = (v, new_time, new_weight)
                current_state_id = (u, current_time, current_weight)
                came_from[new_state_id] = current_state_id

                # Push the new state into the priority queue
                heapq.heappush(priority_queue, (new_cost, v, new_time, new_weight))

    # If the queue empties, no valid path was found
    print(f"Failed. Visited {nodes_visited} states.")
    return [], 0.0, nodes_visited


def reconstruct_path(came_from, final_state):
    """
    Rebuilds the path by backtracking from the destination to the start.
    """
    path = []
    curr = final_state
    # Follow the chain of states backwards
    while curr:
        node_id = curr[0]
        path.append(node_id)
        curr = came_from.get(curr)
    # Reverse the path to get start → end
    return path[::-1]
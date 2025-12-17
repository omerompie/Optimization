

import random
from main_tryout import build_graph

nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()



Node_coordinates = node_coords



start_node = 0
goal_node = 610




def RandomTrajectory(start_node, goal_node, graph, n_rings=29, rng=None):

    rng = rng or random #use rng if rng != 0

    trajectory = [start_node] #start of the trajectory

    current = start_node #where we are at this moment

    max_edges = n_rings + 1 #maximum amount of edges of one trajectory
    edges_taken = 0  #to prevent we fall into a loop (only happens if our graph is not correct)

    while current != goal_node: #continue until goal node is reached

        edges = graph.get(current, []) #get the outgoing edges by calling the adjacency list(graph)

        if not edges:
            raise ValueError(
                f"Node {current} does not have outgoing edges, cannot reach {goal_node}."
            ) #safety check. Raises a value error if the node doesn't have outgoing edges

        neighbors = [neighbor_id for (neighbor_id, _) in edges] #our adjecency lists still has costs. i put a dummy in it that all edge costs are 0 because we don't work with edge costs, only trajectory costs. the _ throws away the costs in this line

        next = rng.choice(neighbors) #choose a random neighbor

        trajectory.append(next) #add it to the list of nodes

        current = next #update current node

        edges_taken += 1 #add the edge to the total edges
        if edges_taken > max_edges:
            raise RuntimeError(
                "Trajectory is longer than expectd. Bug in the graph"
            ) #another safety check to see if the graph is not bugged


    return trajectory

def MutateSolution(solution, graph, n_rings=29, rng=None, max_tries=200):

    rng = rng or random #same as for define random trajectory

    expected_len = n_rings + 2 #the expected length of the trajectory. will be used  for safety check
    if len(solution) != expected_len:
        raise ValueError(f"Solution lengte {len(solution)} != expected {expected_len}.")

    start_node = solution[0]
    goal_node = solution[-1]

    for point in range(max_tries): #max tries is the max amount of tries to find a feasible mutation
        ring_mutation = rng.randrange(0, n_rings) #choose a random ring number
        position = ring_mutation + 1  #the node of ring r is on index r + 1

        prev_node = solution[position - 1]
        old_node  = solution[position]

        prev_edges = graph.get(prev_node, []) #get the outgoing edges out of the previous node
        if not prev_edges: #if previous edge is [] (empty), try again. so make a new mutation
            continue

        feasible_options = [nid for (nid, _) in prev_edges if nid != old_node] #make a list of feasible alternatives from previous node and filter the old node
        if not feasible_options:
            continue #if it gives an [], the old node was the only option from the previous node

        new_node = rng.choice(feasible_options) #choose a random feasible option


        new_solution = solution[:position] + [new_node] #get the list of the nodes of the trajectory before the point of mutation and add the new node

        current = new_node
        remaining_edges_max = n_rings - ring_mutation
        steps = 0 #for the safety check later. Checks if it gives a feasible route

        while current != goal_node:
            edges = graph.get(current, [])
            if not edges:
                break #stops the loop if there are not any outgoing edges anymore

            neighbors = [nid for (nid, _) in edges]
            next = rng.choice(neighbors)

            new_solution.append(next)
            current = next

            steps += 1
            if steps > remaining_edges_max:
                break # if this is the case, the new solution is not feasible.

        if len(new_solution) == expected_len and new_solution[0] == start_node and new_solution[-1] == goal_node: #ensures that only a feasible solution returns
            return new_solution

    return solution




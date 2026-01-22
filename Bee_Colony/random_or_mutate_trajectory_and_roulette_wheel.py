""""
this python file defines the functions for generating random trajectories, mutating trajectories
and defines a function to do a roulette wheel for the onlooker phase
"""



import random
from graph_build_for_bee.build_graph_function import build_graph
import numpy as np


nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph() #load our graph


start_node = 0 #AMS
goal_node = 610 #JFK






def RandomTrajectory(start_node, goal_node, graph, n_rings=29, rng=None): #define the function to create a trajectory

    if rng is None:
        rng = np.random.default_rng() #this is for testing the algorithm without a seed. Later,  seeds will be applied

    trajectory = [start_node] #start of the trajectory

    current = start_node #where we are at this moment

    max_edges = n_rings + 1 #maximum amount of edges of one trajectory
    edges_taken = 0  #to prevent we fall into a loop (only happens if our graph is not correct)

    while current != goal_node: #continue until goal node is reached

        edges = graph.get(current, []) #get the outgoing edges by calling the adjacency list(graph)

        if not edges: #if edges is an empty list
            raise ValueError(
                f"Node {current} does not have outgoing edges, cannot reach {goal_node}."
            ) #safety check. Raises a value error if the node doesn't have outgoing edges

        neighbors = [neighbor_id for (neighbor_id, _) in edges] #our adjecency lists still has costs. i put a dummy in it that all edge costs are 0 because we don't work with edge costs, only trajectory costs. the _ throws away the costs in this line

        next = int(rng.choice(neighbors)) #choose a random neighbor. the int() is for later, otherwise the nodes come out as this: np.int64(17)

        trajectory.append(next) #add it to the list of nodes

        current = next #update current node

        edges_taken += 1 #add the edge to the total edges
        if edges_taken > max_edges:
            raise RuntimeError(
                "Trajectory is longer than expectd. Bug in the graph"
            ) #another safety check to see if the graph is not bugged


    return trajectory

def MutateSolution(solution, graph, n_rings=29, rng=None, max_tries=200): #define a function which is going to mutate a trajectory

    if rng is None:
        rng = np.random.default_rng()  # this is for testing the algorithm without a seed. later, seeds will be applied

    expected_len = n_rings + 2 #the expected length of the trajectory. will be used  for safety check. Amount of nodes is the amount of rings + 2 (start and end node)
    if len(solution) != expected_len:
        raise ValueError(f"Solution length {len(solution)} != expected {expected_len}.") #for testing this function.

    start_node = solution[0] #schiphol
    goal_node = solution[-1] #new york jfk

    ring_mutation = int(rng.integers(0, n_rings)) #choose a random ring number (integer)
    position = ring_mutation + 1  #the node of ring r is on solution index r + 1

    prev_node = solution[position - 1] #the node in the previous ring
    old_node  = solution[position] #the node that is selected

    prev_edges = graph.get(prev_node, []) #get the outgoing edges out of the previous node
    if not prev_edges:
        return None #if there are not any outgoing edges, return None. for testing this function

    feasible_options = [nid for (nid, _) in prev_edges if nid != old_node] #make a list of feasible alternatives from previous node and filter the old node
    if not feasible_options:
        return None #if it gives an [], the old node was the only option from the previous node

    new_node = int(rng.choice(feasible_options)) #choose a random feasible option. int() for the same reason as previous

    new_solution = solution[:position] + [new_node] #get the list of the nodes of the trajectory before the point of mutation and add the new node

    current = new_node #now we are going to generate the rest of the trajectory
    remaining_edges_max = n_rings - ring_mutation #define the remaining edges
    steps = 0 #for the safety check later. Checks if it gives a feasible route. every next edge is a step

    while current != goal_node:
        edges = graph.get(current, []) #get the outgoing edges for the current node
        if not edges:
            break #stops the loop if there are not any outgoing edges anymore

        neighbors = [nid for (nid, _) in edges] #again, list the neighbors and remove the dummy costs
        next = int(rng.choice(neighbors)) #choose a neighbor

        new_solution.append(next) #add the node to the solution
        current = next #make next the current node

        steps += 1 #add a step
        if steps > remaining_edges_max:
            break # if this is the case, the new solution is not feasible.

    if len(new_solution) == expected_len and new_solution[0] == start_node and new_solution[-1] == goal_node: #ensures that only a feasible solution returns
        return new_solution

    return None #returns none if something goes wrong. for testing the function





"""
The next function is the input for the roulette wheel. It works as follows:
During the onlooker phase. different trajectories will be compared to each other. 
Better trajectories get a higher score a. 
This score will be divided by the sum of all a values to get the probability.
This function convert all probabilities into intervals between 0 and 1
For example: if a probability of index i is 0.5. This function assigns the interval 0.0 to 0.5 to it. 
the next solution j has a probability of 0.3. this function assigns the interval 0.5 to 0.8 to it. 
Later, the random function calls a number between 0 or 1. As can be seen, higher probabilities have higher 
chances to be selected by the  function.
"""


def select_index_by_probability(prob_list, rng = None): #define the function
    if rng is None:
        rng = np.random.default_rng() #if no seed is used.
    r = rng.random()  # random number between 0 and 1
    cumulative = 0.0  # cumulative sum
    for index in range(len(prob_list)): #go through all the indices
        cumulative += prob_list[index] #add the probability of this index to the running total
        if r <= cumulative: #if the r is smaller than or equal to the current cumulative total, r falls inside the range of that index and that index is chosen
            return index #return that index
    return len(prob_list) -1 #fallback by rounding numbers. if r is bigger than the cumulative (due to floating numbers for example) return the last index




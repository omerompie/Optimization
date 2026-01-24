
from src.grid import generate_grid, build_adjacency_list

"""
Graph generation (Bee Colony)

We generate the same waypoint graph structure as for Dijkstra (same nodes and adjacency).
The adjacency-list builder requires an edge_cost_fn argument, because Dijkstra needs a
static cost per edge.

For the Bee Colony algorithm we do not use these per-edge costs: each candidate route is
evaluated afterwards with get_trajectory_cost, which computes the total cost using
time- and weight-dependent effects (wind, fuel burn, etc.).

Therefore, we provide a dummy edge_cost_fn that returns 0.0 so the adjacency list can be
built without affecting the Bee Colony optimisation.
"""

def calculate_edge_cost(a, b):
    # Dummy:
    return 0.0


def build_graph(): #this function which builds the graph with all the nodes (identifications and coordinates)
    SCHIPHOL = (52.308056, 4.764167) #schiphol coordinate
    JFK = (40.641766, -73.780968) #JFK coordinate

    N_RINGS = 29 #amount of rings in our graph
    N_ANGLES = 21 #amount of waypoints in our graph
    RING_SPACING_KM = 200.0 #distance between rings
    MAX_WIDTH_KM = 1800.0 #max width with respect to the great circle route in kilometers
    BASE_WITDH_M = 40000.0 #base width in meters

    nodes, node_coords = generate_grid(
        origin=SCHIPHOL,
        destination=JFK,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        ring_spacing_km=RING_SPACING_KM,
        max_width_km=MAX_WIDTH_KM,
        base_width_m=BASE_WITDH_M
    )   #call the generate grid function with our defined parameters

    graph = build_adjacency_list(
        node_coords=node_coords,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        edge_cost_fn=calculate_edge_cost,
    ) #build the adjacency list. With our dummy for the costs. each nodes gets a list of adjecent nodes. later used for trajectory generation

    return nodes, node_coords, graph, N_RINGS, N_ANGLES







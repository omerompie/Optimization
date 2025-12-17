"""
Deze main tryout heb ik gedaan omdat ik de main functie om de graph te genereren moest opsplitsen in 2
aangezien hij uit twee parts bestond, eentje om de graph te bouwen en eentje om te kijken voor bugs
in de bees heb ik alleen de graph nodig, daarom heb ik hem opgesplitst. om de oude te behouden
heb ik een nieuw bestand gemaakt, deze, waarin ik het heb opgesplitst om in bees te gebruiken :)
"""

from src.grid import generate_grid, build_adjacency_list
from src.vinc import v_direct
from src.ansp import get_ansp_cost_for_edge

def calculate_edge_cost(a, b):
    # Dummy: alleen zodat build_adjacency_list kan draaien.
    # Heeft geen invloed op  bee-algoritme als je later get_trajectory_cost gebruikt.
    return 0.0


def build_graph():
    SCHIPHOL = (52.308056, 4.764167)
    JFK = (40.641766, -73.780968)

    N_RINGS = 29
    N_ANGLES = 21
    RING_SPACING_KM = 200.0
    MAX_WIDTH_KM = 1800.0
    BASE_WITDH_KM = 40000.0

    nodes, node_coords = generate_grid(
        origin=SCHIPHOL,
        destination=JFK,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        ring_spacing_km=RING_SPACING_KM,
        max_width_km=MAX_WIDTH_KM,
        base_width_m=BASE_WITDH_KM
    )

    graph = build_adjacency_list(
        node_coords=node_coords,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        edge_cost_fn=calculate_edge_cost,
    )

    return nodes, node_coords, graph, N_RINGS, N_ANGLES


def main():
    nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()

    print(f"Grid generation complete. Total nodes including AMS and JFK: {len(nodes)}")
    print("Sample nodes:")
    for nid in [0, 1, 20, 100, 300, 500, 610]:
        if nid in node_coords:
            print(f"  Node {nid}: lat={node_coords[nid][0]:.6f}, lon={node_coords[nid][1]:.6f}")

    print(f"\nNumber of nodes: {len(node_coords)}")
    print(f"Number of edges from AMS (node 0): {len(graph[0])}")

    # Check an internal node connections
    sample_id = 1 + 5 * N_ANGLES + 10  # for example, ring 5, angle 10
    print(f"Outgoing edges from node {sample_id} (lat={node_coords[sample_id][0]:.6f}, lon={node_coords[sample_id][1]:.6f}):")
    for edge in graph[sample_id]:
        neigh_id, cost = edge
        print(f"  -> Node {neigh_id} (lat={node_coords[neigh_id][0]:.6f}, lon={node_coords[neigh_id][1]:.6f}), cost: {cost:.2f} meters")

    # Uncomment below to write waypoints for plotting
    with open("../grid_waypoints_lonlat.txt", "w") as f:
        for nid in sorted(node_coords.keys()):
            lat, lon = node_coords[nid]
            f.write(f"{lat}, {lon}\n")


if __name__ == "__main__":
    main()
from src.grid import generate_grid, build_adjacency_list
from src.vinc import v_direct
from src.ansp import get_ansp_cost_for_edge

def calculate_edge_cost(a, b):
    # distance, bearing (for time, wind, etc.)
    dist_m, bearing = v_direct(a, b)
    dist_km = dist_m / 1000.0
    # ... your TAS, wind, GS, time, fuel_kg, fuel_cost, time_cost ...

    ansp_cost = get_ansp_cost_for_edge(a, b)

    total_cost = ansp_cost
    return total_cost


def main():
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
    print(f"Grid generation complete. Total nodes including AMS and JFK: {len(nodes)}")
    print("Sample nodes:")
    for nid in [0, 1, 20, 100, 300, 500, 610]:
        if nid in node_coords:
            print(f"  Node {nid}: lat={node_coords[nid][0]:.6f}, lon={node_coords[nid][1]:.6f}")

    graph = build_adjacency_list(
        node_coords=node_coords,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        edge_cost_fn=calculate_edge_cost,
    )

    print(f"\nNumber of nodes: {len(node_coords)}")
    print(f"Number of edges from AMS (node 0): {len(graph[0])}")

    # Check an internal node connections
    sample_id = 1 + 5 * N_ANGLES + 10  # for example, ring 5, angle 10
    print(f"Outgoing edges from node {sample_id} (lat={node_coords[sample_id][0]:.6f}, lon={node_coords[sample_id][1]:.6f}):")
    for edge in graph[sample_id]:
        neigh_id, cost = edge
        print(f"  -> Node {neigh_id} (lat={node_coords[neigh_id][0]:.6f}, lon={node_coords[neigh_id][1]:.6f}), cost: {cost:.2f} meters")

    #Uncomment below to write waypoints for plotting
    with open("grid_waypoints_lonlat.txt", "w") as f:
        for nid in sorted(node_coords.keys()):
            lat, lon = node_coords[nid]
            f.write(f"{lat}, {lon}\n")

if __name__ == "__main__":
    main()


# LINK for the plot: https://www.mapcustomizer.com/map/max-spread-1800km

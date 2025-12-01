# main.py

from src.grid import generate_grid

def main():
    # Schiphol and JFK coordinates
    SCHIPHOL = (52.308056, 4.764167)
    JFK = (40.641766, -73.780968)

    nodes, node_coords = generate_grid(
        origin=SCHIPHOL,
        destination=JFK,
        n_rings=29,
        n_angles=21,
        ring_spacing_km=200.0,
        angular_spread_deg=20.0,
    )

    total_nodes = len(nodes)
    print(f"Total nodes (including AMS and JFK): {total_nodes}")

    # AMS and JFK sanity
    print("Node 0 (AMS):", node_coords[0])
    last_id = max(node_coords.keys())
    print(f"Last node id (JFK): {last_id}, coords: {node_coords[last_id]}")

    # Sample some interior nodes
    print("Sample nodes:")
    for nid in [1, 21, 100, 300, 500]:
        if nid in node_coords:
            print(f"  Node {nid}: {node_coords[nid]}")

if __name__ == "__main__":
    main()

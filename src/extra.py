import math
from typing import Dict, List, Tuple, Callable
from collections import defaultdict
from .vinc import v_direct, v_inverse

# Type aliases for clarity
NodeCoords = Dict[int, Tuple[float, float]]
Graph = Dict[int, List[Tuple[int, float]]]


def generate_grid(
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        n_rings: int,
        n_angles: int,
        ring_spacing_km: float,
        max_width_km: float,
        base_width_m: float,
) -> Tuple[List[Tuple[float, float]], Dict[int, Tuple[float, float]]]:
    """
    Generate 2D lateral grid between origin and destination.
    """
    AMS_lat, AMS_lon = origin
    JFK_lat, JFK_lon = destination

    # Calculate initial bearing and total distance
    total_dist_m, initial_bearing = v_direct(origin, destination)

    nodes: List[Tuple[float, float]] = []
    node_coords: Dict[int, Tuple[float, float]] = {}

    # 1. Add Origin Node (AMS)
    nodes.append((AMS_lat, AMS_lon))
    node_coords[0] = (AMS_lat, AMS_lon)
    node_id = 1

    for ring_idx in range(n_rings):
        # Distance along the Great Circle
        ring_distance_m = (ring_idx + 1) * ring_spacing_km * 1000.0

        # Stop if we overshoot the destination
        if ring_distance_m >= total_dist_m:
            break

        # --- WIDTH CALCULATION ---
        # Progress from 0.0 (start) to 1.0 (end)
        progress = ring_idx / (n_rings - 1)
        sine_factor = math.sin(math.pi * progress)

        # Base width + Sine bulge
        current_width_m = (max_width_km * 1000.0 * sine_factor) + base_width_m
        half_width_m = current_width_m / 2.0

        # --- CONVERT WIDTH TO ANGLE ---
        # avoid div/0 for very small distances
        if ring_distance_m < 1000:
            angle_spread_rad = math.radians(90)
        else:
            angle_spread_rad = math.atan(half_width_m / ring_distance_m)

        current_spread_deg = math.degrees(angle_spread_rad)

        # Calculate angle step
        if n_angles > 1:
            current_step = 2 * current_spread_deg / (n_angles - 1)
        else:
            current_step = 0

        # Generate points for this ring
        for angle_idx in range(n_angles):
            angle_offset = -current_spread_deg + angle_idx * current_step
            bearing = initial_bearing + angle_offset
            lat, lon = v_inverse(AMS_lat, AMS_lon, bearing, ring_distance_m)

            nodes.append((lat, lon))
            node_coords[node_id] = (lat, lon)
            node_id += 1

    # 3. Add Destination Node (JFK)
    nodes.append((JFK_lat, JFK_lon))
    # Note: node_id here is the next available ID after the last ring
    node_coords[node_id] = (JFK_lat, JFK_lon)

    return nodes, node_coords


def build_adjacency_list(
        node_coords: NodeCoords,
        n_rings: int,  # We will ignore this argument and calculate the REAL value
        n_angles: int,
        edge_cost_fn: Callable[[Tuple[float, float], Tuple[float, float]], float],
) -> Graph:
    """
    Build adjacency list for ring/angle grid.
    Automatically detects if fewer rings were generated than requested.
    """

    # --- ROBUST FIX FOR CRASH ---
    # The generation might have stopped early if the rings overshot the destination.
    # We infer the ACTUAL number of rings from the node list.
    # Logic: JFK is the last node. Its ID is (1 + actual_rings * n_angles).
    JFK_id = max(node_coords.keys())
    AMS_id = 0

    # Reverse engineer the actual ring count:
    # (JFK_id - AMS - JFK_itself) / n_angles
    # = (JFK_id - 1) / n_angles
    actual_n_rings = (JFK_id - 1) // n_angles

    def node_id_of(r: int, k: int) -> int:
        # Helper to get ID of node at ring r, angle k
        return 1 + r * n_angles + k

    # 1) Build plain list of directed edges (u, v)
    edges: List[Tuple[int, int]] = []

    # AMS -> all nodes in ring 0
    # (Only if we have at least one ring)
    if actual_n_rings > 0:
        for k in range(n_angles):
            edges.append((AMS_id, node_id_of(0, k)))

    # Internal rings: r = 0 .. actual_n_rings-2
    for r in range(actual_n_rings - 1):
        for k in range(n_angles):
            src = node_id_of(r, k)

            # 1. Straight forward
            edges.append((src, node_id_of(r + 1, k)))

            # 2. Diagonal Left
            if k > 0:
                edges.append((src, node_id_of(r + 1, k - 1)))

            # 3. Diagonal Right
            if k < n_angles - 1:
                edges.append((src, node_id_of(r + 1, k + 1)))

    # Last ring -> JFK
    if actual_n_rings > 0:
        last_r = actual_n_rings - 1
        for k in range(n_angles):
            edges.append((node_id_of(last_r, k), JFK_id))
    else:
        # Edge case: Direct link if 0 rings (shouldn't happen with valid params)
        edges.append((AMS_id, JFK_id))

    # 2) Convert edges into adjacency list with costs
    graph: Graph = defaultdict(list)

    for u, v in edges:
        cost = edge_cost_fn(node_coords[u], node_coords[v])
        graph[u].append((v, cost))

    # Ensure JFK exists with no outgoing edges
    if JFK_id not in graph:
        graph[JFK_id] = []

    return graph
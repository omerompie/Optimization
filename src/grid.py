# src/grid.py

import math
from typing import Dict, List, Tuple
from .vinc import v_direct, v_inverse


def generate_grid(
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        n_rings: int,
        n_angles: int,
        ring_spacing_km: float,
        max_width_km: float,  # CHANGED: We now define the max width in KM, not degrees
        base_width_m: float,
) -> Tuple[List[Tuple[float, float]], Dict[int, Tuple[float, float]]]:
    """
    Generate 2D lateral grid between origin and destination.

    Uses a fixed Lateral Width (km) approach to ensure symmetry.
    The grid starts narrow, reaches 'max_width_km' in the middle,
    and narrows symmetrically at the end.
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

        # --- SINE WAVE LOGIC (SYMMETRICAL WIDTH) ---
        # Calculate progress from 0.0 to 1.0
        progress = ring_idx / (n_rings - 1)

        # DEFINE YOUR BASE WIDTH HERE (The width at the start and end)
        # Currently hardcoded to 40 km. Change this to 10 km for a tighter pinch.

        # --- SINE WAVE LOGIC ---
        progress = ring_idx / (n_rings - 1)
        sine_factor = math.sin(math.pi * progress)

        # Now we add the base width to the sine calculation
        # The sine wave adds the EXTRA width on top of the base
        current_width_m = (max_width_km * 1000.0 * sine_factor) + base_width_m

        # --- CONVERT WIDTH TO ANGLE ---
        # Geometry: tan(theta) = Opposite / Adjacent
        # angle = atan( half_width / distance )
        # This naturally makes the angle LARGE at the start and SMALL at the end
        half_width_m = current_width_m / 2.0

        # Prevent division by zero or weirdness at very small distances
        if ring_distance_m < 1000:
            angle_spread_rad = math.radians(90)  # Cap at 90 deg
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
    node_coords[node_id] = (JFK_lat, JFK_lon)

    return nodes, node_coords

from collections import defaultdict
from typing import Dict, List, Tuple, Callable
from .vinc import v_direct

NodeCoords = Dict[int, Tuple[float, float]]
Graph = Dict[int, List[Tuple[int, float]]]


def build_adjacency_list(
    node_coords: NodeCoords,
    n_rings: int,
    n_angles: int,
    edge_cost_fn: Callable[[Tuple[float, float], Tuple[float, float]], float],
) -> Graph:
    """
    Build adjacency list for ring/angle grid.

    node_coords: {node_id: (lat, lon)}
    n_rings: number of rings (same as used in generate_grid)
    n_angles: number of angles per ring
    edge_cost_fn: function (coordA, coordB) -> cost (float)

    Returns:
        graph: {node_id: [(neighbor_id, cost), ...]}
    """

    def node_id_of(r: int, k: int) -> int:
        return 1 + r * n_angles + k

    AMS_id = 0
    JFK_id = 1 + n_rings * n_angles

    # 1) Build plain list of directed edges (u, v)
    edges: List[Tuple[int, int]] = []

    # AMS -> all nodes in ring 0
    for k in range(n_angles):
        edges.append((AMS_id, node_id_of(0, k)))

    # Internal rings: r = 0 .. n_rings-2
    for r in range(n_rings - 1):
        for k in range(n_angles):
            src = node_id_of(r, k)
            # straight
            edges.append((src, node_id_of(r + 1, k)))
            # left
            if k > 0:
                edges.append((src, node_id_of(r + 1, k - 1)))
            # right
            if k < n_angles - 1:
                edges.append((src, node_id_of(r + 1, k + 1)))

    # Last ring -> JFK
    last_r = n_rings - 1
    for k in range(n_angles):
        edges.append((node_id_of(last_r, k), JFK_id))

    # 2) Convert edges into adjacency list with costs
    graph: Graph = defaultdict(list)

    for u, v in edges:
        cost = edge_cost_fn(node_coords[u], node_coords[v])
        graph[u].append((v, cost))

    # Ensure JFK exists with no outgoing edges
    if JFK_id not in graph:
        graph[JFK_id] = []

    return graph

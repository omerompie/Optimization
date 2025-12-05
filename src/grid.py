# src/grid.py

from typing import Dict, List, Tuple
from .vinc import v_direct, v_inverse
import math

def generate_grid(
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        n_rings: int,
        n_angles: int,
        ring_spacing_km: float,
        max_angular_spread_deg: float,
        min_spread_factor: float = 0.6,  # NEW PARAMETER
) -> Tuple[List[Tuple[float, float]], Dict[int, Tuple[float, float]]]:
    """
    Generate 2D lateral grid with rounded diamond shape.

    Spread varies smoothly: moderate at start/end, maximum in middle.

    Args:
        min_spread_factor: Minimum spread as fraction of max_angular_spread_deg.
                          E.g., 0.4 means 40% spread at AMS and JFK.
    """
    AMS_lat, AMS_lon = origin
    JFK_lat, JFK_lon = destination

    _, initial_bearing = v_direct(origin, destination)

    nodes: List[Tuple[float, float]] = []
    node_coords: Dict[int, Tuple[float, float]] = {}

    nodes.append((AMS_lat, AMS_lon))
    node_coords[0] = (AMS_lat, AMS_lon)
    node_id = 1

    for ring_idx in range(n_rings):
        ring_distance_m = (ring_idx + 1) * ring_spacing_km * 1000.0

        # Progress from 0.0 (start) to 1.0 (end)
        progress = ring_idx / (n_rings - 1) if n_rings > 1 else 0.5

        # Distance from midpoint (0.0 at center, 0.5 at ends)
        distance_from_center = abs(progress - 0.5)

        # Inverted parabola: peaks at 1.0 in center, drops to 0.0 at ends
        parabola_factor = 1.0 - (2.0 * distance_from_center) ** 2

        # Blend between min and max spread
        spread_factor = min_spread_factor + (1.0 - min_spread_factor) * parabola_factor

        # Current spread for this ring
        current_angular_spread = max_angular_spread_deg * spread_factor

        # Angle step for this ring
        if n_angles == 1:
            angle_step = 0.0
        else:
            angle_step = 2 * current_angular_spread / (n_angles - 1)

        for angle_idx in range(n_angles):
            angle_offset = -current_angular_spread + angle_idx * angle_step
            bearing = initial_bearing + angle_offset
            lat, lon = v_inverse(AMS_lat, AMS_lon, bearing, ring_distance_m)

            nodes.append((lat, lon))
            node_coords[node_id] = (lat, lon)
            node_id += 1

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

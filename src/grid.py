import math
from typing import Dict, List, Tuple, Callable
from collections import defaultdict
from .vinc import v_direct, v_inverse

# --- TYPE DEFINITIONS ---
NodeCoords = Dict[int, Tuple[float, float]]
Graph = Dict[int, List[Tuple[int, float]]]
EdgeCostFunc = Callable[[Tuple[float, float], Tuple[float, float]], float]


def _calculate_width_at_ring(
        ring_idx: int,
        total_rings: int,
        max_width_km: float,
        base_width_m: float
) -> float:
    """
    Internal helper: Calculates the grid width at a specific ring index using a sine wave.
    """
    if total_rings <= 1:
        return base_width_m

    # Progress: 0.0 (start) -> 1.0 (end)
    progress = ring_idx / (total_rings - 1)

    # Sine factor: 0 -> 1 -> 0 (Bulges in the middle)
    sine_factor = math.sin(math.pi * progress)

    # Final Width = Base + (Bulge * Sine)
    return (max_width_km * 1000.0 * sine_factor) + base_width_m


def generate_grid(
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        n_rings: int,
        n_angles: int,
        ring_spacing_km: float,
        max_width_km: float,
        base_width_m: float,
) -> Tuple[List[Tuple[float, float]], NodeCoords]:
    """
    Generates a cigar-shaped 2D grid of nodes between origin and destination.
    """

    # 1. SETUP
    nodes: List[Tuple[float, float]] = []
    node_coords: NodeCoords = {}

    # Add Origin (Node 0)
    nodes.append(origin)
    node_coords[0] = origin

    next_node_id = 1
    total_dist_m, initial_bearing = v_direct(origin, destination)

    # 2. GENERATE RINGS
    for ring_idx in range(n_rings):

        # Calculate forward distance along the Great Circle
        current_dist_m = (ring_idx + 1) * ring_spacing_km * 1000.0

        # SAFETY STOP: Do not generate rings beyond the destination
        if current_dist_m >= total_dist_m:
            break

        # Calculate Grid Width at this specific ring
        current_width_m = _calculate_width_at_ring(
            ring_idx, n_rings, max_width_km, base_width_m
        )
        half_width_m = current_width_m / 2.0

        # Calculate Angular Spread (Opening angle from Origin)
        # Avoid division by zero for very small distances
        if current_dist_m < 1000:
            spread_angle_rad = math.radians(90)
        else:
            spread_angle_rad = math.atan(half_width_m / current_dist_m)

        spread_angle_deg = math.degrees(spread_angle_rad)

        # Calculate angle step size (Lateral spacing)
        if n_angles > 1:
            step_deg = (2 * spread_angle_deg) / (n_angles - 1)
        else:
            step_deg = 0

        # Create nodes for this ring
        for angle_i in range(n_angles):
            # Calculate lateral offset
            angle_offset = -spread_angle_deg + (angle_i * step_deg)
            final_bearing = initial_bearing + angle_offset

            # Project new coordinate
            lat, lon = v_inverse(origin[0], origin[1], final_bearing, current_dist_m)

            nodes.append((lat, lon))
            node_coords[next_node_id] = (lat, lon)
            next_node_id += 1

    # 3. ADD DESTINATION
    # The ID will be whatever is next after the last ring
    nodes.append(destination)
    node_coords[next_node_id] = destination

    return nodes, node_coords


def build_adjacency_list(
        node_coords: NodeCoords,
        n_rings: int,  # Kept for interface consistency, but ignored in logic
        n_angles: int,
        edge_cost_fn: EdgeCostFunc,
) -> Graph:
    """
    Builds the graph connections (Edges).

    CRITICAL: Automatically detects the *actual* number of rings generated.
    This prevents crashes if the grid generation stopped early (e.g., hit land).
    """

    # --- 1. DETECT GRID STRUCTURE ---
    # Logic: Destination ID = 1 + (Rings * Angles)
    # Therefore: Rings = (Dest_ID - 1) / Angles

    start_node_id = 0
    end_node_id = max(node_coords.keys())

    actual_n_rings = (end_node_id - 1) // n_angles

    # Helper: Calculate ID of a specific node
    def get_id(ring_idx: int, angle_idx: int) -> int:
        return 1 + (ring_idx * n_angles) + angle_idx

    edges: List[Tuple[int, int]] = []

    # --- 2. BUILD EDGES ---

    # Case A: START -> Ring 0
    if actual_n_rings > 0:
        for k in range(n_angles):
            target_node = get_id(0, k)
            edges.append((start_node_id, target_node))
    else:
        # Edge Case: Start -> End directly (No rings fit)
        edges.append((start_node_id, end_node_id))

    # Case B: Ring -> Ring (Internal)
    # We connect Ring `r` to Ring `r+1`
    for r in range(actual_n_rings - 1):
        for k in range(n_angles):
            src_node = get_id(r, k)

            # 1. Straight connection
            edges.append((src_node, get_id(r + 1, k)))

            # 2. Left Diagonal (if not on left edge)
            if k > 0:
                edges.append((src_node, get_id(r + 1, k - 1)))

            # 3. Right Diagonal (if not on right edge)
            if k < n_angles - 1:
                edges.append((src_node, get_id(r + 1, k + 1)))

    # Case C: Last Ring -> END
    if actual_n_rings > 0:
        last_ring_idx = actual_n_rings - 1
        for k in range(n_angles):
            src_node = get_id(last_ring_idx, k)
            edges.append((src_node, end_node_id))

    # --- 3. CALCULATE COSTS ---
    graph: Graph = defaultdict(list)

    for u, v in edges:
        # Calculate physical cost (distance/wind/etc passed via wrapper)
        # Note: edge_cost_fn usually returns 0 here and is calculated dynamically in solver
        cost = edge_cost_fn(node_coords[u], node_coords[v])
        graph[u].append((v, cost))

    # Ensure End Node exists in graph (even if it has no outgoing edges)
    if end_node_id not in graph:
        graph[end_node_id] = []

    return graph
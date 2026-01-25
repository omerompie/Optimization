import math
from typing import Dict, List, Tuple, Callable
from collections import defaultdict
from .vinc import v_direct, v_inverse

# These are just type aliases to make the code more readable
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
    # To make it more robust, here is a check to avoid division by zero. And just use the predifind base width.
    if total_rings <= 1:
        return base_width_m

    # Calculate how far through the rings we are (0.0 at start, 1.0 at end)
    progress = ring_idx / (total_rings - 1)

    """
    For the search space we wanted to make a sort of a double funnel shape.
    Which starts small and widens to the end and then in reverse. 
    What this does is to make a the search space especially bigger.
    In order to create a funnel shape at the start and which widens around the end, A simple sine wave
    is used to create a bulge in the middle. And its also easier to calculate with a progress value.
    
    For example 
    At progress=0: sin(0) = 0 (narrow at start)
    At progress=0.5: sin(π/2) = 1 (widest in middle)
    At progress=1.0: sin(π) = 0 (narrow at end)
    """
    sine_factor = math.sin(math.pi * progress)

    # Final Width = Base + (Bulge * Sine)
    # This is to make sure the grid bulges in the middle and tapers at the ends
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
    Generates a  2D grid of nodes between origin and destination.
    """

    # 1. SETUP
    # Initialize empty lists to store all nodes and their coordinates
    nodes: List[Tuple[float, float]] = []
    node_coords: NodeCoords = {}

    # Add Origin (Node 0) (starting point)
    nodes.append(origin)
    node_coords[0] = origin

    # Start counting node IDs from 1 (since 0 is the origin)
    next_node_id = 1

    # Calculate total distance and initial bearing from origin to destination
    # v_direct returns (distance_in_meters, bearing_in_degrees)
    total_dist_m, initial_bearing = v_direct(origin, destination)

    # 2. GENERATE RINGS
    # Each ring is a row of nodes perpendicular to the origin-destination line
    for ring_idx in range(n_rings):

        # Calculate how far forward this ring should be from the origin
        # (ring_idx + 1) because we start at ring 1, not ring 0
        current_dist_m = (ring_idx + 1) * ring_spacing_km * 1000.0

        # Safety
        # If the ring would be past the destination, stop generating rings
        if current_dist_m >= total_dist_m:
            break

        # Calculate how wide the grid should be at this specific ring
        # Uses the sine wave function to create the cigar bulge
        current_width_m = _calculate_width_at_ring(
            ring_idx, n_rings, max_width_km, base_width_m
        )

        # Half-width is used for calculations (distance from center to edge)
        half_width_m = current_width_m / 2.0

        # Calculate the angular spread from the origin's perspective
        # This is the opening angle how wide the cone opens at this distance
        # Uses simple arctangent: tan(angle) = opposite/adjacent = half_width/distance
        if current_dist_m < 1000:
            # Safety: if too close to origin, use 90 degrees to avoid issues
            spread_angle_rad = math.radians(90)
        else:
            # Calculate the angle based on width and distance
            spread_angle_rad = math.atan(half_width_m / current_dist_m)

        # Convert the spread angle from radians to degrees for easier calculations
        spread_angle_deg = math.degrees(spread_angle_rad)

        # Calculate the angular step between nodes in this ring
        # We need to distribute n_angles nodes across the width
        if n_angles > 1:
            # Divide the total angular spread by (n_angles - 1) to get even spacing
            # Example: 3 nodes need 2 gaps between them
            step_deg = (2 * spread_angle_deg) / (n_angles - 1)
        else:
            # If only 1 angle, no stepping needed (just the center)
            step_deg = 0

        # Creating all the nodes for this ring
        for angle_i in range(n_angles):
            # Calculate the lateral offset for this specific node
            # Start from the left edge (-spread_angle_deg) and step right
            angle_offset = -spread_angle_deg + (angle_i * step_deg)
            # Final bearing = straight-line bearing ± lateral offset
            final_bearing = initial_bearing + angle_offset

            # Project the new coordinate using the calculated bearing and distance
            # v_inverse takes (start_lat, start_lon, bearing, distance)
            # and returns (end_lat, end_lon)
            lat, lon = v_inverse(origin[0], origin[1], final_bearing, current_dist_m)

            # Add this node to our collections
            nodes.append((lat, lon))
            node_coords[next_node_id] = (lat, lon)
            # Increment for the next node
            next_node_id += 1

    # 3. ADD DESTINATION
    # The destination is the final node (after all rings)
    nodes.append(destination)
    node_coords[next_node_id] = destination

    # Return both the list of coordinates and the mapping dictionary
    return nodes, node_coords


def build_adjacency_list(
        node_coords: NodeCoords,
        n_rings: int,  # Kept for consistency, but ignored in logic
        n_angles: int,
        edge_cost_fn: EdgeCostFunc,
) -> Graph:
    """
    Builds the graph connections (Edges).

    it can also detects the *actual* number of rings generated.
    This prevents crashes if the grid generation stopped early.
    """

    # --- 1. DETECT GRID STRUCTURE ---
    # We need to figure out how many rings were ACTUALLY created
    # (might be less than n_rings if we hit the destination early)
    # Logic: Destination ID = 1 + (Rings * Angles)
    # Therefore: Rings = (Dest_ID - 1) / Angles

    start_node_id = 0
    # Destination is always the highest node ID
    end_node_id = max(node_coords.keys())

    # Calculate actual rings: Total nodes = 1 (origin) + (rings × angles) + 1 (destination)
    # So: rings = (end_node_id - 1) / angles
    # use integer division to get the exact number of complete rings
    actual_n_rings = (end_node_id - 1) // n_angles

    # Helper: Calculate ID of a specific node
    # Formula: node_id = 1 + (ring_index × n_angles) + angle_index
    # The +1 is because node 0 is the origin
    def get_id(ring_idx: int, angle_idx: int) -> int:
        return 1 + (ring_idx * n_angles) + angle_idx

    # Initialize list to store all edges (connections between nodes)
    edges: List[Tuple[int, int]] = []

    # ------------------------------------------------------------------------------------------------------------------
    # Build the structure so which node connects to which

    # 1: Connect start to the first ring
    if actual_n_rings > 0:
        # Connect origin to every node in ring 0
        for k in range(n_angles):
            target_node = get_id(0, k)
            edges.append((start_node_id, target_node))
    else:
        # if no rings fit, connect start directly to end
        edges.append((start_node_id, end_node_id))

    # 2: Ring -> Ring (Internal)
    # We connect Ring `r` to Ring `r+1`, so that we stop at actual_n_rings - 1
    for r in range(actual_n_rings - 1):
        # For each node in the current ring
        for k in range(n_angles):
            # Get the ID of the current source node
            src_node = get_id(r, k)

            # 1. Straight connection
            edges.append((src_node, get_id(r + 1, k)))

            # 2. Left Diagonal (if not on left edge)
            if k > 0:
                edges.append((src_node, get_id(r + 1, k - 1)))

            # 3. Right Diagonal (if not on right edge)
            if k < n_angles - 1:
                edges.append((src_node, get_id(r + 1, k + 1)))

    # 3: Last Ring -> END
    if actual_n_rings > 0:
        # The last ring is at index (actual_n_rings - 1)
        last_ring_idx = actual_n_rings - 1
        # Connect every node in the last ring to the destination
        for k in range(n_angles):
            src_node = get_id(last_ring_idx, k)
            edges.append((src_node, end_node_id))

    # 4. Build graph structure (adjacency list)
    graph: Graph = defaultdict(list)

    for u, v in edges:
        # Calculate physical cost (distance/wind/etc passed via wrapper)
        # edge_cost_fn usually returns 0 here and is calculated dynamically in solver
        cost = edge_cost_fn(node_coords[u], node_coords[v])
        # Add this edge to the graph:
        graph[u].append((v, cost))

    # Ensure End Node exists in graph (even if it has no outgoing edges)
    if end_node_id not in graph:
        graph[end_node_id] = []

    return graph
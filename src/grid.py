# src/grid.py

"""
Grid generation for lateral AMS–JFK optimization.
Creates rings at fixed distances from origin with angular deviations
around the great-circle initial bearing.
"""

from typing import Dict, List, Tuple

from .geometry import distance_and_bearing, v_inverse


def generate_grid(
    origin: Tuple[float, float],
    destination: Tuple[float, float],
    n_rings: int = 29,
    n_angles: int = 21,
    ring_spacing_km: float = 200.0,
    angular_spread_deg: float = 20.0,
) -> Tuple[List[Tuple[float, float]], Dict[int, Tuple[float, float]]]:
    """
    Generate 2D lateral grid between origin and destination.

    origin, destination: (lat_deg, lon_deg)
    n_rings: number of distance rings from origin
    n_angles: number of angular samples per ring
    ring_spacing_km: radial distance between rings (km)
    angular_spread_deg: +/- spread around initial bearing (degrees)

    Returns:
        nodes: list of (lat, lon) in node_id order
        node_coords: dict {node_id: (lat, lon)}
    """
    AMS_lat, AMS_lon = origin
    JFK_lat, JFK_lon = destination

    # Great-circle bearing; distance not used here yet but computed for completeness
    _, initial_bearing = distance_and_bearing(origin, destination)

    nodes: List[Tuple[float, float]] = []
    node_coords: Dict[int, Tuple[float, float]] = {}

    # Node 0 = origin
    nodes.append((AMS_lat, AMS_lon))
    node_coords[0] = (AMS_lat, AMS_lon)
    node_id = 1

    # Angular step between samples
    if n_angles == 1:
        angle_step = 0.0
    else:
        angle_step = 2 * angular_spread_deg / (n_angles - 1)

    for ring_idx in range(n_rings):
        # Distance of this ring from origin (meters)
        ring_distance_m = (ring_idx + 1) * ring_spacing_km * 1000.0

        for angle_idx in range(n_angles):
            angle_offset = -angular_spread_deg + angle_idx * angle_step
            bearing = initial_bearing + angle_offset

            lat, lon = v_inverse(AMS_lat, AMS_lon, bearing, ring_distance_m)

            nodes.append((lat, lon))
            node_coords[node_id] = (lat, lon)
            node_id += 1

    # Last node = destination
    nodes.append((JFK_lat, JFK_lon))
    node_coords[node_id] = (JFK_lat, JFK_lon)

    return nodes, node_coords

from typing import Tuple
from .vinc import v_direct

Coord = Tuple[float, float]  # (lat, lon)

def _in_box(lat: float, lon: float,
            lat_min: float, lat_max: float,
            lon_min: float, lon_max: float) -> bool:
    return (lat_min <= lat <= lat_max) and (lon_min <= lon <= lon_max)


def _get_region(lat: float, lon: float) -> str:
    """
    Determines the ANSP region based on Lat/Lon.
    Prioritizes specific regions (UK/IRE) before broad ocean/continent bands.
    """

    # 1. UK / Ireland (more specific box)
    # Rough bounds: 48N–60N, longitudes -12W to +2E
    if 48.0 <= lat <= 60.0 and -12.0 <= lon <= 2.0:
        return "UK_IRE"

    # 2. North America (West of -60 lon)
    if lon < -60.0:
        return "NA"

    # 3. North Atlantic (ocean between NA and UK/Ireland)
    # Latitude band to avoid Azores/Africa
    if -60.0 <= lon < -10.0 and 40.0 <= lat <= 70.0:
        return "NAT"

    # 4. Fallback: Continental Europe (rest of route start)
    return "EU"


def _get_rate_eur_per_km(region: str) -> float:
    """
    Effective en-route ANSP cost per km for a heavy long-haul aircraft (~250 t).
    Approximate, derived from public unit rates.
    """
    if region == "UK_IRE":
        return 0.9   # €/km
    if region == "NAT":
        return 0.4   # €/km
    if region == "NA":
        return 0.5   # €/km
    # EU or fallback
    return 0.7       # €/km


def get_ansp_cost_for_edge(a: Coord, b: Coord) -> float:
    """
    Approximate ANSP cost for one edge by assigning the whole edge
    to the region containing its midpoint and multiplying by distance.
    """
    lat_a, lon_a = a
    lat_b, lon_b = b

    # Midpoint (simple average)
    lat_mid = 0.5 * (lat_a + lat_b)
    lon_mid = 0.5 * (lon_a + lon_b)

    region = _get_region(lat_mid, lon_mid)
    rate = _get_rate_eur_per_km(region)

    dist_m, _ = v_direct(a, b)
    dist_km = dist_m / 1000.0

    return rate * dist_km

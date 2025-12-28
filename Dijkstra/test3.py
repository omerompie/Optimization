import sys
import os

# --- PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src.test import generate_grid

# ==========================================
#        GRID CONFIGURATION
# ==========================================
# Using your standard settings to test the new "Parabola" shape
SCHIPHOL = (52.308056, 4.764167)
JFK = (40.641766, -73.780968)

N_RINGS = 29
N_ANGLES = 21
RING_SPACING_KM = 200.0
MAX_WIDTH_KM = 1800.0  # The max width in the middle
BASE_WIDTH_M = 40000.0  # The width at the very ends


def main():
    print("--- TESTING NEW GRID GENERATION (INVERTED PARABOLA) ---")
    print(f"Settings: {N_RINGS} Rings, {N_ANGLES} Angles, Max Width {MAX_WIDTH_KM}km")

    # 1. GENERATE
    nodes, node_coords = generate_grid(
        origin=SCHIPHOL,
        destination=JFK,
        n_rings=N_RINGS,
        n_angles=N_ANGLES,
        ring_spacing_km=RING_SPACING_KM,
        max_width_km=MAX_WIDTH_KM,
        base_width_m=BASE_WIDTH_M
    )

    print(f"Successfully generated {len(nodes)} nodes.")

    # 2. SAVE FOR VISUALIZATION
    # This overwrites the file that 'visualize.py' reads
    output_file = "grid_waypoints_lonlat.txt"

    with open(output_file, "w") as f:
        for nid in sorted(node_coords.keys()):
            lat, lon = node_coords[nid]
            f.write(f"{lat}, {lon}\n")

    print(f"\n✅ Coordinates saved to '{output_file}'")
    print("Run your 'visualize_map.py' (or 'visualize.py') now to see the new shape!")


if __name__ == "__main__":
    main()
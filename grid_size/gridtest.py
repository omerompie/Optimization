from vinc import v_direct, v_inverse

# YOUR COORDINATES
SCHIPHOL = (52.308056, 4.764167)      # lat, lon
JFK = (40.641766, -73.780968)

# STEP 1: Great Circle Baseline (highway)
distance_AMS_JFK, gc_bearing = v_direct(SCHIPHOL, JFK)
print(f"AMS-JFK: {distance_AMS_JFK/1000:.0f}km, bearing {gc_bearing:.1f}°")

# STEP 2: Generate RING 1 (300km from AMS)
ring1_dist = 300000  # meters
ring1_angles = [-15, -10, -5, 0, 5, 10, 15]  # ±15° deviations

ring1_points = []
print("\nRING 1 (300km):")
for angle_dev in ring1_angles:
    heading = gc_bearing + angle_dev
    lat, lon = v_inverse(SCHIPHOL[0], SCHIPHOL[1], heading, ring1_dist)
    ring1_points.append((lat, lon))
    print(f"  {angle_dev:+3d}° → ({lat:.3f}, {lon:.3f})")

# STEP 3: Generate RING 2 (600km from AMS)
ring2_dist = 600000
ring2_points = []
print("\nRING 2 (600km):")
for angle_dev in ring1_angles:  # same angles
    heading = gc_bearing + angle_dev
    lat, lon = v_inverse(SCHIPHOL[0], SCHIPHOL[1], heading, ring2_dist)
    ring2_points.append((lat, lon))
    print(f"  {angle_dev:+3d}° → ({lat:.3f}, {lon:.3f})")

# STEP 4: PLOT IT (copy-paste to Jupyter/Matplotlib)
import matplotlib.pyplot as plt
import numpy as np

# All points
points = [SCHIPHOL] + ring1_points + ring2_points + [JFK]
lats = [p[0] for p in points]
lons = [p[1] for p in points]
labels = ['AMS', 'R1_-15°','R1_-10°','R1_-5°','R1_0°','R1_+5°','R1_+10°','R1_+15°',
          'R2_-15°','R2_-10°','R2_-5°','R2_0°','R2_+5°','R2_+10°','R2_+15°','JFK']

plt.figure(figsize=(10,8))
plt.scatter(lons, lats, c='red', s=100)
for i, label in enumerate(labels):
    plt.annotate(label, (lons[i], lats[i]), xytext=(5,5), textcoords='offset points')
plt.plot([SCHIPHOL[1], JFK[1]], [SCHIPHOL[0], JFK[0]], 'b--', label='Great Circle Highway')
plt.xlabel('Longitude'); plt.ylabel('Latitude')
plt.title('3-Ring Toy Grid: AMS → JFK')
plt.grid(True); plt.legend()
plt.show()


from vinc import v_direct

def edge_distance(nodeA, nodeB, coords):
    # coords is a list: [AMS] + ring1_points + ring2_points
    lat1, lon1 = coords[nodeA]
    lat2, lon2 = coords[nodeB]
    d_m, _ = v_direct((lat1, lon1), (lat2, lon2))
    return d_m  # meters


coords = [SCHIPHOL] + ring1_points + ring2_points + [JFK]

# indexes:
# 0  = AMS
# 1–7  = R1_-15 ... R1_+15
# 8–14 = R2_-15 ... R2_+15
# 15 = JFK

routes = {
    "A": [0, 2, 9, 15],    # AMS → R1_-10° → R2_-10° → JFK
    "B": [0, 4, 11, 15],   # AMS → R1_0°  → R2_0°  → JFK
    "C": [0, 6, 13, 15],   # AMS → R1_+10° → R2_+10° → JFK
}

for name, path in routes.items():
    total = 0
    for i in range(len(path)-1):
        d = edge_distance(path[i], path[i+1], coords)
        total += d
    print(f"Route {name} total distance: {total/1000:.1f} km")

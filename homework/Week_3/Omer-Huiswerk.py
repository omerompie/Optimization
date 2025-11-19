# -*- coding: utf-8 -*-
"""

@ Adaptaed to Python by Alejandro Murrieta-Mendoza

INTRODUCTION:

    THIS IS A TOY PROBLEM DESIGNED FOR YOUR BRAIN.
    TO DEVELOP CREATIVIY AND CRITICAL THINKING.
    PLEASE TRY NOT TO USE AI. IT DEFEATS THE PURPOSE.


In this workshop, you will optimize a flight trajectory using two different
methods. First, analyze the following code for three different trajectories
(left, middle and right). You can also find distance factors, which are
randomized factors that simulates the effect of the wind on the aircraft's speed.
For example, a distance factor of 1.1 would mean that the distance between
point A and point B is increased by 10%, simulating headwind.
A distance factor of 0.9 simulates tailwinds thus the distance is reduced.


This is your DATA (See Figure 1 in DLO to understand this):
    ALL IN DEGREES
lon_lef = [4.76, 4.87, 3.69, 2.36, 2.74, 2.88, 2.69]
lat_lef = [52.30, 52.05, 50.31, 48.41, 46.09, 43.82, 41.88]
lon_mid = [4.76, 4.79, 3.62, 2.287, 2.67, 2.81, 2.69]
lat_mid = [52.30, 52.04, 50.30, 48.39, 46.09, 43.81, 41.88]
lon_rig = [4.76, 4.72, 3.55, 2.21, 2.59, 2.73, 2.69]
lat_rig = [52.30, 52.04, 50.30, 48.39, 46.09, 43.81, 41.88]

    NO UNITS (Wind Factor)
midDF = [1.1, 1.2, 1, 0.96, 0.99, 0.98, 0.95]
lefDF = [1.1, 0.95, 0.96, 0.99, 1.2, 1.2, 0.95]
rigDF = [1.1, 0.9, 0.97, 1, 1.2, 1.2, 0.95]

lon_mid and lat_mid are the coordinates for the reference trajectory
lon_rig and lat rig are the coordinates for the trajectory at the right
midDF, leftDF, and rig DF are the distance factores (wind emulation)


"""

"""
1.- Place the vinc.py file (wotkshop 1) in the same directory as this file. 
Then load the v_direct and v_inverse functions. 
"""

"""

2.- Download the function vinc.py from brightspace and place it in the SAME
directory as where this file is placed. You also need to import file from
function. What do yo think this file is doing?. Feel free to open it
and to take a look at it. 



3.- Observe how the function is used    """
# boston = (lat,long) - Longitudes west of Greenwish are negative.

from vinc import v_direct, v_inverse
import matplotlib.pyplot as plt

# boston = (42.3541165, -71.0693514)
# newyork = (40.7791472, -73.9680804)
# x = v_direct(boston, newyork)  # In m and degrees
# print("The distance between Boston and New York is: " + str(x[0]) + " m.")
# print("The initial azimuth  between Boston and New York is: " + str(x[1]) + " degrees")

"""
3.- Find the coordinates of Schipol, Los Angeles (LAX), and Narita (NAA) in degrees. 
"""
ams_lat = 52.374
ams_lon = 4.88969
AMS = (ams_lat, ams_lon) # respect the order

naa_lat = 35.765
naa_lon = 140.3860
NAA = (naa_lat, naa_lon)

lalaland_lat = 34.05
lalaland_lon = -118.24
LAX = (lalaland_lat, lalaland_lon)
"""
4.- Use the imported function v_direct to find the distances between AMS - LAX, 
     AMS - NAA, and LAX-NAA in meters, kilometers and nautical miles. 
     Print the results
"""
# x = v_direct(AMS, LAX)  # In m and degrees
# x_1 = v_direct(AMS, NAA)
# x_2 = v_direct(LAX, NAA)
#
# print(f"The distance between Amsterdam and LAX is: {x[0]:.2f} m.")
# print(f"The distance between Amsterdam and NAA is: {x_1[0]:.2f} m.")
# print(f"The distance between LAX and NAA is: {x_2[0]:.2f} m.")
#
# print(f"The initial azimuth  between Amsterdam and LAX is: {x[1]:.2f} degrees")
# print(f"The initial azimuth  between Amsterdam and NAA is: {x_1[1]:.2f} degrees")
# print(f"The initial azimuth  between LAX and NAA is: {x_2[1]:.2f} degrees")

"""

5.- Using the imported functions. Place 4 waypoints located 150 nautical miles
    West, East, North, and South from Schiphol. Plot the waypoints. 
"""
# CODE

distance = 150 * 1852


def placewaypoints(AMS, distance):
    north_lat, north_lon = v_inverse(lat1=AMS[0], lon1=AMS[1], az12=0, s=distance)
    south_lat, south_lon = v_inverse(lat1=AMS[0], lon1=AMS[1], az12=180, s=distance)
    east_lat, east_lon = v_inverse(lat1=AMS[0], lon1=AMS[1], az12=90, s=distance)
    west_lat, west_lon = v_inverse(lat1=AMS[0], lon1=AMS[1], az12=270, s=distance)
    north = (north_lat, north_lon)
    south = (south_lat, south_lon)
    east = (east_lat, east_lon)
    west = (west_lat, west_lon)
    return north, south, east, west


def plot_waypoints(AMS, points):
    # We combine AMS (center) with the points passed in
    all_points = [AMS] + list(points)

    lats = [p[0] for p in all_points]
    lons = [p[1] for p in all_points]

    # 'ro' = Red Dots.
    plt.plot(lons, lats, 'ro')
    # Force aspect ratio so it doesn't look squashed
    plt.axis('equal')
    plt.show()

print(placewaypoints(AMS, distance))
plot_waypoints(AMS, (placewaypoints(AMS, distance)))

"""
6.- Load the data shown in the introduction  (the 9 lists above)
"""

#This is your DATA (See Figure 1 in DLO to understand this):
#    ALL IN DEGREES
lon_lef = [4.76, 4.87, 3.69, 2.36, 2.74, 2.88, 2.69]
lat_lef = [52.30, 52.05, 50.31, 48.41, 46.09, 43.82, 41.88]
lon_mid = [4.76, 4.79, 3.62, 2.287, 2.67, 2.81, 2.69]
lat_mid = [52.30, 52.04, 50.30, 48.39, 46.09, 43.81, 41.88]
lon_rig = [4.76, 4.72, 3.55, 2.21, 2.59, 2.73, 2.69]
lat_rig = [52.30, 52.04, 50.30, 48.39, 46.09, 43.81, 41.88]

#    NO UNITS (Wind Factor)
midDF = [1.1, 1.2, 1, 0.96, 0.99, 0.98, 0.95]
lefDF = [1.1, 0.95, 0.96, 0.99, 1.2, 1.2, 0.95]
rigDF = [1.1, 0.9, 0.97, 1, 1.2, 1.2, 0.95]


# lon_mid and lat_mid are the coordinates for the reference trajectory
# lon_rig and lat rig are the coordinates for the trajectory at the right
# midDF, leftDF, and rig DF are the distance factores (wind emulation)


"""
7.- Using a For loop, calculate the total distance, including the distance
    factors, for each one of the trajectories. Use the average of distance
    factors between point A and point B. Example, if the aircraft is at the
    first waypoint of the middle trajectory, and it flies to the second
    waypoint of the middle trajectory, the distance factor to be used
    would be (1.1+1.2)/2 (see data above). 
    Which one is the shortest trajectory?
    Print the result in km and in nautical miles

"""
# CODE


"""
8.- In this step, a simple greedy optimization algorithm should be applied.
    Try to optimize your distance by calculating at each waypoint, the
    shortest path. The aircraft should calculate the costs of going to either
    one of the options (left, middle or right), and fly to the least expensive.
    This process should be repeated until the aircraft reaches the last waypoint.
    Show this trajectory on a map. You can move along mid, left or right. 
"""
# CODE

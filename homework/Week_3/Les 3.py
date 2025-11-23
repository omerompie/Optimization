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
lon_rig and lat rit are the coordinates for the trajectory at the right
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

from vinc import v_direct

from vinc import v_inverse

boston = (42.3541165, -71.0693514)
newyork = (40.7791472, -73.9680804)
x = v_direct(boston, newyork)  # In m and degrees
print("The distance between Boston and New York is: " + str(int(x[0])) + " m.")
print("The initial azimuth  between Boston and New York is: " + str(int(x[1])) + " degrees")

"""
3.- Find the coordinates of Schipol, Los Angeles (LAX), and Narita (NAA) in degrees. 
"""
ams_lat = 52.308056
ams_lon = 4.764167
AMS = (ams_lat, ams_lon)  # respect the order

naa_lat = 35.7647
naa_lon = 140.3860
NAA = (naa_lat, naa_lon)

lalaland_lat = 33.94250
lalaland_lon = -118.40800
LAX = (lalaland_lat, lalaland_lon)

x = v_direct(AMS, LAX)
print("The distance between Amsterdam and Los Angeles is: " + str(int((x[0]/1000))) + " km or " + str(int((x[0]/1000/1.852))) + ' NM.')
print("The initial azimuth  between Amsterdam and Los Angeles is: " + str(int(x[1])) + " degrees")

x2 = v_direct(AMS, NAA)

print('')

print("The distance between Amsterdam and Tokyo is: " + str(int((x2[0]/1000))) + " km or " + str(int((x2[0]/1000/1.852))) + ' NM.')
print("The initial azimuth  between Amsterdam and Tokyo is: " + str(int(x2[1])) + " degrees")

x3 = v_direct(NAA, LAX)

print('')

print("The distance between Los Angeles and Tokyo is: " + str(int((x3[0]/1000))) + " km or " + str(int((x3[0]/1000/1.852))) + ' NM.' )
print("The initial azimuth  between Los Angeles and Tokyo is: " + str(int(x3[1])) + " degrees")

"""
4.- Use the imported function v_direct to find the distances between AMS - LAX, 
     AMS - NAA, and LAX-NAA in meters, kilometers and nautical miles. 
     Print the results
"""
"""

5.- Using the imported functions. Place 4 waypoints located 150 nautical miles
    West, East, North, and South from Schiphol. Plot the waypoints. 
"""

w1lat, w1lon = v_inverse(ams_lat, ams_lon , 0, (150*1.852)*1000)
w2lat, w2lon = v_inverse(ams_lat, ams_lon , 180, (150*1.852)*1000)
w3lat, w3lon = v_inverse(ams_lat, ams_lon , 90, (150*1.852)*1000)
w4lat, w4lon = v_inverse(ams_lat, ams_lon , 270, (150*1.852)*1000)
w1 = (w1lat, w1lon)
w2 = (w2lat, w2lon)
w3 = (w3lat, w3lon)
w4 = (w4lat, w4lon)

print(w1, w2, w3, w4)

"""
6.- Load the data shown in the introduction  (the 9 lists above)
"""
lon_lef = [4.76, 4.87, 3.69, 2.36, 2.74, 2.88, 2.69]
lat_lef = [52.30, 52.05, 50.31, 48.41, 46.09, 43.82, 41.88]
lon_mid = [4.76, 4.79, 3.62, 2.287, 2.67, 2.81, 2.69]
lat_mid = [52.30, 52.04, 50.30, 48.39, 46.09, 43.81, 41.88]
lon_rig = [4.76, 4.72, 3.55, 2.21, 2.59, 2.73, 2.69]
lat_rig = [52.30, 52.04, 50.30, 48.39, 46.09, 43.81, 41.88]

    #NO UNITS (Wind Factor)
midDF = [1.1, 1.2, 1, 0.96, 0.99, 0.98, 0.95]
lefDF = [1.1, 0.95, 0.96, 0.99, 1.2, 1.2, 0.95]
rigDF = [1.1, 0.9, 0.97, 1, 1.2, 1.2, 0.95]

#lon_mid and lat_mid are the coordinates for the reference trajectory
#lon_rig and lat rit are the coordinates for the trajectory at the right
#midDF, leftDF, and rig DF are the distance factores (wind emulation)
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
def total_distance(lat, lon, DF):
    total_km = 0

    for i in range(len(lat) - 1):
        dist, azimuth_r = v_direct((lat[i], lon[i]), (lat[i+1], lon[i+1]))

        # Gemiddelde distance factor
        DF_avg = (DF[i] + DF[i+1]) / 2

        total_km += (dist * DF_avg)/1000

    return total_km


#Nu de trajectories berekenen
d_mid = total_distance(lat_mid, lon_mid, midDF)
d_lef = total_distance(lat_lef, lon_lef, lefDF)
d_rig = total_distance(lat_rig, lon_rig, rigDF)

print('De afstand van het middel traject is ' + str(int(d_mid)) + ' kilometer, dat van het linker traject is ' + str(int(d_lef)) + ' kilometer en dat van het rechter traject is ' + str(int(d_rig)) + ' kilometer.')




"""
8.- In this step, a simple greedy optimization algorithm should be applied.
    Try to optimize your distance by calculating at each waypoint, the
    shortest path. The aircraft should calculate the costs of going to either
    one of the options (left, middle or right), and fly to the least expensive.
    This process should be repeated until the aircraft reaches the last waypoint.
    Show this trajectory on a map. You can move along mid, left or right. 
"""
def greedy_trajectory(lat_mid, lon_mid,
                      lat_lef, lon_lef,
                      lat_rig, lon_rig,
                      midDF, lefDF, rigDF):


    current = "mid"
    trajectory = [current]
    total_km = 0


    for i in range(len(lat_mid) - 1):

        # Coords van huidige positie op index i
        if current == "mid":
            lat0, lon0 = lat_mid[i], lon_mid[i]
        elif current == "left":
            lat0, lon0 = lat_lef[i], lon_lef[i]
        else:
            lat0, lon0 = lat_rig[i], lon_rig[i]


        distances = {}


        distL, _ = v_direct((lat0, lon0), (lat_lef[i+1], lon_lef[i+1]))
        DF_L = (get_df(current, i, lefDF, midDF, rigDF) + lefDF[i+1]) / 2
        distances["left"] = distL * DF_L


        distM, _ = v_direct((lat0, lon0), (lat_mid[i+1], lon_mid[i+1]))
        DF_M = (get_df(current, i, lefDF, midDF, rigDF) + midDF[i+1]) / 2
        distances["mid"] = distM * DF_M


        distR, _ = v_direct((lat0, lon0), (lat_rig[i+1], lon_rig[i+1]))
        DF_R = (get_df(current, i, lefDF, midDF, rigDF) + rigDF[i+1]) / 2
        distances["right"] = distR * DF_R


        next_choice = min(distances, key=distances.get)


        total_km += (distances[next_choice])/1000


        current = next_choice
        trajectory.append(current)

    return trajectory, total_km


def get_df(track, i, lefDF, midDF, rigDF):
    if track == "mid":
        return midDF[i]
    if track == "left":
        return lefDF[i]
    return rigDF[i]



trajectory, greedy_dist = greedy_trajectory(
    lat_mid, lon_mid,
    lat_lef, lon_lef,
    lat_rig, lon_rig,
    midDF, lefDF, rigDF
)

print("Greedy trajectory:", trajectory)
print('En deze route geeft een totale afstand van ' + str(int(greedy_dist)) + ' kilometers.')

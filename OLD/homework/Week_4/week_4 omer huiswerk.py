#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This worksop aims to help you to
1) use vicenty's functions to compute distance and azimuth (refresh)
3) understand how to create a waypoint given a coord, distance, and azimuth.
4) create a geodesic traectory given just two waypoints
5) how to plot your waypoints in an external website .

All this could help you to create waypoints in your assignment

INSTRUCTIONS:
    1.- Place the file "vinc.py" in the same folder as you have placed this file
    2.- Solve it
"""

from vinc import v_direct, v_inverse # Import an amazing library.

# Be rsue that you have placed this file in the same folder


# =============================================================================
# # 1.- Create and print 40 equidistant waypoints from LAX to Schiphol.
# # Print them and plot them in https://www.mapcustomizer.com/
# # mapcustomizer format: lat,lon
# # Extra challenge: Include the azimuth in a vector.
# # Extra challenge: Place them in a .txt file as the instructions here:
# # https://www.w3schools.com/python/python_file_write.asp
# =============================================================================
print("")
print("EXERCISE 1")
print("")
# Hint: First compute the distance between LAX and AMS and divide it by 40

AMS = (52.308056, 4.764167)
LAX = (33.9424964,-118.4080486)

distance, az = v_direct(LAX, AMS)
print(f"distance between AMS and LAX is: {distance:.2f} meters\nazimuth is: {az:.2f} degrees ")

step_size = distance / 40

All_waypoints = []
print(az)

for i in range(1, 41):
    current_total_distance = step_size * i
    new_point = v_inverse(LAX[0], LAX[1], az, current_total_distance)
    All_waypoints.append(new_point)

with open('waypoints.txt', 'w') as f:
    # write elements of list
    for point in All_waypoints:
        f.write(f"{point[0]}, {point[1]}\n")

#http://dwtkns.com/pointplotter/
with open('waypoints_reversed.txt', 'w') as f:
    # write elements of list
    for point in All_waypoints:
        f.write(f"{point[1]}, {point[0]}\n")



print(All_waypoints)


print("")
print("EXERCISE 2 ENDS")
print("")

"""
It is true that mapcustomizer is not the best to be used to plot a graph. 
However, you can do some research online for different tools that can help you
http://dwtkns.com/pointplotter/ is a bit better. 
http://www.hamstermap.com/quickmap.php uses google maps

Another Tutorial on how to create files:
    https://www.guru99.com/reading-and-writing-files-in-python.html

"""

##============================================================================
## 2.- Giving the graph belw,
## Develop an algorithm that identifies and prints all the possible combinations
## of trajectories. Save ALL the options in a list of lists.
##============================================================================
graphs = [[0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0]]
# This is the adjacent matrix

# The Matrix
graphs = [[0, 1, 1, 1, 0, 0, 0, 0],
          [0, 0, 0, 0, 1, 1, 0, 0],
          [0, 0, 0, 0, 0, 1, 0, 0],
          [0, 0, 0, 0, 0, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0]]


def get_neighbors(node_index, matrix):
    neighbors = []
    # ITERATE through the row for 'node_index'
    # IF the value is 1, append the column index to 'neighbors'
    # TODO: Write this loop
    return neighbors


def find_all_paths(current_node, destination, path, all_paths):
    # 1. Update the path with the current node
    path = path + [current_node]

    # 2. Base Case: Did we reach the end?
    if current_node == destination:
        all_paths.append(path)
        return

    # 3. Recursive Step: Where can we go from here?
    # TODO: Call get_neighbors() for the current node
    # TODO: Loop through those neighbors
    # TODO: Inside the loop, call find_all_paths(...) for the neighbor

    return all_paths


# Execution
master_list = []
find_all_paths(0, 7, [], master_list)
print("All Trajectories found:")
for p in master_list:
    print(p)



##============================================================================
## 3.- Using the same data as in workshop 2, Develop an algorithm
## that makes a random decision on what waypoint, t should follow next.
## Print the final distance. Print the real and the wind one
##============================================================================


##============================================================================
## 4.- Using the same data as in workshop 2, Develop a greedy algorithm
## Add an heuristic to the cost. At each waypoint, compute and add  the remaining distance
## distance from your waypoin to the end point. Take wind into account. Compare
## the normal greedy and the greedy + heuristic.
##============================================================================


###### END OF WORKSHOP 3 PART 1  ######

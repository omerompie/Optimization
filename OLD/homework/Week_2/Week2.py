import math
from OLD.homework.Week_2.airport_data import airport_data

#General Variables
V = 10
EDGES = [(0, 1), (0, 2), (0, 3), (0, 8), (1, 4), (1, 5), (2, 5), (3, 5), (3, 7), (4, 9), (5, 9), (7, 9), (8, 9)]

#-------------------------------------Q1--------------------------------------------------------------

def create_adjacency_matrix(V, edges):
    # Initialize an empty V x V matrix with all zeros
    M = []
    for i in range(V):
        M.append([0] * V)

    # Populate the matrix based on the edges
    for u, v in edges:
        M[u][v] = 1

    return M

matrix = create_adjacency_matrix(V, EDGES)
for row in matrix:
    print(row)


#-------------------------------------Q5--------------------------------------------------------------

#Adjactent list - better

from collections import defaultdict

D = defaultdict(list)

for u, v in EDGES:
    D[u].append(v)


"""
node_id = 0
name = airport_data[node_id]['name']
location = airport_data[node_id]['coords']
"""

#Check if the route is possible
def check_route_possible(route):
    for i in range(len(route)-1):
        if route[i+1] not in D[route[i]]:
            return False
    return True

def haversine(route):
    r = 6371
    distance = 0
    d = 0

    for i in range(len(route)-1):
        u = airport_data[route[i]]['coords']
        v = airport_data[route[i+1]]['coords']

        lat1 = u[0]
        lon1 = u[1]
        lat2 = v[0]
        lon2 = v[1]

        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance += r * c #in meters
    return distance


# ID of airports
"""
list of airports
0: AMS (Amsterdam)

1: CDG (Paris)

2: FRA (Frankfurt)

3: PRG (Prague)

4: TRN (Turin)

5: MXP (Milan)

7: VCE (Venice)

8: IST (Istanbul)

9: FCO (Rome)

"""

# AMS - FRA - MXP - FCO
route_1 = [0 , 2, 5, 9]

#PRG. Now you want to visit PRG - VCE - FCO
route_2 = [3, 7, 9]

route = route_1


if check_route_possible(route) == True:
    print(f"Route is possible. Distance: {haversine(route):.2f} km")
else:
    print("Route is not possible.")



#----------------------extra-----------------------------------
"""

def dfs_recursive(node):
    print(node)
    for nei_node in D[node]:
        if nei_node not in seen:
            seen.add(nei_node)
            dfs_recursive(nei_node)

source = 0
seen = set()
seen.add(source)


def find_all_routes(start, end, max_len):
    routes = []

    def dfs(path):
        current = path[-1]

        # If destination reached, store route
        if current == end:
            routes.append(path.copy())
            return

        # Stop if too long
        if len(path) > max_len:
            return

        # Explore neighbors
        for nei in D[current]:
            if nei not in path:  # avoid cycles
                dfs(path + [nei])

    dfs([start])
    return routes


def shortest_route(start, end, max_len):
    all_routes = find_all_routes(start, end, max_len)

    if not all_routes:
        return None, None  # no valid path

    # Compute distances
    distances = [(route, haversine(route)) for route in all_routes]

    # Choose minimum-distance route
    best_route, best_distance = min(distances, key=lambda x: x[1])

    return best_route, best_distance

best_route, best_distance = shortest_route(0, 9, max_len=5)

print("Shortest route:", best_route)
print(f"Distance: {best_distance:.2f} km")

"""
POPULATION_SIZE = 20 #voor nu klein zodat we snel antwoord krijgen, kan opgeschaald worden
MAX_ITERATIONS = 100 #zelfde als voor pupulation: klein voor nu
LIMIT = 15 #zelfde als voor population: klein voor nu

from main_tryout import build_graph

nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()

Node_coordinates = node_coords

NP = POPULATION_SIZE
Numiter = MAX_ITERATIONS
Limit = LIMIT

start_node = Node_coordinates[0] #Schiphol
end_node = Node_coordinates[610] #JFK






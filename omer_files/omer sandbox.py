import math

graph = {
    0: [(1, 0.0), (2, 0.0)],
    1: [(3, 0.0), (4, 0.0)],
    2: [(4, 0.0)],
    3: [],
    4: []
}

current = 1
edges = graph.get(current, [])
print(edges)

neighbors = [n for n, _ in edges]
print(neighbors)

list_1 = [1, 2, 3, 6
          ]
print(list_1[-1])

u = 5
v = 10
speed_ms = math.sqrt(u ** 2 + v ** 2)

# Un test de l'algorithme de Dijkstra
# https://www.delftstack.com/fr/howto/python/dijkstra-algorithm-python/

import sys

class Graph():

    def __init__(self, vertx):
        self.dim = vertx
        self.graph = [[0 for column in range(vertx)]
                      for row in range(vertx)]

    def pSol(self, dist):
        print("Distance of vertex from source")
        for node in range(self.dim):
            print(node, "t", dist[node])

    def node_with_min_distance(self, dist, visited):
        min = sys.maxsize
        for v in range(self.dim):
            if dist[v] < min and visited[v] == False:
                min = dist[v]
                min_index = v
        return min_index

    def dijk(self, source):

        distance = [sys.maxsize] * self.dim
        distance[source] = 0
        # initialize list of visited nodes
        visited = [False] * self.dim

        for cout in range(self.dim):
            print("Visited", visited)
            u = self.node_with_min_distance(distance, visited)
            visited[u] = True
            print(f"ligne u vaut : {u}")
            for v in range(self.dim):
                print(f"test pour u {u} du noeud v {v} ")
                print(f"{self.graph[u][v]}, {visited[u]}, {distance[u] + self.graph[u][v]}")
                if self.graph[u][v] > 0 \
                        and visited[v] == False \
                        and distance[v] > distance[u] + self.graph[u][v]:

                    distance[v] = distance[u] + self.graph[u][v]
        self.pSol(distance)


f = Graph(9)
f.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
           [4, 0, 8, 0, 0, 0, 0, 11, 0],
           [0, 8, 0, 7, 0, 4, 0, 0, 2],
           [0, 0, 7, 0, 9, 14, 0, 0, 0],
           [0, 0, 0, 9, 0, 10, 0, 0, 0],
           [0, 0, 4, 14, 10, 0, 2, 0, 0],
           [0, 0, 0, 0, 0, 2, 0, 1, 6],
           [8, 11, 0, 0, 0, 0, 1, 0, 7],
           [0, 0, 2, 0, 0, 0, 6, 7, 0]
           ]

f.dijk(0)

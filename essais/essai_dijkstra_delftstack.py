# Un test de l'algorithme de Dijkstra
# https://www.delftstack.com/fr/howto/python/dijkstra-algorithm-python/

import sys

class Graph():

    def __init__(self, vertx):
        self.dim = vertx
        self.graph = [[0 for column in range(vertx)]
                      for row in range(vertx)]
        self.parent = [None] * self.dim

    def pSol(self, dist):
        print("Distance of vertex from source")
        print(dist)
        # for node in range(self.dim):
        #     print(node, "t", dist[node])
        print(self.parent)

    def node_with_min_distance(self, dist, visited):
        min = sys.maxsize
        for v in range(self.dim):
            if dist[v] < min and not visited[v]:
                min = dist[v]
                min_index = v
        return min_index

    def dijk(self, source):

        distance = [sys.maxsize] * self.dim
        distance[source] = 0
        # initialize list of visited nodes
        visited = [False] * self.dim

        for _ in range(self.dim):
            print("Distances", distance)
            print("Visited", visited)
            print()
            u = self.node_with_min_distance(distance, visited)
            print("Noeud non visité avec la plus petite distance : ", u, ". On travaille maintenant sur ce noeud.")

            visited[u] = True
            print(f"Le noeud {u} est marqué comme visité.")
            print("Visited", visited)
            print(f"ligne pour u = {u} vaut : {self.graph[u]}")

            for v in range(self.dim):
                print(f"Noeud v {v} , val = {self.graph[u][v]} .", end = '')
                if not visited[v]:
                    if self.graph[u][v] > 0:
                        print(f"Valeur possible ? Est-ce que cela vaut le coup d'aller de {u} à {v} ?",
                              f"Alors que nous avons déjà une solution pour aller en {v} par une autre voie ? ")
                        print(f"Le cout actuel pour {v} : {distance[v]}",
                              f"Cout actuel pour arriver sur {u} : {distance[u]}, "
                              f"Pour passer de {u} à {v} : {self.graph[u][v]} ", end = '')
                        if distance[v] > distance[u] + self.graph[u][v]:
                            print(f"Valeur retenue ! {distance[u] + self.graph[u][v]}")
                            distance[v] = distance[u] + self.graph[u][v]
                            self.parent[v] = u
                            print(f"distance : {distance}")
                        else:
                            print("Trajet non intéressant")
                    else:
                        print("Valeur nulle")
                else:
                    print("déjà visité")

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

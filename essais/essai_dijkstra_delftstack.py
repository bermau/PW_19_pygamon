# Un test de l'algorithme de Dijkstra
# Au départ j'ai utilisé
# https://www.delftstack.com/fr/howto/python/dijkstra-algorithm-python/

import sys

class Graph():

    def __init__(self, vertx):
        self.dim = vertx
        self.graph = [[0 for column in range(self.dim)]
                      for row in range(self.dim)]
        self.distance = [sys.maxsize] * self.dim
        self.parent = [None] * self.dim

    def pSol(self):
        print("Distance of node from source : ")
        print(self.distance)
        print("Parent of last move :")
        print(self.parent)

    def describe_old(self, source_node, dest_node):
        """Return the shortest path between 2 nodes"""
        node = dest_node
        print(f"Pour aller du node {source_node} au node {node}")
        print(f"il faut passer par {self.parent[node]}")
        if self.parent[node] == source_node:
            print("Et vous êtes arrivé.")
        else:
            self.describe(source_node, self.parent[node] )

    def describe(self, source_node, dest_node):
        """Return the shortest path between 2 nodes"""
        node = dest_node
        path = [node]
        print(f"Pour aller du node {source_node} au node {node}")

        while node != source_node:
            path.append(self.parent[node])
            node = self.parent[node]
        path.reverse()
        print(path)
        for point in path:
            print(f"({point})", end = '')
            if point != dest_node:
                print(f" -- {self.graph[point][path[point+1]]} -> ", end='')
            else:
                print(" Cout total : ", self.distance[dest_node])
        return path

    def node_with_min_distance(self, dist, visited):
        min = sys.maxsize
        for v in range(self.dim):
            if dist[v] < min and not visited[v]:
                min = dist[v]
                min_index = v
        return min_index

    def dijk(self, source):
        """Calculates all shortest distances from source to any node"""

        self.distance[source] = 0
        # initialize list of visited nodes
        visited = [False] * self.dim

        for _ in range(self.dim):
            print("Distances", self.distance)
            print("Visited", visited)
            print()
            u = self.node_with_min_distance(self.distance, visited)
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
                        print(f"Le cout actuel pour {v} : {self.distance[v]}",
                              f"Cout actuel pour arriver sur {u} : {self.distance[u]}, "
                              f"Pour passer de {u} à {v} : {self.graph[u][v]} ", end = '')
                        if self.distance[v] > self.distance[u] + self.graph[u][v]:
                            print(f"Valeur retenue ! {self.distance[u] + self.graph[u][v]}")
                            self.distance[v] = self.distance[u] + self.graph[u][v]
                            self.parent[v] = u
                            print(f"distance : {self.distance}")
                        else:
                            print("Trajet non intéressant")
                    else:
                        print("Valeur nulle")
                else:
                    print("déjà visité")
        self.pSol()


f = Graph(9)
# Explication : chaque ligne indique le cout pour passer d'une ligne à la colonne.
# Un zéro indique qu'on ne peut pas passer.

# Depuis le noeud 2, on peut passer sur le noeud 3 pour un cout de 7
# Depuis le noeud 2, on ne peut pas passer sur les noeuds 0, 4, 6, 7
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

f.describe(0,8)
# for n in range(0, f.dim):
#     f.describe(0, n)

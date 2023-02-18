# Un test de l'algorithme de Dijkstra
# Adaptation à un damier

import sys
from pprint import pprint

class Point:
    def __init__(self, x, y ):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point ({self.x}, {self.y})"

    def top(self):
        return Point(self.x-1, self.y)

    def bottom(self):
        return Point(self.x + 1, self.y)

    def left(self):
        return Point(self.x, self.y-1)

    def right(self):
        return Point(self.x, self.y+1)

MAX = 9999

class Graph():

    def __init__(self, x, y ):
        self.row_nb = x
        self.col_nb = y
        self.graph = [[0 for _ in range(y)] for row in range(x)]
        self.distance = [[MAX for _ in range(y)] for row in range(x)]
        self.visited = [[False for _ in range(y)] for row in range(x)]
        self.parent = [[None for _ in range(y)] for row in range(x)]

    def print_visited(self):
        print('. . 0 1 2 3 4 5 6 7 8')
        for i, row in enumerate(self.visited):
            print("{:>2}".format(str(i)), end='') #  "{:>2}"
            for r in row:
                if r == True:
                    print (' X', end = '')
                else:
                    print("  ", end = '')
            print()

    def print_distances(self):
        print('.  . 0  1  2  3  4  5  6  7  8')
        for i, row in enumerate(self.distance):
            print("{:>3}".format(str(i)), end='') #  "{:>2}"
            for r in row:
                if r == MAX :
                    print ('  /', end = '')
                else:
                    print("{:>3}".format(str(r)), end='')
            print()

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

    def node_with_min_distance(self, p):
        """Doit retourner un point et sa direction
        Ce point est non déjà décrit. et son accès est le plus faible autres frères."""
        min = MAX
        best_index = None
        best_direction = None
        print('Point en entrée de sélection', p)
        neighbors = [[p.top(), 'T'], [p.bottom(), 'B'], [p.left(), 'L'], [p.right(), 'R']]
        for v, dir in neighbors:
                if self.distance[v.x][v.y] < min and not self.visited[v.x][v.y]:
                    min = self.distance[v.x][v.y]
                    best_index = v
                    best_direction = dir

        return best_index, best_direction

    def dijkstra(self, source):
        """Calculates all shortest distances from source to any node"""
        self.distance[source.x][source.y] = 0
        self.visited[source.x][source.y] = True

        # initialize list of self.visited nodes
        # self.visited = [False] * self.dim
        u = source
        for _ in range(20):
            self.print_visited()
            self.print_distances()

            print()
            u, dir = self.node_with_min_distance(u)
            print("Noeud non visité avec la plus petite distance : ", u, ". On travaille maintenant sur ce noeud.")

            self.visited[u.x][u.y] = True
            print(f"Le noeud {u} est marqué comme visité.")
            print("Visited", self.visited)
            print(f"ligne pour u = {u} vaut : {self.graph[u]}")

            for v in range(30):
                print(f"Noeud v {v} , val = {self.graph[u][v]} .", end = '')
                if not self.visited[v]:
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
            self.print_distances()
        self.pSol()


f = Graph(6, 9)
# Explication : chaque ligne indique le cout pour passer d'une ligne à la colonne.
# Un zéro indique qu'on ne peut pas passer.

# Depuis le noeud 2, on peut passer sur le noeud 3 pour un cout de 7
# Depuis le noeud 2, on ne peut pas passer sur les noeuds 0, 4, 6, 7
f.graph = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 1, 0, 0, 1, 0, 1],
           [1, 1, 0, 1, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 1, 0, 0, 1],
           [1, 0, 0, 1, 0, 1, 0, 0, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1],
           ]

START = Point(1, 1)
DEST = Point(4, 6)
f.dijkstra(START)
#
# f.describe(0,8)
# for n in range(0, f.dim):
#     f.describe(0, n)

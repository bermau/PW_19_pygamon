# Une implémentation de Dijkstra
# origine :
# https://www.geeksforgeeks.org/python/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/

from pprint import pprint

MAX = 99999


class Graph:
    def __init__(self, vertices):

        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
        self.dist = [999999 for column in range(vertices)]
        self.predecessor = [-1 for column in range(vertices)] # Une ligne contenant pour
        # le node prédécesseur pour chaque node
        self.calc = []  # un tableau récapitulatif.
        self.src_node = None
        self.dst_node = None


    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.V):
            print(node, "\t\t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
        """Renvoie le node non exploré qui a le plus court chemin dans la liste des nodes"""

        # Initialize minimum distance for next node
        min = MAX

        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):
        self.src_node = src

        dist = [MAX] * self.V
        dist[src] = 0
        sptSet = [False] * self.V  # Similaire ligne basse du tableau. indique qu'un nœud a été entièrement exploré.
        tableau = {}
        for _ in range(self.V):  #

            # Pick the minimum distance vertex from the set of vertices not yet processed.
            # u is equal to src in first iteration
            u = self.minDistance(dist, sptSet)
            print(f"étude du point {u} . Porter ce point à gauche")

            # Put the minimum distance vertex in the shortest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices of the picked vertex only if the current
            # distance is greater than new distance and the vertex in not in the shortest path tree
            for v in range(self.V):
                nv_cout = dist[u] + self.graph[u][v]
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > nv_cout:
                    dist[v] = nv_cout
                    self.predecessor[v] = u

            self.calc.append((u, dist.copy()))
            self.calc.append((u, sptSet.copy()))
            self.calc.append((v, "-" * self.V))

        self.printSolution(dist)

        return dist

    def detailed_path_to(self, node):
        """Retourne une liste de [noeud, cout_cumulé]
        """
        self.dst_node = node
        path = []
        while node != self.src_node:
            path.append((node, self.dist[node]))
            node = self.predecessor[node]
        path.append((self.src_node, 0))
        path.reverse()
        return path

    def print_detailed_path_to(self, node):
        """Afficher une liste de [noeud, cout_cumulé] bien présentée, avec le coût total
        """

        self.dst_node = node
        path = []
        while node != self.src_node:
            path.append((node, self.dist[node]))
            node = self.predecessor[node]
        path.append((self.src_node, 0))
        path.reverse()
        print(f"Path from {self.src_node} to {self.dst_node} ")
        print(f"[{self.src_node}]", end='')
        prev_cost = 0
        for node, cumul in path[1:]:
            print(f" +{cumul-prev_cost}-> " , end = '')
            print(f"[{node}]",  end = "")
            prev_cost = cumul
        print()
        print(f"Full cost is {self.dist[self.dst_node]}")

    def path_to(self, node):
        """Retourne une liste de [noeud]
        """
        self.dst_node = node
        path = []
        while node != self.src_node:
            path.append(node)
            node = self.predecessor[node]
        path.append(self.src_node)
        path.reverse()
        return path

# Main
g = Graph(9)
# Ci-dessous, il y a 9 points. La connection entre ces points est donnée par
# une matrice d'adjacence, qui indique les 9 x 9 chemins possibles entre les points.
g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
           [4, 0, 8, 0, 0, 0, 0, 11, 0],
           [0, 8, 0, 7, 0, 4, 0, 0, 2],
           [0, 0, 7, 0, 9, 14, 0, 0, 0],
           [0, 0, 0, 9, 0, 10, 0, 0, 0],
           [0, 0, 4, 14, 10, 0, 2, 0, 0],
           [0, 0, 0, 0, 0, 2, 0, 1, 6],
           [8, 11, 0, 0, 0, 0, 1, 0, 7],
           [0, 0, 2, 0, 0, 0, 6, 7, 0]
           ]

def show_steps(tableau):
    for letter, line in tableau:
        print(letter, "\t", end = '')
        for case in line:
            if case == MAX:
                case = 'Max'
            elif case is True:
                case = 'T'
            elif case is False:
                case = 'F'

            print(case, end = "\t")
        print()

g.dist = g.dijkstra(5)
pprint(g.calc)

show_steps(g.calc)
print(g.detailed_path_to(8))
print(g.path_to(8))
g.print_detailed_path_to(8)
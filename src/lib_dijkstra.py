# Mon implementation d'un algorithme de type Dijkstra. Certainement pas la meilleure.

from random import randint


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point ({self.x}, {self.y})"

    def __repr__(self):
        return f"Point ({self.x}, {self.y})"

    def top(self):
        return Point(self.x - 1, self.y)

    def bottom(self):
        return Point(self.x + 1, self.y)

    def left(self):
        return Point(self.x, self.y - 1)

    def right(self):
        return Point(self.x, self.y + 1)

MAX = 9999

class DijkstraManager:

    def __init__(self, graph):

        self.graph = graph
        self.row_nb = len(graph)
        self.col_nb = len(graph[0])
        self.distance = [[MAX for _ in range(self.col_nb)] for _ in range(self.row_nb)]
        self.visited = [[False for _ in range(self.col_nb)] for _ in range(self.row_nb)]
        self.parent = [[None for _ in range(self.col_nb)] for _ in range(self.row_nb)]

    def print_header(self, n):
        """
        Prints the header of a table with a specified number of columns.

        Args:
            n (int): The number of spaces to print before the first column.

        Returns:
            None

        Example:
            If self.col_nb == 3 and n == 2, this function would print:
            "  .  0  1  2"
        """
        print(' '*(n-1) + '.', end='')
        nb_format = "{: "+str(n)+"d}"
        for i in range(self.col_nb):
            print(nb_format.format(i), end='')
        print()

    def print_visited(self):
        self.print_header(2)
        for i, row in enumerate(self.visited):
            print("{:>2}".format(str(i)), end='')  # "{:>2}"
            for r in row:
                if r:
                    print(' X', end='')
                else:
                    print("  ", end='')
            print()

    def print_distances(self):
        self.print_header(3)
        for i, row in enumerate(self.distance):
            print("{:>3}".format(str(i)), end='')
            for j, r in enumerate(row):
                if r == MAX:
                    if self.graph[i][j] == 1:
                        print("  |", end='')
                    else:
                        print('  ?', end='')
                else:
                    print("{:>3}".format(str(r)), end='')
            print()

    def pSol(self):
        print("**** oSol ****")
        self.print_distances()

    def get_path(self, source_node, dest_node, verbose=False):
        """Return the shortest path between 2 nodes"""
        node = dest_node
        path = [dest_node]

        while node != source_node:
            dir_letter = self.parent[node.x][node.y]
            if dir_letter == 'L':
                next_point = node.right()
            elif dir_letter == 'R':
                next_point = node.left()
            elif dir_letter == 'T':
                next_point = node.bottom()
            elif dir_letter == 'B':
                next_point = node.top()
            else:
                raise ValueError(f"dir = {dir_letter}")
            path.append(next_point)
            node = next_point
        path.reverse()
        if verbose:
            print(f"Pour aller du node {source_node} au node {dest_node}")
            print(f"Path from {source_node} to {dest_node} is : ")
            for point in path:
                print(f"{point}", end='')
                if point != dest_node:
                    print(f" -- 1 -> ", end='')
                else:
                    print("\nTotal cost : ", self.distance[dest_node.x][dest_node.y])
        return path

    def node_with_min_distance(self, p):
        """Doit retourner un point et sa direction
        Ce point est non déjà décrit. et son accès est le plus faible autres frères."""
        verbose = False
        local_min = MAX
        best_index = None
        best_direction = None
        if verbose:
            print('Point en entrée de sélection', p)
        neighbors = [[p, '0'], [p.top(), 'T'], [p.bottom(), 'B'], [p.left(), 'L'], [p.right(), 'R']]
        for v, dir in neighbors:
            if self.distance[v.x][v.y] < local_min and not self.visited[v.x][v.y]:
                local_min = self.distance[v.x][v.y]
                best_index = v
                best_direction = dir

        return best_index, best_direction

    def choose_non_visited_rnd_point(self):
        while True:
            p = Point(randint(1, self.row_nb - 2), randint(1, self.col_nb - 2))
            if not self.visited[p.x][p.y]:
                break
        return p

    def all_points_are_expored(self):
        for i in range(self.row_nb):
            for j in range(self.col_nb):
                if not self.visited[i][j] and self.graph[i][j] == 0:
                    return False
        return True

    def dijkstra(self, source, verbose = 0):
        """Calculates all shortest distances from source to all nodes."""

        self.distance[source.x][source.y] = 0
        self.visited[source.x][source.y] = False
        u = source
        loop_i = 0

        while True:
            loop_i += 1
            for passage_for_a_rnd_point in range(20):
                if verbose >= 2:
                    self.print_visited()
                if verbose >= 1:
                    self.print_distances()

                u, dir = self.node_with_min_distance(u)  # During first execution, return the source point.
                if not u:
                    break
                if verbose:
                    print("Noeud non visité avec la plus petite distance : ", u, ". On travaille maintenant sur ce noeud.")
                self.visited[u.x][u.y] = True
                if verbose:
                    print(f"Le noeud {u} est marqué comme visité.")
                self.print_visited()
                #  print(f"ligne pour u = {u} vaut : {self.graph[u]}")
                # On examine ici tous les mouvements possibles depuis v. Soit 4 points.
                neighbors = [[u.top(), 'T'], [u.bottom(), 'B'], [u.left(), 'L'], [u.right(), 'R']]
                for neighbor, dir in neighbors:
                    print(f"Noeud neighbor {neighbor} , val = {self.graph[neighbor.x][neighbor.y]} .", end='')
                    if not self.visited[neighbor.x][neighbor.y]:
                        if self.graph[neighbor.x][neighbor.y] == 0:
                            print(f"Valeur possible ?\nEst-ce que cela vaut le coup d'aller de {u} à {neighbor} ?",
                                  f"Alors que nous avons déjà une solution pour aller en {neighbor} par une autre "
                                  f"voie ? ")
                            print(f"Le cout actuel pour {neighbor} : {self.distance[neighbor.x][neighbor.y]}",
                                  f"Cout actuel pour arriver sur {u} : {self.distance[u.x][u.y]}, "
                                  f"Pour passer de {u} à {neighbor} : 1 ", end='')

                            if self.distance[neighbor.x][neighbor.y] > self.distance[u.x][u.y] + 1:
                                print(f"Valeur retenue ! {self.distance[u.x][u.y] + 1}")
                                self.distance[neighbor.x][neighbor.y] = self.distance[u.x][u.y] + 1
                                self.parent[neighbor.x][neighbor.y] = dir
                            else:
                                if verbose:
                                    print("Trajet plus coûteux donc non intéressant")
                        else:
                            if verbose:
                                print("Mur")
                            self.visited[neighbor.x][neighbor.y] = True
                    else:
                        print("déjà visité")
                print("All neighbors visited")
                if verbose >=1:
                    self.print_distances()

            # self.pSol()
            if verbose:
                print("Fin passage ", loop_i)
            # On passe à un autre point aléatoire
            if self.all_points_are_expored() or loop_i > 300:
                break
            u = self.choose_non_visited_rnd_point()

        print(f"Tout semble exploré après {loop_i} passages.")


def area_to_point(tmx_data, area, reduction_factor):
    # area is a Pygame.rect
    # Attention : le Point et area n'ont pas le même sens d'orientation :
    area_center = area.center   # (x : décalage vers droite
                                #  , y : décalage vers bas)
    # Point a une orientation de type Numpy, Pandas, etc.
    tile_size = reduction_factor
    return Point(area_center[1]//tile_size, area_center[0]// tile_size)

if __name__ == '__main__':
    # Explication : chaque ligne indique le cout pour passer d'une ligne à la colonne.
    # Un zéro indique qu'on ne peut pas passer. Dans cette structure le coût est toujours constant.

    graph = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 1, 0, 0, 1, 0, 1],
             [1, 1, 0, 1, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 1, 0, 0, 1],
             [1, 0, 0, 1, 0, 1, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1],
             ]
    f = DijkstraManager(graph)

    START = Point(1, 1)
    DEST = Point(4, 6)
    f.dijkstra(START, verbose = 1)
    f.get_path(START, DEST, verbose=True)

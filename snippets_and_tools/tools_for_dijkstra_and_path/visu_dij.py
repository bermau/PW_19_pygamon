import networkx as nx
import matplotlib.pyplot as plt

MAX = 99999

# Votre matrice d'adjacence
graph_matrix = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
                [4, 0, 8, 0, 0, 0, 0, 11, 0],
                [0, 8, 0, 7, 0, 4, 0, 0, 2],
                [0, 0, 7, 0, 9, 14, 0, 0, 0],
                [0, 0, 0, 9, 0, 10, 0, 0, 0],
                [0, 0, 4, 14, 10, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 2, 0, 1, 6],
                [8, 11, 0, 0, 0, 0, 1, 0, 7],
                [0, 0, 2, 0, 0, 0, 6, 7, 0]]


def visualiser_graphe(matrix, chemin=None):
    """
    Visualise un graphe à partir d'une matrice d'adjacence

    Args:
        matrix: matrice d'adjacence
        chemin: liste de sommets formant un chemin à mettre en évidence (optionnel)
    """
    # Créer un graphe non orienté
    G = nx.Graph()
    n = len(matrix)

    # Ajouter les arêtes avec leurs poids
    for i in range(n):
        for j in range(i + 1, n):  # i+1 pour éviter les doublons (graphe non orienté)
            if matrix[i][j] > 0:
                G.add_edge(i, j, weight=matrix[i][j])

    # Configuration de la figure
    plt.figure(figsize=(12, 8))

    # Position des nœuds (disposition en cercle pour une belle visualisation)
    pos = nx.spring_layout(G, seed=45, k=2, iterations=50)
    # if chemin:
    print(f"{pos=}")   # Cet ordre ne correspond à ... rien ? normal pour un dico

    # Couleurs des nœuds
    node_colors = ['lightblue'] * n
    if chemin:
        for node in chemin:
            node_colors[node] = 'orange'
        # La source et destination en couleurs spéciales
        node_colors[chemin[0]] = 'lightgreen'
        node_colors[chemin[-1]] = 'lightcoral'

        print(f"{node_colors=}")  #  VRAI : color for list of node in 0, 1, 2, 3 ... etc order

    # Dessiner les nœuds
    nx.draw_networkx_nodes(G, pos,
                           nodelist = range(n),
                           node_color=node_colors,
                           node_size=700,
                           edgecolors='purple',
                           linewidths=2)

    # Dessiner les labels des nœuds
    nx.draw_networkx_labels(G, pos,
                            font_size=24 ,
                            font_weight='bold')


    # Identifier les arêtes du chemin si un chemin est fourni
    edges_chemin = []
    if chemin:
        for i in range(len(chemin) - 1):
            edges_chemin.append((chemin[i], chemin[i + 1]))

    # Dessiner les arêtes normales
    edges_normales = [e for e in G.edges() if e not in edges_chemin and tuple(reversed(e)) not in edges_chemin]
    nx.draw_networkx_edges(G, pos,
                           edgelist=edges_normales,
                           width=2,
                           alpha=0.5,
                           edge_color='gray')


    # Dessiner les arêtes du chemin en rouge
    if edges_chemin:
        nx.draw_networkx_edges(G, pos,
                               edgelist=edges_chemin,
                               width=4,
                               alpha=1,
                               edge_color='red')

    # Dessiner les poids des arêtes
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos,
                                 edge_labels=edge_labels,
                                 font_size=10,
                                 font_weight='bold',
                                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    plt.title("Graphe avec poids des arêtes", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()





class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def minDistance(self, dist, sptSet):
        min_val = MAX
        min_index = 0

        for v in range(self.V):
            if dist[v] < min_val and sptSet[v] == False:
                min_val = dist[v]
                min_index = v

        return min_index

    def dijkstra(self, src):
        dist = [MAX] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
        predecesseur = [-1] * self.V

        for _ in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True

            for v in range(self.V):
                nv_cout = dist[u] + self.graph[u][v]
                if (self.graph[u][v] > 0 and
                        sptSet[v] == False and
                        dist[v] > nv_cout):
                    dist[v] = nv_cout
                    predecesseur[v] = u

        return dist, predecesseur

    def extraire_chemin(self, predecesseur, src, dest):
        chemin = []
        current = dest

        while current != -1:
            chemin.append(current)
            current = predecesseur[current]

        chemin.reverse()

        if chemin[0] != src:
            return None

        return chemin

if __name__ == "__main__":
    # Exemple 1 : Visualiser tout le graphe
    # print("=== Graphe complet ===")
    g = Graph(9)
    g.graph = graph_matrix
    visualiser_graphe(graph_matrix)

    # Exemple 2 : Visualiser avec un chemin mis en évidence
    # (Utilisons le résultat de Dijkstra)

    # Calculer le plus court chemin de 0 à 4

    source = 0
    destination = 8
    distances, predecesseurs = g.dijkstra(source)
    chemin_optimal = g.extraire_chemin(predecesseurs, source, destination)

    print(f"\n=== Chemin optimal de {source} à {destination} ===")
    print(f"Chemin : {' → '.join(map(str, chemin_optimal))}")
    print(f"Coût total : {distances[destination]}")

    # Visualiser avec le chemin mis en évidence
    visualiser_graphe(graph_matrix, chemin=chemin_optimal)
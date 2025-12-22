import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np


class CreateurGrapheInteractif:
    """
    Créateur de graphe interactif avec matplotlib

    Instructions:
    - Clic gauche : ajouter un sommet
    - Clic droit sur 2 sommets successifs : ajouter une arête
    - Boutons pour sauvegarder et exporter
    """

    def __init__(self):
        self.G = nx.Graph()
        self.pos = {}
        self.node_counter = 0
        self.selected_nodes = []

        # Variables pour le déplacement des noeuds
        self.dragging_node = None
        self.drag_offset = (0, 0)

        # Configuration de la figure
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.subplots_adjust(bottom=0.2)

        # Zone de dessin
        self.ax.set_xlim(-1, 11)
        self.ax.set_ylim(-1, 11)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title("Créateur de graphe interactif\n"
                          "Clic gauche: ajouter sommet | "
                          "Clic droit: sélectionner 2 sommets pour créer arête",
                          fontsize=12, fontweight='bold')

        # Boutons
        ax_clear = plt.axes((0.1, 0.05, 0.15, 0.05))
        ax_export = plt.axes((0.3, 0.05, 0.15, 0.05))
        ax_matrice = plt.axes((0.5, 0.05, 0.15, 0.05))

        self.btn_clear = Button(ax_clear, 'Effacer')
        self.btn_export = Button(ax_export, 'Exporter code')
        self.btn_matrice = Button(ax_matrice, 'Voir matrice')

        self.btn_clear.on_clicked(self.clear_graph)
        self.btn_export.on_clicked(self.export_code)
        self.btn_matrice.on_clicked(self.show_matrix)

        # Zone de texte pour le poids des arêtes
        ax_weight = plt.axes((0.75, 0.05, 0.1, 0.05))
        self.weight_box = TextBox(ax_weight, 'Poids:', initial="1")

        # Connecter les événements souris
        # noinspection PyTypeChecker
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        # noinspection PyTypeChecker
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

        self.redraw()
        plt.show()

    def on_press(self, event):
        """Gestion du clic de souris (début)"""
        if event.inaxes != self.ax:
            return

        x, y = event.xdata, event.ydata

        # Vérifier si on clique sur un nœud existant
        clicked_node = self.find_nearest_node(x, y, threshold=0.5)

        if event.button == 1:  # Clic gauche
            if clicked_node is not None:
                # Commencer le déplacement
                self.dragging_node = clicked_node
                nx, ny = self.pos[clicked_node]
                self.drag_offset = (x - nx, y - ny)
                print(f"Déplacement du sommet {clicked_node}...")
            else:
                # Ajouter un nouveau sommet
                self.add_node(x, y)

        elif event.button == 3:  # Clic droit
            if clicked_node is not None:
                self.select_node_for_edge(clicked_node)

    def on_motion(self, event):
        """Gestion du mouvement de la souris"""
        if event.inaxes != self.ax:
            return

        if self.dragging_node is not None:
            # Déplacer le nœud
            x, y = event.xdata, event.ydata
            new_x = x - self.drag_offset[0]
            new_y = y - self.drag_offset[1]

            # Contraindre dans les limites
            new_x = max(-0.5, min(10.5, new_x))
            new_y = max(-0.5, min(10.5, new_y))

            self.pos[self.dragging_node] = (new_x, new_y)
            self.redraw()

    def on_release(self, event):
        """Gestion du relâchement de la souris"""
        if self.dragging_node is not None:
            print(f"Sommet {self.dragging_node} déplacé à {self.pos[self.dragging_node]}")
            self.dragging_node = None

    def add_node(self, x, y):
        """Ajoute un nouveau sommet"""
        node_id = self.node_counter
        self.G.add_node(node_id)
        self.pos[node_id] = (x, y)
        self.node_counter += 1
        print(f"Sommet {node_id} ajouté à ({x:.2f}, {y:.2f})")
        self.redraw()

    def find_nearest_node(self, x, y, threshold=0.5):
        """Trouve le sommet le plus proche d'une position"""
        min_dist = threshold
        nearest = None

        for node, (nx, ny) in self.pos.items():
            dist = np.sqrt((x - nx) ** 2 + (y - ny) ** 2)
            if dist < min_dist:
                min_dist = dist
                nearest = node

        return nearest

    def select_node_for_edge(self, node):
        """Sélectionne un sommet pour créer une arête"""
        if node in self.selected_nodes:
            return

        self.selected_nodes.append(node)
        print(f"Sommet {node} sélectionné")

        if len(self.selected_nodes) == 2:
            # Créer l'arête
            try:
                weight = float(self.weight_box.text)
            except ValueError:
                weight = 1.0

            n1, n2 = self.selected_nodes
            self.G.add_edge(n1, n2, weight=weight)
            print(f"Arête ajoutée : {n1} <-> {n2} (poids: {weight})")

            self.selected_nodes = []
            self.redraw()
        else:
            self.redraw()

    def redraw(self):
        """Redessine le graphe"""
        self.ax.clear()
        self.ax.set_xlim(-1, 11)
        self.ax.set_ylim(-1, 11)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title("Créateur de graphe interactif\n"
                          "Clic gauche: ajouter sommet | "
                          "Clic droit: sélectionner 2 sommets pour créer arête",
                          fontsize=12, fontweight='bold')

        if len(self.G.nodes()) == 0:
            self.fig.canvas.draw()
            return

        # Couleurs des nœuds
        node_colors = ['lightblue' if n not in self.selected_nodes
                       else 'yellow' for n in self.G.nodes()]

        # Dessiner les nœuds
        nx.draw_networkx_nodes(self.G, self.pos,
                               node_color=node_colors,
                               node_size=500,
                               edgecolors='black',
                               linewidths=2,
                               ax=self.ax)

        # Dessiner les labels
        nx.draw_networkx_labels(self.G, self.pos,
                                font_size=14,
                                font_weight='bold',
                                ax=self.ax)

        # Dessiner les arêtes
        nx.draw_networkx_edges(self.G, self.pos,
                               width=2,
                               alpha=0.6,
                               ax=self.ax)

        # Dessiner les poids
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos,
                                     edge_labels=edge_labels,
                                     font_size=10,
                                     ax=self.ax)

        self.fig.canvas.draw()

    def clear_graph(self, event):
        """Efface tout le graphe"""
        self.G.clear()
        self.pos = {}
        self.node_counter = 0
        self.selected_nodes = []
        print("Graphe effacé")
        self.redraw()

    def show_matrix(self, event):
        """Affiche la matrice d'adjacence"""
        if len(self.G.nodes()) == 0:
            print("Le graphe est vide")
            return

        # Créer la matrice d'adjacence
        nodes = sorted(self.G.nodes())
        n = len(nodes)
        matrix = [[0 for _ in range(n)] for _ in range(n)]

        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if self.G.has_edge(node1, node2):
                    weight = self.G[node1][node2].get('weight', 1)
                    matrix[i][j] = weight

        print("\n" + "=" * 50)
        print("MATRICE D'ADJACENCE")
        print("=" * 50)
        print("    ", end="")
        for node in nodes:
            print(f"{node:4}", end="")
        print()

        for i, row in enumerate(matrix):
            print(f"{nodes[i]:2}  ", end="")
            for val in row:
                print(f"{val:4}", end="")
            print()
        print("=" * 50 + "\n")

    def export_code(self, event):
        """Exporte le code Python pour créer ce graphe"""
        if len(self.G.nodes()) == 0:
            print("Le graphe est vide")
            return

        nodes = sorted(self.G.nodes())
        n = len(nodes)
        matrix = [[0 for _ in range(n)] for _ in range(n)]

        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if self.G.has_edge(node1, node2):
                    weight = self.G[node1][node2].get('weight', 1)
                    matrix[i][j] = weight

        print("\n" + "=" * 50)
        print("CODE PYTHON GÉNÉRÉ")
        print("=" * 50)
        print(f"# Graphe avec {n} sommets")
        print(f"graph_matrix = [")
        for row in matrix:
            print(f"    {row},")
        print("]")
        print("=" * 50 + "\n")


# Mode 1: Interface interactive complète
print("=== CRÉATEUR DE GRAPHE INTERACTIF ===")
print("\nInstructions:")
print("- Clic GAUCHE : Ajouter un sommet")
print("- Clic DROIT : Sélectionner 2 sommets pour créer une arête")
print("- Modifier le poids dans la zone de texte avant de créer l'arête")
print("- Utiliser les boutons pour exporter ou voir la matrice")
print("\nLancement de l'interface...\n")

createur = CreateurGrapheInteractif()

# Mode 2: Création programmatique simple (alternative)
print("\n\n=== ALTERNATIVE: CRÉATION PROGRAMMATIQUE ===")
print("Si vous préférez créer le graphe par code:\n")

exemple = """
import networkx as nx
import matplotlib.pyplot as plt

# Créer un graphe vide
G = nx.Graph()

# Ajouter des sommets
G.add_nodes_from([0, 1, 2, 3, 4])

# Ajouter des arêtes avec poids
G.add_edge(0, 1, weight=4)
G.add_edge(0, 2, weight=2)
G.add_edge(1, 2, weight=1)
G.add_edge(1, 3, weight=5)
G.add_edge(2, 3, weight=8)
G.add_edge(2, 4, weight=10)
G.add_edge(3, 4, weight=2)

# Visualiser
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', 
        node_size=700, font_size=16, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()

# Obtenir la matrice d'adjacence
import numpy as np
matrix = nx.to_numpy_array(G)
print(matrix)
"""

print(exemple)
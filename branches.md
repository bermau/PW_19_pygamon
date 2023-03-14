# Suivi des branches 

## 22_01_collect_mushroom.
Mes champignons sont sur 2 blocs :
le supérieur est d'index 43, l'inférieur est d'index 46. Le problème est sans doute celui de la collecte des diamants. 

J'ai écrit une fonction find_mushrooms dans map.py.. qui plante tout...

Je reviens sur 77f3d84c. Pycharm m'affiche un avertissement. J'ai compris comment en faire une branche.

Finalement, j'ai trouvé un moyen de générer des pièces (coins), qui sont traitées comme on l'attend. Les pièces ne sont pas déduites des cartes. 

## 23_02_coins_from_maps
La stratégie de la branche ci-dessus ne fonctionne pas : je ne parviens pas à modifier dynamiquement une carte tmx. J'ai cherché longtemps en vain comment cacher une tuile ou un lot de tuile par programmation. Je n'ai pas trouvé. J'ai donc changé de stratégie : je traite les pièces (Coins) comme des Sprites.  
La position de ces sprites est déduite de la carte. Sur la carte, on va créer des objets de type coins.
De plus la valeur de la pièce est aléatoire. 

Merge sur master
## 23_02_ajouter_autres_joueurs
J'ai ajouté des NPC (Non playing Characters), ou PNG (Personnages non joueurs) en français. Ils se déplacent d'une façon primaire dans des carrés rectangles prédéfinis. 

Merged sur master
## devel

## 23_02_PNJ_en_mouvement_diagonal
Faire en sorte que le regard du PNG soit dans le sens de la marche ! Fait. Je cherche ensuite à faire en sorte que le 
PNG navigue en diagonal entre deux zones. 

self.rect n'est pas à jour. Résolu

## 23_02_tester_dijkstra
Maintenant que mes lutins se déplacent aléatoirement de façon autonome, (mais sans respecter les zones interdites), je fais faire en sorte qu'ils se déplacent entre 2 points, en évitant les obstacles. Je vais tester l'algorithme de
Dijkstra. OK premier succès. 

## 23_02_improve_dijkstra
Semble abandonné (grisé sur le log de Git)

## 23_02_implementer_dijkstra
La carte tmx permet de définir des zones où les NPC doivent passer. Ces zones (area) sont nommés 'robin_path1', 'robin_path2'... 
Une fonction détecte ces zones par une expression régulière et les compte. 

Le NPC se déplace à présent entre 2 zones de promenades (walk) choisies aléatoirement. 

Entre ces deux areas de walk, le chemin est calculé par uen algorithme de Dijkstra. Il est assez mal réalisé par moi, mais il fonctionne.  

 J'ai résolu le problème du saut initial du NPC. Cela était dû à l'absence de mise à jour de sa variable old_position. 
Cette variable est maintenant mise à jour avant chaque mouvement. De plus j'ai fait en sorte que les NPC ne soit pas concernées par le détecteur de collision de la MapManager.check_collision(). Je décide de faire en sorte que le NPC ait une route correctement calculée. La route actuelle n'est pas parfaite : le NPC passe encore un petit peu sur l'eau. Il s'agît sans doute d'une erreur de géométrie. 
MERGED sur devel
## 23_02_improve_2d_structure
Travail pour créer une structure 2 en deux dimension. Non utilisé. 

## 23_03_dessiner_sur_le_jeu
J'ai besoin d'outils pour dessiner sur le jeu. Cela peut permettre de debugger en  dessinant une zone cible sur le jeu.

Dans `lib_drawing_tools.py`, j'ai créé une classe `DebugRect`, pour afficher un rectangle sur un écran. On peut l'utiliser pour visualiser une zone sur toutes les cartes ou sur une carte en particulier.

Pour afficher un rectangle sur toutes les cartes, on peut par modifier le fichier `game.py` ainsi : On ajoute en fin de fonction `Run().__init__()` le code suivant : 

``` python
       # Une zone à encadrer pour debugger
        self.game_indic = DebugRect('pink', pygame.Rect(300, 200, 40, 16), 3)  # pour tous les mondes
```

et on glisse dans la boucle `run()`, juste avant l'appel à `flip()`, responsable de l'affichage :
``` python
    self.game_indic.render(self.screen)
    pygame.display.flip()
```

De façon similaire, on peut afficher un rectangle pour un monde particulier dans `map.py`. Pour cela, après enregistrement d'une carte avec la fonction `register_map`, on ajoute un objet de type `DebugRect` à cette carte : 
```python
        self.register_map('world',
                          portals=[Portal(from_world="world", origin_point='enter_house', target_world="house",
                                          teleport_point="spawn_from_world")],
                          npcs=[  # NPC('paul', nb_areas=4),
                              NPC('robin', self, 'world')], )

        # Ajouter un rectangle indicateur dans la carte world.
        self.maps['world'].indic = DebugRect('red', pygame.Rect(400, 200, 100, 50), 6)
```

Puis on modifie la fonction `draw() `ainsi : 

```python
    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)
        # On ajoute un indicateur pour debugger certaines cartes
        if self.current_map == 'world':
            self.maps['world'].indic.render(self.screen)
```
Résultats : 

| ![world_and_indicators.png](images%2Fworld_and_indicators.png)                                         | ![house_and_indicator.png](images%2Fhouse_and_indicator.png)    |
|--------------------------------------------------------------------------------------------------------|-----|

Un cadre rose (sur toutes les cartes) et un cadre rouge sur la carte 'monde' uniquement. 

## 23_03_pourquoi_NPC_passe_sur_l_eau
Mon NPC se déplace tout seul, et il respecte à peu près les zones d'eau et les zones de collision. Dans certains cas, il ne déplace sur l'eau. Pour comprendre ce qu'il se passe j'ai ajouté une grille (cf. `lib_drawing_tools.py`) et des carrés pour indiquer les zones interdites selon la carte simplifiée. De plus j'ai écrit une fonction de pause. L'ensemble permet d'analyser les erreurs. Exemple d'erreur : 
![](/home/bertrand/important/prog_local/PW_19_pygamon/images/le_fautif.png). 
Le NPC est sur l'eau. Or l'eau est perçue comme interdite selon la carte simplifiée. Les zones interdites de la carte simplifiée sont marquées d'un carré bleu. 

Pour analyser l'erreur, j'initialise le générateur de nombre aléatoire avec l'instruction `seed()` dans `maps.py`. Je me suis rendu compte que l'erreur portait sur les premiers instants du jeu. 

L'erreur venait du fait qu'au cours de la promenade, le NPC considérait qu'il avait obtenu le point suivant trop tôt (dès le premier mouvement en quittant le premier point). J'ai résolu le problème en remplaçant la fonction de type `Rect.collide` par une fonction de type `Rect.contain`() dans le test de collision du NPC.

# Les importations : 
main.py  : 
  from game import Game

game.py : 
    from src.map import MapManager
    import player
    from player import Player
    from counter import Counter

map.py:
    from src.player import NPC
    from lib_dijkstra import Point

player.py:
    from map import Graph, Point, area_to_point

counter:
    - 


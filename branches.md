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
J'ai ajouté des NPC (Non playing Characters), PNG Personnages non joueurs. Ils se déplacent d'une façon primaire dans des
carrés rectangles prédéfinis. 

Merged sur master
## devel




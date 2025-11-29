# Importing the library
from time import sleep

import pygame

# Initializing Pygame
pygame.init()

# Initializing surface
fenetre = pygame.display.set_mode((400, 300))

# Insérer un tmx

# Nom du fichier TMX (même dossier)
TMX_FILE = "ts_dungeon.png"

# Créer un surface bleue
surf_2_bleue = pygame.Surface((50,50))
surf_2_bleue.fill("red")
# placer la surface bleue
fenetre.blit(surf_2_bleue, (100,20))
# Initialing Color
color_rect = (155, 120, 0)


# Drawing Rectangle
pygame.draw.rect(fenetre, color_rect, pygame.Rect(30, 30, 60, 60))

pygame.display.flip()

sleep(2)
# input("OK3")
# Importing the library
from time import sleep
import pygame
from pytmx.util_pygame import load_pygame

# Initializing Pygame
pygame.init()

# Initializing surface
fenetre = pygame.display.set_mode((200, 100))
fenetre.fill("pink")

# load an image from a tmx file
carte_tmx = load_pygame("donjon_mini.tmx")
x_pixels = carte_tmx.width * carte_tmx.tilewidth
y_pixels = carte_tmx.height * carte_tmx.tileheight

# Pour afficher l'image d'une couche, il faut afficher tuile par tuile.
for layer in carte_tmx.visible_layers:
    for x, y, tile in layer.tiles():
        fenetre.blit(tile, (x * carte_tmx.tilewidth, y * carte_tmx.tileheight))

# Create a blue surface
blue_surface = pygame.Surface((50, 50))
blue_surface.fill("blue")

fenetre.blit(blue_surface, (100, 20))

# display for 2 seconds
pygame.display.flip()


pygame.image.save(fenetre, "image_from_tmx_with_transparency.png")

sleep(1)

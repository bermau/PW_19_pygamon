# Importing the library
from time import sleep
import pygame
from pytmx.util_pygame import load_pygame
from pytmx import TiledTileLayer

# Initializing Pygame
pygame.init()

# Initializing surface
fenetre = pygame.display.set_mode((600, 400))
fenetre.fill("pink")

# load an image from a tmx file
carte_tmx = load_pygame("carte_donjon.tmx")
x_pixels = carte_tmx.width * carte_tmx.tilewidth
y_pixels = carte_tmx.height * carte_tmx.tileheight

# extract first layer
# pytmx ne sait pas "afficher l'image d'une layer".
# Il faut afficher tuile par tuile les tuiles d'un layer

for layer in carte_tmx.visible_layers:
    for x, y, tile in layer.tiles():
        fenetre.blit(tile, (x * carte_tmx.tilewidth, y * carte_tmx.tileheight))


# Create a blue surface
blue_surface = pygame.Surface((50, 50))
blue_surface.fill("blue")

fenetre.blit(blue_surface, (100, 20))

# Create a red surface with alpha
red_surface = pygame.Surface((100, 60), pygame.SRCALPHA)
# red_surface.set_alpha(100)
red_surface.fill((155, 120, 0, 100))
fenetre.blit(red_surface,(30, 30))

# import a png (which has a transparent layout)
file = "ts_dungeon.png"
png_surface = pygame.image.load(file)
png_surface.set_alpha(150)
fenetre.blit(png_surface, (200,100))

# display for 2 seconds
pygame.display.flip()
sleep(4)

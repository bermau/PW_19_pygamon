# Importing the library
from time import sleep
import pygame

# Initializing Pygame
pygame.init()

# Initializing surface
fenetre = pygame.display.set_mode((600, 400))
fenetre.fill("pink")

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
png_surface.set_alpha(50)
fenetre.blit(png_surface, (200,100))

# display for 2 seconds
pygame.display.flip()
sleep(5)

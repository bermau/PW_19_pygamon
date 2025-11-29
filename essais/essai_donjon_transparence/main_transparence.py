# Importing the library
from time import sleep
import pygame

# Initializing Pygame
pygame.init()

# Initializing surface
fenetre = pygame.display.set_mode((400, 300))

# color :
fenetre.fill("pink")

# Create a blue surface
blue_surface = pygame.Surface((50, 50))
blue_surface.fill("blue")

fenetre.blit(blue_surface, (100, 20))

# Create a red surface
red_surface = pygame.Surface((100, 60))
red_surface.set_alpha(100)
red_surface.fill((155, 120, 0))


fenetre.blit(red_surface,(30, 30))

# Drawing Rectangle
# pygame.draw.rect(fenetre, red_surface, pygame.Rect(30, 30, 100, 60))

# display for 2 seconds
pygame.display.flip()
sleep(2)

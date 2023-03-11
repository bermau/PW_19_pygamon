"""Tools to draw over the main game"""

import pygame

class MyRect():
    def __init__(self):
        self.zone = pygame.Rect(122, 150, 80, 80)

    def render(self, screen):
        pass
        pygame.draw.rect(screen, "blue", self.zone, 3)
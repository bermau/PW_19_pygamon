"""Tools to draw over the main game"""

import pygame

class DebugRect():
    def __init__(self, color, pygame_rect, l_width):

        self.zone = pygame_rect
        self.color = color
        self.l_width = l_width

    def render(self, screen):
        pass
        pygame.draw.rect(screen, self.color, self.zone, self.l_width)
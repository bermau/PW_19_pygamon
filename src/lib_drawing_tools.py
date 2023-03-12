"""Tools to draw over the main game"""

import pygame

display = True


class DebugRect():
    def __init__(self, color, pygame_rect, l_width):
        self.zone = pygame_rect
        self.color = color
        self.l_width = l_width

    def render(self, screen):
        if display:
            pygame.draw.rect(screen, self.color, self.zone, self.l_width)



def render_world_grill(screen, map):
    reduc = 2
    tw = map.tmx_data.tilewidth * reduc
    th = map.tmx_data.tileheight * reduc
    w = map.tmx_data.width
    h = map.tmx_data.height

    for x in range(0, w * tw, tw):
        for y in range(0, h * th, th):
            rect = pygame.Rect(x, y, tw, th)
            pygame.draw.rect(screen, "white", rect, 1)

def render_simple_world(screen, map):

    pass

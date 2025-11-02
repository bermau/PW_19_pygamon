"""Tools to draw over the main game"""

import pygame

display = False   # peut être modifié dans game.py pour un usage plus général


class DebugRect:
    def __init__(self, color, pygame_rect, l_width):
        self.zone = pygame_rect
        self.color = color
        self.l_width = l_width

    def render(self, screen):
        if display:
            pygame.draw.rect(screen, self.color, self.zone, self.l_width)


def render_world_grid(screen, map):
    if display:
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
    if display:
        for i, line in enumerate(map.simple_map):
            for j, col in enumerate(line):
                if map.simple_map[i][j] == 1:
                    rect_ = pygame.Rect(j * 32 + 12, i * 32 + 12, 12, 12)
                    pygame.draw.rect(screen, "blue", rect_, 2)

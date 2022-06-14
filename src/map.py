from dataclasses import dataclass
import pygame, pytmx, pyscroll

@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group:pyscroll.PyscrollGroup

    
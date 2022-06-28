import pygame, pytmx, pyscroll


name = 'world'


pygame.init()
screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Study Dinosaure aventure")/


tmx_data = pytmx.util_pygame.load_pygame(f"../map/{name}.tmx")

map_data = pyscroll.data.TiledMapData(tmx_data)


input("totototo ? ")


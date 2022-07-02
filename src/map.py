from dataclasses import dataclass

import pygame
import pyscroll
import pytmx


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]


class MapManager:
    def __init__(self, screen, player):
        self.maps = dict()  # "house" -> Map ("house", walls, group)
        self.screen = screen
        self.player = player
        self.current_map = 'world'

        self.register_map('world', portals=[
            Portal(from_world="world", origin_point='enter_house', target_world="house",
                   teleport_point="spawn_house")
        ])
        self.register_map('house', portals=[
            Portal(from_world='house', origin_point='enter_world', target_world='world',
                   teleport_point="spawn_world")
        ])
        self.teleport_player('player')

    def teleport_player(self, pos_name):
        point = self.get_object(pos_name)
        self.player.position[0] = point.x - 16
        self.player.position[1] = point.y - 32  # pour régler le niveau des pieds.
        self.player.save_location()

    def register_map(self, name, portals=None):
        if portals is None:
            portals = []
        print("Switch to world")
        # Charger les cartes
        tmx_data = pytmx.util_pygame.load_pygame(f"map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # Définir une liste de collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # # Ajouter en wall toute la zone d'eau, sauf s'il y a un path par-dessus
        if 'water' in tmx_data.layernames:
            for y, line in enumerate(tmx_data.layernames['water'].data):
                for x, cell in enumerate(line):
                    if cell != 0 and tmx_data.layernames['path'].data[y][x] == 0:
                        walls.append(pygame.Rect(x * 16, y * 16, 16, 16))

        # Dessiner le groupe de calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        print("Groupe de calques")
        print(group)
        group.add(self.player)

        # Créer un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals)

    def check_collision(self):
        # portals
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        # collisions
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        # self.group.update()
        self.check_collision()

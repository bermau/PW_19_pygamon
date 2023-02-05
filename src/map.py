import re
from dataclasses import dataclass

import pygame
import pyscroll
import pytmx
from random import randint

from src.player import NPC


def groups_in_list(lst, code='X', blank=' '):
    """Find a list of continuous signs.
    >>> groups_in_list ((' ', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', ' '))
    [(2, 6), (8, 9)]
    >>> groups_in_list ((' ', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X'))
    [(2, 6), (8, 9)]
    """
    walls = []
    again = True
    current = 0
    while again:
        try:
            first = lst.index(code, current)
        except ValueError:
            break
        try:
            last = lst.index(blank, first + 1)
        except ValueError:
            last = len(lst)

        if last:
            walls.append((first, last - 1))
            current = last
        else:
            again = False
    return walls


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


# Vient de https://coderslegacy.com/pygame-platformer-coins-and-images/
class Coin(pygame.sprite.Sprite):
    values = (1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 5, 10, 10, 20, 50)

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("../map/coin.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 16)
        self.value = Coin.values[randint(0, len(Coin.values)-1)]

    def move_back(self):
        pass


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]

class MapManager:
    """General manager of all maps"""
    def __init__(self, master_game, screen, player):
        """Charge les cartes, puis téléporte le joueur et enfin les NPC"""
        self.master_game = master_game
        self.maps = dict()  # "house" -> Map ("house", walls, group)
        self.screen = screen
        self.player = player
        # self.single_npc = single_npc
        self.current_map = 'world'

        # Dans Portal on indique comment les sorties (= comment entrer dans un autre monde)
        # Attention le from_world doit absolument avoir tous les origine_points.
        self.register_map('world',
                          portals=[Portal(from_world="world", origin_point='enter_house', target_world="house",
                                          teleport_point="spawn_from_world")],
                          npcs=[NPC('paul', nb_areas=4), NPC('robin', nb_areas=4)]
                          )

        self.register_map('house',
                          portals=[
                              Portal(from_world='house', origin_point='enter_world', target_world='world',
                                     teleport_point="spawn_from_house"),
                              Portal(from_world='house', origin_point='enter_dungeon', target_world='dungeon',
                                     teleport_point="spawn_from_house")
                          ])

        self.register_map('dungeon',
                          portals=[
                              Portal(from_world='dungeon', origin_point='enter_house', target_world='house',
                                     teleport_point="spawn_from_dungeon"),
                              Portal(from_world='dungeon', origin_point='enter_world', target_world='world',
                                     teleport_point="spawn_from_dungeon")
                          ])

        self.teleport_player('player')
        self.teleport_npcs()

    def teleport_player(self, player_name):
        point = self.get_object(player_name)
        self.player.position[0] = point.x - 16
        self.player.position[1] = point.y - 32  # pour régler le niveau des pieds.
        self.player.save_location()

    def register_map(self, map_name, portals=None, npcs=None):
        if npcs is None:
            npcs = []
        if portals is None:
            portals = []
        print("Registering map", map_name)

        # Charger les cartes
        tmx_data = pytmx.util_pygame.load_pygame(f"../map/{map_name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # Définir une liste de collisions et champignons
        walls = []
        # Je vais ajouter des coins comme des sprites (méthode venant de
        # https://coderslegacy.com/pygame-platformer-coins-and-images/ )
        coins = pygame.sprite.Group()

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "coin_place":
                coins.add(Coin((obj.x - 24, obj.y - 24)))  # Valeur mal ajustée

        # Ajouter en wall toute la zone d'eau, sauf s'il y a un path par-dessus
        water_blocks = []
        if 'water' in tmx_data.layernames:
            for y, line in enumerate(tmx_data.layernames['water'].data):
                line_wall = []
                for x, cell in enumerate(line):
                    if cell != 0 and tmx_data.layernames['path'].data[y][x] == 0:
                        line_wall.append('X')
                    else:
                        line_wall.append(' ')
                water_blocks.append(line_wall)

            for y, line in enumerate(water_blocks):
                for group in groups_in_list(line, code='X', blank=' '):
                    walls.append(pygame.Rect(group[0] * 16, y * 16, (group[1] - group[0] + 1) * 16, 16))

        # Dessiner le groupe de calques
        # default_layer à 0 : bonhomme sur herbe, sous chemin
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5) # Pourquoi 5 :
        group.add(self.player)
        # group.add(npcs)
        group.add(coins)
        for npc in npcs:
            group.add(npc)

        # Créer un objet Map
        self.maps[map_name] = Map(map_name, walls, group, tmx_data, portals, npcs)

    def teleport_npcs(self):
        for map_name in self.maps:
            map_data = self.maps[map_name]
            for npc in map_data.npcs:
                npc.load_points(self)
                npc.teleport_npc()

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
                    self.master_game.point_counter.points += 100

        # collisions, coins
        for my_sprite in self.get_group().sprites():
            if my_sprite.feet.collidelist(self.get_walls()) > -1:
                my_sprite.move_back()
            if isinstance(my_sprite, Coin):
                if self.player.feet.colliderect(my_sprite):
                    print(f"Miam ! {my_sprite.value} points !!")
                    self.master_game.point_counter.points += my_sprite.value
                    my_sprite.kill()

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def get_objects_regex(self, regex):
        """Return objectd witch name match with a regex"""
        AA = self.get_map().tmx_data

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        """Fonction pour toutes les maps, appelée à chaque image"""
        self.get_group().update()
        self.check_collision()
        # Bouger les NPC
        for npc in self.get_map().npcs:
            npc.move()

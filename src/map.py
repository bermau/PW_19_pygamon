from dataclasses import dataclass

import pygame
import pyscroll
import pytmx


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
            again = False
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


@dataclass
class Mushroom:
    """A champignon est un rect avec un certain nombre de points et un indicateur pour l'afficher ou non."""
    rect : pygame.Rect
    points: int  # nombre de points
    display: bool


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    mushrooms: list[Mushroom]


class MapManager:
    def __init__(self, master_game, screen, player):
        self.master_game = master_game
        self.maps = dict()  # "house" -> Map ("house", walls, group)
        self.screen = screen
        self.player = player
        self.current_map = 'world'

        self.register_map('world', portals=[
            Portal(from_world="world", origin_point='enter_house', target_world="house",
                   teleport_point="spawn_from_world")
        ])
        # Dans Portal on indique comment les sorties (= comment entrer dans un autre monde)
        # Attention le from_world doit absolument avoir tous les origine_points.
        self.register_map('house', portals=[
            Portal(from_world='house', origin_point='enter_world', target_world='world',
                   teleport_point="spawn_from_house"),
            Portal(from_world='house', origin_point='enter_dungeon', target_world='dungeon',
                   teleport_point="spawn_from_house")
        ])

        self.register_map('dungeon', portals=[
            Portal(from_world='dungeon', origin_point='enter_house', target_world='house',
                   teleport_point="spawn_from_dungeon"),
            Portal(from_world='dungeon', origin_point='enter_world', target_world='world',
                   teleport_point="spawn_from_dungeon")
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
        print("Registering map", name)
        # Charger les cartes
        tmx_data = pytmx.util_pygame.load_pygame(f"../map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # Définir une liste de collisions et champignons
        walls = []
        mushrooms = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "mushroom":
                mushrooms.append(Mushroom(pygame.Rect(obj.x, obj.y, obj.width, obj.height), points=15, display=True))
                print("Found a mushroom....")

        # # Ajouter en wall toute la zone d'eau, sauf s'il y a un path par-dessus
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
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        group.add(self.player)

        # Créer un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, mushrooms)

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
                    # self.master_game.point_counter
                    self.master_game.point_counter.points += 100

        # collisions
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_mushrooms()) > -1:
                print("Mushroom")
                self.master_game.point_counter.points += 20
                # Il faut désactiver le champignon ramassé.

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_mushrooms(self):
        return self.get_map().mushrooms

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        # self.group.update()
        self.check_collision()

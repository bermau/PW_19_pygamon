import os
import re
from dataclasses import dataclass
from pprint import pprint

import pygame
import pyscroll
import pytmx
from pytmx import TiledTileLayer
from random import randint, seed

from src.player import NPC
from lib_drawing_tools import DebugRect, render_world_grid, render_simple_world

verbose = True
# seed(1)
START_WITH_MAP = 'garden'   # OK : 'dungeon', 'world', mais BUG avec 'house'

pygame.mixer.init()

def groups_in_list(lst, code='X', blank=' '):
    """Find a list of continuous signs. This is used to try to reduce memory usage.
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


def play_sound_(file_path=None):
    """Play an audio file as a buffered sound sample

    :param str file_path: audio file (default data/secosmic_low.wav)
    """
    # choose a desired audio format
    pygame.mixer.init(11025)  # raises exception on fail

    # load the sound
    sound = pygame.mixer.Sound(file_path)

    # start playing
    print("Playing Sound...")
    channel = sound.play()

    # poll until finished
    while channel.get_busy():  # still playing
        print("  ...still going...")
        pygame.time.wait(1000)
    print("...Finished")

REP = os.getcwd()

# Init des sons
# music :
MUSIC = os.path.join("../sounds/080415pianobgm3popver.ogg")
pygame.mixer.music.load(MUSIC)
pygame.mixer.music.play(100)

# Sound (bing/slap....)
sound_rep = os.path.join(REP, "..", "venv", "lib/python3.10/site-packages/pygame/examples/data" )
coin_sound = pygame.mixer.Sound(os.path.join(sound_rep, "whiff.wav"))
fine_sound = pygame.mixer.Sound(os.path.join(sound_rep, "boom.wav"))


# Vient de https://coderslegacy.com/pygame-platformer-coins-and-images/
class Coin(pygame.sprite.Sprite):
    """Coin Management.  Gestion des Pièces. En début de partie, la valeur de la pièce n'est pas affichée.
    Quand le personnage touche la pièce, la valeur de la pièce sera affichéee.
    """
    # Intentionally, there are more 1 point coins than 50 points coins. Some coins have negative values.
    values = (-1, -2, -50, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 5, 5, 5, 10, 10, 20, 50)
    # values = (-1, -2, -50, -1, -1, -1, -1, -1, -2, -2, -2, -2, -2, -5, -5, 5, 10, 10, 20, 50)

    def __init__(self, pos, screen):
        super().__init__()
        self.never_touched = True
        self.name = 'coin'
        self.screen = screen
        self.image = pygame.image.load("../images/coin.png")

        self.rect = self.image.get_rect()
        self.center = self.rect.center
        self.rect.topleft = pos
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 16)
        self.value = Coin.values[randint(0, len(Coin.values) - 1)]
        self.coin_icon_name = None  # icon with a value of the coin
        self.counter_for_explosion = 20
        self.biginning_of_the_end_time = None  # Début de la mort de la pièce
        self.coin_text_str = str(self.value)
        myfont = pygame.font.Font('../dialogs/dialog_font.ttf', 42)
        self.coin_text = myfont.render(self.coin_text_str, True, 'purple')
        self.display_time = 3000               # µs of effect when the coin is touched
        self.init_coin()

    def init_coin(self):
        if self.value > 0:
            self.coin_icon_name = f"../images/coin_{self.value}.png"
        else:
            self.coin_icon_name = "../images/fine.png"

    def effect_during_death(self):
        """Action durant quelques secondes"""
        if not self.biginning_of_the_end_time:
            self.biginning_of_the_end_time = pygame.time.get_ticks()

            if self.value > 0:
                coin_sound.play()
            else:
                fine_sound.play()

            self.image = pygame.image.load(self.coin_icon_name)

        current_time = pygame.time.get_ticks()
        if current_time - self.biginning_of_the_end_time < self.display_time:
            self.display_its_last_secondes()
        else:
            self.kill()

    def display_its_last_secondes(self):
        """Display the coin value, for a few seconds"""
        self.screen.blit(self.coin_text, self.rect)
        if pygame.time.get_ticks() - self.biginning_of_the_end_time > self.display_time:
            self.kill()


def describe_tile(tile):
    """Describe a tile"""
    print(f"\talpha: {tile.get_alpha()}",  "colorkey:", tile.get_colorkey(),
          f"\tmask:{tile.get_masks() }")


@dataclass
class Map:
    name: str
    tmx_data: pytmx.TiledMap
    simple_map: list
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    portals: list[Portal]
    npcs: list[NPC]


class MapManager:
    """General manager of all maps"""

    def __init__(self, master_game, screen, player, verbose=False):
        """Charge les cartes, puis téléporte le joueur et enfin les NPC"""
        self.master_game = master_game
        self.maps = dict()  # "house" -> Map ("house", walls, group)
        self.screen = screen
        self.player = player
        self.verbose = verbose
        self.current_map = START_WITH_MAP

        # Portal indique comment entrer dans un autre monde.
        # Attention le from_world doit absolument avoir tous les origin_points.
        self.register_map('garden',
                          portals=[
                              Portal(from_world="garden", origin_point='enter_house', target_world="house",
                                     teleport_point="spawn_from_garden"),
                              Portal(from_world="garden", origin_point='enter_dungeon', target_world="dungeon",
                                     teleport_point="spawn_from_garden")
                          ],

                          npcs=[NPC('paul', self, 'garden'),
                               NPC('robin', self, 'garden')],
                          )

        # Ajouter un rectangle indicateur dans la carte world.
        # Nécessite lib_drawing_tools.display = True
        self.maps['garden'].indic = DebugRect('red', pygame.Rect(400, 200, 100, 50), 3)

        # Enregistrer les autres cartes.
        self.register_map('house',
                          portals=[
                              Portal(from_world='house', origin_point='enter_garden', target_world='garden',
                                     teleport_point="spawn_from_house"),
                              Portal(from_world='house', origin_point='enter_dungeon', target_world='dungeon',
                                     teleport_point="spawn_from_house")
                          ])

        self.register_map('dungeon',
                          portals=[
                              Portal(from_world='dungeon', origin_point='enter_house', target_world='house',
                                     teleport_point="spawn_from_dungeon"),
                              Portal(from_world='dungeon', origin_point='enter_garden', target_world='garden',
                                     teleport_point="spawn_from_dungeon")
                          ], verbose= True)
        print("FIN DEFINITION DES CARTES")

        self.teleport_player('player')
        print("FIN TELEPORT PLAYER") # PAS DE BU ICI
        # Le BUG sur house a lieu dans teleport NPC. Sans doute parce que la carte simple de house est vide.
        self.teleport_npcs()  # Déduit les areas de la carte. Calcule le chemin simple de la promenade
        print("FIN TELEPORT NPC")
        self.define_npcs_debuggers()


    def register_map(self, map_name, portals=None, npcs=None, verbose=False):
        if npcs is None:
            npcs = []
        if portals is None:
            portals = []
        if verbose:
            print(f"register_map() : Registering map '{map_name}'")

        # Charger les cartes
        tmx_data = pytmx.util_pygame.load_pygame(f"../map/{map_name}.tmx")
        # corriger les cartes du bug de transparence :
        CORRECT_TRANSPARENCY = True
        EXPLAIN_MAP_TRANSPARENCY = True

        if CORRECT_TRANSPARENCY:

            for layer in tmx_data.visible_layers:
                if isinstance(layer, TiledTileLayer):
                    for (x, y, gid) in layer:
                        tile = tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            # La ligne ci-dessous montre que les tiles fautifs ont un colorkey à (255, 255, 255, 255).
                            print(f"x = {x}\ty = {y} \tGID = {gid}",  end = '')
                            describe_tile(tile)
                            COLOR_KEY = (0, 0, 0, 255)
                            if tile.get_colorkey() != COLOR_KEY:
                                # pour éviter que le fond ne soit noir sur les layers 2 et plus
                                tile.set_colorkey(COLOR_KEY)

        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # Définir une liste de collisions
        walls = []

        # Ajouter des pièces/coins en tant que sprites.
        coins = pygame.sprite.Group()

        # placement des walls et des coins
        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "coin_place":
                coins.add(Coin((obj.x - 24, obj.y - 24), self.screen))  # Valeur mal ajustée

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

        # Dessiner le groupe de calques. Si default_layer = 0 : bonhomme sur herbe, sous chemin
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)  # Pourquoi 5 :
        group.add(self.player)
        # group.add(npcs)
        group.add(coins)  ## ??? mais coins est un groupe de Coin ???
        for npc in npcs:
            group.add(npc)

        # Fabriquer une carte simplifiée de 0 et de 1 pour les walls
        # Cette carte est fausse pour "house".
        simple_map = build_simple_map_from_tmx(tmx_data, walls, reduction_factor=2)
        print(f"représentation  simplifiée de la carte pour {map_name}")
        show_simple_page(simple_map)

        # Créer un objet Map
        self.maps[map_name] = Map(map_name, tmx_data, simple_map, walls, group, portals, npcs)

    def teleport_npcs(self):
        for map_name in self.maps:
            print(f"Je traite le monde {map_name}")
            for npc in self.maps[map_name].npcs:
                print(f"Je téléporte {npc.name}")
                npc.calculate_then_teleport(self)


    def teleport_player(self, player_name):
        point = self.get_object(player_name)
        self.player.position[0] = point.x - 16
        self.player.position[1] = point.y - 32  # pour régler le niveau des pieds.
        self.player.save_location()

    def define_npcs_debuggers(self):
        verbose = False
        for npc in self.maps['garden'].npcs:
            for ar in npc.areas:
                if verbose:
                    print(f"Je traite {ar} pour {npc} de {npc.areas}")
                npc.add_indic('green', ar, 3)

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
            # fix BUG_SAUT : Ne reculer que si le sprite est un Player, pas un NPC
            # if isinstance(my_sprite, Player):
            if my_sprite.name == "player":
                if my_sprite.feet.collidelist(self.get_walls()) > -1:
                    my_sprite.move_back()

            if isinstance(my_sprite, Coin):
                coin = my_sprite
                if self.player.feet.colliderect(coin):
                    if coin.never_touched:
                        if verbose:
                            print(f"Miam ! {coin.value} points !!")
                        self.master_game.point_counter.points += coin.value
                        coin.never_touched = False
                    coin.effect_during_death()

                elif coin.biginning_of_the_end_time:
                    coin.display_its_last_secondes()
                    # coin.kill()

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    # trouver automatiquement le nombre d'objets correspondant à une regex
    # par exemple "paul_path\d"
    def get_object_by_regex(self, a_map, regex):
        """Return objects witch name match with a regex"""
        carte = a_map.tmx_data
        all_objects = carte.objects

        matching_lst = []
        for tiled_object in all_objects:
            if re.match(regex, str(tiled_object.name)):
                obj = self.get_object(tiled_object.name)
                matching_lst.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        return matching_lst

    def update(self):
        """Fonction pour toutes les maps, appelée à chaque image"""
        self.get_group().update()
        self.check_collision()

        # Ici on pourrait gérer les effets sur les coins en train de mourir.

        # Bouger les NPC
        for npc in self.get_map().npcs:
            npc.move()
        pygame.display.flip()

    def draw(self):
        # Dessine la carte
        self.get_group().draw(self.screen)
        # La ligne suivante est à l'origine du décalage de l'affichage du texte.
        # self.get_group().center(self.player.rect.center)  # ??? ref à player ?? adéquat pour NPC
        # On ajoute des indicateurs pour debugger certaines cartes
        if self.current_map == 'world':
            self_maps_world_ = self.maps['world']
            # self_maps_world_.indic.render(self.screen)
            render_world_grid(self.screen, self_maps_world_)
            render_simple_world(self.screen, self_maps_world_)

            for npc in self_maps_world_.npcs:
                for one_indic in npc.indic:
                    one_indic.render(self.screen)


def build_simple_map_from_tmx(tmx_data, walls_block_list, reduction_factor) -> list:
    """Deduce a 2 dimensions array from a tmx map"""
    bin_map = []
    size = tmx_data.tilewidth
    map_w = tmx_data.width * size
    map_h = tmx_data.height * size
    steps = size * reduction_factor
    dec = int(steps / reduction_factor)
    for i, y in enumerate(range(0 + dec, map_h + dec, steps)):
        line_map = []
        for j, x in enumerate(range(0, map_w, steps)):
            # pygame.Rect est ci un très petit carré (presque un point) de position x, y
            # collide list attend des surfaces (Rect) et non pas un point}
            PP = pygame.Rect(x, y, 1, 1)
            if PP.collidelist(walls_block_list) != -1:  # See documentation of colidelist()
                line_map.append(1)
            else:
                line_map.append(0)
        bin_map.append(line_map)

    return bin_map

def show_simple_page(map):
    """
    print a semi-graphicaldisplay of the map

    :param map: a simple map (list of list of (0 or 1)
    :return:
    """
    g_map = []
    for i, row in enumerate(map):
        line = ''
        for j, value in enumerate(row):
            if value == 1:
                translation = 'ZZ'
            elif value == 0:
                translation = '  '
            else:
                print (f"Erreur sur la valeur en rangée ={i}, colonne = {j} : {value}" )
            line += translation
        g_map.append(line)
    pprint(g_map)
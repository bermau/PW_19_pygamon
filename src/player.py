import random
from random import randint
import pygame

from essais.essai_dijkstra_damier import title
from lib_dijkstra import DijkstraManager, Point, pyrect_to_point, point_to_pyrect
from src.lib_drawing_tools import DebugRect

verbose = False


class Entity(pygame.sprite.Sprite):

    def __init__(self, name, x, y, screen=None):
        super().__init__()
        self.name = name
        self.sprite_sheet = pygame.image.load(f'../sprites/{name}.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()  # position du sprite
        self.position = [x, y]
        self.screen = screen if screen else None

        # Mon sprite mesure 32 * 32
        self.images = {
            'down': self.get_image(0, 0),
            'left': self.get_image(0, 32),
            'right': self.get_image(0, 64),
            'up': self.get_image(0, 96)
        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 16)
        self.old_position = self.position.copy()
        self.speed = 2

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, attitude):
        # ('up', 'down', 'left', 'right')
        self.image = self.images[attitude]
        self.image.set_colorkey((0, 0, 0))

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image


class Player(Entity):
    def __init__(self, x, y):
        super().__init__('player', x, y)


class NPC(Entity):
    def __init__(self, name, map_manager, map_name, screen=None):

        super().__init__(name, 500, 550, screen)
        self.name = name  #
        self.change_animation("left")
        self.map_manager = map_manager
        self.map_name = map_name
        self.debug_count = 0
        self.move_direction = None
        self.indic = []  # Liste d'indicateurs de débogage

        # Les zones issues de la carte tmx. Elles sont désignées par un nom de type robin_path1.
        # J'appelle cette zone une area. Elle est de type pygame.Rect
        self.areas = []  # Les areas : liste de pygame.Rect
        self.areas_nb = None
        self.current_area_idx = None  # ndint(0, self.nb_areas-1)  # index de area
        self.next_area_idx = None

        # Entre 2 zones, on définit une promenade / walk. Le chemin de la promenade est trouvé selon un algorithme 
        # simple ou un algorithme de Dijkstra.
        self.use_dijkstra = True

        # les points de la carte simplifiée pour résoudre la promenade/ walk.        
        self.djik = None  # Objet pour résoudre le chemin selon Dijkstra.
        # Les points ci dessous sont utilisé pour guider le mouvement dans la promenade.
        self.prev_point = None  # Le Point d'où lon vient. Sera initialisé par init_dijkstra
        self.next_point = None  # Le Point où l'on va
        self.next_point_rect: pygame.Rect = None  # Son équivalent en pygame.rect
        self.next_dir = None
        # Il faut penser à lancer les méthodes de début après création de NPC:
        # par exemple define_first_target()

    def calculate_next_area_idx(self):
        while True:
            rnd = randint(0, self.areas_nb - 1)
            if rnd != self.current_area_idx:
                self.next_area_idx = rnd
                break

    def modify_speed(self):
        self.speed = self.speed + randint(-1, 1)
        if self.speed == 0:
            self.speed = 1
        elif self.speed == 4:
            self.speed = 3

    def calculate_move_direction(self):
        """Algorithme très primaire. Il a besoin de déterminer la direction générale à prendre."""
        target_point = self.areas[self.next_area_idx].center
        feet_point = self.feet.center

        rect = pygame.Rect(feet_point[0], feet_point[1],
                           target_point[0] - feet_point[0], target_point[1] - feet_point[1])
        x, y, w, h = rect
        if w > 0:
            if h > 0:
                self.move_direction = 'SE'
            else:
                self.move_direction = 'NE'
        else:  # W est neg
            if h > 0:
                self.move_direction = 'SW'
            else:
                self.move_direction = 'NW'
        print(f"Nouvelle cible : {self.next_area_idx}, direction : {self.move_direction}")

    def calculate_dijkstra(self, verbose=False):
        """Lit la carte simplifiée.
        L'algorithme utilise une version réduite de la carte. La réduction est de 1 ou 2 fois la taille des
        tuiles.
        Convertit une zone (area) en un Point de la carte simplifiée.
        Donc, on convertit ce que j'appelais area (zone) en Point
        """
        map = self.map_manager.maps[self.map_name].simple_map
        self.dijk = DijkstraManager(map)

        start_area = self.areas[self.current_area_idx]
        start_point = pyrect_to_point(self.map_manager.maps[self.map_name], start_area, 32)

        next_area = self.areas[self.next_area_idx]
        map_name = self.map_manager.maps[self.map_name]
        end_point = pyrect_to_point(map_name, next_area, 32)

        if verbose:
            print(f"Il faut aller du point {start_point} au point {end_point}")
        self.dijk.dijkstra(start_point, verbose=0)

        self.dijk.format_path(start_point, end_point, verbose=True)

        self.prev_point = start_point
        self.dijk.give_next_instruction()  # IMPORTANT : on élimine la dernière valeur
        self.next_point, self.next_dir = self.dijk.give_next_instruction()
        self.next_point_rect = pygame.Rect(point_to_pyrect(map_name, self.next_point))
        print("Fin de calcul du Dijkstra")
        print(f"{self.next_dir} point_actuel: {self.rect} next_point: {self.next_point} ; next_point_rect : {self.next_point_rect}")

    def define_first_target(self):
        self.current_area_idx = 0  # index de area
        # Pour le run, utiliser ces lignes
        self.calculate_next_area_idx()
        # self.calculate_move_direction()
        # Pour une mise au point, utiliser ces lignes
        # self.next_pyrect_idx = 2
        # self.move_direction = 'SE'

    def teleport_npc(self):
        first_area = self.areas[self.current_area_idx]
        self.position[0] = first_area.x
        self.position[1] = first_area.y
        self.save_location()

    def move(self):
        self.save_location()  # Tentative de résolution d'un GROS BUG
        self.debug_count += 1
        if self.use_dijkstra:
            self.move_dij()
        else:
            self.move_classical()

    def move_dij(self):
        """Mouvement automatique. Algorithme type Djikstra à ma façon.
        Cette fonction est en cours d'écriture"""
        sens = self.next_dir
        if sens == 'R':
            self.move_right()
        elif sens == 'L':
            self.move_left()
        elif sens == 'B':
            self.move_down()
        elif sens == 'T':
            self.move_up()
        elif sens is None:
            pass
        else:
            raise ValueError(f"{sens} : error code letter")

        if self.rect.colliderect(self.next_point_rect):
            print("  ***************         COLISION       **************")
            self.prev_point = self.next_point  # ne sert à rien pour l'instant
            self.next_point, self.next_dir = self.dijk.give_next_instruction()
            if self.next_point:
                self.next_point_rect = pygame.Rect(point_to_pyrect(self.map_name, self.next_point))
            else:
                print("********** Arrivé ! ************")
                # Trouver une nouvelle cible au NPC
                self.current_area_idx = self.next_area_idx
                self.calculate_next_area_idx()
                self.calculate_dijkstra()


        print(f"{self.debug_count}, {sens} actuel : point_actuel: {self.prev_point} rect: {self.rect} next_point: {self.next_point} ; next_point_rect : {self.next_point_rect}")
        print(f"next_dir devient {self.next_dir}")
        pass

    def move_classical(self):
        """Mouvement automatique. Algorithme primaire."""
        feet_rect = self.feet
        target_rect = self.areas[self.next_area_idx]
        feet_to_target_rect = pygame.Rect(feet_rect.x, feet_rect.y,
                                          target_rect.x - feet_rect.x, target_rect.y - feet_rect.y)
        move_vert = None
        move_horz = None
        if self.move_direction == 'SE':
            move_horz = self.move_right
            move_vert = self.move_down
            self.change_animation("right")

        elif self.move_direction == 'NW':
            move_horz = self.move_left
            move_vert = self.move_up
            self.change_animation("left")

        elif self.move_direction == 'SW':
            move_horz = self.move_left
            move_vert = self.move_down
            self.change_animation("left")

        elif self.move_direction == 'NE':
            move_horz = self.move_right
            move_vert = self.move_up
            self.change_animation("right")

        if feet_to_target_rect.height == 0:
            feet_to_target_rect.height = 5
            move_vert()
        else:
            # odd n'est sans doute pas le bon terme.
            try:
                odd_horiz_mvt = feet_to_target_rect.width / (feet_to_target_rect.height + feet_to_target_rect.width)
            except ZeroDivisionError:
                odd_horiz_mvt = 0.95

            if verbose:
                print(f"{feet_to_target_rect}, {self.name} Odd ratio : {odd_horiz_mvt}")

            if odd_horiz_mvt == 0:
                move_vert()
            else:
                rnd = random.random()
                # print(f"La valeur aléatoire est {rnd} ; limite de probabilité vaut {odd_horiz_mvt} : ", end = '')
                if rnd > odd_horiz_mvt:
                    move_vert()
                else:
                    move_horz()

        if self.rect.colliderect(target_rect):
            self.current_area_idx = self.next_area_idx
            self.calculate_next_area_idx()
            self.calculate_move_direction()

    def add_indic(self, *rectpy):
        print(f"Passe ici : ")
        self.indic.append(DebugRect(*rectpy))
import random
import pygame
from random import randint

verbose = False

class Entity(pygame.sprite.Sprite):

    def __init__(self, name, x, y, screen=None):
        super().__init__()
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
    def __init__(self, name, nb_areas, screen=None):

        super().__init__(name, 500, 550, screen)
        self.name = name
        self.change_animation("left")
        self.nb_areas = nb_areas
        self.areas = []  # Les areas : liste de Rect

        self.current_area_idx = randint(0, self.nb_areas-1)  # index de area
        self.next_areas_idx = None
        # self.define_first_target()

    def calculate_next_area_idx(self):

        while True:
            rnd = randint(0, self.nb_areas-1)
            if rnd != self.current_area_idx:
                self.next_areas_idx = rnd
                break
        print(f"La prochaine cible a un indice de {self.next_areas_idx}")
        self.modify_speed()

    def modify_speed(self):
        # modify speed
        self.speed = self.speed + randint(-1, 1)
        if self.speed == 0:
            self.speed = 1
        elif self.speed == 4:
            self.speed = 3

    def calculate_move_direction(self):
        """Mon algorithme est assez primaire. Il a besoin de déterminer la direction générale à prendre."""
        target_point = self.areas[self.next_areas_idx].center
        feet_point = self.feet.center

        rect = pygame.Rect(feet_point[0], feet_point[1],
                           target_point[0] - feet_point[0], target_point[1] - feet_point[1])
        x, y, w, h = rect
        print("Le rectangle est ", x, y, w, h)
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
        print(f"Nouvelle cible : {self.next_areas_idx}, direction : {self.move_direction}")

    def define_first_target(self):
        self.current_area_idx = 0  # index de area
        self.next_areas_idx = 2
        self.move_direction = 'SE'

    def teleport_npc(self):
        first_area = self.areas[self.current_area_idx]
        self.position[0] = first_area.x
        self.position[1] = first_area.y
        self.save_location()

    def load_areas(self, maps_manager):
        """Récupère les objets de la carte qui indiquent la position de passage du NPC, et les transforme en liste de
        pygame. Rect"""
        for num in range(1, self.nb_areas + 1):
            obj = maps_manager.get_object(f'{self.name}_path{num}')
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            self.areas.append(rect)

    def move(self):
        """Mouvement automatique. Algorithme très primaire."""
        feet_rect = self.feet
        target_rect = self.areas[self.next_areas_idx]
        feet_to_target_rect = pygame.Rect(feet_rect.x, feet_rect.y,
                                target_rect.x - feet_rect.x, target_rect.y - feet_rect.y)
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

            if verbose: print(f"{feet_to_target_rect}, {self.name} Odd ratio : {odd_horiz_mvt}")

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
            print(f"NEXT TARGET for {self.name}")
            self.current_area_idx = self.next_areas_idx
            self.calculate_next_area_idx()
            self.calculate_move_direction()

    def rectangular_move(self):
        """Sera appelé à chaque étape : calcul un mouvement automatique du NPC"""
        # current_idx = self.current_area_idx
        # target_idx = self.next_areas_idx

        current_rect = self.areas[self.current_area_idx]
        target_rect = self.areas[self.next_areas_idx]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.change_animation('down')  # 'up', 'down', 'left', 'right'
            self.move_down()
        elif current_rect.y >= target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.change_animation('up')
            self.move_up()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.change_animation('right')
            self.move_right()
        elif current_rect.x >= target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.change_animation('left')
            self.move_left()

        if self.rect.colliderect(target_rect):
            self.calculate_next_area_idx()

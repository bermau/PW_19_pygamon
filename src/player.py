import random

import pygame
from random import randint

TEST = True


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
        self.current_area_idx = 0  # index de area
        self.next_areas_idx = 1
        self.move_direction = 'NW'  # 'N', 'W','E', 'S', 'NW', 'NE', 'SW', 'SE'

        if TEST:
            self.define_test_target()
        #     self.calculate_move_direction()

    def calculate_next_area_idx(self):
        if TEST:
            if self.current_area_idx == 0:
                self.current_area_idx = 2
                self.next_areas_idx = 0
                self.move_direction = 'NW'

            elif self.current_area_idx == 2:
                self.current_area_idx = 0
                self.next_areas_idx = 2
                self.move_direction = 'SE'
            else:
                raise ValueError("Cas pas prévu")

        else:
            # areas is a Rect
            self.current_area_idx += 1
            if self.current_area_idx == self.nb_areas:
                self.current_area_idx = 0
            self.next_areas_idx += 1
            if self.next_areas_idx == self.nb_areas:
                self.next_areas_idx = 0

            # modify speed
            self.speed = self.speed + randint(-1, 1)
            if self.speed == 0:
                self.speed = 1
            elif self.speed == 5:
                self.speed = 4

    def define_test_target(self):
        self.current_area_idx = 0  # index de area
        self.next_areas_idx = 2
        self.move_direction = 'SE'

    def teleport_npc(self):
        first_area = self.areas[0]
        self.position[0] = first_area.x
        self.position[1] = first_area.y
        self.save_location()

    def load_points(self, maps_manager):
        """Récupère les objets de la carte qui indiquent la position de passage du NPC, et les transforme en liste de
        pygame. Rect"""
        for num in range(1, self.nb_areas + 1):
            obj = maps_manager.get_object(f'{self.name}_path{num}')
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            self.areas.append(rect)

    def move(self):
        if TEST:
            current_rect = self.rect
            target_rect = self.areas[self.next_areas_idx]
            main_rect = pygame.Rect(current_rect.x, current_rect.y,
                                    target_rect.x - current_rect.x, target_rect.y - current_rect.y)
            if self.move_direction == 'SE':
                move1 = self.move_right
                move2 = self.move_down
            elif self.move_direction == 'NW':
                move1 = self.move_up
                move2 = self.move_left

            if main_rect.height == 0:
                main_rect.height = 1
                move2()
            else:
                odd_ratio = main_rect.width / main_rect.height
                print(f"{main_rect}, {self.name} Odd ratio : {odd_ratio}")

                if odd_ratio == 0:
                    move2()
                else:
                    prob = 1 / odd_ratio
                    rnd = random.random()
                    print(f"La valeur aléatoire est {rnd} ; prob vaut {prob}")
                    if rnd < prob:
                        move2()
                    else:
                        move1()

            if self.rect.colliderect(target_rect):
                self.calculate_next_area_idx()
                # self.calculate_move_direction()

        else:
            self.rectangular_move()

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

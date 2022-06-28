import pygame
import pyscroll
import pytmx

from player import Player
from src.map import MapManager


class Game:

    def __init__(self):
        pygame.init()
        # créer la fenêtre du jeu

        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Dinosaure aventure")

       # generer un joueur
       #  player_position = tmx_data.get_object_by_name('player')
        self.player = Player(0, 0)
        self.map_manager = MapManager(self.screen, self.player)

        # # rect de collision pour entrer dans la maison
        # enter_house = self.map_manager.  tmx_data.get_object_by_name('enter_house')
        # self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')


    def update(self):
        # self.group.update()
        self.map_manager.update()

        # # Entrée sortie de la maison

        # if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
        if self.map_manager.get_map() == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'
        #
        # # Entrée dans le jardin
        # if self.map == 'house' and self.player.feet.colliderect(self.enter_world_rect):
        #     self.switch_world()
        #     self.map = 'world'


    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()

            self.map_manager.draw()
            pygame.display.flip()
            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    running = False
            clock.tick(60) # nb images /sec
        pygame.quit()
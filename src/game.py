import pygame
from player import Player
from src.map import MapManager
from counter import Counter

class Game:

    def __init__(self):
        pygame.init()

        # créer la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Dinosaure aventure")

        # générer un joueur
        self.player = Player(0, 0)
        # self.single_npc = NPC('robin', 600, 500)

        self.map_manager = MapManager(self, self.screen, self.player,)

        # Un compteur
        self.point_counter = Counter()

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
        self.map_manager.update()

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            self.player.save_location()
            self.handle_input()

            self.map_manager.update()
            self.map_manager.draw()
            self.point_counter.render(self.screen)

            pygame.display.flip()

            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    running = False

            clock.tick(60)  # nb images /sec
        pygame.quit()


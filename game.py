import pygame
import pyscroll
import pytmx

from player import Player


class Game:

    def __init__(self):
        pygame.init()
        # créer venêtre du jeu

        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Dinosaure aventure")
        # Charger les cartes
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1
       # generer un joueur
        player_position = tmx_data.get_object_by_name('player')
        self.player = Player(player_position.x, player_position.y)

        # Dessiner le groupe de calc
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=0)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            print("UP")
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            self.handle_input()
            self.group.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()
            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    running = False
            clock.tick(60) # nb images /sec
        pygame.quit()
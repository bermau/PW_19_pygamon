import pygame

from src.map import MapManager

from player import Player
from counter import Counter
from lib_drawing_tools import DebugRect
import lib_drawing_tools

lib_drawing_tools.display = False


class Game:
    def __init__(self):
        pygame.init()
        # Init le son

        # pygame.mixer.init()

        # Créer la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("La Grande Aventure")
        # Générer un joueur
        self.player = Player(0, 0)
        # Gestionnaire de cartes
        self.map_manager = MapManager(self, self.screen, self.player, verbose=True)
        # Un compteur
        self.point_counter = Counter()
        # Une zone à encadrer pour debugger
        self.game_indic = DebugRect('pink', pygame.Rect(300, 250, 80, 120), 3)  # pour tous les mondes

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
        # Boucle. Arrêt par la fermeture de la fenêtre ou Q. "P" pour pause, puis Esc
        clock = pygame.time.Clock()

        myfont = pygame.font.SysFont("monospace", 32)
        # myfont = pygame.font.Font('../dialogs/dialog_font.ttf', 18)

        pause_text = r"""<Esc> to resume or [Q] to quit."""
        text_pause = myfont.render(pause_text, True, 'purple')

        running, pause = True, False
        while running:
            self.player.save_location()
            self.handle_input()

            self.map_manager.update()
            self.map_manager.draw()
            self.point_counter.render(self.screen)
            self.game_indic.render(self.screen)

            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    running = False
                if even.type == pygame.KEYDOWN and even.key == pygame.K_p:
                    pause = True

                while pause:
                    self.screen.blit(text_pause, (50, 400))
                    pygame.display.flip()

                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT or ev.type == pygame.KEYDOWN and ev.key == pygame.K_q:
                            pause = False
                            running = False
                        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                            pause = False
                        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_p:
                            pause = True

            pygame.display.flip()
            clock.tick(60)  # nb images /sec
        pygame.quit()

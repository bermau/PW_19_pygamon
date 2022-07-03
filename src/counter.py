import pygame


class Counter:

    X_POS = 700
    Y_POS = 50

    def __init__(self):
        self.box = pygame.image.load('../dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (100, 50))
        self.text = "000"
        self.points = 0
        # J'ai été obligé d'ajouter cette ligne, sinon les fonts ne sont pas initialisés.
        pygame.font.init()
        self.font = pygame.font.Font('../dialogs/dialog_font.ttf', 18)

    def render(self, screen):
        screen.blit(self.box, (self.X_POS, self.Y_POS))
        text = self.font.render("{:05}".format(self.points), False, (0, 0, 0))
        screen.blit(text, (self.X_POS + 20, self.Y_POS + 5 ))



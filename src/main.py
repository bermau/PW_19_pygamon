import pygame

from game import Game

import os
print(os.getcwd())

if __name__ == '__main__':
    pygame.init()

    my_game = Game()
    my_game.run()


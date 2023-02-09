import pygame
import player
from game import Game


import os
print(os.getcwd())

if __name__ == '__main__':
    pygame.init()

    my_game = Game()

    print(f"player.screen vaut {player.SCREEN}")
    my_game.run()


"""Lancement du jeu en 2D"""

import pygame
# from logging_config import setup_logging
from game import Game

import os
import logging

# Configuration du logging (une seule fois)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../pygame.log', mode= 'w'),
        logging.StreamHandler()  # Pour afficher aussi dans la console
    ]
)

# # Désactiver ou limiter les logs de pyscroll et autres bibliothèques
# logging.getLogger('pyscroll').setLevel(logging.WARNING)  # Ne log que WARNING et plus
#

# Désactiver TOUS les logs qui ne sont pas les vôtres
# Mettre le root logger à WARNING
logging.getLogger().setLevel(logging.WARNING)

# Puis réactiver DEBUG uniquement pour VOS modules
logging.getLogger(__name__).setLevel(logging.DEBUG)
# Si vous avez d'autres modules à vous :
logging.getLogger('game').setLevel(logging.DEBUG)
logging.getLogger('map').setLevel(logging.DEBUG)
logging.getLogger('lib_dijkstra').setLevel(logging.DEBUG)

if __name__ == '__main__':
    # setup log
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Démarrage du LOG dans {logger}")
    logger.info(f"cwd ={os.getcwd()}")

    # setup game
    pygame.init()
    my_game = Game()
    my_game.run()


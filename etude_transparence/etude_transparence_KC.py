import pygame
import pytmx

# Initialiser pygame
pygame.init()


# Créer la fenêtre du jeu
# screen = pygame.display.set_mode((800, 800))
# pygame.display.set_caption("La Grande Aventure")

tiles_in_pixels = 16
width=15
height=20

# Créer la fenêtre
screen = pygame.display.set_mode((width * tiles_in_pixels,
                                  height * tiles_in_pixels))
pygame.display.set_caption("Carte TMX")

# Charger la carte TMX
tmx_data = pytmx.load_pygame("cartes/monde.tmx")


# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessiner la carte
    screen.fill((0, 0, 0))

    print(tmx_data.layers)

    for layer in tmx_data.visible_layers:
        for x, y, image in layer:
            screen.blit(image, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

    pygame.display.flip()

pygame.quit()
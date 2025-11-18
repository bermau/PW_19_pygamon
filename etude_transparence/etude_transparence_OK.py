# affiche_tmx.py
import sys
import pygame
from pytmx.util_pygame import load_pygame
from pytmx import TiledTileLayer

pygame.init()
FPS = 60
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# Nom du fichier TMX (même dossier)
TMX_FILE = "cartes/monde.tmx"

# Chargement de la carte (les images référencées dans le TMX sont chargées automatiquement)
tmx = load_pygame(TMX_FILE)

# Taille totale de la carte en pixels
map_w = tmx.width * tmx.tilewidth
map_h = tmx.height * tmx.tileheight

# Pré-rendu de la carte sur une surface (simple et rapide pour affichage)
map_surface = pygame.Surface((map_w, map_h)
                             , pygame.SRCALPHA
                             )

print(list(tmx.visible_layers))

for layer in tmx.visible_layers:
    print(f"Je traite le layer {layer}")
    if isinstance(layer, TiledTileLayer):
        print("Ce layer est à dessiner")
        # pytmx rend un TiledTileLayer itérable
        for i, (x, y, gid) in enumerate(layer):
            tile = tmx.get_tile_image_by_gid(gid)
            if tile :
                # La ligne ci-dessous montre que les tiles fautifs ont un colorkey à (255, 255, 255, 255).

                print("gid", gid, "alpha:", tile.get_alpha(), "colorkey:", tile.get_colorkey(), "has per-pixel alpha?:",
                          tile.get_masks() != (0, 0, 0, 0))
                col_k = tile.get_colorkey()
                tile = tile.convert()
                tile.set_colorkey([col_k])
                print("gid", gid, "alpha:", tile.get_alpha(), "colorkey:", tile.get_colorkey(), "has per-pixel alpha?:",
                          tile.get_masks() != (0, 0, 0, 0))

                map_surface.blit(tile, (x * tmx.tilewidth, y * tmx.tileheight))

# Caméra / décalage pour scroller
cam_x, cam_y = 0, 0
SCROLL_SPEED = 400  # pixels / seconde

def clamp(val, minv, maxv):
    return max(minv, min(maxv, val))

running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # secondes écoulées depuis la frame précédente
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Déplacement caméra avec flèches (ou WASD)
    keys = pygame.key.get_pressed()
    vx = vy = 0
    if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
        vx = -SCROLL_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        vx = SCROLL_SPEED
    if keys[pygame.K_UP]    or keys[pygame.K_w]:
        vy = -SCROLL_SPEED
    if keys[pygame.K_DOWN]  or keys[pygame.K_s]:
        vy = SCROLL_SPEED

    cam_x += vx * dt
    cam_y += vy * dt

    # Limiter la caméra pour ne pas sortir de la carte
    cam_x = clamp(cam_x, 0, max(0, map_w - SCREEN_W))
    cam_y = clamp(cam_y, 0, max(0, map_h - SCREEN_H))

    # Affichage
    screen.fill((0, 0, 0))
    screen.blit(map_surface, (-int(cam_x), -int(cam_y)))
    pygame.display.flip()

pygame.quit()
sys.exit()

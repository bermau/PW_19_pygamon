import pygame




class Entity(pygame.sprite.Sprite):

    def __init__(self, name,  x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'../sprites/{name}.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()  # position du sprite
        self.position = [x, y]

        # Mon sprite mesure 32 * 32
        self.images = {
            'down': self.get_image(0, 0),
            'left': self.get_image(0, 32),
            'right': self.get_image(0, 64),
            'up': self.get_image(0, 96)
        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 16)
        self.old_position = self.position.copy()
        self.speed = 2

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey((0, 0, 0))

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed
        print(self.position[1])

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image


class Player(Entity):
    def __init__(self,  x, y):
        super().__init__('player', x, y)


class NPC(Entity):
    def __init__(self, name, nb_points):
        super().__init__(name, 500, 550)
        self.name= name
        self.change_animation("left")
        self.nb_points = nb_points
        self.points = []
        self.current_point = 0

    def teleport_npc(self):
        premier_point = self.points[self.current_point]

        self.position[0] = premier_point.x
        self.position[1] = premier_point.y
        self.save_location()

    def load_points(self, maps_manager):
        """Récupères les objets de la carte qui indiquent la position de passage du NPC, et les transforme en liste de
        pygame.Rect"""
        for num in range(1, self.nb_points+1):
            obj= maps_manager.get_object(f'{self.name}_path{num}')
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            self.points.append(rect)

    def move(self):
        """Sera appelé à chaque étape : calcul un mouvement automatique du NPC"""
        current_point = self.current_point
        target_point = current_point + 1

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]
        print(self.position[0], self.position[1])
        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y >= target_rect.y and abs(current_rect.x - target_rect.x)< 3:
            self.move_up()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y)< 3:
            self.move_right()
        elif current_rect.x >= target_rect.x and abs(current_rect.y - target_rect.y)< 3:
            self.move_left()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point
        if self.current_point == self.nb_points -1:
            self.current_point = 1









# Define the Bird class
import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        # Initialize properties
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [0, 0]
        self.dragging = False
        self.drag_start_pos = (0, 0)

    def update(self):
        # Update bird's position based on dragging or velocity
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.centerx = mouse_pos[0]
            self.rect.centery = mouse_pos[1]
        else:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]    

    def start_drag(self):
        # Start dragging the bird
        self.dragging = True
        self.drag_start_pos = self.rect.center

    def end_drag(self):
        # Release the bird and set its velocity based on drag direction
        self.dragging = False
        mouse_pos = pygame.mouse.get_pos()
        # Gives the angle of line connecting
        direction = math.atan2(self.drag_start_pos[1] - mouse_pos[1], 
                               self.drag_start_pos[0] - mouse_pos[0])
        speed = 10

        # Determines both the speed and the direction in which the bird travels
        self.velocity = [speed * math.cos(direction), 
                         speed * math.sin(direction)]
        
    def hit_enemy(self):
        return 100

# Define the Button class
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, action):
        super().__init__()
        # Initialize properties
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

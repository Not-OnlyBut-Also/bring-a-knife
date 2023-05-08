import pygame
from game import constant, startup
import random
import math

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[startup.VISIBLE]):
        super().__init__(groups)
        self.sheet = startup.PARTICLE_SHEET
        self.image = self.sheet[random.choice(range(len(self.sheet)))]
        self.rect = self.image.get_rect(center=pos)
        self.angle = random.choice(range(-181, 0))
        self.speed = random.choice(range(1, 11))
        self.gravity = 1
        self.move_x = self.speed * math.cos(math.radians(self.angle))
        self.move_y = self.speed * math.sin(math.radians(self.angle))
        self.lifetime = random.choice(range(2, 16))
        self.life_lived = 0
    def update(self):
        if self.life_lived <= self.lifetime:
            self.rect.x += self.move_x
            self.rect.y += self.move_y
            self.move_y += self.gravity
            self.life_lived += 1
        else:
            self.kill()
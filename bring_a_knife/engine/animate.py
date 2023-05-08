import pygame
from game import constant

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, pos, sheet, state, groups, animations):
        super().__init__(groups)
        self.animations = animations
        self.state = state
        self.sheet = sheet
        self.flipped = False
        self.frame = self.animations[self.state]["frames"][0]
        self.cycle = 0
        self.image = self.sheet[self.frame]
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
    def update(self):
        self.animate()
    def animate(self):
        if self.cycle % (constant.FPS // self.animations[self.state]["speed"]) == 0:
            if self.frame > self.animations[self.state]["frames"][1]:
                self.frame = self.animations[self.state]["frames"][0]
                if "on end" in self.animations[self.state]:
                    for action in self.animations[self.state]["on end"]:
                        action()
            self.image = self.sheet[self.frame]
            self.flip()
            self.frame += 1
        self.cycle += 1
    def set_state(self, state, flipped=False):
        if self.state != state or self.flipped != flipped:
            self.flipped = flipped
            self.state = state
            self.frame = self.animations[self.state]["frames"][0]
            self.image = self.sheet[self.frame]
            self.flip()
            self.cycle = 0
    def flip(self):
        if self.flipped == True:
            self.image = pygame.transform.flip(self.image, True, False)
import pygame
from game import constant, startup

class UiBar(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[startup.UI]):
        super().__init__(groups)
        self.image = pygame.surface.Surface((0, constant.HEIGHT))
        self.image.fill(constant.GRAY_BLUE)
        self.rect = self.image.get_rect(topleft=pos)
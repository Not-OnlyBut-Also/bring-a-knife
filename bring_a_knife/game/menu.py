import pygame
from game import constant, startup, king_scene
from engine import state, text

class Menu(state.State):
    def __init__(self, screen=startup.DISPLAY):
        startup.MUSIC_CHANNEL.stop()
        super().__init__(screen)
        self.next_state = king_scene.KingScene
        self.next_args = [0]
        self.title = Title((
            constant.WIDTH // 2,
            constant.HEIGHT // 2))
        self.text = text.Text(
            (constant.WIDTH // 2,
            constant.HEIGHT // 2 + self.title.image.get_height() // 2 + 32),
            "Press ENTER to Start",
            constant.WIDTH,
            typed=False,
            pulse =True)
        self.key_held = True
    def update(self):
        super().update()
        self.text.update()
        if pygame.key.get_pressed()[pygame.K_RETURN] and self.key_held == False:
            self.key_held = True
            self.next = True
        elif self.key_held == True and not pygame.key.get_pressed()[pygame.K_RETURN]:
            self.key_held = False

class Title(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[startup.VISIBLE]):
        super().__init__(groups)
        self.image = startup.TITLE_IMG
        self.rect = self.image.get_rect(center=pos)
import pygame
from game import constant, startup, player, menu
from engine import state, text

class WinScreen(state.State):
    def __init__(self, screen=startup.DISPLAY):
        super().__init__(screen)
        self.next_state = menu.Menu
        self.key_held = False
        self.congrats = text.Text(
            (self.screen.get_width() // 2,
            self.screen.get_height() // 2),
            "CONGRATS!",
            constant.WIDTH,
            typed=False,
            pulse=True)
        self.message = text.Text(
            (self.screen.get_width() // 2,
            self.screen.get_height() // 2 + self.congrats.height + 4),
            "You killed everyone.",
            constant.WIDTH,
            typed=False)
        self.nothing = text.Text(
            (self.screen.get_width() // 2,
            self.screen.get_height() // 2 + self.congrats.height + 4 + self.message.height + 4),
            "You are king of nothing.",
            constant.WIDTH,
            typed=False)
        self.player = player.Player(
            None,
            (self.screen.get_width() // 2,
            self.screen.get_height() // 2 + self.congrats.height + 4 + self.message.height + 4 + self.nothing.height + 4),
            cutscene=True)
    def check_entered(self):
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            if self.key_held == False:
                self.next = True
        elif self.key_held == True:
            self.key_held = False
    def update(self):
        super().update()
        self.congrats.update()
        self.check_entered()
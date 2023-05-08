import pygame
import asyncio
from game import constant, startup

class Game:
    def __init__(self, title, screen_size, bg, fps):
        pygame.init()
        pygame.mixer.init(channels=3)
        self.screen = pygame.display.set_mode(screen_size)
        startup.init()
        self.display = startup.DISPLAY
        pygame.display.set_caption(title)
        self.bg = bg
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.states = startup.STATES
        self.current_state = "menu"
        self.active = self.states[self.current_state]()
        self.running = True
    async def run(self):
        while self.running == True:
            if self.active.next == True:
                self.active = self.active.move_on()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(constant.BG)
            self.screen.blit(self.display, (startup.DISPLAY_X, startup.DISPLAY_Y))
            self.display.fill(constant.BG)
            self.active.update()
            startup.SPECIAL_EFFECT.draw(self.screen)
            startup.SPECIAL_EFFECT.update()
            pygame.display.update()
            await asyncio.sleep(0)
            self.clock.tick(self.fps)
        pygame.quit()
    def set_state(self, state):
        self.current_state = state
        self.active = self.states[self.current_state]()

if __name__ == "__main__":
    game = Game(
        constant.TITLE,
        (
            constant.WIDTH + constant.MARGIN_X * 2,
            constant.HEIGHT + constant.MARGIN_Y * 2),
        constant.BG,
        constant.FPS)
    asyncio.run(game.run())
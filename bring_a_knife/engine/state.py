from game import constant, startup
import random

class State:
    def __init__(self, screen=startup.DISPLAY):
        self.screen = screen
        self.next_state = None
        self.next_args = []
        self.next = False
        self.shake_timer = None
    def update(self):
        startup.VISIBLE.draw(self.screen)
        startup.VISIBLE.update()
        if self.shake_timer != None:
            self.shake()
    def shake(self, shake_time=10):
        if self.shake_timer == None:
            self.shake_timer = shake_time
        if self.shake_timer > 0:
            startup.DISPLAY_X += random.choice((range(-3, 3)))
            startup.DISPLAY_Y += random.choice((range(-3, 3)))
            self.shake_timer -= 1
        else:
            startup.DISPLAY_X, startup.DISPLAY_Y = constant.MARGIN_X, constant.MARGIN_Y
            self.shake_timer = None
    def kill(self):
        for sprite in startup.VISIBLE:
            sprite.kill()
    def move_on(self):
        self.kill()
        return self.next_state(*self.next_args)
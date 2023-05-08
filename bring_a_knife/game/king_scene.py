import pygame
from game import startup, constant, enemy, board, win_screen
from engine import state, animate, text
import json

class KingScene(state.State):
    def __init__(self, round_number=0, screen=startup.DISPLAY):
        super().__init__(screen)
        self.next_state = board.Board
        self.next_args = [round_number]
        self.king = enemy.King(
            None,
            (self.screen.get_width() // 2,
            self.screen.get_height() // 2),
            "-",
            state="idle_unarmed",
            cutscene=True)
        self.king.rect.center = self.king.pos
        self.dialogue_file = open("data/kings_speech.json", "r")
        self.round_number = round_number
        self.second_to_last = False
        self.last = False
        try:
            all_dialogue = json.load(self.dialogue_file)
            self.dialogue = all_dialogue[self.round_number]
            self.line = 0
            self.wrap = 400
            self.text = text.Text(
                (self.screen.get_width() // 2,
                self.screen.get_height() // 2 + self.king.image.get_height() // 2),
                self.dialogue[self.line],
                self.wrap)
            if self.round_number == len(all_dialogue) - 2:
                startup.MUSIC_CHANNEL.stop()
                self.second_to_last = True
            elif self.round_number == len(all_dialogue) - 1:
                self.last = True
        except:
            self.text = None
            self.next_state = win_screen.WinScreen
            self.next_args = []
            self.next = True
        self.dialogue_file.close()
        self.key_held = True
        self.flash = None
    def update(self):
        super().update()
        if self.text != None and self.flash == None:
            self.text.update()
            self.check_entered()
        elif self.flash != None:
            self.play_flash()
    def check_entered(self):
        if self.key_held == False and pygame.key.get_pressed()[pygame.K_RETURN]:
            self.key_held = True
            if self.text.done == True:
                self.text.kill()
                if self.last == True and self.line == len(self.dialogue) - 2:
                    self.play_flash()
                elif self.line < len(self.dialogue) - 1:
                    self.line += 1
                    self.text = text.Text(
                        (self.screen.get_width() // 2,
                        self.screen.get_height() // 2 + self.king.image.get_height() // 2),
                        self.dialogue[self.line],
                        self.wrap)
                else:
                    self.next = True
                    if self.second_to_last == True:
                        startup.MUSIC_CHANNEL.stop()
                        startup.MUSIC_CHANNEL.play(startup.BOSS_MUSIC)
            else:
                self.text.complete()
        elif self.key_held == True and not pygame.key.get_pressed()[pygame.K_RETURN]:
            self.key_held = False
    def play_flash(self):
        if self.flash == None:
            self.shake(20)
            self.flash = Flash()
            startup.SFX_CHANNEL.play(startup.DEROBE_SOUND)
        elif self.flash.count > 0 and self.king.state != "idle_derobed":
            self.king.set_state("idle_derobed")
        elif self.flash.done == True:
            self.flash.kill()
            self.line += 1
            self.text = text.Text(
                (self.screen.get_width() // 2,
                self.screen.get_height() // 2 + self.king.image.get_height() // 2),
                self.dialogue[self.line],
                self.wrap)
            self.flash = None

class Flash(pygame.sprite.Sprite):
    def __init__(self, groups=[startup.SPECIAL_EFFECT]):
        super().__init__(groups)
        self.image = pygame.Surface(
            (constant.WIDTH + constant.MARGIN_X * 2,
            constant.HEIGHT + constant.MARGIN_Y * 2))
        self.image.fill(constant.WHITE)
        self.alpha = 0
        self.image.set_alpha(self.alpha)
        self.pos = (self.image.get_width() // 2, self.image.get_height() // 2)
        self.rect = self.image.get_rect(center=self.pos)
        self.count = 0
        self.stay_flashed = constant.FPS // 5
        self.done = False
    def update(self):
        self.flash()
    def flash(self):
        if self.alpha < 255 and self.count <= 0:
            self.alpha += 15
            self.image.set_alpha(self.alpha)
        elif self.count < self.stay_flashed:
            self.count += 1
        elif self.count == self.stay_flashed and self.alpha > 0:
            self.alpha -= 15
            self.image.set_alpha(self.alpha)
        elif self.count == self.stay_flashed:
            self.done = True
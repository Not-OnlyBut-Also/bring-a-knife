import pygame
from game import constant, startup
import random

class Text:
    def __init__(self, pos, text, wrap, typed=True, pulse=False, color=constant.WHITE, font=startup.FONT):
        self.font = font
        self.text = text
        self.lines = []
        words = self.text.split(" ")
        built_line = ""
        line_pos = (pos[0], pos[1])
        for word in words:
            if built_line == "":
                addition = word
            else:
                addition = " " + word
            if self.font.size(built_line + addition)[0] > wrap:
                self.lines.append(Line(line_pos, built_line, typed=typed, color=color, font=font))
                line_pos = (line_pos[0], line_pos[1] + self.font.size(built_line)[1] + 4)
                built_line = ""
                addition = word
            built_line += addition
        if built_line != "":
            self.lines.append(Line(line_pos, built_line, typed=typed, color=color, font=font))
        self.width = 0
        self.height = 0
        for line in self.lines:
            if self.font.size(line.text)[0] > self.width:
                self.width = self.font.size(line.text)[0]
            self.height += self.font.size(line.text)[1]
        self.typed = typed
        self.line_index = 0
        self.done = not self.typed
        self.pulse = pulse
    def update(self):
        if self.typed == True and self.line_index < len(self.lines):
            if self.lines[self.line_index].done == False:
                self.lines[self.line_index].type_out()
            else:
                self.line_index += 1
        elif self.typed == True:
            self.done = True
        if self.pulse == True:
            for line in self.lines:
                line.pulse()
    def complete(self):
        for line in self.lines:
            if line.done == False:
                line.complete()
    def change_layer(self, layer):
        for line in self.lines:
            startup.VISIBLE.change_layer(line, layer)
    def kill(self):
        for line in self.lines:
            line.kill()

class Line(pygame.sprite.Sprite):
    def __init__(self, pos, text, typed=True, color=constant.WHITE, font=startup.FONT, groups=[startup.VISIBLE]):
        super().__init__(groups)
        self.font = font
        self.text = text
        self.index = len(self.text)
        self.done = True
        if typed == True:
            display_text = ""
            self.index = -1
            self.done = False
        else:
            display_text = self.text
        self.color = color
        self.image = self.font.render(display_text, False, self.color)
        self.pos = pos
        self.rect = self.font.render(self.text, False, self.color).get_rect(center=pos)
        self.alpha = 255
        self.direction = -25
    def type_out(self):
        if self.index < len(self.text):
            startup.SFX_CHANNEL.play(random.choice(startup.TALK_SOUNDS))
            self.index += 1
            self.image = self.font.render(self.text[0:self.index], False, self.color)
            self.rect = self.image.get_rect(center=self.pos)
        else:
            self.done = True
    def complete(self):
        self.index = len(self.text)
        self.image = self.font.render(self.text[0:self.index], False, self.color)
        self.rect = self.image.get_rect(center=self.pos)
        self.done = True
    def pulse(self):
        if (
            self.alpha <= 150
            and self.direction < 0
            or self.alpha >= 255
            and self.direction > 0
        ):
            self.direction = -self.direction
        self.alpha += self.direction
        self.image.set_alpha(self.alpha)
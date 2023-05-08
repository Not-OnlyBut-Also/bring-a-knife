import pygame
import math
from game import constant, startup

class Bullet(pygame.sprite.Sprite):
    def __init__(self, board, pos, direction, color="gray", speed=constant.TILE_SIZE, groups=[startup.VISIBLE, startup.BULLETS]):
        self.board = board
        if not startup.SHOOT_CHANNEL.get_busy():
            startup.SHOOT_CHANNEL.play(startup.SHOOT_SOUND)
        super().__init__(groups)
        startup.VISIBLE.change_layer(self, 3)
        self.sheet = startup.BULLET_SHEET
        self.colors = {
            "blue" : 0,
            "yellow" : 2,
            "red" : 4,
            "green" : 6,
            "purple" : 8,
            "gray" : 10
        }
        self.color = self.colors[color]
        self.image = self.sheet[self.color]
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.move_x, self.move_y = self.rect.topleft
        self.spd = speed
        self.direction = direction
        self.speed = (
            self.spd * self.direction[0],
            self.spd * self.direction[1])
        self.count = 0
        self.face_direction()
    def update(self):
        if self.count == constant.FPS // 3:
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]
            self.count = 0
        self.count += 1
        if (
            self.rect.x < self.board.left_bound
            or self.rect.x > self.board.right_bound
            or self.rect.y < self.board.upper_bound
            or self.rect.y > self.board.lower_bound
        ):
            self.kill()
    def face_direction(self):
        if (
            0 not in self.speed
            and abs(self.speed[0]) == abs(self.speed[1])
            and self.color % 2 == 0
        ):
            self.color += 1
            self.image = self.sheet[self.color]
        if self.speed[0] < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.color % 2 == 0:
            if self.speed[1] < 0:
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.speed[1] > 0:
                self.image = pygame.transform.rotate(self.image, 270)
        else:
            if self.speed[1] > 0:
                self.image = pygame.transform.flip(self.image, False, True)

class Laser(Bullet):
    def __init__(self, board, shooter, pos, direction, color="gray", groups=[startup.VISIBLE, startup.BULLETS]):
        super().__init__(board, pos, direction, color=color, groups=groups)
        self.groups = groups
        startup.VISIBLE.change_layer(self, 2)
        self.shooter = shooter
        self.sheet = startup.LASER_SHEET
        self.colors = {
            "blue" : 1,
            "yellow" : 4,
            "red" : 7,
            "green" : 10,
            "purple" : 13,
            "gray" : 16
        }
        self.color_code = color
        self.color = self.colors[self.color_code]
        self.image = self.sheet[self.color]
        self.rect = self.image.get_rect(topleft=self.pos)
        self.parts = []
        self.first = False
        self.last = False
        self.ended = False
        self.change_based_on_pos()
        self.face_direction()
    def update(self):
        if self.first == True:
            if self.count == 1 and self.ended == False:
                self.parts.append(Laser(
                    self.board,
                    self.shooter,
                    (self.pos[0] + constant.TILE_SIZE * self.direction[0] * (len(self.parts) + 1),
                    self.pos[1] + constant.TILE_SIZE * self.direction[1] * (len(self.parts) + 1)),
                    self.direction,
                    color=self.color_code,
                    groups=self.groups))
                self.count = 0
                self.check_ended()
            elif self.ended == True:
                if self.count == constant.FPS:
                    self.kill()
            self.count += 1
    def face_direction(self):
        if self.direction[0] == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.direction[1] == -1:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction[1] == 1:
            self.image = pygame.transform.rotate(self.image, 270)
    def change_based_on_pos(self):
        if (
            self.rect.topleft[0] == self.shooter.rect.topleft[0] + constant.TILE_SIZE * self.direction[0]
            and self.direction[0] != 0
            or self.rect.topleft[1] == self.shooter.rect.topleft[1] + constant.TILE_SIZE * self.direction[1]
            and self.direction[1] != 0
        ):
            self.image = self.sheet[self.color - 1]
            self.first = True
        elif (
            self.rect.topleft[0] == self.board.right_bound and self.shooter.rect.topleft[0] != self.board.right_bound
            or self.rect.topleft[0] == self.board.left_bound and self.shooter.rect.topleft[0] != self.board.left_bound
            or self.rect.topleft[1] == self.board.lower_bound and self.shooter.rect.topleft[1] != self.board.lower_bound
            or self.rect.topleft[1] == self.board.upper_bound and self.shooter.rect.topleft[1] != self.board.upper_bound
        ):
            self.image = self.sheet[self.color + 1]
            self.last = True
    def check_ended(self):
        for part in self.parts:
            if part.last == True:
                self.ended = True
    def kill(self):
        if self.first == True:
            for part in self.parts:
                part.kill()
        super().kill()
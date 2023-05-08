import pygame
from game import constant, startup, bullet
from engine import animate, particle

class Player(animate.AnimatedSprite):
    def __init__(self, board, pos, none=None, cutscene=False, groups=[startup.VISIBLE, startup.PLAYER]):
        self.board = board
        super().__init__(pos, startup.PLAYER_SHEET, "idle", groups,
            {
                "idle" : {
                    "frames" : [0, 4],
                    "speed" : 15
                },
                "idle_crowned" : {
                    "frames" : [6, 10],
                    "speed" : 15
                }
            }
        )
        self.cutscene = cutscene
        if self.cutscene == True:
            self.set_state("idle_crowned")
            self.rect = self.image.get_rect(center=(pos[0], pos[1] + self.image.get_height() // 2))
        self.key_held = 0
        self.held_speed = constant.FPS // 5
        self.blood_count = 40
    def update(self):
        super().update()
        if self.cutscene == False:
            if self.board.started >= self.board.start:
                self.move()
                self.stab()
                self.shot()
    def move(self):
        pressed = pygame.key.get_pressed()
        if (
            pressed[pygame.K_RIGHT]
            and self.key_held == 0
            and self.rect.left < self.board.right_bound
        ):
            self.rect.x += constant.TILE_SIZE
            self.key_held = self.held_speed
            self.flipped = False
        elif (
            pressed[pygame.K_LEFT]
            and self.key_held == 0
            and self.rect.left > self.board.left_bound
        ):
            self.rect.x -= constant.TILE_SIZE
            self.key_held = self.held_speed
            self.flipped = True
        elif (
            pressed[pygame.K_UP]
            and self.key_held == 0
            and self.rect.top > self.board.upper_bound
        ):
            self.rect.y -= constant.TILE_SIZE
            self.key_held = self.held_speed
        elif (
            pressed[pygame.K_DOWN]
            and self.key_held == 0
            and self.rect.top < self.board.lower_bound
        ):
            self.rect.y += constant.TILE_SIZE
            self.key_held = self.held_speed
        elif (
            self.key_held > 0
            and not pressed[pygame.K_RIGHT]
            and not pressed[pygame.K_LEFT]
            and not pressed[pygame.K_UP]
            and not pressed[pygame.K_DOWN]
        ):
            self.key_held = 0
        elif self.key_held > 0:
            self.key_held -= 1
    def stab(self):
        enemy_stabbed = pygame.sprite.spritecollideany(self, startup.ENEMIES)
        if enemy_stabbed != None:
            enemy_stabbed.stabbed()
    def shot(self):
        bullet_hit = pygame.sprite.spritecollideany(self, startup.BULLETS)
        if bullet_hit != None:
            if type(bullet_hit) is bullet.Bullet:
                bullet_hit.kill()
            for num in range(self.blood_count):
                particle.Particle(self.rect.center)
            startup.SFX_CHANNEL.play(startup.SHOT_SOUND)
            self.board.shake()
            self.kill()
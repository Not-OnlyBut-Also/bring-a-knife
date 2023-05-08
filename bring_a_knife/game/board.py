import pygame
from game import constant, startup
from game import player, enemy, king_scene
from engine import state, text

class Board(state.State):
    def __init__(self, round_number=0, screen=startup.DISPLAY, board_data=constant.BOARDS):
        if startup.MUSIC_CHANNEL.get_busy() == False:
            startup.MUSIC_CHANNEL.play(startup.BOARD_MUSIC, loops=-1)
        super().__init__(screen)
        self.next_state = Board
        self.next_args = [round_number]
        self.started = 0
        self.start = 25
        self.countdown = Countdown()
        self.end_timer = -1
        self.key_held = True
        self.skip_held = True
        self.data_dict = {
            "9" : player.Player,
            "T" : enemy.ThreeShooter,
            "B" : enemy.Bubblegun,
            "G" : enemy.Ghoulie,
            "P" : enemy.Pollineer,
            "S" : enemy.Smiley,
            "M" : enemy.Majesty,
            "H" : enemy.Hotlips,
            "K" : enemy.King
        }
        self.upper_bound, self.lower_bound, self.left_bound, self.right_bound = None, None, None, None
        self.round_number = round_number
        self.board_data = board_data[self.round_number]
        self.diff_x = ((self.screen.get_width() - 4) - len(self.board_data[0].split(" ")) * constant.TILE_SIZE) // 2
        self.diff_y = ((self.screen.get_height() - 4) - len(self.board_data) * constant.TILE_SIZE) // 2
        for row_index in range(len(self.board_data)):
            items = self.board_data[row_index].split(" ")
            for col_index in range(len(items)):
                x = col_index * constant.TILE_SIZE + self.diff_x
                y = row_index * constant.TILE_SIZE + self.diff_y
                Tile((x, y))
                if row_index == 0 and self.upper_bound == None:
                    self.upper_bound = y
                elif row_index == len(self.board_data) - 1 and self.lower_bound == None:
                    self.lower_bound = y
                if col_index == 0 and self.left_bound == None:
                    self.left_bound = x
                elif col_index == len(items) - 1 and self.right_bound == None:
                    self.right_bound = x
                col = items[col_index]
                move = col[1]
                for key in self.data_dict:
                    if key in col:
                        self.data_dict[key](self, (x, y), move)
    def update(self):
        super().update()
        if pygame.key.get_pressed()[pygame.K_r]:
            if self.key_held == False:
                self.next = True
                self.round_number -= 1
        elif self.key_held == True:
            self.key_held = False
        self.skip()
        if len(list(startup.ENEMIES)) == 0  or len(list(startup.PLAYER)) == 0:
            if self.end_timer < 0:
                self.end_timer = self.start
        if self.started < self.start:
            self.started += 1
            if self.started % 8 == 0:
                self.countdown.count()
                startup.SFX_CHANNEL.play(startup.COUNTDOWN_SOUNDS[self.started // 8 - 1])
        elif self.started == self.start:
            self.started += 1
            self.countdown.kill()
        if self.end_timer > 0:
            self.end_timer -= 1
        elif self.end_timer == 0:
            if len(list(startup.ENEMIES)) == 0:
                self.next_state = king_scene.KingScene
                self.next_args = [self.round_number + 1]
                self.next = True
            elif len(list(startup.PLAYER)) == 0:
                self.next = True
    def skip(self):
        if pygame.key.get_pressed()[pygame.K_s]:
            if self.skip_held == False:
                for baddy in startup.ENEMIES:
                    if type(baddy) != enemy.King:
                        baddy.stabbed()
        elif self.skip_held == True:
            self.skip_held = False

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups=[startup.VISIBLE, startup.TILES]):
        super().__init__(groups)
        self.sheet = startup.TILE_SHEET
        self.image = self.sheet[0]
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.player = None
        self.highlighted = False
        self.telegraph_timer = 0
        self.enemy = None
        self.warned = False
        self.color = None
        self.color_dict = {
            "blue" : 3,
            "yellow" : 4,
            "red" : 5,
            "green" : 6,
            "purple" : 7,
            "gray" : 8
        }
    def update(self):
        self.player = pygame.sprite.spritecollideany(self, startup.PLAYER)
        if self.player != None and self.player.rect.topleft == self.pos and self.telegraph_timer == 0:
            if self.highlighted == False:
                self.image = self.sheet[1]
                self.highlighted = True
                startup.VISIBLE.change_layer(self, 1)
        elif self.highlighted == True and self.telegraph_timer == 0:
            self.image = self.sheet[0]
            self.highlighted = False
            startup.VISIBLE.change_layer(self, 0)
        if self.telegraph_timer != 0:
            self.telegraph(self.color, self.enemy)
    def telegraph(self, color, enemy):
        if self.telegraph_timer == 0:
            self.enemy = enemy
            self.color = self.color_dict[color]
            self.image = self.sheet[self.color]
            startup.VISIBLE.change_layer(self, 1)
            self.telegraph_timer = constant.FPS + 1
        else:
            self.telegraph_timer -= 1
            if self.telegraph_timer == 0 or self.enemy not in startup.ENEMIES:
                self.warned = False
                self.image = self.sheet[0]
                startup.VISIBLE.change_layer(self, 0)
            elif (
                self.telegraph_timer > 0
                and self.warned == False
                and self.player != None
                and self.player.rect.topleft == self.pos
            ):
                self.warned = True
                startup.SFX_CHANNEL.play(startup.WARNING_SOUND, loops=2)
            elif self.telegraph_timer % 10 == 0:
                self.image = self.sheet[2]
            elif self.telegraph_timer % 5 == 0:
                self.image = self.sheet[self.color]

class Countdown(pygame.sprite.Sprite):
    def __init__(self, groups=[startup.VISIBLE]):
        super().__init__(groups)
        startup.SFX_CHANNEL.play(startup.COUNTDOWN_SOUNDS[0])
        self.image = pygame.surface.Surface(
            (constant.WIDTH + 4,
            constant.HEIGHT + 4))
        self.image.fill(constant.BLACK)
        self.image.set_alpha(175)
        self.pos = (self.image.get_width() // 2, self.image.get_height() // 2)
        self.rect = self.image.get_rect(center=self.pos)
        self.countdown = 3
        startup.VISIBLE.change_layer(self, 6)
        self.text = text.Text(
            (self.image.get_width() // 2,
            self.image.get_height() // 2),
            str(self.countdown),
            constant.WIDTH,
            typed=False)
        self.text.change_layer(6)
    def count(self):
        self.countdown -= 1
        if self.countdown == 0:
            self.countdown = "FIGHT!"
        self.text.kill()
        self.text = text.Text(
            (self.image.get_width() // 2,
            self.image.get_height() // 2),
            str(self.countdown),
            constant.WIDTH,
            typed=False)
        self.text.change_layer(6)
    def kill(self):
        self.text.kill()
        super().kill()
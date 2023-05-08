import pygame
from game import constant, startup, bullet
from engine import animate, particle
import random

class Enemy(animate.AnimatedSprite):
    def __init__(self, board, pos, sheet, reload_speed=constant.FPS // 2, telegraph_time=constant.FPS, speed="-", color="gray", turning=True, groups=[startup.VISIBLE, startup.ENEMIES]):
        self.board = board
        super().__init__(pos, sheet, "idle", groups,
            {
                "idle" : {
                    "frames" : [0, 4],
                    "speed" : 15
                }
            }
        )
        self.extra = 0
        self.direction = (1, 0)
        self.turning = turning
        self.telegraph_time = telegraph_time
        self.reload_speed = reload_speed + self.telegraph_time
        self.reload_timer = self.telegraph_time
        self.move_speed = self.reload_speed + constant.FPS // 2
        self.move_timer = self.move_speed - self.telegraph_time
        self.moved = False
        self.movement_dict = {
            "R" : (1, 0),
            "L" : (-1, 0),
            "U" : (0, -1),
            "D" : (0, 1),
            "-" : (0, 0)
        }
        self.speed = (
            self.movement_dict[speed][0] * constant.TILE_SIZE,
            self.movement_dict[speed][1] * constant.TILE_SIZE)
        self.bullet_coords = []
        self.bullet_color = color
        self.shoot_dir = self.direction
        self.blood_count = 25
        self.cutscene = False
    def update(self):
        super().update()
        if self.cutscene == False:
            self.moved = False
            if self.turning == True:
                self.face_player()
            self.prep()
    def prep(self):
        if self.reload_timer == self.telegraph_time:
            self.telegraph()
        elif self.reload_timer <= 0:
            self.reload_timer = self.reload_speed
            self.shoot()
        self.reload_timer -= 1
        self.move_timer -= 1
        if self.move_timer <= 0:
            self.move()
    def telegraph(self):
        self.make_bullet_coords()
        for tile in startup.TILES:
            if tile.pos in self.bullet_coords and tile.telegraph_timer == 0:
                tile.telegraph(self.bullet_color, self)
    def shoot(self):
        for coord in self.bullet_coords.copy():
            if (
                coord[0] > self.board.left_bound - 1
                and coord[0] < self.board.right_bound + 1
                and coord[1] > self.board.upper_bound - 1
                and coord[1] < self.board.lower_bound + 1
            ):
                bullet.Bullet(self.board, coord, self.shoot_dir, self.bullet_color)
            self.bullet_coords.remove(coord)
    def make_bullet_coords(self):
        pass
    def face_player(self):
        for player in startup.PLAYER:
            if player.rect.x - self.rect.x != 0:
                dir_x = (player.rect.x - self.rect.x) / abs((player.rect.x - self.rect.x))
            else:
                dir_x = 0
            if player.rect.y - self.rect.y != 0:
                dir_y = (player.rect.y - self.rect.y) / abs((player.rect.y - self.rect.y))
            else:
                dir_y = 0
            self.direction = (dir_x, dir_y)
        if self.direction[0] < 0 and self.flipped == False:
            self.flipped = True
        elif self.direction[0] > 0 and self.flipped == True:
            self.flipped = False
    def move(self):
        if (
            self.rect.x + self.speed[0] > self.board.right_bound - self.extra
            or self.rect.x + self.speed[0] < self.board.left_bound
        ):
            self.speed = (-self.speed[0], self.speed[1])
        if (
            self.rect.y + self.speed[1] < self.board.upper_bound
            or self.rect.y + self.speed[1] > self.board.lower_bound - self.extra
        ):
            self.speed = (self.speed[0], -self.speed[1])
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        enemy_bumped = pygame.sprite.spritecollideany(self, startup.ENEMIES)
        if (
            enemy_bumped != None
            and enemy_bumped != self
            and enemy_bumped.rect.topleft == self.rect.topleft
            and enemy_bumped.moved == True
        ):
            self.rect.x -= self.speed[0]
            self.rect.y -= self.speed[1]
        self.moved = True
        self.move_timer = self.move_speed
    def stabbed(self):
        startup.SFX_CHANNEL.play(startup.STAB_SOUND)
        self.board.shake()
        for num in range(self.blood_count):
            particle.Particle(self.rect.center)
        self.kill()

class ThreeShooter(Enemy):
    def __init__(self, board, pos, speed):
        super().__init__(board, pos, startup.THREE_SHOOTER_SHEET, speed=speed, color="yellow")
    def make_bullet_coords(self):
        self.shoot_dir = self.direction
        for num in range(3):
            if self.shoot_dir[0] != 0:
                move_x = self.shoot_dir[0]
            else:
                move_x = num - 1
            if self.shoot_dir[1] != 0 and self.shoot_dir[0] == 0:
                move_y = self.shoot_dir[1]
            else:
                move_y = num - 1
            self.bullet_coords.append(
                (self.rect.topleft[0] + constant.TILE_SIZE * move_x,
                self.rect.topleft[1] + constant.TILE_SIZE * move_y))

class Bubblegun(Enemy):
    def __init__(self, board, pos, speed):
        super().__init__(board, pos, startup.BUBBLEGUN_SHEET, speed=speed, color="purple")
    def make_bullet_coords(self):
        self.shoot_dir = self.direction
        self.bullet_coords.append(
            (self.rect.topleft[0] + constant.TILE_SIZE * self.shoot_dir[0],
            self.rect.topleft[1] + constant.TILE_SIZE * self.shoot_dir[1]))

class Ghoulie(Enemy):
    def __init__(self, board, pos, shoot_dir):
        super().__init__(board, pos, startup.GHOULIE_SHEET, reload_speed=constant.FPS, color="gray")
        self.shoot_dir = self.movement_dict[shoot_dir]
        self.skip = None
    def make_bullet_coords(self):
        if self.shoot_dir[0] != 0:
            self.bullet_count = len(self.board.board_data)
        elif self.shoot_dir[1] != 0:
            self.bullet_count = len(self.board.board_data[0].split(" "))
        skip = random.choice([num for num in range(self.bullet_count) if num != self.skip])
        self.skip = skip
        for num in range(self.bullet_count):
            if self.shoot_dir[0] == 0:
                move_x = num - (self.rect.topleft[0] - self.board.diff_x) // constant.TILE_SIZE
                move_y = self.shoot_dir[1]
            elif self.shoot_dir[1] == 0:
                move_x = self.shoot_dir[0]
                move_y = num - (self.rect.topleft[1] - self.board.diff_y) // constant.TILE_SIZE
            if num != self.skip:
                self.bullet_coords.append(
                    (self.rect.topleft[0] + constant.TILE_SIZE * move_x,
                    self.rect.topleft[1] + constant.TILE_SIZE * move_y))

class Pollineer(Enemy):
    def __init__(self, board, pos, speed):
        super().__init__(board, pos, startup.POLLINEER_SHEET, speed=speed, color="green")
        self.shoot_dir = None
        self.finishing_dir = None
        self.restart = True
        self.spiral_dict = {
            (-1, 0)   : (-1, -1),
            (-1, -1) : (0, -1),
            (0, -1)  : (1, -1),
            (1, -1)  : (1, 0),
            (1, 0)   : (1, 1),
            (1, 1)   : (0, 1),
            (0, 1)   : (-1, 1),
            (-1, 1)  : (-1, 0)
        }
        self.keys = list((self.spiral_dict.keys()))
        self.values = list(self.spiral_dict.values())
    def shoot(self):
        super().shoot()
        if self.restart == False:
            self.reload_timer = self.telegraph_time + 1
    def make_bullet_coords(self):
        if self.restart == True:
            self.shoot_dir = self.direction
            self.finishing_dir = self.keys[self.values.index(self.direction)]
            self.restart = False
        else:
            self.shoot_dir = self.spiral_dict[self.shoot_dir]
        self.bullet_coords.append(
            (self.rect.topleft[0] + constant.TILE_SIZE * self.shoot_dir[0],
            self.rect.topleft[1] + constant.TILE_SIZE * self.shoot_dir[1]))
        if self.shoot_dir != self.finishing_dir:
            self.move_timer = self.move_speed
        else:
            self.restart = True

class Smiley(Enemy):
    def __init__(self, board, pos, shoot_dir):
        super().__init__(board, pos, startup.SMILEY_SHEET, color="red", reload_speed=constant.FPS * 1.5, turning=False)
        self.laser = None
        self.shoot_dir = self.movement_dict[shoot_dir]
        if self.shoot_dir[0] != 0:
            bullet_coverage = len(self.board.board_data)
            diff = self.board.diff_x
        elif self.shoot_dir[1] != 0:
            bullet_coverage = len(self.board.board_data[0].split(" "))
            diff = self.board.diff_y
        for index in range(bullet_coverage):
            pos = index * constant.TILE_SIZE + diff
            if (
                self.shoot_dir[0] < 0 and self.pos[0] > pos
                or self.shoot_dir[0] > 0 and self.pos[0] < pos
            ):
                self.bullet_coords.append((pos, self.pos[1]))
            elif (
                self.shoot_dir[1] < 0 and self.pos[1] > pos
                or self.shoot_dir[1] > 0 and self.pos[1] < pos
            ):
                self.bullet_coords.append((self.pos[0], pos))
        if self.shoot_dir[1] != 0:
            self.turning = True
        if self.shoot_dir[0] == -1:
            self.flipped = True
    def shoot(self):
        self.laser = bullet.Laser(
                self.board,
                self,
                (self.rect.topleft[0] + constant.TILE_SIZE * self.shoot_dir[0],
                self.rect.topleft[1] + constant.TILE_SIZE * self.shoot_dir[1]),
                self.shoot_dir,
                self.bullet_color)
    def update(self):
        super().update()
        if self.laser != None and self.laser.ended == False:
            self.reload_timer = self.reload_speed

class Majesty(Enemy):
    def __init__(self, board, pos, speed):
        super().__init__(board, pos, startup.MAJESTY_SHEET, speed=speed, color="blue")
    def make_bullet_coords(self):
        self.shoot_dir = self.direction
        if abs(self.shoot_dir[0]) == abs(self.shoot_dir[1]):
            bullet_directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        else:
            bullet_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for direction in bullet_directions:
            self.bullet_coords.append(
                (self.rect.topleft[0] + constant.TILE_SIZE * direction[0],
                self.rect.topleft[1] + constant.TILE_SIZE * direction[1]))

class Hotlips(Enemy):
    def __init__(self, board, pos, speed):
        super().__init__(board, pos, startup.HOTLIPS_SHEET, speed=speed, color="red")
        self.shoot_directions = [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]
    def shoot(self):
        for coord in self.bullet_coords:
            bullet.Bullet(
                self.board,
                coord,
                self.shoot_directions[self.bullet_coords.index(coord)],
                self.bullet_color)
        self.bullet_coords = []
    def make_bullet_coords(self):
        for direction in self.shoot_directions:
            self.bullet_coords.append(
                (self.rect.topleft[0] + constant.TILE_SIZE * direction[0],
                self.rect.topleft[1] + constant.TILE_SIZE * direction[1]))

class King(Enemy):
    def __init__(self, board, pos, speed, state="idle_armed", cutscene=False):
        super().__init__(board, pos, startup.KING_SHEET, reload_speed=constant.FPS // 10, speed=speed, color="green")
        self.animations =             {
                "idle_unarmed" : {
                    "frames" : [0, 4],
                    "speed" : 15
                },
                "idle_armed" : {
                    "frames" : [5, 9],
                    "speed" : 15
                },
                "idle_derobed" : {
                    "frames" : [10, 14],
                    "speed" : 15
                }
            }
        if self.board != None and self.board.round_number == len(constant.BOARDS) - 1:
            self.set_state("idle_derobed")
        else:
            self.set_state(state)
        self.extra = constant.TILE_SIZE
        self.shoot_directions = [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]
        self.bullet_direction_dict = {}
        self.current_attack = None
        self.cutscene = cutscene
        self.blood_count = 150
        self.health = 6
        if self.state == "idle_derobed":
            self.health = 0
        startup.VISIBLE.change_layer(self, 5)
    def jump(self):
        self.reload_timer = self.telegraph_time
        self.move_timer = self.telegraph_time
        self.bullet_coords = []
        new_x, new_y = [], []
        if self.rect.x // constant.TILE_SIZE < len(self.board.board_data[0].split(" ")) // 2:
            for num in range(4, (self.board.right_bound - self.extra) // constant.TILE_SIZE):
                if self.rect.x + num * constant.TILE_SIZE <= self.board.right_bound - self.extra:
                    new_x.append(self.rect.x + num * constant.TILE_SIZE)
        else:
            for num in range(-self.board.right_bound // constant.TILE_SIZE, -3):
                if self.rect.x + num * constant.TILE_SIZE >= self.board.left_bound:
                    new_x.append(self.rect.x + num * constant.TILE_SIZE)
        if self.rect.y // constant.TILE_SIZE < len(self.board.board_data) // 2:
            for num in range(3, (self.board.lower_bound - self.extra) // constant.TILE_SIZE):
                if self.rect.y + num * constant.TILE_SIZE <= self.board.lower_bound - self.extra:
                    new_y.append(self.rect.y + num * constant.TILE_SIZE)
        else:
            for num in range(-self.board.lower_bound // constant.TILE_SIZE, -3):
                if self.rect.y + num * constant.TILE_SIZE >= self.board.upper_bound:
                    new_y.append(self.rect.y + num * constant.TILE_SIZE)
        self.rect.x = random.choice(new_x)
        self.rect.y = random.choice(new_y)
    def shoot(self):
        if self.state != "idle_derobed" and self.current_attack != self.circle_shot:
            super().shoot()
        elif self.current_attack == self.circle_shot:
            for coord in self.bullet_coords:
                bullet.Bullet(
                    self.board,
                    coord,
                    self.bullet_direction_dict[coord],
                    self.bullet_color)
        self.bullet_coords = []
    def make_bullet_coords(self):
        if self.state != "idle_derobed":
            for player in startup.PLAYER:
                distance_x = pygame.math.Vector2(self.rect.center[0], 0).distance_to((player.rect.topleft[0], 0))
                distance_y = pygame.math.Vector2(0, self.rect.center[1]).distance_to((0, player.rect.topleft[1]))
                if distance_x >= constant.TILE_SIZE * 5 or distance_y >= constant.TILE_SIZE * 5:
                    self.current_attack = self.shoot_wall
                elif (
                    abs(self.direction[0]) == 1
                    and self.direction[1] == 0
                    or abs(self.direction[1]) == 1
                    and self.direction[0] == 0
                ):
                    self.current_attack = self.shoot_four
                else:
                    self.current_attack = random.choice([self.circle_shot, self.shoot_four])
            self.current_attack()
    def shoot_four(self):
        self.shoot_dir = self.direction
        for num in range(4):
            if self.shoot_dir[0] != 0:
                if self.shoot_dir[0] == 1:
                    move_x = self.shoot_dir[0] * 2
                else:
                    move_x = self.shoot_dir[0]
            else:
                move_x = num - 1
            if self.shoot_dir[1] != 0 and self.shoot_dir[0] == 0:
                if self.shoot_dir[1] == 1:
                    move_y = self.shoot_dir[1] * 2
                else:
                    move_y = self.shoot_dir[1]
            else:
                move_y = num - 1
            self.bullet_coords.append(
                (self.rect.topleft[0] + constant.TILE_SIZE * move_x,
                self.rect.topleft[1] + constant.TILE_SIZE * move_y))
    def circle_shot(self):
        self.bullet_direction_dict = {}
        for direction in self.shoot_directions:
            if direction[0] == 1:
                if direction[1] == 1:
                    self.bullet_coords.append(
                        (self.rect.topleft[0] + constant.TILE_SIZE * direction[0] + self.extra,
                        self.rect.topleft[1] + constant.TILE_SIZE * direction[1] + self.extra))
                    self.bullet_direction_dict[self.bullet_coords[-1]] = direction
                else:
                    self.bullet_coords.append(
                        (self.rect.topleft[0] + constant.TILE_SIZE * direction[0] + self.extra,
                        self.rect.topleft[1] + constant.TILE_SIZE * direction[1]))
                    self.bullet_direction_dict[self.bullet_coords[-1]] = direction
                    if direction[1] == 0:
                        self.bullet_coords.append(
                            (self.rect.topleft[0] + constant.TILE_SIZE * direction[0] + self.extra,
                            (self.rect.topleft[1] + constant.TILE_SIZE * direction[1]) + self.extra))
                        self.bullet_direction_dict[self.bullet_coords[-1]] = direction
            elif direction[1] == 1:
                self.bullet_coords.append(
                    (self.rect.topleft[0] + constant.TILE_SIZE * direction[0],
                    self.rect.topleft[1] + constant.TILE_SIZE * direction[1] + self.extra))
                self.bullet_direction_dict[self.bullet_coords[-1]] = direction
                if direction[0] == 0:
                    self.bullet_coords.append(
                        ((self.rect.topleft[0] + constant.TILE_SIZE * direction[0]) + self.extra,
                        self.rect.topleft[1] + constant.TILE_SIZE * direction[1] + self.extra))
                    self.bullet_direction_dict[self.bullet_coords[-1]] = direction
            else:
                self.bullet_coords.append(
                    (self.rect.topleft[0] + constant.TILE_SIZE * direction[0],
                    self.rect.topleft[1] + constant.TILE_SIZE * direction[1]))
                self.bullet_direction_dict[self.bullet_coords[-1]] = direction
                if direction[0] == 0:
                    self.bullet_coords.append(
                        ((self.rect.topleft[0] + constant.TILE_SIZE * direction[0]) + self.extra,
                        self.rect.topleft[1] + constant.TILE_SIZE * direction[1]))
                    self.bullet_direction_dict[self.bullet_coords[-1]] = direction
                if direction[1] == 0:
                    self.bullet_coords.append(
                        (self.rect.topleft[0] + constant.TILE_SIZE * direction[0],
                        (self.rect.topleft[1] + constant.TILE_SIZE * direction[1]) + self.extra))
                    self.bullet_direction_dict[self.bullet_coords[-1]] = direction
    def shoot_wall(self):
        self.shoot_dir = self.direction
        if self.shoot_dir[1] != 0:
            self.bullet_count = len(self.board.board_data[0].split(" "))
            self.shoot_dir = (0, self.shoot_dir[1])
        elif self.shoot_dir[0] != 0:
            self.bullet_count = len(self.board.board_data)
            self.shoot_dir = (self.shoot_dir[0], 0)
        skip = random.choice(range(self.bullet_count))
        for num in range(self.bullet_count):
            if self.shoot_dir[0] == 0:
                move_x = num - (self.rect.topleft[0] - self.board.diff_x) // constant.TILE_SIZE
                if self.shoot_dir[1] == 1:
                    move_y = self.shoot_dir[1] * 2
                else:
                    move_y = self.shoot_dir[1]
            elif self.shoot_dir[1] == 0:
                if self.shoot_dir[0] == 1:
                    move_x = self.shoot_dir[0] * 2
                else:
                    move_x = self.shoot_dir[0]
                move_y = num - (self.rect.topleft[1] - self.board.diff_y) // constant.TILE_SIZE
            if num != skip:
                self.bullet_coords.append(
                    (self.rect.topleft[0] + constant.TILE_SIZE * move_x,
                    self.rect.topleft[1] + constant.TILE_SIZE * move_y))
    def face_player(self):
        for player in startup.PLAYER:
            if (
                player.rect.x - self.rect.x != 0
                and player.rect.x - (self.rect.x + self.extra) != 0
            ):
                dir_x = (player.rect.x - self.rect.x) / abs((player.rect.x - self.rect.x))
            else:
                dir_x = 0
            if (
                player.rect.y - self.rect.y != 0
                and player.rect.y - (self.rect.y + self.extra) != 0
            ):
                dir_y = (player.rect.y - self.rect.y) / abs((player.rect.y - self.rect.y))
            else:
                dir_y = 0
            self.direction = (dir_x, dir_y)
        if self.direction[0] < 0 and self.flipped == False:
            self.flipped = True
        elif self.direction[0] > 0 and self.flipped == True:
            self.flipped = False
    def stabbed(self):
        startup.SFX_CHANNEL.play(startup.STAB_SOUND)
        self.board.shake()
        if self.health == 0:
            for num in range(self.blood_count):
                particle.Particle(self.rect.center)
            self.kill()
        else:
            for num in range(self.blood_count // 4):
                particle.Particle(self.rect.center)
            self.health -= 1
            self.jump()
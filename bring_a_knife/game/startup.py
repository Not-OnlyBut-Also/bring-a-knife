import pygame
from game import constant
from engine import spritesheet

def init():
    global DISPLAY, DISPLAY_X, DISPLAY_Y
    DISPLAY = pygame.Surface((constant.WIDTH + 4, constant.HEIGHT + 4))
    DISPLAY.fill(constant.BG)
    DISPLAY_X, DISPLAY_Y = constant.MARGIN_X, constant.MARGIN_Y
    
    global TITLE_FONT, FONT
    FONT = pygame.font.Font("assets/fonts/04B_03__.TTF", size=22)
    
    global VISIBLE, SPECIAL_EFFECT, TILES, PLAYER, BULLETS, ENEMIES
    VISIBLE = pygame.sprite.LayeredUpdates()
    SPECIAL_EFFECT = pygame.sprite.Group()
    TILES = pygame.sprite.Group()
    PLAYER = pygame.sprite.Group()
    BULLETS = pygame.sprite.Group()
    ENEMIES = pygame.sprite.Group()
    
    global TITLE_IMG
    TITLE_IMG = pygame.image.load("assets/sprites/title.png").convert_alpha()
    
    global TILE_SHEET, PLAYER_SHEET, BULLET_SHEET, LASER_SHEET, PARTICLE_SHEET
    TILE_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/tile.png").convert_alpha(), width=132, height=132)
    PLAYER_SHEET = (
        spritesheet.interpret(pygame.image.load("assets/sprites/player.png").convert_alpha())
        + spritesheet.interpret(pygame.image.load("assets/sprites/player_crowned.png").convert_alpha(), width=256, height=256))
    BULLET_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/bullet.png").convert_alpha())
    LASER_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/laser.png").convert_alpha())
    PARTICLE_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/particles.png").convert_alpha(), width=4, height=4)
    
    global THREE_SHOOTER_SHEET, BUBBLEGUN_SHEET, GHOULIE_SHEET, POLLINEER_SHEET, SMILEY_SHEET, MAJESTY_SHEET, HOTLIPS_SHEET, KING_SHEET
    THREE_SHOOTER_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/three_shooter.png").convert_alpha())
    BUBBLEGUN_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/bubblegun.png").convert_alpha())
    GHOULIE_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/ghoulie.png").convert_alpha())
    POLLINEER_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/pollineer.png").convert_alpha())
    SMILEY_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/smiley.png").convert_alpha())
    MAJESTY_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/majesty.png").convert_alpha())
    HOTLIPS_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/hotlips.png").convert_alpha())
    KING_SHEET = spritesheet.interpret(pygame.image.load("assets/sprites/king.png").convert_alpha(), width=256, height=256)
    
    global COUNTDOWN_SOUNDS, TALK_SOUNDS, WARNING_SOUND, SHOT_SOUND, STAB_SOUND, DEROBE_SOUND, SHOOT_SOUND, SHOOT_CHANNEL, SFX_CHANNEL
    COUNTDOWN_SOUNDS = [pygame.mixer.Sound(f"assets/sounds/countdown{i}.ogg") for i in range(3)]
    TALK_SOUNDS = [pygame.mixer.Sound(f"assets/sounds/talk{i}.ogg") for i in range(3)]
    WARNING_SOUND = pygame.mixer.Sound("assets/sounds/warning.ogg")
    SHOT_SOUND = pygame.mixer.Sound("assets/sounds/shot.ogg")
    STAB_SOUND = pygame.mixer.Sound("assets/sounds/stab.ogg")
    DEROBE_SOUND = pygame.mixer.Sound("assets/sounds/derobe.ogg")
    SHOOT_SOUND = pygame.mixer.Sound("assets/sounds/shoot.ogg")
    SHOOT_CHANNEL = pygame.mixer.Channel(0)
    SFX_CHANNEL = pygame.mixer.Channel(1)
    
    global BOARD_MUSIC, BOSS_MUSIC, MUSIC_CHANNEL
    BOARD_MUSIC = pygame.mixer.Sound("assets/sounds/board_music.ogg")
    BOSS_MUSIC = pygame.mixer.Sound("assets/sounds/goblin_kings_theme.ogg")
    MUSIC_CHANNEL = pygame.mixer.Channel(2)
    
    global STATES
    from game import menu, king_scene, board, win_screen
    STATES = {
        "menu" : menu.Menu,
        "king scene" : king_scene.KingScene,
        "board" : board.Board,
        "win screen" : win_screen.WinScreen
    }
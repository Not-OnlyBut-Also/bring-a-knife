import pygame
from game import constant

def interpret(full_sheet, width=constant.TILE_SIZE, height=constant.TILE_SIZE):
    sprite_width, sprite_height = full_sheet.get_width()//width, full_sheet.get_height()//height
    sprites = []
    for y in range(sprite_height):
        for x in range(sprite_width):
            sprites.append(full_sheet.subsurface((x * width, y * height, width, height)))
    return sprites
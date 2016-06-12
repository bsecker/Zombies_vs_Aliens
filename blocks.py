"""
Module for managing platforms.
"""
import pygame
import random
 
from spritesheet_functions import SpriteSheet
 
# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite

GRASS_MIDDLE          = (0, 0, 70, 70)
DIRT_MIDDLE           = (70, 0, 70, 70)
SPAWN_BLOCK           = (70, 0, 70, 70)
BUSH_1                = (0, 70, 70, 70)
BUSH_2                = (210, 0, 70, 70)


class Block(pygame.sprite.Sprite):
    """ Block the user can jump on """
 
    def __init__(self, sprite_sheet_data):
        """ Block constructor. Assumes constructed with user passing in
            an array of 4 numbers like what's defined at the top of this
            code. """
        pygame.sprite.Sprite.__init__(self)
 
        sprite_sheet = SpriteSheet("Resources/Sprites/spritesheet_tiles.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])
 
        self.rect = self.image.get_rect()

class PickupSpawnerBlock(Block):
    """ Block where pickups drop to"""
    def __init__(self):
        Block.__init__(self, SPAWN_BLOCK)

class Bush(Block):
    def __init__(self):
        Block.__init__(self, random.choice([BUSH_1, BUSH_2]))
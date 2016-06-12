"""
Module for managing platforms.
"""
import pygame
 
from spritesheet_functions import SpriteSheet
 
# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite

GRASS_LEFT            = (576, 720, 70, 70)
GRASS_RIGHT           = (576, 576, 70, 70)
GRASS_MIDDLE          = (0, 0, 70, 70)
DIRT_MIDDLE           = (70, 0, 70, 70)
STONE_PLATFORM_LEFT   = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT  = (792, 648, 70, 40)


class Block(pygame.sprite.Sprite):
    """ Block the user can jump on """
 
    def __init__(self, sprite_sheet_data):
        """ Block constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
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
        Block.__init__(self, STONE_PLATFORM_MIDDLE)
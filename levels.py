import pygame
import constants
import blocks
import entities
import random

class Level:
    """Generic superclass used to define a level. Child classes have specific level info."""
    def __init__(self, player):
        self.block_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.entity_list= pygame.sprite.Group()
        self.active_sprite_list = pygame.sprite.Group()
        self.player = player

        #draw background
        self.background = pygame.surface.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)).convert()
        self.background.fill(constants.BG_COLOUR)

        #how far this world has been scrolled left/right
        self.world_shift = 0

    def update(self):
        self.block_list.update()
        self.enemy_list.update()
        self.entity_list.update()


    def render(self, surface):
        """draw the background and all the entities"""

        surface.blit(self.background, (0,0))#(self.world_shift // 3,0))
        
        #draw all sprite lists
        self.block_list.draw(surface)
        self.enemy_list.draw(surface)
        self.enemy_list.draw(surface)

    def shift_world(self, shift_x):
        """ When the user moves left/right scroll everything:"""
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for block in self.block_list:
            block.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

    def add_zombie(self, x, y):
        #add zombie:
        zombie = entities.Zombie(self.player)
        zombie.rect.x = x
        zombie.rect.y = y # 
        zombie.level = self
        self.enemy_list.add(zombie)
        return zombie


class Level_01(Level):
    """Level 1: Front of Chapel"""
    def __init__(self, player):
        """create level"""
        Level.__init__(self, player)

        self.level_limit = -1500
        #self.background = pygame.image.load("background_01.png").convert()
        #self.background.set_colorkey(constants.WHITE)
                #draw background
        self.background = pygame.surface.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)).convert()
        self.background.fill(constants.BG_COLOUR)

        # Array with width, height, x, and y of blocks
        # level = [ [blocks.GRASS_LEFT, 500, 500],
        #           [blocks.GRASS_MIDDLE, 0, 300],
        #           [blocks.GRASS_MIDDLE, 570, 500],
        #           [blocks.GRASS_RIGHT, 640, 500],
        #           [blocks.GRASS_LEFT, 800, 400],
        #           [blocks.GRASS_MIDDLE, 870, 400],
        #           [blocks.GRASS_RIGHT, 940, 400],
        #           [blocks.GRASS_LEFT, 1000, 500],
        #           [blocks.GRASS_MIDDLE, 1070, 500],
        #           [blocks.GRASS_RIGHT, 1140, 500],
        #           [blocks.STONE_PLATFORM_LEFT, 1120, 280],
        #           [blocks.STONE_PLATFORM_MIDDLE, 1190, 280],
        #           [blocks.STONE_PLATFORM_RIGHT, 1260, 280],
        #           ]
        level = self.generate_random_level(3500)
 
        # Go through the array above and add blocks
        for _block in level:
            block = blocks.Block(_block[0])
            block.rect.x = _block[1]
            block.rect.y = _block[2]
            block.player = self.player
            self.block_list.add(block)

    def generate_random_level(self, size):
        """
        Currently just makes a bottom row, and randomly places blocks on a row above. 
        looks terrible
        """
        _bs = 70 # Block size
        _x = -30*_bs
        _y = constants.SCREEN_HEIGHT - _bs
        level = []
        while _x <= size:
            if random.randrange(0,2) == 1:
                level.append([blocks.GRASS_MIDDLE, _x, _y-_bs])
                level.append([blocks.DIRT_MIDDLE, _x, _y]) #dirt underneath
            else:
                level.append([blocks.GRASS_MIDDLE, _x, _y])

            _x += _bs

        print 'created {0} blocks'.format(len(level))
        return level

    def spawn_zombies(self):
        """Handles waves and zombie spawning"""
        self.zombie = self.add_zombie(230, constants.SCREEN_HEIGHT - self.player.rect.height - 50)
        self.active_sprite_list.add(self.zombie)
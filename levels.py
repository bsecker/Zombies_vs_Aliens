import pygame
import constants
import blocks
import entities
import random
import time

from message_functions import Messages

class Level:
    """ Generic superclass used to define a level. Child classes have specific level info."""
    def __init__(self, player):
        self.block_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.entity_list= pygame.sprite.Group()
        self.player_list= pygame.sprite.LayeredUpdates()
        self.player = player

        # Draw background
        self.background = pygame.surface.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)).convert()
        self.background.fill(constants.BG_COLOUR)

        # How far this world has been scrolled left/right
        self.world_shift = 0

        # Zombie spawn points
        self.spawn1 = None
        self.spawn2 = None
        self.zombie_chance = 150

        # Pickup
        self.pickup_spawn_time = time.time()
        self.pickup_spawn_min = time.time() + 1
        self._next_spawn = 10
        self.pickup_spawn_loc = None
        self.last_pickup = 0

        # Score
        self.score = 0
        self.score_file = open("data.dat", 'w+')

        # Font
        self.font = pygame.font.SysFont(None, 36)

        # Initialise Messages
        self.messages = Messages(self.font)

    def update(self):
        self.block_list.update()
        self.enemy_list.update()
        self.entity_list.update()
        self.player_list.update()

        self.spawn_zombies()
        self.spawn_pickups()

        self.messages.update()

        # Increment score as long as player is alive
        if self.player.alive == True:
            self.score += 0.005

    def render(self, surface):
        """draw the background and all the entities"""

        surface.blit(self.background, (0,0))#(self.world_shift // 3,0))
        
        # Draw all sprite lists
        self.block_list.draw(surface)
        self.enemy_list.draw(surface)
        self.entity_list.draw(surface)
        self.player_list.draw(surface)
        self.messages.draw(surface)

        # Draw UI
        self.draw_healthbar(surface,self.player.health)
        self.draw_score(surface, self.score)
        self.draw_ammo(surface)



    def shift_world(self, shift_x):
        """ When the user moves left/right scroll everything:"""
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for block in self.block_list:
            block.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for entity in self.entity_list:
            entity.rect.x += shift_x

        self.pickup_spawn_loc += shift_x

    def add_zombie(self, x, y):
        #add zombie:
        zombie = entities.Zombie(self.player)
        zombie.rect.x = x
        zombie.rect.y = y # 
        zombie.level = self
        self.enemy_list.add(zombie)
        return zombie

    def spawn_zombies(self):
        """Handles waves and zombie spawning"""
        if random.randrange(0,int(self.zombie_chance)) == 1:
            self.zombie = self.add_zombie(random.choice([self.spawn1, self.spawn2]), 0) # Spawn at top of screen (zombies don't feel fall damage))
            if self.zombie_chance > 20:
                self.zombie_chance +=- 0.25

    def spawn_pickups(self):
        """handles ammo and healthpack drops. They drop from the sky at a specific point."""

        if time.time() >= self.pickup_spawn_min:
            
            # alternate between health and ammo
            if self.last_pickup == 1:
                pickup = entities.Ammopack(self.player)
            else:
                pickup = entities.Healthpack(self.player)

            #place healthpack in middle of tile
            pickup.rect.centerx = self.pickup_spawn_loc+random.randint(-45,45)
            pickup.rect.y = 0
            self.entity_list.add(pickup)

            #reset and make longer as time goes on
            self._next_spawn += random.randrange(1, 5)
            self.pickup_spawn_min += self._next_spawn
            self.last_pickup = not self.last_pickup
            self.messages.message("{0} dropped! Next drop in {1} seconds".format(str(pickup.entity_id),str(self._next_spawn)))


    def draw_healthbar(self, surface, health):
        """Draw player health as a rectangle"""
        _max_width = 100 # Width of healthbar
        pygame.draw.rect(surface, constants.RED, (50, 50, _max_width, 20))
        if self.player.health > 0:
            pygame.draw.rect(surface, constants.GREEN, (50, 50, self.player.health,20))

    def draw_score(self, surface, score):
        """Render score"""
        score_text = self.font.render(str(int(score)), 1, constants.YELLOW)
        surface.blit(score_text, (constants.HALF_SCREEN_WIDTH, 50))

    def draw_fps(self, surface, fps):
        """Developer function to draw measure of current FPS of program."""
        fps_text = self.font.render(str(int(fps.get_fps())), 1, constants.YELLOW)
        surface.blit(fps_text, (constants.SCREEN_WIDTH-70, 70))

    def draw_ammo(self, surface):
        """draw player ammo"""
        clip_text = self.font.render("{0}/{1}".format(str(self.player.current_weapon.clip_ammo),str(self.player.current_weapon.ammo_amount)), 1, constants.WHITE)
        surface.blit(clip_text, (constants.SCREEN_WIDTH-75, 50))   

        grenades_text = self.font.render(str(self.player.grenades), 1, constants.WHITE)
        surface.blit(grenades_text, (constants.SCREEN_WIDTH-75, 70))      

class Level_01(Level):
    """
    Level 1
    Other levels aren't being used yet, but doing it like this leaves it open for the future.
    """
    def __init__(self, player):
        """create level"""
        Level.__init__(self, player)

        self.level_limit = -1570
        self.spawn1 = -2000
        self.spawn2 = 2000

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
 
        ### Go through the array above and add blocks:
        ### TO DO: REDO THIS FOR MISC ITEMS (TREES ETC)

        # get list of grass blocks and choose two 
        #_grass_list = [_i for _i in level if _i[0] == blocks.GRASS_MIDDLE]
        #_sample = random.sample(_grass_list, 2)

        for _block in level:
            # Change two grass blocks into spawn tiles for pickups
            #if _block in _sample:
            #    block = blocks.Block(blocks.STONE_PLATFORM_MIDDLE)
            #else:
            # If block is a spawnblock
            if _block[0] == blocks.STONE_PLATFORM_LEFT:
                block = blocks.PickupSpawnerBlock()
                self.pickup_spawn_loc = _block[1] 
            else:
                block = blocks.Block(_block[0])
            block.rect.x = _block[1]
            block.rect.y = _block[2]
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
            _direction = random.randrange(0,5)
            # Go up
            if _direction == 1:
                if _y > constants.SCREEN_HEIGHT-(_bs*3):
                    _y +=- _bs
            # Go down
            elif _direction == 2:
                if _y < constants.SCREEN_HEIGHT-_bs:
                    _y += _bs

            level.append([blocks.GRASS_MIDDLE, _x, _y])

            # Add blocks underneath
            if _y <= constants.SCREEN_HEIGHT-(_bs*2):
                level.append([blocks.DIRT_MIDDLE, _x, _y+_bs])
                level.append([blocks.DIRT_MIDDLE, _x, _y+_bs*2])
            elif _y <= constants.SCREEN_HEIGHT-_bs:
                level.append([blocks.DIRT_MIDDLE, _x, _y+(_bs*2)])

            # Add ammo drop point
            if _x == 700:
                level.append([blocks.STONE_PLATFORM_LEFT, _x, _y]) 

            _x+= _bs 

        # Add a block to the end that the zombies can jump on
        level.append([blocks.GRASS_MIDDLE, _x, constants.SCREEN_HEIGHT-_bs]) 

        


        print 'creating {0} blocks..'.format(len(level))
        return level


import pygame
import constants
import math

from spritesheet_functions import SpriteSheet

class Base_Entity(pygame.sprite.Sprite):
    """Entity Superclass."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Entity(Base_Entity):
    """
    Entity Base Class. For Zombies, player, etc
    """
    def __init__(self):
        Base_Entity.__init__(self)

        self.max_gravity = 20
        self.jump_speed = 9
        self.gravity_accel = .30
        self.move_speed = 7
        self.alive = True

        self.x_vel = 0 
        self.y_vel = 0
        self.direction = 'L'



        self.width = 20
        self.height = 60
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.RED)
        self.rect = self.image.get_rect()

        self.level = None

    def update(self):
        self.calc_gravity()

        # Move left/right
        self.rect.x += self.x_vel
        #collide with objects
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        for block in block_hit_list:
            if self.x_vel > 0:
                self.rect.right = block.rect.left
            elif self.x_vel < 0:
                self.rect.left = block.rect.right

        #move up/down
        self.rect.y += self.y_vel
        # collide with objects
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.y_vel > 0:
                self.rect.bottom = block.rect.top
            elif self.y_vel < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.y_vel = 0


    def calc_gravity(self):
        """ Calculate effect of gravity. """
        if self.y_vel <= self.max_gravity:
            self.y_vel += self.gravity_accel
 
        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.y_vel >= 0:
            self.y_vel = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(block_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.y_vel = -self.jump_speed

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.x_vel = -self.move_speed
        self.direction = 'L'
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.x_vel = self.move_speed
        self.direction = 'R'
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.x_vel = 0

class Zombie(Entity):
    def __init__(self, player):
        Entity.__init__(self)
        self.move_speed = 1
        self.player = player

    def update(self):
        """
        'Brains' for the zombies go here
        """
        Entity.update(self)

        # Head towards player
        if self.rect.x <= self.player.rect.x:
            self.go_right()
        else:
            self.go_left()

        # Jump if colliding with an object (REWRITE THIS IN FEWER LINES)
        # move to the right a bit and check collisions then back
        self.rect.x += 2
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        self.rect.x +=- 2
        if len(block_hit_list) > 0:
            self.jump()
        self.rect.x +=- 2

        #check left
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        self.rect.x += 2
        if len(block_hit_list) > 0:
            self.jump()

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.ammo = 100
        self.health = 100
        self.rot = 0

    def fire(self):
        """ attack with current weapon 
        TEMPORARY"""
        bullet = Bullet(self.direction)
        bullet.rect.x = self.rect.x
        bullet.rect.y = self.rect.y
        bullet.level = self.level
        return bullet

class Weapon(Base_Entity):
    def __init__(self):
        """Superclass for all player weapons."""
        Base_Entity.__init__(self)

class Pistol(Weapon):
    def __init__(self):
        Weapon.__init__(self)


class Bullet(Base_Entity):
    """
    TO DO: for now, just spawn bullets - in future handle bullet creation by weapon classes
    """
    def __init__(self, dir):
        Base_Entity.__init__(self)
        self.direction = dir
        self.move_speed = 10

        self.width = 5
        self.height = 5
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.RED)
        self.rect = self.image.get_rect()

        self.level = None

    def update(self):
        # Move left/right
        if self.direction == 'L':
            self.rect.x +=- self.move_speed
        else:
            self.rect.x += self.move_speed

        # Collide with objects
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        if len(block_hit_list) > 0:
            self.kill()

        current_position = self.rect.x + self.level.world_shift

        # # Destroy if outside world
        if current_position > -self.level.level_limit:
            self.kill()
        elif current_position < self.level.level_limit:
            self.kill()

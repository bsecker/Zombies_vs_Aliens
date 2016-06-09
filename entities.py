import pygame
import constants
import math
import time
import random

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
 
        # Prevent going off the bottom of the screen.
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
        self.health = 3

    def update(self):
        """
        'Brains' for the zombies go here
        """
        Entity.update(self)

        # Die
        if self.health <= 0:
            self.kill()
            self.level.score += 5

        # Head towards player
        if self.rect.x <= self.player.rect.x:
            self.go_right()
        else:
            self.go_left()

        # Jump if colliding with an object (REWRITE THIS IN FEWER LINES)
        # move to the right a bit and check collisions then back
        self.rect.x += 5
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        self.rect.x +=- 5
        if len(block_hit_list) > 0:
            self.jump()

        #check left
        self.rect.x +=- 5        
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        self.rect.x += 5
        if len(block_hit_list) > 0:
            self.jump()

class Player(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.health = 100

        # Weapons
        self.weapon_list = None
        self.current_weapon = None

        # Frames of animated walking left/right
        self.walking_frames_l = []
        self.walking_frames_r = []

        sprite_sheet = SpriteSheet("Resources/Sprites/p1_walk.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)

         # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
 
        # Set the image the player starts with
        self.image = self.walking_frames_r[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        self.ammo_pickup_sound = pygame.mixer.Sound("Resources/Sounds/sound_ammo_pickup.wav")
        self.grenade_throw_sound = pygame.mixer.Sound("Resources/Sounds/sound_grenade_throw.wav")

    def update(self):
        Entity.update(self)

        # health
        if self.health <= 0:
            self.health = 0
            self.kill()

        # collide with zombies
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        if len(enemy_hit_list) > 0:
            self.health +=- 1

        # collide with entities
        entity_hit_list = pygame.sprite.spritecollide(self, self.level.entity_list, False)
        if len(entity_hit_list) > 0:
            if entity_hit_list[0].entity_id == 'ammopack':
                entity_hit_list[0].kill()
                self.level.score += 10
                self.ammo_pickup_sound.play()

                #add ammo to all guns
                self.get_ammo_pack()

            elif entity_hit_list[0].entity_id == 'healthpack':
                entity_hit_list[0].kill()
                self.level.score += 15
                self.ammo_pickup_sound.play()

                # Add score
                self.health += 25
                if self.health > 100: # limit to 100
                    self.health == 100

            elif entity_hit_list[0].entity_id == 'grenade':
                if entity_hit_list[0].exploding == True:
                    self.health +=- 25

        # Do walking animation
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

    def get_ammo_pack(self):
        """ Add ammo to all weapons (apart from sword)"""
        self.weapon_list[0].ammo_amount += 12
        self.weapon_list[1].ammo_amount += 20 

    def throw_grenade(self):
        """ Throw a grenade """
        grenade = Grenade(self.direction)
        grenade.rect.x = self.rect.x+(self.rect.width/2)
        grenade.rect.y = self.rect.y
        grenade.level = self.level
        self.level.entity_list.add(grenade)
        self.grenade_throw_sound.play()


class Weapon(Base_Entity):
    def __init__(self, player):
        """Superclass for all player weapons."""
        Base_Entity.__init__(self)
        self.player = player
        self.fire_time = 0 # elapsed time between firing
        self.state = 'firing'
        self.reload_time = 100

        self.direction = self.player.direction
        self.level = player.level

        self.fire_sound = None

    def update(self):
        self.rect.center = self.player.rect.center
        self.direction = self.player.direction

        if self.direction == 'R':
            self.image = self.images[0]
        else:
            self.image = self.images[1]

        self.fire_time += 1

class Machete(Weapon):
    """Melee Weapon. Infinite Ammo, close range."""
    def __init__(self, player):
        Weapon.__init__(self, player)
        self.min_fire_time = 50
        self.swinging = False
        self.angle = 0 # sword angle
        self.max_angle = -90
        self.swing_speed = 10 # how fast the sword rotates
        self.swing_dir = 'R'
        self.clip_ammo = 1
        self.ammo_amount = 1

        self.images = []
        self.images.append(pygame.image.load("Resources/Sprites/sprite_machete.png").convert_alpha())
        self.images.append(pygame.transform.flip(self.images[0], True, False)) # Flipped 
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.fire_sound = pygame.mixer.Sound("Resources/Sounds/sound_machete_fire.wav")
        self.hit_sound = pygame.mixer.Sound("Resources/Sounds/sound_machete_hit.wav")

    def update(self):
        Weapon.update(self)

        # Swing Sword
        if self.swinging == True:
            if self.swing_dir == 'R':
                if self.angle >= self.max_angle:
                    self.angle +=- self.swing_speed
                    self.image = self.rot_center( self.image, self.angle)
                else:
                    self.swinging = False
                    self.angle = 0
                    self.fire_time = 0

            elif self.swing_dir == 'L':
                if self.angle <= -self.max_angle:
                    self.angle += self.swing_speed
                    self.image = self.rot_center(self.image, self.angle)
                else:
                    self.swinging = False
                    self.angle = 0
                    self.fire_time = 0

            # Collide with enemies
            enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
            if len(enemy_hit_list) > 0:
                enemy_hit_list[0].kill()
                self.hit_sound.play()


    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def use_weapon(self):
        """Swing Sword"""
        if self.fire_time >= self.min_fire_time:
            self.swinging = True

            self.swing_dir = self.player.direction
            self.fire_sound.play()

    def reload(self):
        """ no need to reload."""
        pass

class Pistol(Weapon):
    """ fires a single bullet at a time, large amount of ammo"""
    def __init__(self, player):
        Weapon.__init__(self, player)
        self.min_fire_time = 8 # minimum time required to shoot
        self.clip_size = 10 # amount of ammo per clip
        self.clip_ammo = 10
        self.ammo_amount = 100
        self.reload_time = 100

        # Image list - [0] facing right and [1] facing left
        self.images = []
        self.images.append(pygame.image.load("Resources/Sprites/sprite_pistol.png").convert_alpha())
        self.images.append(pygame.transform.flip(self.images[0], True, False)) # Flipped 
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.fire_sound = pygame.mixer.Sound("Resources/Sounds/sound_pistol_fire.wav")
        self.reload_sound = pygame.mixer.Sound("Resources/Sounds/sound_pistol_reload.wav")

    def update(self):
        # Reload weapon
        if self.clip_ammo == 0:
            self.state = 'reloading'

        if self.state == 'reloading':
            if self.fire_time == 1:
                self.reload_sound.play()
            if self.fire_time >= self.reload_time:
                if self.ammo_amount > 0:
                    self.clip_ammo = self.clip_size
                    self.state = 'firing'
                    self.ammo_amount +=- self.clip_size

        # Do parent stuff 
        Weapon.update(self)

    def reload(self):
        """Manually reload the weapon"""
        self.state = 'reloading'
        self.fire_time = 0


    def use_weapon(self):
        """Called when player presses the fire button - attempt to use weapon.
        For pistols: reload whole magazine. """
        if self.state == 'firing':
            if self.fire_time >= self.min_fire_time:
                if self.clip_ammo >= 1:
                    self.clip_ammo +=- 1
                    self.fire()
                    self.fire_time = 0

    def fire(self):
        """ attack with current weapon """
        bullet = Bullet(self.direction)
        bullet.rect.x = self.rect.x+(self.rect.width/2)
        bullet.rect.y = self.rect.y+(self.rect.height/2)
        bullet.level = self.level
        self.level.entity_list.add(bullet)
        self.fire_sound.play()


class Shotgun(Weapon):
    """ fires 3 bullets at a time"""
    def __init__(self, player):
        Weapon.__init__(self, player)
        self.images = []
        self.images.append(pygame.image.load("Resources/Sprites/sprite_shotgun.png").convert_alpha())
        self.images.append(pygame.transform.flip(self.images[0], True, False)) # Flipped 
        self.image = self.images[0]

        self.min_fire_time = 50 # minimum time required to shoot
        self.clip_size = 6 # amount of ammo per clip
        self.clip_ammo = 6 # amount of ammo currently in clip
        self.ammo_amount = 20 # maximum starting ammo (all clips) in gun
        self.reload_time = 70 # minimum time it takes to reload
        self.reload_x = 0 # how much it has reloaded

        self.rect = self.image.get_rect()
        self.fire_sound = pygame.mixer.Sound("Resources/Sounds/sound_shotgun_fire.wav")
        self.reload_sound = pygame.mixer.Sound("Resources/Sounds/sound_shotgun_reload.wav")

    def update(self):
        Weapon.update(self)
        self.reload_x += 1

        if self.reload_x >= self.reload_time:
            if self.ammo_amount > 0:
                if self.clip_ammo < self.clip_size:
                    self.clip_ammo += 1
                    self.reload_x = 0
                    self.ammo_amount +=- 1
                    self.reload_sound.play()

    def reload(self):
        """Shotgun's have auto reload - no need to reload."""
        pass

    def use_weapon(self):
        """Called when player presses the fire button - attempt to use weapon.
        For shotguns: incremental """
        if self.fire_time > self.min_fire_time:
            if self.clip_ammo >= 1:
                self.clip_ammo +=- 1
                self.fire()
                self.fire_time = 0
                self.reload_x = 0

                self.fire_sound.play()


    def fire(self):
        """ Fire three bullets """
        for _i in range(3):
            bullet = Bullet(self.direction)
            bullet.rect.x = self.rect.x+(self.rect.width/2)
            bullet.rect.y = self.rect.y+(self.rect.height/2)+(10*_i)
            bullet.level = self.level
            self.level.entity_list.add(bullet)

class Bullet(Base_Entity):
    def __init__(self, direction):
        Base_Entity.__init__(self)
        self.entity_id = 'bullet' # Entity identifier
        self.direction = direction
        self.move_speed = 20
        self.max_time = 50
        self.alive_time = 0

        self.width = 7
        self.height = 7
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.BLACK)
        self.rect = self.image.get_rect()

        self.level = None
        self.hit_sound = random.choice([
            pygame.mixer.Sound("Resources/Sounds/sound_bullet_hit.wav"),
            pygame.mixer.Sound("Resources/Sounds/sound_bullet_hit2.wav")
            ])

    def update(self):
        """Update Bullet"""

        # Delete if max time reached
        if self.alive_time > self.max_time:
            self.kill()
        else:
            self.alive_time += 1

        # Move left/right
        if self.direction == 'L':
            self.rect.x +=- self.move_speed
        else:
            self.rect.x += self.move_speed

        # Collide with objects
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        if len(block_hit_list) > 0:
            self.kill()

        # Collide with enemies
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        if len(enemy_hit_list) > 0:
            self.kill()
            enemy_hit_list[0].health +=- 1
            self.hit_sound.play()

class Grenade(Entity):
    """ Special attack that damages alot of enemies. 
    inherit from Entity as it is affected by gravity """
    def __init__(self, direction):
        Entity.__init__(self)
        self.move_speed = 10
        self.entity_id = 'grenade'
        self.direction = direction
        self.fire_time = 0
        self.explode_time = 100 # time until exploded
        self.explode_radius = 100 # explode radius
        self.exploding = False

        self.image = pygame.image.load("Resources/Sprites/sprite_grenade.png")
        self.rect = self.image.get_rect()

        if self.direction == 'L':
            self.x_vel = -self.move_speed
        else:
            self.x_vel = self.move_speed

        self.explode_sound = pygame.mixer.Sound("Resources/Sounds/sound_grenade_explode.wav")

    def update(self):
        Entity.update(self)
        self.fire_time += 1

        # slow down if landed
        self.rect.y += 1
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        self.rect.y +=- 1
        if len(block_hit_list) > 0:
            if self.direction == 'R':
                if self.x_vel > 0:
                    self.x_vel +=- 1
            else:
                if self.x_vel < 0:
                    self.x_vel += 1

        # explode
        if self.fire_time >= self.explode_time:
            self.exploding = True
            self.explode()

    def explode(self):
        """ Detonate """
        self.explode_sound.play()
        
        # kill enemies in a radius

        # increase rect size
        self.rect.x +=- self.explode_radius
        self.rect.width += self.explode_radius*2
        self.rect.y +=- self.explode_radius
        self.rect.height += self.explode_radius*2


        #hit enemies
        enemy_hit_list  = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemy_hit_list:
            enemy.kill()

        self.kill()


class Ammopack(Base_Entity):
    """ Pickup - entity that drops from the sky and gives the player ammo."""
    def __init__(self, player):
        Base_Entity.__init__(self)
        self.player = player
        self.level = self.player.level
        self.entity_id = 'ammopack'
        self.image = pygame.image.load("Resources/Sprites/sprite_ammopack.png").convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.y_vel = 3 # How fast ammo pack drops
        self.current_pos = self.level.world_shift

    def update(self):
        #move up/down
        self.rect.y += self.y_vel

        # collide with objects
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)

        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.y_vel > 0:
                self.rect.bottom = block.rect.top
            # Stop our vertical movement
            self.y_vel = 0

class Healthpack(Ammopack):
    """A different type of ammo pack - gives health instead."""
    def __init__(self, player):
        Ammopack.__init__(self, player)
        self.entity_id = 'healthpack'
        self.image = pygame.image.load("Resources/Sprites/sprite_healthpack.png").convert_alpha()
        self.rect = self.image.get_rect()
"""

http://superpixeltime.com/

Side Scroller 
ideas:
- Mike Sivali - main character
- Enemies:
	- Student Zombies
- Boss battles:
	- Mr Stack
	- Wirecam

- set in school grounds
- pixel art
- primo bottles for health
- weapons: http://i.imgur.com/4kZny.png
	- Samurai Sword
	- Shotgun
	- Pistol
	- Megaphone
- Snack Shack - armoury
- intercom
rooms:
	- outside the office
	- ranks quad
		- dildo above the podium
	- hallway 
	- new gym

"""
import pygame, sys
from pygame.locals import *


#constants
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


#Init Colours
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)

BG_COLOUR = BLACK

class Base_Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class Entity(Base_Entity):
	"""
	Entity Base Class. For Zombies, player, etc
	"""
	def __init__(self):
		Base_Entity.__init__(self)

		self.max_gravity = 20
		self.jump_speed = 10
		self.gravity_accel = 0.5
		self.move_speed = 7
		self.alive = True

		self.x_vel = 0 
		self.y_vel = 0

		self.width = 20
		self.height = 60
		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(RED)
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
		if self.y_vel == 0:
			self.y_vel = 1
		else:
			self.y_vel += .35
 
		# See if we are on the ground.
		if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.y_vel >= 0:
			self.y_vel = 0
			self.rect.y = SCREEN_HEIGHT - self.rect.height

	def jump(self):
		""" Called when user hits 'jump' button. """
 
		# move down a bit and see if there is a platform below us.
		# Move down 2 pixels because it doesn't work well if we only move down
		# 1 when working with a platform moving down.
		self.rect.y += 2
		block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
		self.rect.y -= 2
 
		# If it is ok to jump, set our speed upwards
		if len(block_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
			self.y_vel = -self.jump_speed

	# Player-controlled movement:
	def go_left(self):
		""" Called when the user hits the left arrow. """
		self.x_vel = -self.move_speed
 
	def go_right(self):
		""" Called when the user hits the right arrow. """
		self.x_vel = self.move_speed
 
	def stop(self):
		""" Called when the user lets off the keyboard. """
		self.x_vel = 0

class Zombie(Entity):
	def __init__(self):
		pass

class Player(Entity):
	def __init__(self):
		Entity.__init__(self)

class Block(Base_Entity):
	def __init__(self, width, height):
		Base_Entity.__init__(self)
		
		self.image = pygame.Surface([width, height])
		self.image.fill(GREEN)
 
		self.rect = self.image.get_rect()

class Level:
	"""Generic superclass used to define a level. Child classes have specific level info."""
	def __init__(self, player):
		self.block_list = pygame.sprite.Group()
		self.enemy_list = pygame.sprite.Group()
		self.player = player

		#draw background
		self.background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
		self.background.fill(WHITE)

		#how far this world has been scrolled left/right
		self.world_shift = 0
		self.level_limit = -1000


	def add_entity(self, entity):
		"""stores and entity then advancess the current ID"""
		self.entities[self.entity_id] = entity
		entity.id = self.entity_id
		self.entity_id += 1

	def remove_entity(self, entity):
		del self.entities[entity.id]

	def update(self):
		self.block_list.update()
		self.enemy_list.update()

	def get(self, entity_id):
		"""find the entity, given its id (or None if not found)"""
		if entity_id in self.entities:
			return self.entities[entity_id]
		else:
			return None

	def render(self, surface):
		"""draw the background and all the entities"""
		surface.blit(self.background, (0,0))
		
		#draw all sprite lists
		self.block_list.draw(surface)
		self.enemy_list.draw(surface)

	def shift_world(self, shift_x):
		""" When the user moves left/right scroll everything:"""
		self.world_shift += shift_x

		# Go through all the sprite lists and shift
		for block in self.block_list:
			block.rect.x += shift_x
 
		for enemy in self.enemy_list:
			enemy.rect.x += shift_x

	def generate_level(self):
		pass

class Level_01(Level):
	"""Level 1: Front of Chapel"""
	def __init__(self, player):
		"""create level"""
		Level.__init__(self, player)

		self.level_limit = -1500

		# Array with width, height, x, and y of blocks
		level = [[210, 70, 500, 500],
				 [210, 70, 800, 400],
				 [210, 70, 1000, 500],
				 [210, 70, 1120, 280],
				 ]

		# Go through the array above and add blocks
		for _block in level:
			block = Block(_block[0], _block[1])
			block.rect.x = _block[2]
			block.rect.y = _block[3]
			block.player = self.player
			self.block_list.add(block)

def terminate():
	pygame.quit()
	sys.exit()

def main():
	pygame.init()

	screen_size = (SCREEN_WIDTH,SCREEN_HEIGHT)
	screen = pygame.display.set_mode(screen_size)

	pygame.display.set_caption("Sivali Simulator") #######CHANGE THIS
	
	# create player
	player = Player()

	# Create all levels
	level_list = []
	level_list.append(Level_01(player))

	#hardcode curent level 
	current_level = level_list[0]
	active_sprite_list = pygame.sprite.Group()
	player.level = current_level
	player.rect.x = 340
	player.rect.y = SCREEN_HEIGHT - player.rect.height
	active_sprite_list.add(player)

	FPSCLOCK = pygame.time.Clock()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.go_left()
				if event.key == pygame.K_RIGHT:
					player.go_right()
				if event.key == pygame.K_UP:
					player.jump()
 
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and player.x_vel < 0:
					player.stop()
				if event.key == pygame.K_RIGHT and player.x_vel > 0:
					player.stop()

		#update level
		active_sprite_list.update()
		current_level.update()

		# Shift the world if the player is near the boundary
		if player.rect.right >= 500:
			diff = player.rect.right - 500
			player.rect.right = 500
			current_level.shift_world(-diff)
 
		# If the player gets near the left side, shift the world right (+x)
		if player.rect.left <= 120:
			diff = 120 - player.rect.left
			player.rect.left = 120
			current_level.shift_world(diff)


		# Draw
		current_level.render(screen)
		active_sprite_list.draw(screen)

		FPSCLOCK.tick(FPS)

		pygame.display.update()

if __name__ == '__main__':
	main()

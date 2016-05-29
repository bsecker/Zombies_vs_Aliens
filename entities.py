import pygame, constants

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
		self.jump_speed = 10
		self.gravity_accel = 0.5
		self.move_speed = 7
		self.alive = True

		self.x_vel = 0 
		self.y_vel = 0
		self.direction = 'L'

		

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
		Entity.__init__(self)
		self.move_speed = 1

	def update(self):
		Entity.update(self)
		self.go_right()

class Player(Entity):
	def __init__(self):
		Entity.__init__(self)

class Block(Base_Entity):
	def __init__(self, width, height):
		Base_Entity.__init__(self)
		
		self.image = pygame.Surface([width, height])
		self.image.fill(GREEN)
 
		self.rect = self.image.get_rect()
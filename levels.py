import pygame
from constants import *
import blocks
import entities

class Level:
	"""Generic superclass used to define a level. Child classes have specific level info."""
	def __init__(self, player):
		self.block_list = pygame.sprite.Group()
		self.enemy_list = pygame.sprite.Group()
		self.player = player

		#draw background
		self.background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
		self.background.fill(BG_COLOUR)

		#how far this world has been scrolled left/right
		self.world_shift = 0


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
		surface.blit(self.background, (self.world_shift // 3,0))
		
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

	def add_zombie(self, x, y):
		#add zombie:
		zombie = entities.Zombie()
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

		self.level_limit = -700
		self.background = pygame.image.load("background_01.png").convert()
		self.background.set_colorkey(WHITE)


		# Array with width, height, x, and y of blocks
		level = [ [blocks.GRASS_LEFT, 500, 500],
				  [blocks.GRASS_MIDDLE, 570, 500],
				  [blocks.GRASS_RIGHT, 640, 500],
				  [blocks.GRASS_LEFT, 800, 400],
				  [blocks.GRASS_MIDDLE, 870, 400],
				  [blocks.GRASS_RIGHT, 940, 400],
				  [blocks.GRASS_LEFT, 1000, 500],
				  [blocks.GRASS_MIDDLE, 1070, 500],
				  [blocks.GRASS_RIGHT, 1140, 500],
				  [blocks.STONE_PLATFORM_LEFT, 1120, 280],
				  [blocks.STONE_PLATFORM_MIDDLE, 1190, 280],
				  [blocks.STONE_PLATFORM_RIGHT, 1260, 280],
				  ]
 
		# Go through the array above and add blocks
		for _block in level:
			block = blocks.Block(_block[0])
			block.rect.x = _block[1]
			block.rect.y = _block[2]
			block.player = self.player
			self.block_list.add(block)

	def spawn_zombies(self):
		"""Handles waves and zombie spawning"""
		zombie = self.add_zombie(230, SCREEN_HEIGHT - self.player.rect.height - 50, self.player)
		active_sprite_list.add(zombie)
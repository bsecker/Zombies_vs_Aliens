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
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768


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
	def __init__(self, world, name):
		Base_Entity.__init__(self)
		self.world = world
		self.name = name

		self.max_gravity = 20
		self.jump_speed = 10
		self.gravity_accel = 0.5
		self.move_speed = 7
		self.alive = True

		self.width = 20
		self.height = 60
		self.image = pygame.Surface([width, height])
		self.image.fill(RED)
		self.rect = self.image.get_rect()

	def update(self):
		pass

	def calc_gravity(self):
		pass

class Zombie(Entity):
	def __init__(self):
		pass

class Player(Entity):
	def __init__(self):
		pass

class World:
	def __init__(self):
		self.entities = {}
		self.entity_id = 0

		#draw background
        self.background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        self.background.fill(WHITE)


	def add_entity(self, entity):
		"""stores and entity then advancess the current ID"""
		self.entities[self.entity_id] = entity

	def remove_entity(self):
		pass

	def update_entity(self):
		pass

	def get_entity(self, entity_id):
		pass

	def render(self, surface):
		pass

	def generate_level(self):
		pass



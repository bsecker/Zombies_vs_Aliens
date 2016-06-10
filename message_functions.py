import pygame
import constants

class Messages(object):
	""" Class used to display messages on the screen. 
	Including messages such as ammo pack drops, death notice, start game, etc
	messages are kept in a stack - new messages are always first in the list
	messages get pushed downwards if another message is called
	"""

	def __init__(self):
		""" Constructor. Initialise variables"""
		self.message_time = 0
		self.fade_time = 0
		self.message_len = 100 # how long a message stays on the screen for
		self.message_stack = []

	def display_message(self, message):
		""" Add message to front of the stack. """
		pass

	def update(self):
		""" update all messages """
		pass

	def draw(self, surface):
		""" draw messages to surface """
		pass
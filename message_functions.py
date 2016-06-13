import pygame
import constants

class Messages(object):
	""" Class used to display messages on the screen. 
	Including messages such as ammo pack drops, death notice, start game, etc
	messages are kept in a stack - new messages are always first in the list
	messages get pushed downwards if another message is called
	"""

	def __init__(self, font):
		""" Constructor. Initialise variables"""
		self.font = font
		self.message_time = 0
		self.fade_time = 0
		self.message_len = 100 # how long a message stays on the screen for
		self.message_stack = []

		self.message_x = constants.HALF_SCREEN_WIDTH
		self.message_y = 150
		self.text_space = 20 # space between messages

	def message(self, message, length = 300):
		""" Add message to front of the stack. """
		self.message_stack.append([message, length])

	def update(self):
		""" update all messages """
		for _i_num, _i in enumerate(self.message_stack):
			if _i[1] > 0:
				_i[1] +=- 1
			else:
				del self.message_stack[_i_num]

	def draw(self, surface):
		""" draw messages to surface """
		for text_num, text in enumerate(self.message_stack[::-1]):
			message_text = self.font.render(text[0], 1, constants.TEXT_COLOUR)
			message_rect = message_text.get_rect()
			message_rect.center = (self.message_x, self.message_y+text_num*self.text_space)
			surface.blit(message_text, message_rect)
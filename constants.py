"""Global Constants"""
import sys
from pygame.locals import *

# Init Colours
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

FPS = 60

# Screen Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
boundary = 350

right_boundary = SCREEN_WIDTH - boundary
left_boundary = boundary

WIN_CAPTION = "Zombie Game"

def terminate():
	"""Terminate pygame, quit nicely"""
	pygame.quit()
	sys.exit()

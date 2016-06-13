"""Global Constants"""
import sys, pygame
from pygame.locals import *

# Init Colours
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (100, 157,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0) 

BG_COLOUR = BLUE
TEXT_COLOUR = GREEN

FPS = 60

# Screen Variables
SCREEN_WIDTH =1200
SCREEN_HEIGHT = 675
HALF_SCREEN_WIDTH = SCREEN_WIDTH/2

boundary = 350

right_boundary = SCREEN_WIDTH - boundary
left_boundary = boundary

WIN_CAPTION = "Really Cool Zombie Game"

def terminate():
    """Terminate pygame, quit nicely"""
    pygame.quit()
    sys.exit()

def translate(value, leftMin, leftMax, rightMin, rightMax):
    """'map' a value in a range to another value"""
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
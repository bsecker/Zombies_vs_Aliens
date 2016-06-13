"""

FONT_CHOOSER
Standalone module to help me choose the right pygame font for games.
Controls:
-left and right - scroll through fonts
-space: print current font in interpreter

"""

import pygame, sys
from pygame.locals import *
 
FPS = 30 # frames per second, the general speed of the program
WIN_WIDTH = 800 # size of window's width in pixels
WIN_HEIGHT = 600 # size of windows' height in pixels
 
HALF_WIN_WIDTH = WIN_WIDTH/2
HALF_WIN_HEIGHT = WIN_HEIGHT/2
 
WIN_CAPTION = 'Font Helper'
 
#Init Colours
#            R    G    B
BLUE     = (  0,   0, 255)
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
 
BGCOLOUR = WHITE

def main():
    global FPSCLOCK, DISPLAYSURF
 
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(WIN_CAPTION)
    FPSCLOCK = pygame.time.Clock()

    font_list = pygame.font.get_fonts()
    font_index = 0
 
 
    while True: #main game loop
        DISPLAYSURF.fill(BGCOLOUR)
 
 
        for event in pygame.event.get(): #event handling loop
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    font_index +=- 1
                if event.key == K_RIGHT:
                    font_index += 1
                if event.key == K_SPACE:
                    print(font_list[font_index])

        font = pygame.font.SysFont(font_list[font_index], 42)
        message_text = font.render('Hello World! My name is Computer.', 1, BLACK)
        message_text_rect = message_text.get_rect()
        message_text_rect.center = (HALF_WIN_WIDTH, HALF_WIN_HEIGHT)
        DISPLAYSURF.blit(message_text, message_text_rect)

        message_text_2 = font.render(font_list[font_index], 1, BLACK)
        message_text_rect_2 = message_text_2.get_rect()
        message_text_rect_2.center = (HALF_WIN_WIDTH, HALF_WIN_HEIGHT)
        message_text_rect_2.centery += 50
        DISPLAYSURF.blit(message_text_2, message_text_rect_2)



 
        pygame.display.update()
        FPSCLOCK.tick(FPS)
 
 
def terminate():
    pygame.quit()
    sys.exit()
 
if __name__=='__main__':
    main()
import pygame
from pygame.locals import *
import constants
import levels
import entities



def main():
    pygame.init()

    screen_size = (constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screen_size, )#pygame.FULLSCREEN)

    pygame.display.set_caption(constants.WIN_CAPTION)
    
    # create player
    player = entities.Player()

    # Create all levels
    level_list = []
    level_list.append(levels.Level_01(player))

    #hardcode curent level 
    current_level = level_list[0]

    player.level = current_level
    player.rect.x = constants.SCREEN_WIDTH/2
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height*2

    current_level.active_sprite_list.add(player)
    current_level.spawn_zombies()

    FPSCLOCK = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                constants.terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_z:
                    bullet = player.fire()
                    current_level.active_sprite_list.add(bullet)
                if event.key == pygame.K_ESCAPE:
                    constants.terminate()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.x_vel < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.x_vel > 0:
                    player.stop()



        #update level
        current_level.active_sprite_list.update()
        current_level.update()
 
        current_position = player.rect.x + current_level.world_shift

        # Shift the world if the player is near the boundary
        if player.rect.right >= constants.right_boundary:
            diff = player.rect.right - constants.right_boundary
            player.rect.right = constants.right_boundary
            if current_position >= current_level.level_limit:
                current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= constants.left_boundary:
            diff = constants.left_boundary - player.rect.left
            player.rect.left = constants.left_boundary
            if current_position <= -current_level.level_limit:
                current_level.shift_world(diff)     


        # Draw
        current_level.render(screen)
        current_level.active_sprite_list.draw(screen)


        FPSCLOCK.tick(constants.FPS)

        pygame.display.update()

if __name__ == '__main__':
    main()
import pygame
from pygame.locals import *
from constants import *
import levels


def main():
	pygame.init()

	screen_size = (SCREEN_WIDTH,SCREEN_HEIGHT)
	screen = pygame.display.set_mode(screen_size, )#pygame.FULLSCREEN)

	pygame.display.set_caption(WIN_CAPTION)
	
	# create player
	player = Player()

	# Create all levels
	level_list = []
	level_list.append(levels.Level_01(player))

	#hardcode curent level 
	current_level = level_list[0]
	active_sprite_list = pygame.sprite.Group()

	player.level = current_level
	player.rect.x = 340
	player.rect.y = SCREEN_HEIGHT - player.rect.height
	active_sprite_list.add(player)

	zombie = current_level.add_zombie(230, SCREEN_HEIGHT - player.rect.height - 50)
	active_sprite_list.add(zombie)

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
				if event.key == pygame.K_ESCAPE:
					terminate()
 
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and player.x_vel < 0:
					player.stop()
				if event.key == pygame.K_RIGHT and player.x_vel > 0:
					player.stop()

		#update level
		active_sprite_list.update()
		current_level.update()
 
		current_position = player.rect.x + current_level.world_shift
		print current_position, current_level.level_limit

		# Shift the world if the player is near the boundary
		if player.rect.right >= right_boundary:
			diff = player.rect.right - right_boundary
			player.rect.right = right_boundary
			if current_position >= current_level.level_limit:
				current_level.shift_world(-diff)
 
		# If the player gets near the left side, shift the world right (+x)
		if player.rect.left <= left_boundary:
			diff = left_boundary - player.rect.left
			player.rect.left = left_boundary
			if current_position <= -current_level.level_limit:
				current_level.shift_world(diff)

		# Draw
		current_level.render(screen)
		active_sprite_list.draw(screen)

		FPSCLOCK.tick(FPS)

		pygame.display.update()

if __name__ == '__main__':
	main()
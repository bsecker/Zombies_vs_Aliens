import pygame
from pygame.locals import *
from constants import *
import levels
import blocks
import entities



def main():
	pygame.init()

	screen_size = (SCREEN_WIDTH,SCREEN_HEIGHT)
	screen = pygame.display.set_mode(screen_size, )#pygame.FULLSCREEN)

	pygame.display.set_caption(WIN_CAPTION)
	
	# create player
	player = entities.Player()

	# Create all levels
	level_list = []
	level_list.append(levels.Level_01(player))

	#hardcode curent level 
	current_level = level_list[0]

	player.level = current_level
	player.rect.x = 340
	player.rect.y = SCREEN_HEIGHT - player.rect.height
	current_level.active_sprite_list.add(player)

	current_level.spawn_zombies()

	FPSCLOCK = pygame.time.Clock()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					player.go_left()
				if event.key == pygame.K_d:
					player.go_right()
				if event.key == pygame.K_w:
					player.jump()
				if event.key == pygame.K_ESCAPE:
					terminate()
 
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a and player.x_vel < 0:
					player.stop()
				if event.key == pygame.K_d and player.x_vel > 0:
					player.stop()

			if event.type == MOUSEBUTTONDOWN:
				bullet = entities.Bullet()
				bullet.rect.x = player.rect.x
				bullet.rect.y = player.rect.y
				current_level.active_sprite_list.add(bullet)

		#update level
		current_level.active_sprite_list.update()
		current_level.update()
 
		current_position = player.rect.x + current_level.world_shift


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
		current_level.active_sprite_list.draw(screen)


		FPSCLOCK.tick(FPS)

		pygame.display.update()

if __name__ == '__main__':
	main()

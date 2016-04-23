import pygame
from pygame.locals import *
import camera, settings

pygame.init()
camera.init()

clock = pygame.time.Clock()
playing = True
while playing:
	dt = 0.001 * clock.tick()
	for event in pygame.event.get():
		if event.type == QUIT:
			playing = False
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				playing = False
			if event.key == K_1:
				camera.zoom(-1)
			if event.key == K_2:
				camera.zoom(1)
	ks = pygame.key.get_pressed()
	dkx = (ks[K_RIGHT] | ks[K_d] | ks[K_e]) - (ks[K_LEFT] | ks[K_a])
	dky = (ks[K_UP] | ks[K_w] | ks[K_COMMA]) - (ks[K_DOWN] | ks[K_s] | ks[K_o])
	camera.scoot((dkx * dt, dky * dt))

	camera.think(dt)

	camera.draw()
	pygame.display.flip()


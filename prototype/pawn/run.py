import pygame
from pygame.locals import *
import camera, settings, state, thing, grid

pygame.init()
camera.init()
thing.init()

def handlemouse(pos):
	if settings.controlscheme == "rando":
		thing.growrandom()

clock = pygame.time.Clock()
playing = True
font = pygame.font.Font(None, 24)
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
		if event.type == MOUSEBUTTONDOWN:
			handlemouse(pygame.mouse.get_pos())
	ks = pygame.key.get_pressed()
	dkx = (ks[K_RIGHT] | ks[K_d] | ks[K_e]) - (ks[K_LEFT] | ks[K_a])
	dky = (ks[K_UP] | ks[K_w] | ks[K_COMMA]) - (ks[K_DOWN] | ks[K_s] | ks[K_o])
	camera.scoot((dkx * dt, dky * dt))

	camera.think(dt)

	camera.draw()
	for t in state.things:
		t.draw()

	mposV = pygame.mouse.get_pos()
	mposG = camera.GconvertV(mposV)
	mposH = grid.HconvertG(mposG)
	lines = [
		"control scheme: %s" % settings.controlscheme,
		"mouse posV: (%d, %d)" % tuple(mposV),
		"mouse posG: (%.2f, %.2f)" % tuple(mposG),
		"mouse posH: (%d, %d)" % tuple(mposH),
		"%.1ffps" % clock.get_fps(),
	]
	for j, line in enumerate(lines):
		img = font.render(line, True, (255, 255, 255))
		camera.screen.blit(img, (10, camera.screen.get_height() - 24 * (len(lines) - j)))
	pygame.display.flip()


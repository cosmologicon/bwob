import pygame
from pygame.locals import *
import camera, settings, state, thing, grid, control

pygame.init()
camera.init()
thing.init()

clock = pygame.time.Clock()
playing = True
font = pygame.font.Font(None, 24)
while playing:
	dt = 0.001 * clock.tick()
	mstate = {
		"pos": pygame.mouse.get_pos(),
		"down": False,
		"up": False,
	}
	kstate = {
		"pressed": pygame.key.get_pressed(),
		"down": set(),
	}
	for event in pygame.event.get():
		if event.type == QUIT:
			playing = False
		if event.type == KEYDOWN:
			kstate["down"].add(event.key)
			if event.key == K_ESCAPE:
				playing = False
		if event.type == MOUSEBUTTONDOWN:
			mstate["down"] = True
		if event.type == MOUSEBUTTONUP:
			mstate["up"] = True
	control.think(dt, mstate, kstate)
	camera.think(dt)
	camera.draw()
	for t in state.things:
		t.draw()
	camera.drawpanel()

	mposV = mstate["pos"]
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


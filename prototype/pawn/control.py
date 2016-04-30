from pygame.locals import *
import thing, camera, settings

cursor = None


def think(dt, mstate, kstate):
	ks = kstate["pressed"]
	dkx = (ks[K_RIGHT] | ks[K_d] | ks[K_e]) - (ks[K_LEFT] | ks[K_a])
	dky = (ks[K_UP] | ks[K_w] | ks[K_COMMA]) - (ks[K_DOWN] | ks[K_s] | ks[K_o])
	camera.scoot((dkx * dt, dky * dt))
	if K_1 in kstate["down"]:
		camera.zoom(-1)
	if K_2 in kstate["down"]:
		camera.zoom(1)


	if settings.controlscheme == "rando":
		if mstate["down"]:
			thing.growrandom()



import pygame
from pygame.locals import *
import thing, camera, settings, state, grid


def clear():
	global cursor
	# Currently selected part, if any
	cursor = None
clear()

def think(dt, mstate, kstate):
	global cursor
	if K_TAB in kstate["down"]:
		s = settings.controlschemes
		settings.controlscheme = s[(s.index(settings.controlscheme) + 1) % len(s)]
		clear()

	ks = kstate["pressed"]
	dkx = (ks[K_RIGHT] | ks[K_d] | ks[K_e]) - (ks[K_LEFT] | ks[K_a])
	dky = (ks[K_UP] | ks[K_w] | ks[K_COMMA]) - (ks[K_DOWN] | ks[K_s] | ks[K_o])
	camera.scoot((dkx * dt, dky * dt))
	if K_1 in kstate["down"]:
		camera.zoom(-1)
	if K_2 in kstate["down"]:
		camera.zoom(1)

	mposV = mstate["pos"]
	mposG = camera.GconvertV(mposV)
	mposH = grid.HconvertG(mposG)
	ingame = camera.grectV.collidepoint(mposV)
	inpanel = camera.prectV.collidepoint(mposV)

	if settings.controlscheme == "rando":
		if mstate["ldown"] and ingame:
			thing.growrandom()
		if mstate["mdown"] and ingame:
			for _ in range(100):
				thing.growrandom()
		if mstate["rdown"] and ingame:
			for _ in range(10):
				thing.growrandom()
	if settings.controlscheme == "tetris":
		if cursor is None:
			cursor = thing.randompart()
		if mstate["ldown"] and ingame and cursor:
			stem = state.edgesH.get(grid.HnearestedgeH(mposH))
			if stem and stem.canattach(cursor):
				thing.grow(stem, cursor)
				cursor = None
		if mstate["ldown"] and inpanel:
			cursor = None

def drawgame():
	if cursor is not None:
		rV = max(1, int(0.25 * camera.VscaleG))
		wV = max(1, int(0.05 * camera.VscaleG))
		for thing in state.things:
			if thing.odgeH and thing.canattach(cursor):
				pV = camera.VconvertG(grid.GconvertH(thing.odgeH[0]))
				pygame.draw.circle(camera.screen, (255, 255, 255), pV, rV, wV)

def drawpanel():
	if settings.controlscheme == "tetris":
		wV, hV = camera.prectV.size
		x0V, y0V = camera.prectV.center
		scale = int(min(wV, hV) * 0.2)
		class view:
			VscaleG = scale
			def VconvertG(self, (xG, yG)):
				return x0V + int(scale * xG), y0V - int(scale * yG)
		if cursor is not None:
			cursor.draw(view())


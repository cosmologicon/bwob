from __future__ import division
import pygame, math
from pygame.locals import *
import thing, camera, settings, state, grid, buttons


def clear():
	global cursor, available
	# Currently selected part, if any
	cursor = None
	if settings.controlscheme == "pyweek":
		available = [None] * 9
		for a in range(9):
			fillslot(a)
	if settings.controlscheme == "utree":
		available = [None] * 9
		map(fillslot, [2, 5, 8])
	
adsG = [(1.4 * dx, 0.9 * dy) for dx, dy in (-1,5),(1,5),(0,3),(-1,1),(1,1),(0,-1),(-1,-3),(1,-3),(0,-5)]
def fillslot(a):
	color, j = divmod(a, 3)
	available[a] = thing.randomorgan(color = color) if j == 2 else thing.randomstalk(color = color)
def availableat((xV, yV)):
	wV, hV = camera.prectV.size
	x0V, y0V = camera.prectV.center
	VscaleG = int(min(wV, hV) * 0.2)
	xG = (xV - x0V) / VscaleG
	yG = -(yV - y0V) / VscaleG
	for (axG, ayG), part in zip(adsG, available):
		dG = math.sqrt((xG - axG) ** 2 + (yG - ayG) ** 2)
		if dG < 0.9:
			return part
	return None
clear()

def think(dt, mstate, kstate):
	global cursor, mposG
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
		if mstate["ldown"] and buttons.paxe.contains(mposV):
			cursor = None if cursor is buttons.paxe else buttons.paxe
		elif mstate["ldown"] and buttons.oaxe.contains(mposV):
			cursor = None if cursor is buttons.oaxe else buttons.oaxe
		elif mstate["ldown"] and cursor is buttons.paxe:
			part = state.edgesH.get(grid.HnearestedgeH(mposH))
			if part and part.canaxe:
				thing.axe(part)
			cursor = None
		elif mstate["ldown"] and cursor is buttons.oaxe:
			for obj in state.things:
				for odgeH in obj.oaxetargets():
					if thing.withinodgeH(odgeH, mposG):
						obj.oaxeat(odgeH)
			cursor = None
		elif mstate["ldown"] and ingame:
			thing.growrandom()
		elif mstate["mdown"] and ingame:
			for _ in range(100):
				thing.growrandom()
		elif mstate["rdown"] and ingame:
			for _ in range(10):
				thing.growrandom()
	if settings.controlscheme == "tetris":
		if mstate["ldown"] and buttons.paxe.contains(mposV):
			cursor = None if cursor is buttons.paxe else buttons.paxe
		elif mstate["ldown"] and buttons.oaxe.contains(mposV):
			cursor = None if cursor is buttons.oaxe else buttons.oaxe
		elif mstate["ldown"] and cursor is buttons.paxe:
			part = state.edgesH.get(grid.HnearestedgeH(mposH))
			if part and part.canaxe:
				thing.axe(part)
			cursor = None
		elif mstate["ldown"] and cursor is buttons.oaxe:
			for obj in state.things:
				for odgeH in obj.oaxetargets():
					if thing.withinodgeH(odgeH, mposG):
						obj.oaxeat(odgeH)
			cursor = None
		if cursor is None:
			cursor = thing.randompart()
		elif mstate["ldown"] and ingame and cursor:
			stem = state.edgesH.get(grid.HnearestedgeH(mposH))
			if stem and stem.canattach(cursor):
				thing.grow(stem, cursor)
				cursor = None
		elif mstate["ldown"] and inpanel:
			cursor = None
	if settings.controlscheme == "pyweek":
		if mstate["ldown"] and buttons.paxe.contains(mposV):
			cursor = None if cursor is buttons.paxe else buttons.paxe
		elif mstate["ldown"] and buttons.oaxe.contains(mposV):
			cursor = None if cursor is buttons.oaxe else buttons.oaxe
		elif mstate["ldown"] and cursor is buttons.paxe:
			part = state.edgesH.get(grid.HnearestedgeH(mposH))
			if part and part.canaxe:
				thing.axe(part)
			cursor = None
		elif mstate["ldown"] and cursor is buttons.oaxe:
			for obj in state.things:
				for odgeH in obj.oaxetargets():
					if thing.withinodgeH(odgeH, mposG):
						obj.oaxeat(odgeH)
			cursor = None
		elif (mstate["ldown"] or mstate["lup"]) and ingame and cursor:
			stem = state.edgesH.get(grid.HnearestedgeH(mposH))
			if stem and stem.canattach(cursor):
				thing.grow(stem, cursor)
				for j, part in enumerate(available):
					if part is cursor:
						fillslot(j)
				cursor = None
		elif mstate["ldown"] and inpanel:
			part = availableat(mposV)
			cursor = None if part is cursor else part
		elif mstate["rdown"] and inpanel:
			part = availableat(mposV)
			if part:
				fillslot(available.index(part))
	if settings.controlscheme == "utree":
		if mstate["ldown"] and buttons.paxe.contains(mposV):
			cursor = None if cursor is buttons.paxe else buttons.paxe
		elif mstate["ldown"] and buttons.oaxe.contains(mposV):
			cursor = None if cursor is buttons.oaxe else buttons.oaxe
		elif mstate["ldown"] and cursor is buttons.paxe:
			part = state.edgesH.get(grid.HnearestedgeH(mposH))
			if part and part.canaxe:
				thing.axe(part)
			cursor = None
		elif mstate["ldown"] and cursor is buttons.oaxe:
			for obj in state.things:
				for odgeH in obj.oaxetargets():
					if thing.withinodgeH(odgeH, mposG):
						obj.oaxeat(odgeH)
			cursor = None
		elif (mstate["ldown"] or mstate["lup"]) and ingame and isinstance(cursor, thing.Organ):
			stem = state.edgesH.get(grid.HnearestedgeH(mposH))
			if stem and stem.canattach(cursor):
				thing.grow(stem, cursor)
				for j, part in enumerate(available):
					if part is cursor:
						fillslot(j)
				cursor = None
		elif mstate["ldown"] and inpanel:
			part = availableat(mposV)
			cursor = None if part is cursor else part
		elif mstate["ldown"] and ingame and cursor is None:
			part = state.edgesH.get(grid.HnearestedgeH(mposH))
			if isinstance(part, (thing.Stalk, thing.Stem)):
				cursor = part
		elif mstate["ldown"] and ingame and isinstance(cursor, (thing.Stalk, thing.Stem)):
			edgeH = grid.HnearestedgeH(mposH)
			redge = grid.redgefromodgeH(cursor.odgeH, edgeH)
			if redge is not None and state.edgesH.get(edgeH) is None:
				cursor.addstalk(redge)
			cursor = None
		elif mstate["lup"] and ingame and isinstance(cursor, (thing.Stalk, thing.Stem)):
			edgeH = grid.HnearestedgeH(mposH)
			redge = grid.redgefromodgeH(cursor.odgeH, edgeH)
			if redge is not None and state.edgesH.get(edgeH) is None:
				cursor.addstalk(redge)
				cursor = None
		elif mstate["rdown"] and inpanel:
			part = availableat(mposV)
			if part:
				fillslot(available.index(part))

# Bezier control points stretching from odgeH to pG
# See notes dated 28 May 2016
def Gstretchpoints(odgeH, pG):
	x0G, y0G = grid.GconvertH(odgeH[0])
	x1G, y1G = grid.GconvertH(odgeH[1])
	x3G, y3G = pG
	nxG, nyG = x1G - x0G, y1G - y0G
	hxG, hyG = (x3G - x0G) / 2, (y3G - y0G) / 2
	hdotn = hxG * nxG + hyG * nyG
	hcrossn = hxG * nyG - hyG * nxG
	if hdotn <= 0:
		mxG, myG = -nxG, -nyG
	else:
		xcG = x0G + hxG - hyG * hcrossn / hdotn
		ycG = y0G + hyG + hxG * hcrossn / hdotn
		mxG, myG = x3G - xcG, y3G - ycG
		m = math.sqrt(mxG ** 2 + myG ** 2)
		if m == 0:
			mxG, myG = nxG, nyG
		else:
			mxG /= m
			myG /= m
	return (x0G, y0G), (x0G + nxG, y0G + nyG), (x3G, y3G), (x3G + mxG, y3G + myG)

def drawgame():
	if cursor is None:
		pass
	elif cursor in [buttons.paxe]:
		for obj in state.things:
			if obj.odgeH and obj.canaxe:
				obj.drawdot((255, 100, 100))
	elif cursor in [buttons.oaxe]:
		for obj in state.things:
			for odgeH in obj.oaxetargets():
				thing.drawdotodgeH(odgeH, (255, 100, 100))
	elif settings.controlscheme == "pyweek" or settings.controlscheme == "utree" and isinstance(cursor, thing.Organ):
		for obj in state.things:
			if obj.odgeH and obj.canattach(cursor):
				obj.drawdot((255, 255, 255))
	elif settings.controlscheme == "utree" and isinstance(cursor, (thing.Stalk, thing.Stem)):
		for dedge in (1, 2, 3, 4, 5):
			edgeH, _ = grid.HturnodgeH(cursor.odgeH, dedge)
			if state.edgesH.get(edgeH) is None:
				thing.drawdotG(grid.GconvertH(edgeH), 0.4, (255, 255, 255))
		pointsG = Gstretchpoints(cursor.odgeH, mposG)
		psV = thing.VbezierpsG(*pointsG, bend = settings.bends[cursor.color], view = camera)
		thing.drawwithborder(psV, settings.colors[cursor.color], 0.2)


def drawpanel():
	if settings.controlscheme == "tetris":
		if cursor not in [None, buttons.paxe]:
			wV, hV = camera.prectV.size
			x0V, y0V = camera.prectV.center
			scale = int(min(wV, hV) * 0.18)
			class view:
				VscaleG = scale
				def VconvertG(self, (xG, yG)):
					return x0V + int(scale * xG), y0V - int(scale * yG)
			cursor.draw(view())
	if settings.controlscheme in ("pyweek", "utree"):
		wV, hV = camera.prectV.size
		x0V, y0V = camera.prectV.center
		scale = int(min(wV, hV) * 0.2)
		class view:
			VscaleG = scale
			def VconvertG(self, (xG, yG)):
				return x0V + int(scale * (xG + dxG)), y0V - int(scale * (yG + dyG))
		for (dxG, dyG), part in zip(adsG, available):
			if part is None:
				continue
			if part is cursor:
				rV = int(view.VscaleG * 0.9)
				pygame.draw.circle(camera.screen, (255, 255, 255), view().VconvertG((0, 0)), rV, 2)
			part.draw(view())
	for button in [buttons.paxe, buttons.oaxe]:
		button.draw()


from __future__ import division

import pygame, math
import settings, grid

# gameplay area
grectV = pygame.Rect((0, 0, settings.gx, settings.wy))
# panel area
prectV = pygame.Rect((settings.gx, 0, settings.wx - settings.gx, settings.wy))

screen = None
def init():
	global screen
	screen = pygame.display.set_mode((settings.wx, settings.wy))


x0G = 0
y0G = 0
z0 = 0
VscaleG = settings.zoom0

def VconvertG((xG, yG)):
	x0V, y0V = grectV.center
	return x0V + int(VscaleG * (xG - x0G)), int(y0V - VscaleG * (yG - y0G))
def GconvertV((xV, yV)):
	x0V, y0V = grectV.center
	return x0G + (xV - x0V) / VscaleG, y0G - (yV - y0V) / VscaleG

def scoot((dx, dy)):
	global x0G, y0G
	x0G += 70 * dx / math.sqrt(VscaleG)
	y0G += 70 * dy / math.sqrt(VscaleG) 

def zoom(dz):
	global z0, VscaleG
	z0 = min(max(z0 + 0.2 * dz, settings.zoomrange[0]), settings.zoomrange[1])
	VscaleG = settings.zoom0 * math.exp(z0)
	

def think(dt):
	pass



def draw():
	w2V, h2V = grectV.width / 2, grectV.height / 2
	xminG = x0G - w2V / VscaleG
	xmaxG = x0G + w2V / VscaleG
	yminG = y0G - h2V / VscaleG
	ymaxG = y0G + h2V / VscaleG

	screen.fill((10, 10, 10), grectV)
	for p0G, p1G in grid.GedgeswithinG((xminG, yminG, xmaxG, ymaxG)):
		pygame.draw.line(screen, (100, 50, 0), VconvertG(p0G), VconvertG(p1G), 1)

def drawpanel():
	screen.fill((200, 160, 200), prectV)



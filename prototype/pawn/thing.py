import pygame, random, math
import camera, grid, state, settings


class Part(object):
	def __init__(self, pH):
		self.pH = pH
		self.pG = grid.GconvertH(pH)
		self.odgeH = None
		self.parent = None
		self.children = {}

	def addtostate(self):
		if self.odgeH:
			edgeH, pH = self.odgeH
			state.edgesH[edgeH] = self
		state.things.append(self)
		for pH, child in self.children.items():
			child.addtostate()

	def attachtoparent(self):
		self.parent.children[self.odgeH] = self

	def removefromstate(self):
		for pH, child in self.children.items():
			child.removefromstate()
		if self in state.things:
			state.things.remove(self)
		if self.odgeH:
			edgeH, pH = self.odgeH
			state.edgesH[edgeH] = None

	def randomstem(self):
		return random.choice(self.children.values()).randomstem()

	def canplace(self, toreplace = None):
		if not all(child.canplace(toreplace) for child in self.children.values()):
			return False
		obj = state.edgesH.get(self.odgeH[0])
		return obj is None or obj in (toreplace or [])

class Core(Part):
	def __init__(self):
		Part.__init__(self, (0, 0))
		colors = 0, 1, 2, 0, 1, 2
		for color, odgeH in zip(colors, grid.HhexodgesH(self.pH)):
			self.children[odgeH] = Stem(odgeH, color, self)

	def draw(self):
		centerV = camera.VconvertG(self.pG)
		rV = int(0.8 * camera.VscaleG)
		pygame.draw.circle(camera.screen, (200, 200, 200), centerV, rV)

def VstempsH(odgeH, bend):
	edgeH, centerH = odgeH
	x0G, y0G = grid.GconvertH(edgeH)
	x1G, y1G = grid.GconvertH(centerH)
	f = 0.3
	dxG, dyG = f * (x1G - x0G), f * (y1G - y0G)
	S, C = math.sin(bend), math.cos(bend)
	dxG, dyG = C * dxG + S * dyG, -S * dxG + C * dyG
	return camera.VconvertG((x0G, y0G)), camera.VconvertG((x0G + dxG, y0G + dyG))

def VstalkpsH(odge0H, odge1H, bend):
	x0G, y0G = grid.GconvertH(odge0H[0])
	x1G, y1G = grid.GconvertH(odge0H[1])
	x2G, y2G = grid.GconvertH(odge1H[0])
	x3G, y3G = grid.GconvertH(odge1H[1])

	dx1G, dy1G = x1G - x0G, y1G - y0G
	dx2G, dy2G = x3G - x2G, y3G - y2G
	a1, a2 = 0.7, 0.4
	S, C = math.sin(bend), math.cos(bend)
	dx1G, dy1G = a1 * (C * dx1G + S * dy1G), a1 * (-S * dx1G + C * dy1G)
	dx2G, dy2G = a2 * (C * dx2G + S * dy2G), a2 * (-S * dx2G + C * dy2G)

	anchorsG = (x0G, y0G), (x0G + dx1G, y0G + dy1G), (x2G - dx2G, y2G - dy2G), (x2G, y2G)
	return map(camera.VconvertG, grid.GbezierG(anchorsG))


class Stem(Part):
	def __init__(self, odgeH, color, parent):
		edgeH, pH = odgeH
		Part.__init__(self, pH)
		self.odgeH = odgeH
		self.color = color
		self.parent = parent

	def randomstem(self):
		return self

	def tostalk(self, branchspec):
		return Stalk(self.odgeH, self.color, self.parent, branchspec)

	def draw(self):
		wV = max(1, int(0.2 * camera.VscaleG))
		wborderV = 2 + wV + int(0.06 * camera.VscaleG)
		p0V, p1V = VstempsH(self.odgeH, settings.bends[self.color])
		pygame.draw.line(camera.screen, (0, 0, 0), p0V, p1V, wborderV)
		pygame.draw.line(camera.screen, settings.colors[self.color], p0V, p1V, wV)

class Stalk(Part):
	def __init__(self, odgeH, color, parent, branchspec):
		edgeH, pH = odgeH
		Part.__init__(self, pH)
		self.odgeH = odgeH
		self.color = color
		self.parent = parent
		self.branchspec = branchspec
		for nrot in branchspec:
			sodgeH = grid.HpathodgeH(self.odgeH, nrot)
			self.children[sodgeH] = Stem(sodgeH, self.color, self)

	def draw(self):
		wV = max(1, int(0.2 * camera.VscaleG))
		wborderV = 2 + wV + int(0.06 * camera.VscaleG)
		for sodgeH in sorted(self.children):
			psV = VstalkpsH(self.odgeH, sodgeH, settings.bends[self.color])
			pygame.draw.lines(camera.screen, (0, 0, 0), False, psV, wborderV)
			pygame.draw.lines(camera.screen, settings.colors[self.color], False, psV, wV)

branchspecs = (1,), (2,), (3,), (4,), (5,), (1,3), (1,4), (2,3), (2,4), (2,5), (3,4), (3,5)

def growrandom():
	stem = state.core.randomstem()
	for _ in range(20):
		branchspec = random.choice(branchspecs)
		stalk = stem.tostalk(branchspec)
		if stalk.canplace([stem]):
			stem.removefromstate()
			stalk.addtostate()
			stalk.attachtoparent()
			break

def init():
	state.core = Core()
	state.core.addtostate()


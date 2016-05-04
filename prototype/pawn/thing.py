import pygame, random, math
import camera, grid, state, settings


class Part(object):
	occupiestile = False
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
		if self.occupiestile:
			state.tilesH[self.pH] = self
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
			if self.occupiestile:
				state.tilesH[pH] = self

	def randomstem(self):
		return random.choice(self.children.values()).randomstem()

	def canplace(self, toreplace = None):
		if not all(child.canplace(toreplace) for child in self.children.values()):
			return False
		obj = state.edgesH.get(self.odgeH[0])
		if obj is not None and obj not in (toreplace or []):
			return False
		if self.occupiestile:
			obj = state.tilesH.get(self.odgeH[1])
			if obj is not None and obj not in (toreplace or []):
				return False
		return True

	def canattach(self, part):
		return False

class Core(Part):
	occupiestile = True
	def __init__(self):
		Part.__init__(self, (0, 0))
		colors = 0, 1, 2, 0, 1, 2
		for color, odgeH in zip(colors, grid.HhexodgesH(self.pH)):
			self.children[odgeH] = Stem(odgeH, color, self)

	def draw(self, view = None):
		view = view or camera
		centerV = view.VconvertG(self.pG)
		rV = int(0.8 * view.VscaleG)
		pygame.draw.circle(camera.screen, (200, 200, 200), centerV, rV)

def VstempsH(odgeH, bend, view):
	edgeH, centerH = odgeH
	x0G, y0G = grid.GconvertH(edgeH)
	x1G, y1G = grid.GconvertH(centerH)
	f = 0.3
	dxG, dyG = f * (x1G - x0G), f * (y1G - y0G)
	S, C = math.sin(bend), math.cos(bend)
	dxG, dyG = C * dxG + S * dyG, -S * dxG + C * dyG
	return view.VconvertG((x0G, y0G)), view.VconvertG((x0G + dxG, y0G + dyG))

def VstalkpsH(odge0H, odge1H, bend, view):
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
	return map(view.VconvertG, grid.GbezierG(anchorsG))


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

	def toorgan(self, label):
		return Organ(self.odgeH, self.color, self.parent, label)

	def canattach(self, part):
		if part.color != self.color:
			return False
		apart = part.attachtostem(self)
		if not apart.canplace([self]):
			return False
		return True

	def draw(self, view = None):
		view = view or camera
		wV = max(1, int(0.2 * view.VscaleG))
		wborderV = 2 + wV + int(0.06 * view.VscaleG)
		p0V, p1V = VstempsH(self.odgeH, settings.bends[self.color], view)
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

	def attachtostem(self, stem):
		return stem.tostalk(self.branchspec)

	def draw(self, view = None):
		view = view or camera
		wV = max(1, int(0.2 * view.VscaleG))
		wborderV = 2 + wV + int(0.06 * view.VscaleG)
		for sodgeH in sorted(self.children):
			psV = VstalkpsH(self.odgeH, sodgeH, settings.bends[self.color], view)
			pygame.draw.lines(camera.screen, (0, 0, 0), False, psV, wborderV)
			pygame.draw.lines(camera.screen, settings.colors[self.color], False, psV, wV)

class Organ(Part):
	occupiestile = True
	def __init__(self, odgeH, color, parent, label):
		edgeH, pH = odgeH
		Part.__init__(self, pH)
		self.odgeH = odgeH
		self.color = color
		self.parent = parent
		self.label = label

	def randomstem(self):
		return None

	def attachtostem(self, stem):
		return stem.toorgan(self.label)

	def draw(self, view = None):
		view = view or camera
		wV = max(1, int(0.2 * view.VscaleG))
		wborderV = 2 + wV + int(0.06 * view.VscaleG)
		rV = max(1, int(0.5 * view.VscaleG))
		routV = 1 + rV + int(0.04 * view.VscaleG)
		p0V = view.VconvertG(grid.GconvertH(self.odgeH[0]))
		p1V = view.VconvertG(grid.GconvertH(self.odgeH[1]))
		pygame.draw.line(camera.screen, (0, 0, 0), p0V, p1V, wborderV)
		pygame.draw.circle(camera.screen, (0, 0, 0), p1V, routV, 0)
		pygame.draw.line(camera.screen, settings.colors[self.color], p0V, p1V, wV)
		pygame.draw.circle(camera.screen, settings.colors[self.color], p1V, rV, 0)
		fontsize = max(2, int(0.8 * view.VscaleG))
		font = pygame.font.Font(None, fontsize)
		surf = font.render(self.label, True, (0, 0, 0))
		camera.screen.blit(surf, surf.get_rect(center = p1V))

branchspecs = (1,), (2,), (3,), (4,), (5,), (1,3), (1,4), (2,3), (2,4), (2,5), (3,4), (3,5)

def randompart():
	color = random.choice([0, 1, 2])
	odgeH = (0, -3), (0, 0)
	if random.random() < 0.1:
		label = random.choice("WXYZ")
		return Organ(odgeH, color, None, label)
	else:
		branchspec = random.choice(branchspecs)
		return Stalk(odgeH, color, None, branchspec)

def grow(stem, part):
	part = part.attachtostem(stem)
	stem.removefromstate()
	part.addtostate()
	part.attachtoparent()

def growrandom():
	for _ in range(20):
		stem = state.core.randomstem()
		if stem:
			break
	if not stem:
		return
	for _ in range(20):
		part = randompart()
		if stem.canattach(part):
			grow(stem, part)
			break

		

def init():
	state.core = Core()
	state.core.addtostate()

import pygame, random, math
import camera, grid, state, settings


def drawdotG(pG, rG, color, view = None):
	view = view or camera
	rV = max(1, int(rG * view.VscaleG))
	wV = max(1, int(0.2 * rG * view.VscaleG))
	pV = view.VconvertG(pG)
	pygame.draw.circle(camera.screen, color, pV, rV, wV)

def drawwithborder(psV, color, wG, view = None):
	view = view or camera
	wV = max(1, int(wG * view.VscaleG))
	wborderV = 2 + wV + int(0.06 * view.VscaleG)
	pygame.draw.lines(camera.screen, (0, 0, 0), False, psV, wborderV)
	pygame.draw.lines(camera.screen, color, False, psV, wV)

class Part(object):
	occupiestile = False
	canaxe = False
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

	def drawdot(self, color, view = None):
		drawdotG(grid.GconvertH(self.odgeH[0]), 0.25, color, view)

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

def VbezierpsG((x0G, y0G), (x1G, y1G), (x2G, y2G), (x3G, y3G), bend, view):
	view = view or camera
 	dx1G, dy1G = x1G - x0G, y1G - y0G
	dx2G, dy2G = x3G - x2G, y3G - y2G
	a1, a2 = 0.7, 0.4
	S, C = math.sin(bend), math.cos(bend)
	dx1G, dy1G = a1 * (C * dx1G + S * dy1G), a1 * (-S * dx1G + C * dy1G)
	dx2G, dy2G = a2 * (C * dx2G + S * dy2G), a2 * (-S * dx2G + C * dy2G)

	anchorsG = (x0G, y0G), (x0G + dx1G, y0G + dy1G), (x2G - dx2G, y2G - dy2G), (x2G, y2G)
	return map(view.VconvertG, grid.GbezierG(anchorsG))


def VstalkpsH(odge0H, odge1H, bend, view):
	return VbezierpsG(
		grid.GconvertH(odge0H[0]),
		grid.GconvertH(odge0H[1]),
		grid.GconvertH(odge1H[0]),
		grid.GconvertH(odge1H[1]),
		bend, view
	)


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

	def addstalk(self, redge):
		stalk = self.tostalk((redge,))
		stalk.attachtoparent()
		self.removefromstate()
		stalk.addtostate()

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
		p0V, p1V = VstempsH(self.odgeH, settings.bends[self.color], view)
		drawwithborder([p0V, p1V], settings.colors[self.color], 0.2, view)

class Stalk(Part):
	canaxe = True
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

	def tostem(self):
		return Stem(self.odgeH, self.color, self.parent)

	def attachtostem(self, stem):
		return stem.tostalk(self.branchspec)

	def addstalk(self, redge):
		branchspec = tuple(sorted(self.branchspec + (redge,)))
		stalk = Stalk(self.odgeH, self.color, self.parent, branchspec)
		for thing in self.children.values():
			thing.parent = stalk
			thing.attachtoparent()
		stalk.attachtoparent()
		self.removefromstate()
		stalk.addtostate()

	def draw(self, view = None):
		for sodgeH in sorted(self.children):
			psV = VstalkpsH(self.odgeH, sodgeH, settings.bends[self.color], view)
			drawwithborder(psV, settings.colors[self.color], 0.2, view)

class Organ(Part):
	occupiestile = True
	canaxe = True
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

	def tostem(self):
		return Stem(self.odgeH, self.color, self.parent)

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

class Starget(object):
	def __init__(self, pH, color):
		self.pH = pH
		self.odgeH = None
		self.pG = grid.GconvertH(self.pH)
		self.color = color
		self.color0 = [int(0.5 * a) for a in settings.colors[color]]
		self.color1 = [min(int(1.5 * a), 255) for a in settings.colors[color]]
	def addtostate(self):
		state.tilesH[self.pH] = self
		state.things.append(self)
	def canplace(self, objs=[]):
		return self.pH not in state.tilesH or state.tilesH[self.pH] in objs
	def think(self, dt):
		pass
	def isactive(self):
		for pH in grid.HhexedgesH(self.pH):
			part = state.edgesH.get(pH)
			if part and (part.pH, part.color) == (self.pH, self.color):
				return True
		return False
	def draw(self):
		xG, yG = self.pG
		dG = 0.6
		psG = [
			(xG + dG * math.sin(a), yG +	 dG * math.cos(a))
			for a in [2 * j * math.tau / 5 for j in range(5)]
		]
		psV = map(camera.VconvertG, psG)
		wV = max(1, int(0.02 * camera.VscaleG))
		color = self.color1 if self.isactive() else self.color0
		pygame.draw.lines(camera.screen, color, True, psV, wV)

def randomorgan(color = None):
	if color is None:
		color = random.choice([0, 1, 2])
	odgeH = (0, -3), (0, 0)
	label = random.choice("WXYZ")
	return Organ(odgeH, color, None, label)
def randomstalk(color = None):
	if color is None:
		color = random.choice([0, 1, 2])
	odgeH = (0, -3), (0, 0)
	branchspec = random.choice(settings.branchspecs)
	return Stalk(odgeH, color, None, branchspec)
def randompart(color = None):
	if random.random() < 0.1:
		return randomorgan(color)
	else:
		return randomstalk(color)

def randomstarget(d):
	while True:
		x, y = random.randint(-d, d), random.randint(-d, d)
		if -d <= x + y <= d:
			break
	color = random.choice([0, 1, 2])
	return Starget((6 * x, 6 * y), color)

def grow(stem, part):
	part = part.attachtostem(stem)
	stem.removefromstate()
	part.addtostate()
	part.attachtoparent()
def axe(part):
	stem = part.tostem()
	part.removefromstate()
	stem.addtostate()
	stem.attachtoparent()

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
	for _ in range(80):
		starget = randomstarget(30)
		if starget.canplace():
			starget.addtostate()


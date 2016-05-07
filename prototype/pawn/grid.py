from __future__ import division

s = 0.8660254037844386  # Hexagonal inradius = sqrt(3) / 2

def GconvertH((xH, yH)):
	return 1/4 * xH, s/6 * xH + s/3 * yH
def HconvertG((xG, yG)):
	return int(round(4 * xG)), int(round(-2 * xG + 4*s * yG))
def HnearesthexH((xH, yH)):
	x0H, dxH = divmod(xH / 6, 1)
	y0H, dyH = divmod(yH / 6, 1)
	A, B, C = dxH - dyH, dxH + 2 * dyH, 2 * dxH + dyH
	if B < 1 > C:
		dxH, dyH = 0, 0
	elif B > 2 < C:
		dxH, dyH = 1, 1
	elif A > 0:
		dxH, dyH = 1, 0
	else:
		dxH, dyH = 0, 1
	return 6 * int(round(x0H + dxH)), 6 * int(round(y0H + dyH))
def HnearestedgeH((xH, yH)):
	x0H, dxH = divmod(xH / 6, 1)
	y0H, dyH = divmod(yH / 6, 1)
	A, B, C = dxH - dyH, dxH + 2 * dyH, 2 * dxH + dyH
	if B > 2 or C > 2:
		if A > 0:
			dxH, dyH = 1, 0.5
		else:
			dxH, dyH = 0.5, 1
	elif B < 1 or C < 1:
		if A > 0:
			dxH, dyH = 0.5, 0
		else:
			dxH, dyH = 0, 0.5
	else:
		dxH, dyH = 0.5, 0.5
	return int(round(6 * (x0H + dxH))), int(round(6 * (y0H + dyH)))


def GedgeswithinG((x0G, y0G, x1G, y1G)):
	pcornerHs = [HnearesthexH(HconvertG((xG, yG))) for xG in (x0G, x1G) for yG in (y0G, y1G)]
	xcornerHs, ycornerHs = zip(*pcornerHs)
	x0H, x1H = min(xcornerHs), max(xcornerHs) + 6
	y0H, y1H = min(ycornerHs), max(ycornerHs)
	
	dHs = (-2, -2), (-4, 2), (-2, 4), (2, 2)
	for xH in range(x0H, x1H, 6):
		for yH in range(y0H, y1H, 6):
			pGs = [GconvertH((xH + dxH, yH + dyH)) for dxH, dyH in dHs]
			for j in range(3):
				yield pGs[j], pGs[j + 1]
def GnearestedgeG(pG):
	return GconvertH(HnearestedgeH(HconvertG(pG)))


def GbezierG(((x0G, y0G), (x1G, y1G), (x2G, y2G), (x3G, y3G)), N = 20):
	curve = []
	for n in range(N + 1):
		f = n / N
		g = 1 - f
		curve.append((
			g ** 3 * x0G + 3 * f * g * (g * x1G + f * x2G) + f ** 3 * x3G,
			g ** 3 * y0G + 3 * f * g * (g * y1G + f * y2G) + f ** 3 * y3G
		))
	return curve

def GbezierH(psH, N = 20):
	return GbezierG([GconvertH(pH) for pH in psH], N)

edgedsH = (3, 0), (0, 3), (-3, 3), (-3, 0), (0, -3), (3, -3)
vertexdsH = (2, 2), (-2, 4), (-4, 2), (-2, -2), (2, -4), (4, -2)

def HhexedgesH((xH, yH)):
	for dxH, dyH in edgedsH:
		yield xH + dxH, yH + dyH
# An odge (oriented edge) is an edge along with one of its two orientations. Its position is given
# by a pair of H-points (edgeH, tileH), which are the position of the edge itself, and the tile that
# the odge is pointing INTO.
def HhexodgesH((xH, yH)):
	for dxH, dyH in edgedsH:
		yield (xH + dxH, yH + dyH), (xH + 2 * dxH, yH + 2 * dyH)

def HflipodgeH(((edgexH, edgeyH), (tilexH, tileyH))):
	return (edgexH, edgeyH), (2 * edgexH - tilexH, 2 * edgeyH - tileyH)

def HturnodgeH(((edgexH, edgeyH), (tilexH, tileyH)), nrot):
	dxH, dyH = tilexH - edgexH, tileyH - edgeyH
	for _ in range(nrot % 6):
		dxH, dyH = -dyH, dxH + dyH
	return (tilexH - dxH, tileyH - dyH), (tilexH, tileyH)
	
def HpathodgeH(odgeH, nrot):
	return HflipodgeH(HturnodgeH(odgeH, nrot))


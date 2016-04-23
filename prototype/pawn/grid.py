from __future__ import division

s = 0.8660254037844386  # Hexagonal inradius = sqrt(3) / 2

def GconvertH((xH, yH)):
	return 1/4 * xH, s/6 * xH + s/3 * yH
def HconvertG((xG, yG)):
	return int(round(4 * xG)), int(round(-2 * xG + 4*s * yG))
def HnearesthexH((xH, yH)):
	return int(round(xH / 6)) * 6, int(round(yH / 6)) * 6

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
				

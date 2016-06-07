import pygame
import camera

class Button(object):
	rV = 30
	fontsize = 40
	def __init__(self, name, pV):
		self.name = name
		self.pV = pV
	def draw(self):
		import control
		color = (140, 60, 60) if self is control.cursor else (80, 0, 0)
		pygame.draw.circle(camera.screen, color, self.pV, self.rV, 0)
		surf = pygame.font.Font(None, self.fontsize).render(self.name, True, (0, 0, 0))
		camera.screen.blit(surf, surf.get_rect(center = self.pV))
		
	def contains(self, pV):
		xV, yV = pV
		x0V, y0V = self.pV
		return (xV - x0V) ** 2 + (yV - y0V) ** 2 < self.rV ** 2

paxe = Button("p.ax", (camera.grectV.right - 35, camera.grectV.bottom - 35))
oaxe = Button("o.ax", (camera.grectV.right - 35, camera.grectV.bottom - 100))



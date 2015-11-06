# -*- coding: utf-8 -*-
import functions
import random
import pygame
from pygame import gfxdraw

x_dim = 800
y_dim = 800
points = 5
poly = []
pygame.init()
screen = pygame.display.set_mode((x_dim, y_dim))


poly = [[100, 100], [700, 100], [700, 700], [100, 700]]

poly = functions.gen_poly(points, (x_dim / 2, y_dim / 2), 5, x_dim / 3)

while True:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			quit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			tmp_srfc = pygame.Surface((x_dim, y_dim))
			tmp_srfc.fill((0, 0, 0))
			screen.blit(tmp_srfc, (0, 0))
			poly = functions.gen_poly(points, (x_dim / 2, y_dim / 2), x_dim / 10, x_dim / 3)
			new_poly = functions.smooth_poly(poly, 1)
			for a in range(6):
				pygame.time.delay(200)
				pygame.display.flip()
				screen.fill((0, 0, 0))
				pygame.gfxdraw.polygon(screen, new_poly, (0, 255, 0))
				new_poly = functions.smooth_poly(new_poly, 1)
				for vertex in poly:
					pygame.gfxdraw.filled_circle(screen, vertex[0], vertex[1], 5, (255, 255, 0))
				pygame.gfxdraw.polygon(screen, poly, (255, 0, 0))

			for vertex in poly:
				pygame.gfxdraw.filled_circle(screen, vertex[0], vertex[1], 5, (255, 255, 0))
			#for vertex in new_poly:
			#	pygame.gfxdraw.filled_circle(screen, vertex[0], vertex[1], 1, (0, 255, 255))
			pygame.gfxdraw.polygon(screen, poly, (255, 0, 0))
			pygame.gfxdraw.polygon(screen, new_poly, (0, 255, 0))
			pygame.display.flip()
	pygame.display.flip()

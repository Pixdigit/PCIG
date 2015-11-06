# -*- coding: utf-8 -*-
import pygame
import os
import numpy
import functions
from datetime import datetime

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
pygame.fastevent.init()

x_dim = 500
y_dim = 500
pygame.display.set_mode((500, 500))
screen = pygame.Surface((x_dim, y_dim))

D_pixels = x_dim * y_dim
star = pygame.image.load("./star1.tif").convert_alpha()

if numpy.random.random() <= 0.8:
	D_stars_min = int(0.000015625 * D_pixels)
	D_stars_max = 10 * D_stars_min
else:
	D_stars_min = int(0.000015625 * D_pixels)
	D_stars_max = int(0.00109375 * D_pixels)

image, mod_image = functions.background(x_dim, y_dim)

try:
	stars = functions.rand_image(x_dim, y_dim, star, D_stars_min, D_stars_max, 1.0)
except ValueError:
	print(("D_max >= D_min :" + str(D_stars_max) + " " + str(D_stars_min)))
	stars = functions.rand_image(x_dim, y_dim, star,
				D_stars_min, D_stars_max + 1, 1.0)
image.blit(stars, (0, 0))
mod_image.blit(stars, (0, 0))

print(("Finished"))
print(("Used " + str(pygame.time.get_ticks()) + "ms."))

show_image = image.copy()
a = 1

pygame.image.save(mod_image,
		"./images/Image - " + str(datetime.now())
		+ "_time_" + str(pygame.time.get_ticks() / 1000)
		+ ".jpg")

while True:
	screen.blit(show_image, (0, 0))

	for event in pygame.fastevent.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.KEYDOWN:
			key = pygame.key.name(event.key)
			if key == "escape":
				exit()
			if key == "return":
				image, mod_image = functions.background(x_dim, y_dim)
				stars = functions.rand_image(x_dim, y_dim, star,
							D_stars_min, D_stars_max, 1.0)
				image.blit(stars, (0, 0))
				show_image = image.copy()
			if key == "space":
				if a == 1:
					a = 2
					show_image = mod_image.copy()
				else:
					a = 1
					show_image = image.copy()
		if event.type == pygame.MOUSEBUTTONDOWN:
			print pygame.mouse.get_pos()
	pygame.display.flip()

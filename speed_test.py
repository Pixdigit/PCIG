# -*- coding: utf-8 -*-
import pygame
import numpy
pygame.init()
for a in range(1920):
	for b in range(1080):
		for c in range(5):
			numpy.random.randint(0, 200)

print pygame.time.get_ticks()
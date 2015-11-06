# -*- coding: utf-8 -*-
import math
import numpy
import pygame
from pygame import gfxdraw  # lint:ok
import constants


def rand_image(x_dim, y_dim, source_img, D_min, D_max, max_depth=0, min_size=2):
	if max_depth > 1:
		raise ValueError("max_depth must be between 0 and 1")
	D_images = numpy.random.randint(D_min, D_max)
	dest_img = pygame.Surface((x_dim, y_dim)).convert_alpha()
	dest_img.fill((0, 0, 0, 0))
	for a in range(D_images):
		x_max_pos = x_dim - (source_img.get_size()[0] / 2.0)
		y_max_pos = y_dim - (source_img.get_size()[1] / 2.0)
		x_pos = int(numpy.random.random() * x_max_pos)
		y_pos = int(numpy.random.random() * y_max_pos)
		x_size = 1
		y_size = 2
		while y_size < min_size or x_size < min_size:
			scale = numpy.random.random()
			x_size = source_img.get_size()[0] - (source_img.get_size()[0]
							* scale * max_depth)
			y_size = source_img.get_size()[1] - (source_img.get_size()[1]
							* scale * max_depth)
		this_src_img = pygame.transform.smoothscale(source_img,
						(int(x_size), int(y_size)))
		dest_img.blit(this_src_img, (x_pos, y_pos))
	return dest_img


def get_array_color(array, x, y):
	red = array[x][y][0]
	green = array[x][y][1]
	blue = array[x][y][2]
	return [red, green, blue]


def set_array_color(array, x, y, color):
	array[x][y][0] = color[0]
	array[x][y][1] = color[1]
	array[x][y][2] = color[2]
	return array


def contrast(color, amount, x_pos, y_pos):
	new_color = []
	for n in range(3):
		color_value = color[n]
		if color_value <= amount:
			color_value = 0
		elif color_value >= (255 - amount):
			color_value = 255
		else:
			color_value = int(round(
					(255.0 / (255 - (2 * amount))) * (color_value - amount) + 0.5))
		new_color.append(color_value)
	return new_color


def background(x_dim, y_dim):
	square_size = ((x_dim + y_dim)) / 2
	image = pygame.Surface((x_dim, y_dim))
	elem_pos = numpy.random.randint(len(constants.palette1))
	main_color = constants.palette1[elem_pos]
	color = main_color
	for color_num in range(25):
		if color_num % 5 == 4:
			elem_pos = numpy.random.randint(len(constants.palette1))
			color = constants.palette1[elem_pos]

		cloud_poly = gen_poly(numpy.random.randint(3, 70),  # amount of points
				(square_size / 2.0, square_size / 2.0),  # center
				int(square_size / 10),  # min_distance
				int(square_size / 4))  # max distance
		for n in range(2):
			cloud_poly = smooth_poly(cloud_poly)

		cloud = pygame.Surface((square_size, square_size))
		cloud.set_colorkey((0, 0, 0))
		pygame.gfxdraw.filled_polygon(cloud, cloud_poly, color)
		cloud.set_alpha(255 - (numpy.random.randint(3, 11) * color_num))

		x_min_pos = int(0 - (square_size / 2))
		x_max_pos = int(x_dim - (square_size / 2))
		y_min_pos = int(0 - (square_size / 2))
		y_max_pos = int(y_dim - (square_size / 2))
		x_pos = numpy.random.randint(x_min_pos, x_max_pos)
		y_pos = numpy.random.randint(y_min_pos, y_max_pos)
		image.blit(cloud, (x_pos, y_pos))

	mod_image = pygame.Surface((x_dim, y_dim))
	relation = 0.2
	old_percent = -1
	array = pygame.surfarray.pixels3d(image.copy())
	new_array = pygame.surfarray.pixels3d(image.copy())
	new_array[:][:] = (0, 0, 0)
	amount_contrast = numpy.random.randint(0, 70)
	x_spread = numpy.random.randint(10, 20)
	y_spread = numpy.random.randint(10, 20)
	for x_point in range(x_dim):
		for y_point in range(y_dim):
			percent = (((x_point + 1) * (y_point + 1) * 100.0)
					/ ((x_dim + 1) * (y_dim + 1)))
			if int(percent) >= old_percent + 1:
				print((int(percent)))
				old_percent += 1
			color_data = [[], [], []]
			for x_off in range(3):  # 3 * 3 grid around current point
				for y_off in range(3):
					try:
						color_data[x_off].append(
								get_array_color(array,
										x_point + (x_off - 1),
										y_point + (y_off - 1)
									)
								)
					except:
						color_data[x_off].append(main_color)
			x_offset = numpy.random.randint(0 - (x_dim / x_spread), x_dim / x_spread)
			y_offset = numpy.random.randint(0 - (y_dim / y_spread), y_dim / y_spread)
			if color_data[1][1] != [0, 0, 0]:
				for color in range(3):
					color_data[1][1][color] += int(
								(main_color[color] - color_data[1][1][color]) * relation)
					rand_dist = numpy.random.randint(-10, 10)
					if 0 > color_data[1][1][color] + rand_dist > 255:
						color_data[1][1][color] += rand_dist
			color_data[1][1] = contrast(color_data[1][1], amount_contrast,
						x_point, y_point)
			try:
				new_array[x_point + x_offset][y_point + y_offset] = color_data[1][1]
			except IndexError:
				pass  # Pixel placed outside window
	mod_image = pygame.surfarray.make_surface(new_array)
	return (image, mod_image)


def smooth_poly(polygon, smoothness=1):

	def list_replace(source_list, old_elem, new_elem):
		new_list = []
		for elem in source_list:
			if elem == old_elem:
				elem = new_elem
			new_list.append(elem)
		return new_list

	def subdivide(poly):
		new_poly = []
		for vertex in poly:
			elem_num = poly.index(vertex)
			middle_point = pygame.Rect(0, 0, 0, 0)
			if (elem_num + 1) < len(poly):
				middle_point.x = (poly[elem_num].x + poly[elem_num + 1].x) / 2.0
				middle_point.y = (poly[elem_num].y + poly[elem_num + 1].y) / 2.0
			else:
				middle_point.x = (poly[elem_num].x + poly[0].x) / 2.0
				middle_point.y = (poly[elem_num].y + poly[0].y) / 2.0
			new_poly.append(middle_point)
		return new_poly

	for vertex in polygon:
		if not type(vertex) == pygame.Rect:
			vertex_rect = pygame.Rect((vertex[0], vertex[1]), (0, 0))
			polygon = list_replace(polygon, vertex, vertex_rect)

	subdivision_poly = subdivide(polygon)
	snd_subdivision_poly = subdivide(subdivision_poly)

	extrapolated_points = []
	smoothness -= 1
	for vertex in polygon:
		elem_num = polygon.index(vertex)
		new_point = pygame.Rect(0, 0, 0, 0)
		new_point.x = int(((polygon[elem_num].x * smoothness)
				+ snd_subdivision_poly[elem_num - 1].x)
					/ (smoothness + 1.0))
		new_point.y = int(((polygon[elem_num].y * smoothness)
				+ snd_subdivision_poly[elem_num - 1].y)
					/ (smoothness + 1.0))
		extrapolated_points.append(new_point)

	total_polygon = []
	for n in range(len(polygon)):
		total_polygon.append(extrapolated_points[n])
		total_polygon.append(subdivision_poly[n])

	final_polygon = []
	for elem in total_polygon:
		final_polygon.append([elem.x, elem.y])
	return final_polygon


def gen_poly(D_points, center_pos, min_dist, max_dist):
	if D_points > 360:
		raise ValueError("Maximum amount of verticies is 360 not " + str(D_points))
	angle = 0
	points = []
	while True:
		for n in range(D_points):
			old_angle = angle
			counter = 0
			while angle == old_angle:
				counter += 1
				angle += numpy.random.randint(0, int((360 - angle) / (D_points - n)))
				if counter > 50 or (angle - old_angle) >= 90:
					break
			distance = numpy.random.randint(min_dist, max_dist)
			rel_x_pos = math.cos(math.radians(angle)) * distance
			rel_y_pos = math.sin(math.radians(angle)) * distance
			x_pos = int(rel_x_pos + center_pos[0])
			y_pos = int(rel_y_pos + center_pos[1])
			points.append([x_pos, y_pos])
		return points
#!/usr/bin/env python3.14 -B -Wd
# -m cProfile -s cumulative
# -B to avoid spamming garbage files, the rest is for profiling

import sys
from os.path import abspath,join,dirname

import pygame
sys.path.insert(0,abspath(join(dirname(__file__),'..')))
#shenanigans to run the script from the IDE
import importlib

SZ = (64,64)

def test(mod, drawfunc):
	RESULT = None
	ng = importlib.import_module(mod)
	name = f"test={drawfunc.__name__}:{mod}"
	@ng.add_scene(name, 75, windowSize=SZ)
	class ParityScene(ng.Scene):
		def onDraw(self) -> None:
			nonlocal RESULT
			if self.frame_counter>2: self.close()
			drawfunc(ng.screen)
			sur = ng.screen.to_surface()
			pygame.image.save(sur,f"tests/files/drawparity/{name}.png")
			RESULT = sur
	ng.Game.start(name)
	sys.modules.pop(mod, None)
	sys.modules.pop("nengin", None)
	return RESULT

import numpy as np

def diff(surf1, surf2):
	a1 = pygame.surfarray.pixels3d(surf1)
	a2 = pygame.surfarray.pixels3d(surf2)
	diff_mask = (a1 != a2).any(axis=2)
	ys, xs = np.where(diff_mask)
	ret = []
	for x, y in zip(xs, ys):
		ret.append((x, y, a1[x, y].copy(), a2[x, y].copy()))
	return ret



def draw_lines(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,0,0,255)
	for i in range(0, 64, 4):
		screen.draw_line((0,i),(63,i))
		screen.draw_line((i,0),(i,63))
	screen.draw_color = (0,255,0,255)
	for i in range(0, 64, 8):
		screen.draw_line((i,0),(63,63-i))
		screen.draw_line((0,i),(63-i,63))

def draw_points(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,255,0,255)
	for x in range(0,64,2):
		for y in range(0,64,2):
			if (x+y)%4==0:
				screen.draw_point((x,y))

def draw_rects(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for i in range(0,32,4):
		screen.draw_color = (i*8,255-i*8,i*4,255)
		screen.draw_rect((i,i,64-2*i,64-2*i))

def fill_rects(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for i in range(0,32,4):
		screen.draw_color = (255-i*8,i*8,128+i*4,255)
		screen.fill_rect((i,i,64-2*i,64-2*i))

def draw_triangles(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for i in range(0,6):
		screen.draw_color = (255,i*40,255-i*40,255)
		screen.draw_triangle((32,8+i*2),(8+i*4,56-i*4),(56-i*4,56-i*4))

def fill_triangles(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for i in range(0,6):
		screen.draw_color = (i*40,255-i*40,255,255)
		screen.fill_triangle((32,8+i*2),(8+i*4,56-i*4),(56-i*4,56-i*4))

def draw_quads(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for i in range(0,5):
		screen.draw_color = (255,i*50,0,255)
		screen.draw_quad((8+i*2,8+i*2),(56-i*2,8+i*2),(56-i*2,56-i*2),(8+i*2,56-i*2))

def fill_quads(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for i in range(0,5):
		screen.draw_color = (0,255-i*50,i*50,255)
		screen.fill_quad((8+i*2,8+i*2),(56-i*2,8+i*2),(56-i*2,56-i*2),(8+i*2,56-i*2))

def draw_rect_grid(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for x in range(0,64,8):
		for y in range(0,64,8):
			screen.draw_color = ((x*4)%256,(y*4)%256,128,255)
			screen.draw_rect((x,y,8,8))

def fill_rect_grid(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for x in range(0,64,8):
		for y in range(0,64,8):
			screen.draw_color = ((y*4)%256,(x*4)%256,200,255)
			screen.fill_rect((x,y,8,8))

def draw_diagonal_lines(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,0,255,255)
	for i in range(0,64,4):
		screen.draw_line((i,0),(63,63-i))
		screen.draw_line((0,i),(63-i,63))

def draw_crosshatch(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (0,255,255,255)
	for i in range(0,64,4):
		screen.draw_line((i,0),(i,63))
		screen.draw_line((0,i),(63,i))

def fill_checkerboard(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for x in range(0,64,8):
		for y in range(0,64,8):
			if (x//8+y//8)%2==0:
				screen.draw_color = (255,255,255,255)
			else:
				screen.draw_color = (0,0,0,255)
			screen.fill_rect((x,y,8,8))

def draw_starburst(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,255,0,255)
	for angle in range(0,360,15):
		import math
		rad = math.radians(angle)
		x = int(32+31*math.cos(rad))
		y = int(32+31*math.sin(rad))
		screen.draw_line((32,32),(x,y))

def fill_nested_triangles(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for i in range(6):
		screen.draw_color = (255-i*40,i*40,128,255)
		screen.fill_triangle((32,10+i*4),(10+i*4,54-i*4),(54-i*4,54-i*4))

def fill_nested_quads(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for i in range(6):
		screen.draw_color = (i*40,255-i*40,128,255)
		screen.fill_quad((10+i*4,10+i*4),(54-i*4,10+i*4),(54-i*4,54-i*4),(10+i*4,54-i*4))

def draw_triangle_grid(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for x in range(0,64,16):
		for y in range(0,64,16):
			screen.draw_color = ((x*4)%256,(y*4)%256,255,255)
			screen.draw_triangle((x+8,y),(x,y+16),(x+16,y+16))

def fill_triangle_grid(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for x in range(0,64,16):
		for y in range(0,64,16):
			screen.draw_color = ((y*4)%256,(x*4)%256,128,255)
			screen.fill_triangle((x+8,y),(x,y+16),(x+16,y+16))

def draw_horizontal_lines(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,0,0,255)
	for y in range(0,64):
		screen.draw_line((0,y),(63,y))

def draw_vertical_lines(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (0,255,0,255)
	for x in range(0,64):
		screen.draw_line((x,0),(x,63))

def draw_steep_lines(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (0,0,255,255)
	for x in range(0,64,4):
		screen.draw_line((x,0),(32,63))

def draw_shallow_lines(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,255,0,255)
	for y in range(0,64,4):
		screen.draw_line((0,y),(63,32))

def draw_overlapping_lines(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for i in range(0,64,8):
		screen.draw_color = (i*4,255-i*4,128,255)
		screen.draw_line((i,0),(63-i,63))
		screen.draw_line((0,i),(63,63-i))

def draw_triangle_fan(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,0,255,255)
	center = (32,32)
	for angle in range(0,360,30):
		import math
		rad = math.radians(angle)
		x = int(32+30*math.cos(rad))
		y = int(32+30*math.sin(rad))
		screen.draw_triangle(center, (x,y), (x,32))

def draw_quad_grid(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	for x in range(0,64,16):
		for y in range(0,64,16):
			screen.draw_color = ((x*4)%256,(y*4)%256,255,255)
			screen.draw_quad((x,y),(x+15,y),(x+15,y+15),(x,y+15))

def draw_diagonal_cross(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (0,255,255,255)
	screen.draw_line((0,0),(63,63))
	screen.draw_line((0,63),(63,0))
	screen.draw_triangle((0,0),(63,0),(32,63))
	screen.draw_quad((0,0),(63,0),(63,63),(0,63))

def draw_line_endpoints(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,128,0,255)
	for i in range(0,64,8):
		screen.draw_line((i,i),(63-i,63-i))
		screen.draw_point((i,i))
		screen.draw_point((63-i,63-i))

def draw_dense_starburst(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (128,255,0,255)
	for angle in range(0,360,5):
		import math
		rad = math.radians(angle)
		x = int(32+31*math.cos(rad))
		y = int(32+31*math.sin(rad))
		screen.draw_line((32,32),(x,y))





def simple_horizontal_line(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,0,0,255)
	screen.draw_line((8,32),(56,32))

def simple_vertical_line(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (0,255,0,255)
	screen.draw_line((32,8),(32,56))

def simple_triangle(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (0,0,255,255)
	screen.draw_triangle((16,48),(32,16),(48,48))

def simple_quad(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,255,0,255)
	screen.draw_quad((16,16),(48,16),(48,48),(16,48))

def simple_cross(screen):
	screen.draw_color = (0,0,0,255)
	screen.clear()
	screen.draw_color = (255,0,255,255)
	screen.draw_line((0,0),(63,63))
	screen.draw_line((0,63),(63,0))



DRAWERS = [
	draw_lines,
	draw_points,
	draw_rects,
	fill_rects,
	draw_triangles,
	fill_triangles,
	draw_quads,
	fill_quads,
	draw_rect_grid,
	fill_rect_grid,
	draw_diagonal_lines,
	draw_crosshatch,
	fill_checkerboard,
	draw_starburst,
	fill_nested_triangles,
	fill_nested_quads,
	draw_triangle_grid,
	fill_triangle_grid,
	draw_horizontal_lines,
	draw_vertical_lines,
	draw_steep_lines,
	draw_shallow_lines,
	draw_overlapping_lines,
	draw_triangle_fan,
	draw_quad_grid,
	draw_diagonal_cross,
	draw_line_endpoints,
	draw_dense_starburst,
	simple_horizontal_line,
	simple_vertical_line,
	simple_triangle,
	simple_quad,
	simple_cross,
]


DRAWERS = [
	#draw_triangles,
	draw_starburst,
	#draw_triangle_grid,
	draw_steep_lines,
	draw_shallow_lines,
	draw_overlapping_lines,
	#draw_triangle_fan,
	#draw_diagonal_cross,
	draw_dense_starburst,
	#simple_triangle,
]






TRU = []
Cc = [0]

for dr in DRAWERS:
	print("-"*100)
	print(dr)
	print("-"*100)
	C = 0
	isd = False
	for _ in diff(test("nengin.glng",dr),test("nengin.ng",dr)):
		#print(f"({x},{y}): {px1} vs {px2}")
		C+=1
		isd = True
	if isd: TRU.append(dr.__name__)
	Cc.append(C)
	print()
	print()
print(TRU)

print(Cc, sum(Cc))
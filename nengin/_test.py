#!/usr/bin/env python3.13 -B -Wd -m cProfile -s cumulative
# -B to avoid spamming garbage files
import sys
import os

from numpy.random.mtrand import randint
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#shenanigans to run the script from the IDE

from nengin import deprecated_alias
import nengin.glng as ng
from nengin.glng import screen
#import nengin.ng as ng

import numpy as np
import pygame as pg


class A:
	@deprecated_alias("wow")
	def test(self): pass
A().test()


class TestParentScene(ng.Scene):
	# This is scene id:1, but no object is ever created so it's
	# not registered and Scene.by_id doesn't know about this
	color = [255,0,0]
	def onKey(self, k):
		if k == pg.K_SPACE: self.color.append(self.color.pop(0))

pg.mouse.set_visible(False)
@ng.add_scene("TestScene",75,"Made with Nengin!", windowSize=(1440-43,900-25))
class NewScreenScene(TestParentScene, debug=True):
	C = {t:[randint(0,255)for i in "RGB"]for t in range(1,30+1)}
	ang = 0
	def onDraw(self) -> None:
		screen.draw_color = 0,0,0
		screen.clear()
		screen.draw_color = 255,0,255
		x,y = pg.mouse.get_pos()
		screen.fill_quad((x,y),(10,10),(y,400-x),(390,390))
		screen.draw_color = 0,255,255
		screen.draw_rect((x,y,100,100))
		screen.fill_rect((x+1,y+2,30,10))

		self.ang += self.dt/100
		ng.screen.draw_color = 255,255,255
		
		ng.screen.fill_ngon((352,352),40+50*13,10000000000,(self.ang))
		#for i in range(30,0,-1):
		#	ng.screen.draw_color = [[max,min][i%2](c1,c2)for c1,c2 in zip(self.C[i],self.color)]
		#	ng.screen.fill_ngon((352,352),40+i*13,59,(self.ang/i))

ng.Game.start("TestScene")

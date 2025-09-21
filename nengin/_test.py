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
@ng.add_scene("TestScene",75,"Made with Nengin!", windowSize=(400,600))
class NewScreenScene(TestParentScene, debug=True):
	C = {t:[randint(0,255)for i in "RGB"]for t in range(1,30+1)}
	ang = 0
	def onDraw(self) -> None:
		screen.draw_color = 0,0,0
		screen.clear()
		x,y = pg.mouse.get_pos()
		screen.draw_color = 0,255,255
		screen.draw_rect((x,y,3,3))

ng.Game.start("TestScene")

#!/usr/bin/env python3.13 -B -Wd -m cProfile -s cumulative
# -B to avoid spamming garbage files
import sys
import os

from numpy.random.mtrand import randint
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#shenanigans to run the script from the IDE

import nengin.glng as ng
#import nengin.ng as ng

import pygame as pg



class TestParentScene(ng.Scene):
	# This is scene id:1, but no object is ever created so it's
	# not registered and Scene.by_id doesn't know about this
	color = [255,0,0]
	def onKey(self, k):
		if k == pg.K_SPACE: self.color.append(self.color.pop(0))


@ng.add_scene("TestScene",75,"Made with Nengin!",704)
class CustomGameScene(TestParentScene):
	def onStart(self, prev: int) -> None:
		self.ang = 0
		self.C = {t:[randint(0,255)for i in "RGB"]for t in range(1,30+1)}
	def onDraw(self) -> None:
		ng.screen.draw_color = 0,0,0
		ng.screen.clear()
		self.ang += self.dt/100
		
		ng.screen.draw_color = 255,255,255
		for i in range(30,0,-1):
			ng.screen.draw_color = [[max,min][i%2](c1,c2) for c1,c2 in zip(self.C[i],self.color)]
			ng.screen.fill_ngon((352,352),40+i*13,3,(self.ang/i))
		"""{1:4, 1.1:4, 1.2:4, 1.3:4, 1.4:4, 1.5:3, 1.6:21, 1.7:9, 2:5, 3:14,
			4:11, 5:23, 6:10, 7:32, 8:21, 9:18, 10:26, 44:45, 50:85, 55:68,
		}"""# maximum visible n-gon of k radius, still need to work on this
		if self.frame_counter >= 8953: self.quit()

ng.Game.start("TestScene")

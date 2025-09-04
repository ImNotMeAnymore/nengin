#!/usr/bin/env python3 -B -Wd
# -B to avoid spamming garbage files
import sys
import os
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


@ng.add_scene("TestScene",60,"Made with Nengin!",704)
class CustomGameScene(TestParentScene):
	def onDraw(self) -> None:
		ng.screen.draw_color = 0,0,0
		ng.screen.clear()
		ng.screen.draw_color = self.color
		ng.screen.fill_triangle((100,500),(500,100),(650,650))


ng.Game("TestScene")

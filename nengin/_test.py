import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import nengin.glng as ng
import pygame as pg

@ng.addScene("TestScene",60,"Made with Nengin!",704)
class CustomGameScene(ng.Scene):
	color = [255,0,0]
	def onDraw(self) -> None:
		ng.screen.draw_color = 0,0,0,0
		ng.screen.clear()
		ng.screen.draw_color = self.color
		ng.screen.fill_triangle((100,500),(500,100),(650,650))
	def onKey(self, k):
		if k == pg.K_SPACE: self.color.append(self.color.pop(0))

ng.Game("TestScene")
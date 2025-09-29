#!/usr/bin/env python3.13 -B -Wd
# -m cProfile -s cumulative
# -B to avoid spamming garbage files, the rest is for profiling

import sys
import importlib
from os.path import abspath,join,dirname
sys.path.insert(0,abspath(join(dirname(__file__),'..')))
#shenanigans to run the script from the IDE
import pygame as pg
import numpy as np
import time



def drawfunc(scr):
	scr.draw_color = 0,0,0
	scr.clear()
def test(module):
	"""
	
	This segfaults for some reason, TODO: investigate
	
	"""
	ng = importlib.import_module(module)
	pg.mouse.set_visible(False)
	name = f"MODULE:<{module}>"
	SURF = None
	@ng.add_scene(name,75,"Made with Nengin!", windowSize=(1,1))
	class ParityScene(ng.Scene, debug=True):
		def onDraw(self) -> None:
			nonlocal SURF
			drawfunc(ng.screen)
			SURF = ng.window.get_surface()
			print(SURF)
			self.close()
	ng.Game.start(name)
	del sys.modules[module]
	del sys.modules["nengin"]
	return SURF

#import nengin.ng as ng


b = test("nengin.ng")#		<Surface(1x1x208)>
a = test("nengin.ng")#	<Surface(656322768x21990x176, colorkey=(0, 0, 0, 255))> #if it doesn't segfault

print(a,b)
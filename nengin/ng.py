#!/usr/bin/env python3.13
# nengin.py, a small pygame-ce wrapper
# Copyright (C) 2024  notmeanymore

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, see
# <https://www.gnu.org/licenses/>.

class NenginError(Exception): pass
if __name__ == "__main__": raise NenginError("Run Your own script. Not Nengin!!!")

from typing import Any
from . import (windowArgs,GenericScene,GenericGame,add_scene,CLOCK)

if GenericGame.__backend__:
	raise NenginError(f"Imported ng when backend '{GenericGame.__backend__}' was already"\
		"imported, choose one and one only!")
GenericGame.__backend__ = "ng"

import pygame as pg


window:pg.Window = pg.Window(**windowArgs)
from pygame._sdl2.video import Renderer as _renderer

screen:_renderer = _renderer(window)

class Scene(GenericScene):
	def onDraw(self) -> None:
		"""last thing that runs every frame"""
		screen.draw_color = 32,36,32
		screen.clear()
	def __globalDraw__(self) -> None:
		self.onDraw()
		screen.present()

class Game(GenericGame):
	def __init__(self, starter:str, metadata:dict[Any,Any]|None=None, run:bool=True, _debug:bool=False):
		super().__init__(starter, window, metadata, run, _debug)
	def _prepareWindow(self) -> None:
		screen.clear()
		screen.present()
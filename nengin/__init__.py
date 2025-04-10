#!/usr/bin/env python3.13
#nengin.py, a small pygame-ce wrapper
#Copyright (C) 2024  notmeanymore

#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.

#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.

#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, see
#<https://www.gnu.org/licenses/>.

__version__ = "0.2.4b"

class GenericNenginError(Exception): pass
if __name__ == "__main__": raise GenericNenginError("Run Your own script. Not Nengin!!!")

from pygame.key import ScancodeWrapper
import pygame as pg
from pygame import Vector2 as __vector, Window as _wndw
from pygame._sdl2.video import Renderer as _rndr # pyright: ignore
from typing import Callable, Type, Any


class _ContextClass(dict[str,"Scene"]):
	def __getitem__(self, k:str) -> "Scene":
		try: return super().__getitem__(k)
		except KeyError: pass
		_ = "\n	· " #IIRC this was a workaround to help a linter not display an KeyError
		# I might change the structure of this later
		raise GenericNenginError(f"Scene {k} not found, registered scenes are:\n	· {_.join(super().keys())}")

_CONTEXTS = _ContextClass()


class Vector(__vector):
	@property
	def xi(self) -> int: return int(self.x)
	@property
	def yi(self) -> int: return int(self.y)
	@property
	def xyi(self) -> tuple[int,int]: return int(self.x),int(self.y)


class DoneFlag(Exception): pass
class Scene:
	__byID__:dict[int,"Scene"] = {}
	__curID__:int = 0
	__game__:"None|Game" = None

	@classmethod
	def nameOf(cls, id:int) -> str: return cls.__byID__[id].name
	@classmethod
	def idOf(cls, name:str) -> int: return _CONTEXTS[name].id

	def __init_subclass__(cls, *, debug:bool=False) -> None:
		cls.__debug:bool = debug
		cls.id:int = cls.__curID__
		Scene.__curID__ += 1

	def changeScene(self, to:str, metadata:dict[Any,Any]={}) -> None:
		assert self.__game__
		assert to != self.name
		return self.__game__.changeSceneTo(to, metadata)
	def close(self) -> None:
		"Could be useful to call window.hide() just before"
		raise DoneFlag(f"{self} Closed the Game")
	quit = close #I'm tired of forgetting it's name

	def __init__(	self, name:str,
					framerate:int,
					windowName:str,
					windowSize:Vector,
					windowPos:int|Vector,
					windowIcon:pg.Surface|None=None,
				) -> None:
		#please redeclare onRegister instead
		self.name:str = name
		self.framerate:int = framerate
		self.windowName:str = windowName
		self.windowSize:Vector = windowSize
		self.windowIcon:pg.Surface|None = windowIcon
		self.windowPos:int|Vector = windowPos
		self.metadata:dict[Any,Any] = {}
		self.__byID__[self.id] = self
		self.__started__:bool = False
		self.framecounter:int = 0
	def onRegister(self) -> None: pass #Use this instead of __init__

	def __globalTick__(self) -> None:
		self.onTick()
		self.framecounter += 1
	def onTick(self) -> None: pass

	def __globalDraw__(self) -> None:
		self.onDraw()
		screen.present()
	def onDraw(self) -> None:
		screen.draw_color = 0,0,0,0
		screen.clear()

	def __globalReset__(self) -> None:
		#self.eat("bugs")
		self.onReset()
		self.metadata.clear()
	def onReset(self) -> None: pass

	def __globalOnEnd__(self, next:int) -> None: self.onEnd(next)
	def onEnd(self, next:int) -> None: pass

	def __globalOnStart__(self, prev:int, meta:dict[Any,Any]={}) -> None:
		self.__globalReset__()
		self.onPreStart(prev)
		self.withMetadata(meta)
		self.onReset()
		window.title = self.windowName
		if self.windowIcon: window.set_icon(self.windowIcon)
		if (self.windowSize.xyi != window.size): window.size = self.windowSize.xyi
		window.position = self.windowPos
		if not self.__started__:
			self.__started__ = True
			self.firstStart()
		self.onStart(prev)
	def onStart(self, prev:int) -> None: pass
	def onPreStart(self, prev:int) -> None:
		#Executes before onReset() and withMetadata()
		pass
	def firstStart(self) -> None:
		# You can use this this instead of onRegister to load stuff on
		# demand rather than everything at register time, so that Scenes
		# never started don't load useless resources
		pass

	def __globalEventHandler__(self, e:pg.event.Event) -> bool|None:
		if e.type == pg.QUIT:				return self.close()
		elif e.type == pg.KEYDOWN:			return self.onKey(e.key)
		elif e.type == pg.MOUSEBUTTONUP:	return self.onMouseUp(e.button, e.pos)
		elif e.type == pg.MOUSEBUTTONDOWN:	return self.onMouseDown(e.button, e.pos)

		return self.eventHandler(e)
	def eventHandler(self, e:pg.event.Event) -> bool:
		# Runs once for every single event every tick, so don't do expensive stuff here
		return False
		# You should't use it for anything other than checking events really

	def __globalKeyHandler__(self, ks:ScancodeWrapper) -> bool|None:
		if ks[pg.K_ESCAPE]: return self.close()
		return self.keyHandler(ks)
	def keyHandler(self, ks:ScancodeWrapper) -> bool|None:
		"runs every tick, ks is list of currently pressed keys"
		return False

	def onKey(self, k:int) -> None: "runs once, when key k is pressed"
	def onMouseUp(self, k:int, pos:Vector) -> None: pass
	def onMouseDown(self, k:int, pos:Vector) -> None: pass


	def withMetadata(self, meta:dict[Any,Any]) -> "Scene":
		# metadata is data needed at the moment, deleted on __globalReset__()
		# For example: Text to draw on a generic dialog bubble Scene
		if meta: self.metadata.update(meta)
		return self
	def __repr__(self) -> str:
		return f"<Scene '{self.name}'({type(self).__name__}):ID({self.id})>"

def addScene(
	name:str, #required
	framerate:int=60,
	windowName:str="Made with Nengin!",
	windowSize:tuple[int]|int|Vector=704, #anything pg.Vector2() accepts will do
	windowPos:int|Vector=pg.WINDOWPOS_UNDEFINED, #same but don't use a single int for this one
	windowIcon:pg.Surface|None=None,
	) -> Callable[[Type[Scene]],Scene]:
	name = str(name)
	if windowIcon: assert isinstance(windowIcon, pg.Surface)
	if windowPos not in (pg.WINDOWPOS_UNDEFINED, pg.WINDOWPOS_CENTERED):
		if isinstance(windowPos, int) and windowPos > 32768:
			raise ValueError("Use a smaller window position or pass it as a tuple")
		else: windowPos = Vector(windowPos)
	def _ret(cls:Type[Scene]) -> Scene:
		nonlocal name, framerate, windowName, windowSize, windowPos, windowIcon
		x,y = Vector(windowSize).xyi
		print(f"Registering: '{name}' [{x} x {y}] (ID:{Scene.__curID__-1})")
		f = _CONTEXTS[name] = cls(
			name, int(framerate), str(windowName), Vector(windowSize), windowPos, windowIcon,
		)
		f.onRegister()
		return f
	return _ret


window = _wndw(title="Loading...", size=(1,1), hidden=True)
window.hide()
screen = _rndr(window)

CLOCK = pg.time.Clock()

class Game:
	currentTick = 0
	def run(self) -> None:
		try:
			while True:
				while self.__changingStack:
						# NOTE: this prevents recursion but makes
						# it possible to become trapped between a
						# Scene changing to another and the other
						# changing back to the original one, also
						# changing to a Scene more than once will
						# now ignore the metadata argument of all
						# but the last call to changeScene(Scene)
					self.cur, meta = self.__changingStack.popitem()
					new:Scene = _CONTEXTS[self.cur]
					self.scene.__globalOnEnd__(new.id)
					new.__globalOnStart__(self.scene.id, meta=meta)
					self.scene = new
				CLOCK.tick(self.scene.framerate)
				events = pg.event.get()
				for e in events:
					if  e.__dict__.get("window") not in (window,None):
						raise GenericNenginError("Multiple windows are not supported")
					self.scene.__globalEventHandler__(e)
				self.scene.__globalKeyHandler__(pg.key.get_pressed())
				self.currentTick += 1
				self.scene.__globalTick__()
				self.scene.__globalDraw__()
		except DoneFlag as e:
			return print(e, "!")
		except Exception as e:
			if self._debug: raise
			print(e,"!!!!!!!")
		finally: pg.quit()

	def __init__(self, starter:str, metadata:dict[Any,Any]={}, _debug:bool=False):
		self._debug = _debug
		global screen, window
		for v in _CONTEXTS.values(): v.__game__ = self
		self.scene:Scene
		self.cur:str
		self.scene = h = _CONTEXTS[starter].withMetadata(metadata)
		self.cur = h.name
		screen.clear()
		h.__globalOnStart__(-1)
		screen.present() #workaround to make an empty non-ticking scene
		if (h.windowPos == pg.WINDOWPOS_UNDEFINED):
			window.position = pg.WINDOWPOS_CENTERED
		window.show()
		return self.run()

	__changingStack:dict[str,dict[Any,Any]] = {}
	def changeSceneTo(self, to:str, metadata:dict[Any,Any]={}) -> None:
		if to in self.__changingStack: del self.__changingStack[to]
		self.__changingStack[to] = metadata

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

__version__ = "0.4.2b"
# 1.0.0 when I have some docs

class GenericNenginError(Exception): pass
if __name__ == "__main__":
	raise GenericNenginError("Run Your own script. Not Nengin(nor this file)!!!!")

import pygame
#print("nengin", __version__)
from pygame.key import ScancodeWrapper
from pygame import Vector2 as _vector, Window as _window
from typing import Callable, Type, Any

"""
# In case I need it, no sense to activate it when there are no warnings
# to activate it simply comment out the first triple "
# TODO: actually use this, what's the point of having it if I don't
import warnings

def deprecated_alias(new:str):
	def dec(f):
		def wr(__fn=f,__nn=new *a, **k):
			warnings.warn(f"{__fn.__name__} is deprecated, use {__nn} instead.",DeprecationWarning,stacklevel=2)
			return __fn(*a, **k)
		return wr
	return dec
" """

class _ContextClass(dict[str,"GenericScene"]):
	def __getitem__(self, k:str) -> "GenericScene":
		try: return super().__getitem__(k)
		except KeyError: pass
		if not self: raise GenericNenginError("No scenes have been registered!")
		s = "\n	· ".join(super().keys())
		raise GenericNenginError(f"Scene {k} not found, registered scenes are:\n	· {s}")

SCENES = _ContextClass()

class Vector(_vector):
	@property
	def xyi(self) -> tuple[int,int]: return int(self.x),int(self.y)
class DoneFlag(Exception): pass

def createScreen():
	raise GenericNenginError("You shouldn't call _generic.py directly")

window = _window(title="Loading...", size=(1,1), hidden=True, opengl=True)

class GenericScene:
	__byID__:dict[int,"GenericScene"] = {}
	__current_ID__:int = 0
	__game__:"GenericGame"
	@classmethod
	def name_of(cls, id:int) -> str: return cls.__byID__[id].name
	@classmethod
	def id_of(cls, name:str) -> int: return SCENES[name].id
	idOf = id_of
	nameOf = name_of
	def __init_subclass__(cls, *, _debug:bool=False) -> None:
		cls._debug:bool = _debug
		cls.id:int = cls.__current_ID__
		GenericScene.__current_ID__ += 1
	def change(self, to:str, metadata:dict[Any,Any]|None=None) -> None:
		return self.__game__.change_scene(to, metadata or {})
	changeScene = change
	def onClose(self):
		"""This should not iterfere with normal closing (as in, raising another error,
		or cancel the close conditionally), change .close() directly for that"""
		window.hide()
	def close(self) -> None:
		"forces the game to close, ignores onEnd(), but calls onClose()"
		self.onClose()
		raise DoneFlag(f"{self} Closed the Game")
	quit = close #I'm tired of forgetting it's name
	def __init__(self,
				name:str,
				framerate:int,
				windowName:str,
				windowSize:Vector,
				windowPos:int|Vector,
				windowIcon:pygame.Surface|None=None,
			) -> None:
		self.name:str = name
		self.framerate:int = framerate
		self.windowName:str = windowName
		self.windowSize:Vector = windowSize
		self.windowIcon:pygame.Surface|None = windowIcon
		self.windowPos:int|Vector = windowPos
		self.metadata:dict[Any,Any] = {}
		self.__byID__[self.id] = self
		self.__started__:bool = False
		self.frame_counter:int = 0
	def onRegister(self) -> None:
		"runs when the scene is being first registered"
	def __globalTick__(self) -> None:
		self.onTick()
		self.frame_counter += 1
	def onTick(self) -> None:
		"runs every frame"
	def __globalDraw__(self) -> None:
		self.onDraw()
		window.flip()
	def onDraw(self) -> None:
		raise GenericNenginError("You shouldn't call _generic.py directly")
		"last thing that runs every frame"
	def __globalReset__(self, prev:int) -> None:
		#self.eat("bugs")
		self.onReset(prev)
		self.metadata.clear()
	def __globalOnEnd__(self, next:int) -> None: self.onEnd(next)
	def onEnd(self, next:int) -> None:
		"run before the next scene starts"
	def onReset(self, prev:int) -> None:
		"very first thing to run every time scene is started"
	def onStart(self, prev:int) -> None:
		"very last thing to run every time scene is started"

	def __globalOnStart__(self, prev:int, meta:dict[Any,Any]|None=None) -> None:
		self.__globalReset__(prev)
		self.withMetadata(meta or {})
		window.title = self.windowName
		if self.windowIcon: window.set_icon(self.windowIcon)
		if (self.windowSize.xyi != window.size): window.size = self.windowSize.xyi
		window.position = self.windowPos
		if not self.__started__:
			self.__started__ = True
			self.firstStart()
		self.onStart(prev)
	def firstStart(self) -> None:
		"""You can use this this instead of onRegister to load stuff on demand
		rather than everything at register time, so that Scenes never started
		don't load useless resources
		"""
	def __globalEventHandler__(self, e:pygame.event.Event) -> None:
		if e.type == pygame.QUIT:	return self.close()
		elif e.type == pygame.KEYDOWN:	return self.onKey(e.key)
		elif e.type == pygame.MOUSEBUTTONUP:	return self.onMouseUp(e.button, e.pos)
		elif e.type == pygame.MOUSEBUTTONDOWN:	return self.onMouseDown(e.button, e.pos)
		return self.eventHandler(e)
	def eventHandler(self, e:pygame.event.Event) -> None:
		"""Runs once for every single event every tick, so don't do expensive stuff here
		You should't use it for anything other than checking events really"""
	def __globalKeyHandler__(self, ks:ScancodeWrapper) -> None:
		if ks[pygame.K_ESCAPE]: return self.close()
		return self.keyHandler(ks)
	def keyHandler(self, ks:ScancodeWrapper) -> None:
		"runs every tick, ks is an array of currently pressed keys"
	def onKey(self, k:int) -> None: "runs once, when key k is pressed"
	def onMouseUp(self, k:int, pos:Vector) -> None: "runs once, when button k is released"
	def onMouseDown(self, k:int, pos:Vector) -> None: "runs once, when button k is pressed"
	def withMetadata(self, meta:dict[Any,Any]) -> "GenericScene":
		"""metadata is data needed at the moment, deleted on __globalReset__()
		For example: Text to draw on a generic dialog bubble Scene
		"""
		if meta: self.metadata.update(meta)
		return self
	def __repr__(self) -> str:
		return f"<Scene '{self.name}'({type(self).__name__}):ID({self.id})>"

def add_scene(
	name:str, #required
	framerate:int=60,
	windowName:str="Made with Nengin!",
	windowSize:tuple[int,int]|int|Vector=704, #anything pygame.Vector2() accepts will do
	windowPos:int|Vector=pygame.WINDOWPOS_UNDEFINED, #same but don't use a single int for this one
	windowIcon:pygame.Surface|None=None,
	) -> Callable[[Type[GenericScene]],GenericScene]:
	name = str(name)
	if windowIcon: assert isinstance(windowIcon, pygame.Surface)
	if windowPos not in (pygame.WINDOWPOS_UNDEFINED, pygame.WINDOWPOS_CENTERED):
		if isinstance(windowPos, int) and windowPos > 32768:
			raise ValueError("Use a smaller window position or pass windowPos as a tuple")
		else: windowPos = Vector(windowPos)
	def _ret(cls:Type[GenericScene]) -> GenericScene:
		nonlocal name, framerate, windowName, windowSize, windowPos, windowIcon
		x,y = Vector(windowSize).xyi
		print(f"Registering: '{name}' [{x} x {y}] (ID:{GenericScene.__current_ID__-1})")
		f = SCENES[name] = cls(
			name, int(framerate), str(windowName), Vector(windowSize), windowPos, windowIcon,
		)
		f.onRegister()
		return f
	return _ret


CLOCK = pygame.time.Clock()


class GenericGame:
	@property
	def _debug(self): return self.__global_debug or self.scene._debug
	global_tick = 0
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
					new:GenericScene = SCENES[self.cur]
					self.scene.__globalOnEnd__(new.id)
					new.__globalOnStart__(self.scene.id, meta=meta)
					self.scene = new
				CLOCK.tick(self.scene.framerate)
				events = pygame.event.get()
				for e in events:
					if e.__dict__.get("window") not in (window,None):
						raise GenericNenginError("Multiple windows are not supported (yet)")
					self.scene.__globalEventHandler__(e)
				self.scene.__globalKeyHandler__(pygame.key.get_pressed())
				self.global_tick += 1
				self.scene.__globalTick__()
				self.scene.__globalDraw__()
		except DoneFlag as e: return print(e)
		except Exception as e:
			if self._debug: raise
			print(e,"!!!!!!!")
		finally: self.finisher()

	def finisher(self):
		# this function gets executed at the very end of Game, after all scenes have been
		# dealt with
		pygame.quit()
	
	def _prepareWindow(self) -> None:
		raise GenericNenginError("You shouldn't call _generic.py directly")

	def __init__(self, starter:str, metadata:dict[Any,Any]|None=None, _debug:bool=False):
		self.__global_debug = _debug
		global window
		for v in SCENES.values(): v.__game__ = self
		self.scene:GenericScene
		self.cur:str
		self.scene = h = SCENES[starter]
		self.cur = h.name
		self._prepareWindow()
		h.__globalOnStart__(-1, metadata or {})
		#window.flip() #workaround to make an empty non-ticking scene
		if (h.windowPos == pygame.WINDOWPOS_UNDEFINED):
			window.position = pygame.WINDOWPOS_CENTERED
		window.show()
		return self.run()

	__changingStack:dict[str,dict[Any,Any]] = {}
	def change_scene(self, to:str, metadata:dict[Any,Any]|None=None) -> None:
		if to in self.__changingStack: del self.__changingStack[to]
		self.__changingStack[str(to)] = metadata or 	{}
	changeSceneTo = change_scene
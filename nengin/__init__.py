#!/usr/bin/env python3.13
# nengin.py, a small pygame-ce wrapper
# Copyright (C) 2025  notmeanymore

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

__version__ = "0.4.13b"
# 1.0.0 when I have some docs

class GenericNenginError(Exception):
	"""Generic Exception"""

if __name__ == "__main__":
	raise GenericNenginError("Run Your own script. Not Nengin(nor this file)!!!!")

import pygame
#print("nengin", __version__)
from pygame.key import ScancodeWrapper
from pygame import Vector2 as _vector
from typing import Callable, Type, Any
from abc import abstractmethod


#"""
# In case I need it, no sense to activate it when there are no warnings
# to activate it simply comment out the first triple "

import warnings
from typing import TypeVar, cast
F = TypeVar("F",bound=Callable[...,Any])
def deprecated_alias(new: str) -> Callable[[F], F]:
	def dec(f: F) -> F:
		def wr(*a: Any, **k: Any) -> Any:
			warnings.warn(f"{f.__name__} is deprecated, use {new} instead.", DeprecationWarning, stacklevel=2)
			return f(*a, **k)
		return cast(F, wr)
	return dec
" """

class ContextClass(dict[str,"GenericScene"]):
	"""dict that errors when no such scene exists"""
	def __getitem__(self, k:str) -> "GenericScene":
		try: return super().__getitem__(k)
		except KeyError: pass
		if not self: raise GenericNenginError("No scenes have been registered!")
		s = "\n	· ".join(super().keys())
		raise GenericNenginError(f"Scene {k} not found, registered scenes are:\n	· {s}")

class Vector(_vector):
	"""pygame's Vector, but with xyi method, should be in pygame itself imo"""
	@property
	def xyi(self) -> tuple[int,int]: return int(self.x),int(self.y)

class DoneFlag(Exception):
	"""This flag indicates the game was closed gracefully, could change"""

SCENES:ContextClass = ContextClass()
CLOCK:pygame.time.Clock = pygame.time.Clock()

windowArgs:dict["str",Any] = { #there's probably a better way of doing this
	"title":"Loading...",	# (str) The title of the window
	"size":(1,1),				# ((int, int)) The size of the window, in screen coordinates
	"position":pygame.WINDOWPOS_UNDEFINED,	# ((int, int) or int) A tuple specifying the window position
														# or WINDOWPOS_CENTERED, or WINDOWPOS_UNDEFINED
	"fullscreen":False,		# (bool) Create a fullscreen window using size as the resolution, videomode change
	"fullscreen_desktop":False,# (bool) Create a fullscreen window using the current desktop resolution
	"opengl":True,			# (bool) Create a window with support for an OpenGL context
	"vulkan":False,			# (bool) Create a window with support for a Vulkan instance
	"hidden":True,				# (bool) Create a hidden window
	"borderless":False,		# (bool) Create a window without borders
	"resizable":False,		# (bool) Create a resizable window
	"minimized":False,		# (bool) Create a mimized window
	"maximized":False,		# (bool) Create a maximized window
	"mouse_grabbed":False,	# (bool) Create a window with grabbed mouse input
	"keyboard_grabbed":False,# (bool) Create a window with grabbed keyboard input
	"input_focus":True,		# (bool) Create a window with input focus
	"mouse_focus":True,		# (bool) Create a window with mouse focus
	"allow_high_dpi":True,	# (bool) Create a window in high-DPI mode if supported
	"mouse_capture":False,	# (bool) Create a window that has the mouse captured (unrelated to INPUT_GRABBED)
	"always_on_top":False,	# (bool) Create a window that is always presented above others
	"utility":False,			# (bool) Create a window that doesn't appear in the task bar
} #Maaaybe a vulkan backend too?

#window:pygame.Window

class GenericScene:
	__byID__:dict[int,"GenericScene"] = {}
	__current_ID__:int = 0
	__game__:"GenericGame"
	@property
	def dt(self): return self.__game__.dt	
	@classmethod
	def name_of(cls, id:int) -> str: return cls.__byID__[id].name
	@classmethod
	def id_of(cls, name:str) -> int: return SCENES[name].id
	idOf = id_of
	nameOf = name_of
	def __init_subclass__(cls, *, debug:bool=False) -> None:
		cls._debug:bool = debug
		cls.id:int = cls.__current_ID__
		GenericScene.__current_ID__ += 1
	def change(self, to:str, metadata:dict[Any,Any]|None=None) -> None:
		return self.__game__.change_scene(to, metadata or {})
	changeScene = change
	def onClose(self) -> None:
		"""This should not iterfere with normal closing (as in, raising another error,
		or cancel the close conditionally), change .close() directly for that"""
		self.__game__.window.hide()
	def close(self) -> None:
		"""forces the game to close, ignores onEnd(), but calls onClose()"""
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
		self.onRegister()
	def onRegister(self) -> None:
		"""runs when the scene is being first registered"""
	def __globalTick__(self) -> None:
		self.onTick()
		self.frame_counter += 1
	def onTick(self) -> None:
		"""runs every frame"""
	def __globalDraw__(self) -> None:
		self.onDraw()
		self.__game__.window.flip()

	@abstractmethod
	def onDraw(self) -> None:
		"""last thing that runs every frame"""

	def __globalReset__(self, prev:int) -> None:
		#self.eat("bugs")
		self.onReset(prev)
		self.metadata.clear()
	def __globalOnEnd__(self, next:int) -> None: self.onEnd(next)
	def onEnd(self, next:int) -> None:
		"""run before the next scene starts"""
	def onReset(self, prev:int) -> None:
		"""very first thing to run every time scene is started"""
	def onStart(self, prev:int) -> None:
		"""very last thing to run every time scene is started"""

	def __globalOnStart__(self, prev:int, meta:dict[Any,Any]|None=None) -> None:
		window:pygame.Window = self.__game__.window
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
		"""runs every tick, ks is an array of currently pressed keys"""
	def onKey(self, k:int) -> None: """runs once, when key k is pressed"""
	def onMouseUp(self, k:int, pos:Vector) -> None: """runs once, when button k is released"""
	def onMouseDown(self, k:int, pos:Vector) -> None: """runs once, when button k is pressed"""
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
	windowSize:tuple[int,int]|int|_vector=704, #anything pygame.Vector2() accepts will do
	windowPos:int|_vector=pygame.WINDOWPOS_UNDEFINED, #same but don't use a single int for this one
	windowIcon:pygame.Surface|None=None,
	) -> Callable[[Type[GenericScene]],GenericScene]:
	"""Decorator for registering scenes
	
	Parameters:
		name (str): unique Scene name
		framerate (int, optional): The target framerate for the scene. default is 60
		windowName (str, optional): Title of window when scene is active
		windowSize (tuple[int,int]|int|Vector, optional): Window size, accepts anything Vector2 accepts, Default is 704
		windowPos (int|Vector, optional): the window position, if None it just centers the screen
		windowIcon (Surface|None, optional): Surface to use as icon, if none it uses pygame's

	Returns:
		Callable[[Type[GenericScene]],GenericScene]: The true decorator, which then returns an **INSTANCE** of the Scene

	Raises:
		ValueError: If windowPos is an invalid value.

	Usage:
		@add_scene("any_name")
		class MyScene(Scene):
			...
	"""
	name = str(name)
	if windowIcon: assert isinstance(windowIcon, pygame.Surface)
	if windowPos not in (pygame.WINDOWPOS_UNDEFINED, pygame.WINDOWPOS_CENTERED):
		if isinstance(windowPos, int) and windowPos > 32768:
			raise ValueError("Use a smaller window position or pass windowPos as a tuple")
	def _ret(cls:Type[GenericScene]) -> GenericScene:
		#nonlocal name, framerate, windowName, windowSize, windowPos, windowIcon
		x,y = Vector(windowSize).xyi
		print(f"Registering: '{name}' [{x} x {y}] (ID:{GenericScene.__current_ID__-1})")
		f = SCENES[name] = cls(name, int(framerate), str(windowName),
					Vector(windowSize), Vector(windowPos), windowIcon)
		return f
	return _ret

class GenericGame:
	__backend__:None|str = None
	
	@property
	def _debug(self):
		"""If debug flag is up, globally or by the scene itself"""
		return self.__global_debug or self.scene._debug
	global_tick = 0
	dt = 0
	
	def run(self) -> None:
		"""Runs the game"""
		self.window.show()
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
				self.dt = CLOCK.tick(self.scene.framerate)
				events = pygame.event.get()
				for e in events:
					if e.__dict__.get("window") not in (self.window,None):
						raise GenericNenginError("Multiple windows are not supported!")
					self.scene.__globalEventHandler__(e)
				self.scene.__globalKeyHandler__(pygame.key.get_pressed())
				self.global_tick += 1
				self.scene.__globalTick__()
				self.scene.__globalDraw__()
		except DoneFlag as e: return print(e)
		except Exception as e:
			if self._debug: raise
			print(f"{type(e)}: {e} !!!!!")
		finally: self.finisher()

	def finisher(self):
		"""this function gets executed at the very end of Game, after all scenes have been dealt with"""
		pygame.quit()
	
	@abstractmethod
	def _prepareWindow(self) -> None:
		"""clears the screen from random noise and other garbage before it's first shown"""

	def __init__(self,
					starter:str,
					window:pygame.Window,
					metadata:dict[Any,Any]|None=None,
					run:bool=False,
					_debug:bool=False):
		"""Starter is the starting scene ID"""
		self.window:pygame.Window = window
		self.__global_debug = _debug
		for v in SCENES.values(): v.__game__ = self
		self.scene:GenericScene
		self.cur:str
		self.scene = h = SCENES[starter]
		self.cur = h.name
		self._prepareWindow()
		h.__globalOnStart__(-1, metadata or {})
		if (h.windowPos == pygame.WINDOWPOS_UNDEFINED):
			window.position = pygame.WINDOWPOS_CENTERED
		if run:
			self.run()
			self.run = lambda *_: print("Don't call .run() if Game has run=True")

	__changingStack:dict[str,dict[Any,Any]] = {}
	def change_scene(self, to:str, metadata:dict[Any,Any]|None=None) -> None:
		if to in self.__changingStack: del self.__changingStack[to]
		self.__changingStack[str(to)] = metadata or 	{}
	changeSceneTo = change_scene
#cengine.py, a small pygame-ce wrapper
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


class GenericNenginError(Exception): pass
if __name__ == "__main__": raise GenericNenginError("Run Your own script. Not Nengin!!!")

import pygame as pg
from pygame import Vector2 as __vector, Window as _wndw
from pygame._sdl2.video import Renderer as _rndr

class _ContextClass(dict):
	def __getitem__(self, k):
		try: return super().__getitem__(k)
		except KeyError: pass
		raise GenericNenginError(f"Scene {k} not found, registered scenes are:\n\t· {"\n\t· ".join(super().keys())}") 
_CONTEXTS = _ContextClass()

class DoneFlag(Exception): pass

class Vector(__vector):
	@property
	def xi(self): return int(self.x)
	@property
	def yi(self): return int(self.y)
	@property
	def xyi(self): return int(self.x),int(self.y)

class Scene:
	__byID__:dict = {}
	__curID__:int = 0

	@classmethod
	def nameOf(cls, id:int): return cls.__byID__[id].name
	@classmethod
	def idOf(cls, name:str): return _CONTEXTS[name].id

	def __init_subclass__(self, *, debug:bool=False):
		self.__debug:bool = debug
		self.__byID__[self.__curID__]:Scene = self
		self.id:int = self.__curID__
		Scene.__curID__ += 1

	def changeScene(self, to:str, metadata:dict={}) -> None:
		assert self.__game__
		assert to != self.name
		return self.__game__.changeSceneTo(to, metadata)
	def close(self) -> None:
		"Could be useful to call window.hide() just before"
		raise DoneFlag(f"{self} Closed the Game")
	quit = exit = end = done = close #I'm tired of forgetting it's name



	def __init__(	self, name:str,
					framerate:int,
					windowName:str,
					windowSize:Vector,
					windowPos:Vector,
					windowIcon:pg.Surface=None,
				) -> None:
		self.name:str = name
		self.framerate:int = framerate
		self.windowName:str = windowName
		self.windowSize:Vector = windowSize
		self.windowIcon:pg.Surface = windowIcon
		self.windowPos:Vector = windowPos
		self.metadata:dict = {}
		self.id:int
		self.__started__:bool = False
		self.framecounter:int = 0
	def onRegister(self) -> None: pass

	def __globalTick__(self) -> None:
		self.onTick()
		self.framecounter += 1
	def onTick(self) -> None: pass #replaces run()

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
	def onEnd(self, next:int) -> None:
		pass


	def __globalOnStart__(self, prev:int, meta:dict={}) -> None:
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
	def onPreStart(self, prev:int) -> None: pass #PREVIOUS TO RESET AND WITHMETA
	def firstStart(self) -> None:
		# most of the time you want to use this instead of __init__ as to load
		# stuff on demand rather than everything at register time
		pass

	def __globalEventHandler__(self, e:pg.event.Event) -> bool:
		if e.type == pg.QUIT: return self.close()
		elif e.type == pg.KEYDOWN:			return self.onKey(e.key)
		elif e.type == pg.MOUSEBUTTONUP:	return self.onMouseUp(e.button, e.pos)
		elif e.type == pg.MOUSEBUTTONDOWN:	return self.onMouseDown(e.button, e.pos)

		return self.eventHandler(e)
	def eventHandler(self, e:pg.event.Event) -> bool:
		"""runs once for every single event every tick, don't do expensive stuff here
		or really, don't do anything other than checking events"""
		return False

	def __globalKeyHandler__(self, ks:list) -> bool:
		if ks[pg.K_ESCAPE]: return self.close()
		return self.keyHandler(ks)
	def keyHandler(self, ks:list) -> bool:
		"runs every tick, ks is list of currently pressed keys"
		return False

	def onKey(self, k:int) -> None:
		"runs once, when key k is pressed"
	def onMouseUp(self, k:int, pos:Vector) -> None: pass
	def onMouseDown(self, k:int, pos:Vector) -> None: pass


	def withMetadata(self, meta:dict): #data needed at the moment, deleted on __globalReset__()
		if meta: self.metadata.update(meta)	#EXAMPLE: Text to draw on generic dialog bubble
		return self
	def __repr__(self) -> str:
		return f"<Scene '{self.name}'({type(self).__name__}) : ID({self.id})>"

	

def addScene(
	name:str, #required
	framerate:int=60,
	windowName:str="Made with Nengin!",
	windowSize:tuple[int]|int=704, #anything pg.Vector2() accepts will do
	windowPos:tuple[int]=pg.WINDOWPOS_UNDEFINED, #don't use a single int for this one
	windowIcon:pg.Surface=None, #
	):
	#It's better for everyone to check this here
	name = str(name)
	framerate = int(framerate)
	windowName = str(windowName)
	windowSize = Vector(windowSize)
	if windowIcon:
		assert isinstance(windowIcon, pg.Surface)

	if windowPos not in (pg.WINDOWPOS_UNDEFINED, pg.WINDOWPOS_CENTERED):
		if isinstance(windowPos, int) and windowPos > 32000:
			raise ValueError("Use a smaller position or declare it as a tuple")
		else: windowPos = Vector(windowPos)

	def _ret(cls:Scene):
		nonlocal name, framerate, windowName, windowSize
		x,y = Vector(windowSize).xyi
		print(f"Registering: '{name}' [{x} x {y}] (ID:{Scene.__curID__-1})")
		f = _CONTEXTS[name] = cls(
			name, framerate,windowName, windowSize, windowPos, windowIcon
			)
		f.onRegister()
		return f

	return _ret


window = _wndw(title="Loading...", size=(1,1), hidden=True)
#window.hide()
screen = _rndr(window)


CLOCK = pg.time.Clock()

class Game:
	currentTick = 0
	def run(self):
		try:
			while True:
				CLOCK.tick(self.scene.framerate)
				events = pg.event.get()
				for e in events:
					if  e.__dict__.get("window") not in (window,None):
						raise GenericNenginError("Multiple windows are not supported")
					self.scene.__globalEventHandler__(e)
				# handling multiple windows will make core functionality to stop
				# working. For example resizing will need to be on a per-window
				# basis instead of a global value and therefore so will be
				# getting SIZE, MIDDLE, VISIBLE and other useful variables
				# It's not imposible to implement but it'll break a lot of stuff
				#
				# pop-ups, alerts, floating-guis and other "restrictive" windows
				# on the other hand, are quite possible, their events need to be
				# handled here then perhaps have one dedicated scene-like object
				# for reacting to events, drawing on them and other fancy stuff,
				# for now tho, all of that is on the TODO list.
				self.scene.__globalKeyHandler__(pg.key.get_pressed())
				self.currentTick += 1
				self.scene.__globalTick__()
				self.scene.__globalDraw__()
		#TODO error checking should lead to crash scene, like Löve2d does
		except DoneFlag as e:
			return print(e, "!")
		except Exception as e:
			if self._debug: raise e from e
			print(e,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		finally: pg.quit()



	def __init__(self, starter:str, _debug:bool=False):
		self._debug = _debug
		global screen,window
		for v in _CONTEXTS.values(): v.__game__ = self
		self.scene:Scene
		self.cur:str
		self.scene = h = _CONTEXTS[starter]
		self.cur = h.name
		window.show()
		screen.clear()
		h.__globalOnStart__(-1)	
		if (h.windowPos == pg.WINDOWPOS_UNDEFINED): window.position = pg.WINDOWPOS_CENTERED
		screen.present()
		return self.run()
		#workaround to make an empty non-ticking scene

	def changeSceneTo(self, to:str, metadata:dict={}):
		new:Scene = _CONTEXTS[to]
		self.cur = to
		self.scene.__globalOnEnd__(new.id)
		new.__globalOnStart__(self.scene.id, meta=metadata)

		self.scene = new
		return new
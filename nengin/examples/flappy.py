#!/usr/bin/env python3.14 -B -Wd
from functools import cache
from math import sin

from pygame._sdl2.video import Texture
import nengin.ng as ng
from nengin.ng import screen, Scene, add_scene
from pygame import FRect as Rect, K_SPACE, Vector2 as Vector, font



X,Y = SIZE = Vector(1,2)*45*8
VIEW = Rect(0,0,X,Y)


font.init()

@cache
def loadText(text:str, f:font.Font) -> Texture:
	return Texture.from_surface(screen, f.render(text, True, (255,255,255)))




@add_scene("flappy-over", windowSize=SIZE)
class FlappyMenu(Scene):
	def onStart(self, prev: int) -> None:
		self.pos = Vector(X//5,Y//3)
		self.rect = Rect(0,0,30,30)
		self.rect.bottom = Y-30
		self.rect.centerx = self.pos.x
		
	def onDraw(self) -> None:
		super().onDraw()
		screen.draw_color = 0,255,0
		screen.draw_rect(self.rect)
		screen.draw_color = 255,0,0
		screen.draw_line((0,Y-30),(X,Y-30))


@add_scene("flappy-menu", windowSize=SIZE)
class FlappyGameOver(Scene):
	def onStart(self, prev: int) -> None:
		self.pos = Vector(X//5,Y//3)
		self.rect = Rect(0,0,30,30)
		self.rect.center = self.pos
		self.menutext = loadText("Press [SPACE] to start!", font.SysFont(("comicsans","ubuntu","sans"), round(X/12)))
		self.menurect = self.menutext.get_rect()
		self.menurect.center = VIEW.center
	def onTick(self) -> None:
		self.pos.y = Y//3+sin(self.frame_counter/20)*15
		self.rect.center = self.pos
	def onDraw(self) -> None:
		super().onDraw()
		screen.draw_color = 0,255,0
		screen.draw_rect(self.rect)
		screen.draw_color = 255,0,0
		screen.draw_line((0,Y-30),(X,Y-30))
		self.menutext.draw(dstrect=self.menurect)
	def onKey(self, k: int) -> None:
		if k == K_SPACE: self.changeScene("flappy-game", {"y":self.rect.centery})



NEX = []

@add_scene("flappy-game", windowSize=SIZE, framerate=144)
class FlappyGame(Scene):
	def onStart(self, prev: int) -> None:
		self.momentum = Vector(0,-10)
		self.pos = Vector(X//5,Y//3)
		self.rect = Rect(0,0,30,30)
		self.pos.y = self.metadata["y"]
	def onTick(self) -> None:
		self.momentum.y += 0.5*self.dt/16
		self.pos += self.momentum*self.dt/16
		self.rect.center = self.pos
		if self.rect.bottom >= Y-30: self.changeScene("flappy-over")
	def onKey(self, k: int) -> None:
		#19*18/4 (85.5) would not allow it to go outside the screen, but 20 will do
		if k == K_SPACE and self.rect.top > 20:
			self.momentum.y = -10
	def onDraw(self) -> None:
		super().onDraw()
		screen.draw_color = 0,255,0
		screen.draw_rect(self.rect)
		screen.draw_color = 255,0,0
		screen.draw_line((0,Y-30),(X,Y-30))

if __name__ == "__main__": ng.Game.start("flappy-menu")

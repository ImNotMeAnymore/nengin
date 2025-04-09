from pygame.key import ScancodeWrapper
import nengin as ng
from nengin import Scene, addScene, screen, Vector
from pygame import font, FRect as Rect, K_LEFT, K_RIGHT, K_a, K_d, K_r, K_SPACE
from pygame._sdl2.video import Texture			# pyright: ignore
from random import choice, randint


X,Y = SIZE = Vector(8,5)*120
VIEW = Rect(0,0,X,Y)

def loadText(text:str, f:font.Font) -> Texture:
	return Texture.from_surface(screen, f.render(text, True, (255,255,255)))

@addScene("end", windowSize=SIZE)
class GameOver(Scene):
	#this could be it's own file, with a generic ending Scene
	def firstStart(self):
		font.init()
		self.gameOverText = loadText("Game Over!", font.SysFont(("comicsans"), round(Y/4)))
		self.gameOverRect = self.gameOverText.get_rect()
		self.gameOverRect.center = VIEW.center
		self.gameOverRect.y -= Y/5
		f = font.SysFont(("comicsans"), round(Y/15))
		self.texts = t = (
			loadText("You lost!  press r to play again or esc to quit",f),
			loadText("You won!  press r to play again or esc to quit",f),
		)
		self.rects = (t[0].get_rect(),t[1].get_rect(),)
		for i in self.rects: i.center = VIEW.center+Vector(0,Y/15)

	def onDraw(self):
		screen.draw_color = 20,20,20
		screen.clear()
		screen.draw_color = 255,255,20
		self.gameOverText.draw(dstrect=self.gameOverRect)
		w:bool = bool(self.metadata.get("win"))
		self.texts[w].color = 128,128,128
		self.texts[w].draw(dstrect=self.rects[w])	
	def onKey(self, k:int):
		if k == K_r: self.changeScene("jump")

@addScene("jump", windowSize=SIZE)
class JumpGame(Scene):
	def onStart(self, prev:int):
		self.pos = 0
		self.player = p = Rect(0,0,8*4,5*10)
		p.centery = VIEW.centerx
		p.centerx = VIEW.centery/3*2
		self.momentum = -9
		self.t = 0

	def onDraw(self):
		screen.draw_color = 20,20,20
		screen.clear()
		
		Ypos = VIEW.centerx
		
		if self.player.centery < Ypos: self.momentum -= 1
		else: self.player.centery = Ypos
		if 0 < self.t:
			self.player.centery = y = Ypos-13*self.t+.3*self.t**2
			self.t += 1
			if y > Ypos:
				self.t = 0
				self.player.centery = Ypos
		self.pos += 10
		screen.draw_color = 255,255,20
		screen.fill_rect(self.player)
		screen.draw_color = 255,255,255
		
		screen.logical_size = 80,50
		#this method is really buggy, you shouldn't touch it under normal circumstances
		#https://github.com/pygame-community/pygame-ce/issues/2923
		#https://github.com/pygame-community/pygame-ce/issues/3244
		#https://github.com/pygame-community/pygame-ce/issues/3245
		screen.draw_line((0,42),(80,42))
		screen.logical_size = SIZE
	def keyHandler(self, ks: ScancodeWrapper) -> bool | None:
		if ks[K_SPACE] and not self.t: self.t = 1
	#	l,r = ks[K_LEFT]or ks[K_a],ks[K_RIGHT]or ks[K_d]
	#	if l and r: return False
	
		
		#if u and self.me.top > 0: self.me.top -= 4
		#if d and self.me.bottom < Y: self.me.bottom += 4

if __name__ == "__main__": ng.Game("jump")

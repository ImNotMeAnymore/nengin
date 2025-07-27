from pygame.key import ScancodeWrapper
import nengin.ng as ng
from nengin.ng import screen
from nengin import Scene, addScene, Vector
from pygame import font, FRect as Rect, K_DOWN, K_UP, K_w, K_s, K_r
from pygame._sdl2.video import Texture			# pyright: ignore
from random import choice, randint


X,Y = SIZE = Vector(8,5)*120
VIEW = Rect(0,0,X,Y)

def almost(n:int|float,w:int|float,e:int|float=5) -> bool: return n-e < w < n+e

def loadText(text:str, f:font.Font) -> Texture:
	return Texture.from_surface(screen, f.render(text, True, (255,255,255)))

@addScene("pong-end", windowSize=SIZE)
class GameOver(Scene):
	def firstStart(self):
		font.init()
		self.gameOverText = loadText("Game Over!", font.SysFont(("comicsans","ubuntu","sans"), round(Y/4)))
		self.gameOverRect = self.gameOverText.get_rect()
		self.gameOverRect.center = VIEW.center
		self.gameOverRect.y -= Y/5
		f = font.SysFont(("comicsans","ubuntu","sans"), round(Y/15))
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
		if k == K_r: self.changeScene("pong")

@addScene("pong", windowSize=SIZE)
class PongGame(Scene):
	def onStart(self, prev:int):
		self.dr = d = Vector(5,0).rotate(randint(20,33)*choice((-1,1)))
		self.sd = d.copy()
		self.me = m = Rect(30,0,20,100)
		self.no = n = Rect(0,0,20,100)
		n.centerx = X-m.centerx
		m.centery = n.centery = Y/2
		self.bl = b = Rect(0,0,16,16)
		b.center = SIZE/2
		self.sh = b.copy()
		self.pongs = 0
	def check(self):
		#I REALLY need to fix this, I have no idea what's what
		bl,sh,dr,sd,no,me = self.bl,self.sh,self.dr,self.sd,self.no,self.me
		#why did I do this
		r = Rect(0,0,4,100)
		if dr.x > 0: r.topleft = no.left,no.y
		else: r.topright = me.right,me.y
		screen.draw_color = 200,10,200
		screen.fill_rect(r)
		if bl.colliderect(r):
			dr.x *= -1
			self.pongs += 1
			if self.pongs > 4:
				n = 1+randint(-30,50)/1000
				dr.xy *= n
				if randint(0,16): sd.xy *= n
		
		if bl.left <= 0: return self.changeScene("pong-end",{"win":False})
		if bl.right >= X: return self.changeScene("pong-end",{"win":True})

		if bl.top <= 0 or bl.bottom >= Y: dr.y *= -1
		if sh.top <= 0 or sh.bottom >= Y:
			sd.y *= -1
			if no.bottom >= Y-90 or no.top <= 90: sh.center = bl.center		
	def think(self):
		if self.dr.x < 0: return
		if almost(self.sh.centery, self.no.centery, 20): return
		t = 4 if self.sh.centery > self.no.centery else -4
		self.no.centery = max(min(self.no.centery+t,Y-50),50)
	def onDraw(self):
		screen.draw_color = 20,20,20
		screen.clear()
		self.think()
		screen.draw_color = 255,255,25
		screen.fill_rect(self.me)
		screen.fill_rect(self.no)
		self.bl.center += self.dr
		if self.frame_counter%60:
			if randint(0,32): self.sh.center += self.sd
			else: self.sh.center = self.bl.center
		self.check()
		screen.draw_color = 255,255,255
		screen.fill_rect(self.bl)
		
	def keyHandler(self, ks: ScancodeWrapper) -> None:
		u,d = ks[K_UP]or ks[K_w],ks[K_DOWN]or ks[K_s]
		if u and d: return
		if u and self.me.top > 0: self.me.top -= 4
		if d and self.me.bottom < Y: self.me.bottom += 4

if __name__ == "__main__": ng.Game("pong")

from pygame.key import ScancodeWrapper
import nengin as ng
from nengin import Scene, addScene, screen, Vector
from pygame import font, FRect as Rect, K_SPACE
from pygame._sdl2.video import Texture			# pyright: ignore
from random import randint


X,Y = SIZE = Vector(8,5)*120
VIEW = Rect(0,0,X,Y)

def loadText(text:str, f:font.Font) -> Texture:
	return Texture.from_surface(screen, f.render(text, True, (255,255,255)))

@addScene("end", windowSize=SIZE)
class GameOver(Scene):
	#this could be it's own file, with a generic ending Scene
	def firstStart(self):
		font.init()
		self.gameOverText = loadText("Game Over!", font.SysFont(("comicsans","ubuntu","sans"), round(Y/4)))
		self.gameOverRect = self.gameOverText.get_rect()
		self.gameOverRect.center = VIEW.center
		self.gameOverRect.y -= Y/5
		f = font.SysFont(("comicsans","ubuntu","sans"), round(Y/15))
		self.texts = t = (
			loadText("You lost!  press spacebar to play again or esc to quit",f),
			loadText("Press spacebar to play or esc to quit",f),
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
		if k == K_SPACE: self.changeScene("jump")

@addScene("jump", windowSize=SIZE)
class JumpGame(Scene):
	def onStart(self, prev:int):
		self.pos = 0
		self.player = p = Rect(0,0,8*4,5*10)
		p.centery = VIEW.centerx
		p.centerx = VIEW.centery/3*2
		self.t = 0
		self.OBS = []

	def onDraw(self):
		screen.draw_color = 20,20,20
		screen.clear()
		Ypos = VIEW.centerx
		if 0 < self.t:
			self.player.centery = y = Ypos-13*self.t+.3*self.t**2
			self.t += 1
			if y > Ypos:
				self.t = 0
				self.player.centery = Ypos
		self.pos += 8+(self.pos/5000)
		screen.draw_color = 255,255,20
		screen.fill_rect(self.player)
		screen.draw_color = 235,235,235

		screen.logical_size = 40,25
		#logical_size is really buggy, you shouldn't touch it under normal circumstances
		#https://github.com/pygame-community/pygame-ce/issues/2923
		#https://github.com/pygame-community/pygame-ce/issues/3244
		#https://github.com/pygame-community/pygame-ce/issues/3245
		screen.draw_line((0,21),(40,21))
		screen.logical_size = SIZE
		
		if not self.OBS: self.OBS.append(self.pos+SIZE.x+160)
		elif self.OBS[-1]+300 < self.pos+SIZE.x:
			if not randint(0,55): self.OBS.append(self.pos+SIZE.x+160)
		
		
		self.OBS = [i for i in self.OBS if i > self.pos]
		
		screen.draw_color = 235,20,235
		r = Rect(0,0,80,48)
		r.centery = Ypos
		dead = False
		for i in self.OBS:
			r.right = i-self.pos
			screen.fill_rect(r)
			if r.colliderect(self.player): dead = True
		
		if dead: self.changeScene("end")
			#screen.draw_line((i-self.pos,0),(i-self.pos,SIZE.y))
		
	def keyHandler(self, ks: ScancodeWrapper) -> bool | None:
		if ks[K_SPACE] and not self.t: self.t = 1

if __name__ == "__main__": ng.Game("end",{"win":True})

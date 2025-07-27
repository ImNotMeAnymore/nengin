from pygame.key import ScancodeWrapper
import nengin.ng as ng
from nengin.ng import screen
from nengin import Scene, addScene, Vector
from pygame import font, FRect as Rect, K_SPACE
from pygame._sdl2.video import Texture			# pyright: ignore
from random import randint


X,Y = SIZE = Vector(8,5)*120
VIEW = Rect(0,0,X,Y)

def loadText(text:str, f:font.Font) -> Texture:
	return Texture.from_surface(screen, f.render(text, True, (255,255,255)))

# OOP example, you can just define a generic Scene class and inherit 
class GenericTitleSubtitle(Scene):
	def firstStart(self):
		title:str = self.metadata["title"]
		sub:str = self.metadata["sub"]
		font.init()
		self.titleText = loadText(title, font.SysFont(("comicsans","ubuntu","sans"), round(Y/4)))
		self.titleRect = _r =  self.titleText.get_rect()
		_r.center = VIEW.center
		_r.y -= Y/5		
		f = font.SysFont(("comicsans","ubuntu","sans"), round(Y/15))
		self.subTitle = loadText(sub,f)
		self.subRect = _r = self.subTitle.get_rect()
		_r.center = VIEW.center
		_r.y += Y/15
	def onDraw(self):
		screen.draw_color = 20,20,20
		screen.clear()
		self.titleText.draw(dstrect=self.titleRect)
		self.subTitle.draw(dstrect=self.subRect)

@addScene("jumper-start", windowSize=SIZE)
class Start(GenericTitleSubtitle):
	def firstStart(self):
		self.metadata["title"] = "Jumper!"
		self.metadata["sub"] = "Press spacebar to play or esc to quit"
		super().firstStart()
		self.titleText.color = 255,255,20
		self.subTitle.color = 128,128,20
		self.player = p = Rect(0,0,8*4,5*10)
		p.centery = VIEW.centerx
		p.centerx = VIEW.centery/3*2
	def onKey(self, k:int):
		if k == K_SPACE: self.changeScene("jumper")
	def onDraw(self):
		super().onDraw()
		screen.draw_color = 255,255,20
		screen.fill_rect(self.player)
		screen.draw_color = 235,235,235
		screen.logical_size = 40,25 #Don't use logical_size please, this is just because I'm lazy
		screen.draw_line((0,21),(40,21))
		screen.logical_size = SIZE.xyi

@addScene("jumper-gameover", windowSize=SIZE)
class GameOver(GenericTitleSubtitle):
	def firstStart(self):
		self.metadata["title"] = "Game Over!"
		self.metadata["sub"] = "You lost! Press spacebar to play again or esc to quit"
		super().firstStart()
		self.titleText.color = 255,255,128
		self.subTitle.color = 128,128,128
	def onKey(self, k:int):
		if k == K_SPACE: self.changeScene("jumper")

@addScene("jumper", windowSize=SIZE)
class JumpGame(Scene):
	def onStart(self, prev:int):
		self.pos = 0
		self.player = p = Rect(0,0,8*4,5*10)
		p.centery = VIEW.centerx
		p.centerx = VIEW.centery/3*2
		self.t = 1
		self.obstacles:list[float] = []
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
		self.pos += 8+self.pos/9999
		screen.draw_color = 255,255,20
		screen.fill_rect(self.player)
		screen.draw_color = 235,235,235
		screen.logical_size = 40,25
		#logical_size is really buggy, you shouldn't touch it under normal circumstances
		#https://github.com/pygame-community/pygame-ce/issues/2923
		#https://github.com/pygame-community/pygame-ce/issues/3244
		#https://github.com/pygame-community/pygame-ce/issues/3245
		screen.draw_line((0,21),(40,21))
		screen.logical_size = SIZE.xyi

		if not self.obstacles: self.obstacles.append(self.pos+SIZE.x+160)
		elif self.obstacles[-1]+300 < self.pos+SIZE.x:
			if not randint(0,55): self.obstacles.append(self.pos+SIZE.x+160)


		self.obstacles = [i for i in self.obstacles if i > self.pos]
		
		screen.draw_color = 235,20,235
		r = Rect(0,0,80,48)
		r.centery = Ypos
		dead = False
		for i in self.obstacles:
			r.right = i-self.pos
			screen.fill_rect(r)
			if r.colliderect(self.player): dead = True
		if dead: self.changeScene("jumper-gameover", {"score":round(self.pos/100)})
			#screen.draw_line((i-self.pos,0),(i-self.pos,SIZE.y))

	def keyHandler(self, ks: ScancodeWrapper) -> None:
		if ks[K_SPACE] and not self.t: self.t = 1

if __name__ == "__main__": ng.Game("jumper-start")

import nengin as ng
from nengin import Scene, addScene, screen, Vector
from pygame import FRect as Rect, K_SPACE



X,Y = SIZE = Vector(1,2)*45*8
VIEW = Rect(0,0,X,Y)

@addScene("flappy-menu", windowSize=SIZE)
class FlappyMenu(Scene):
	def onStart(self, prev: int) -> None:
		self.pos = Vector(X//5,Y//3)
		self.rect = Rect(0,0,30,30)
		self.rect.center = self.pos

	

@addScene("flappy-game", windowSize=SIZE)
class FlappyGame(Scene):
	def onStart(self, prev: int) -> None:
		self.momentum = Vector(0,-3)
		self.pos = Vector(X//5,Y//3)
		self.rect = Rect(0,0,30,30)

	def onTick(self) -> None:
		self.momentum.y += 0.5
		self.pos += self.momentum
		self.rect.center = self.pos
		
		if self.rect.bottom >= Y-30: self.changeScene("flappy-death")

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

if __name__ == "__main__": ng.Game("flappy-menu")

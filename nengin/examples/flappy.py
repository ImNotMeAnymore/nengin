import nengin as ng
from nengin import Scene, addScene, screen, Vector
from pygame import FRect as Rect, K_SPACE



X,Y = SIZE = Vector(8,15)*45
VIEW = Rect(0,0,X,Y)

@addScene("flappy-menu", windowSize=SIZE)
class FlappyMenu(Scene):
	def onStart(self, prev: int) -> None:
		self.momentum = Vector(3,-3)
		self.pos = Vector(X//5,Y//2)
		self.rect = Rect(0,0,30,30)
	
	def onTick(self) -> None:
		self.momentum += (0,0.4)
		self.pos += self.momentum
		self.rect.center = self.pos
		
	def onKey(self, k: int) -> None:
		if k == K_SPACE: self.momentum.y = -3
		
		
	def onDraw(self) -> None:
		screen.draw_color = 0,0,0
		screen.clear()
		screen.draw_color = 0,255,0
		
		
		screen.draw_rect(self.rect)
		
		
if __name__ == "__main__": ng.Game("flappy-menu")

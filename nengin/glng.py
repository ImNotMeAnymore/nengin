
class GLNenginError(Exception): pass
if __name__ == "__main__":
	raise GLNenginError("Run Your own script. Not GlNengin!!!!")

from ._generic import (window,GenericScene,GenericGame,Vector,add_scene,addScene,CLOCK)
import pygame as pg
from OpenGL.GL import (
	glClearColor, glClear, GL_COLOR_BUFFER_BIT,glBegin,GL_LINE_LOOP,
	glVertex2f,glEnd,glColor4f
)

class ScreenWrapper:
	# implements every SDL2 screen method in openGL, for compat purposes
	# don't rely too much on it
	_draw_color = pg.Color(0,0,0)

	@property
	def draw_color(self): return self._draw_color
	@draw_color.setter
	def draw_color(self, value): self._draw_color = pg.Color(value)

	def clear(self):
		c = self._draw_color
		glClearColor(c.r/255, c.g/255, c.b/255, c.a/255)
		glClear(GL_COLOR_BUFFER_BIT)
	def present(): window.flip()
	def to_ndc(self, p): return (2*p[0]/window.size[0]-1,1-2*p[1]/window.size[1])
	def draw_triangle(self,p1,p2,p3):
		c = self._draw_color
		glColor4f(c.r/255, c.g/255, c.b/255, c.a/255)
		glBegin(GL_LINE_LOOP)
		glVertex2f(*self.to_ndc(p1))
		glVertex2f(*self.to_ndc(p2))
		glVertex2f(*self.to_ndc(p3))
		glEnd()

screen = ScreenWrapper()


class Scene(GenericScene):
	def onDraw(self) -> None:
		"last thing that runs every frame"
		glClearColor(32/255, 36/255, 32/255, 1.0)
		glClear(GL_COLOR_BUFFER_BIT)

class Game(GenericGame):
	def _prepareWindow(self) -> None:
		glClearColor(0,0,0,1.0)
		glClear(GL_COLOR_BUFFER_BIT)

class GLNenginError(Exception): pass
if __name__ == "__main__":
	raise GLNenginError("Run Your own script. Not GlNengin!!!!")

from . import (window,GenericScene,GenericGame,Vector,add_scene,addScene,CLOCK)
import pygame as pg
from OpenGL.GL import (
	glClearColor, glClear, GL_COLOR_BUFFER_BIT,glBegin,GL_LINE_LOOP,
	glVertex2f,glEnd,glColor4f
)

import moderngl
import numpy as np
context = moderngl.create_context()

class ScreenWrapper:
	"implements **some** SDL2 screen(Renderer) methods in openGL, for compat purposes"

	def __init__(self):
		self._draw_color = pg.Color(0,0,0)
		self._prog = context.program(
			vertex_shader="""
				#version 330
				in vec2 in_pos;
				void main() {
					gl_Position = vec4(in_pos, 0.0, 1.0);
				}
			""",fragment_shader="""
				#version 330
				uniform vec4 color;
				out vec4 fragColor;
				void main() {
					fragColor = color;
				}
			""")
		self._vbo = context.buffer(reserve=8*4*4) # Up to 8 vertices
		self._vao = context.simple_vertex_array(self._prog,self._vbo,'in_pos')
	@property
	def draw_color(self): return self._draw_color
	@draw_color.setter
	def draw_color(self, value): self._draw_color = pg.Color(value)

	def clear(self):
		c = self._draw_color
		context.clear(c.r/255, c.g/255, c.b/255, c.a/255)

	def present(self): window.flip()
	def to_ndc(self, p): return 2*p[0]/window.size[0]-1,1-2*p[1]/window.size[1]

	def draw_line(self, p1, p2): self._draw_shape((p1,p2), moderngl.LINES)
	def draw_point(self, point): self._draw_shape([point], moderngl.POINTS)

	def draw_rect(self, rect):
		x, y, w, h = rect
		self._draw_shape(((x,y),(x+w,y),(x+w,y+h),(x,y+h)), moderngl.LINE_LOOP)
	def fill_rect(self, rect):
		x, y, w, h = rect
		a,b,c,d = (x, y),(x+w,y),(x+w,y+h),(x,y+h)
		self._draw_shape((a,b,c,c,d,a), moderngl.TRIANGLES)

	def draw_triangle(self, p1, p2, p3): self._draw_shape((p1,p2,p3), moderngl.LINE_LOOP)
	def fill_triangle(self, p1, p2, p3): self._draw_shape((p1,p2,p3), moderngl.TRIANGLES)
		
	def draw_quad(self, p1, p2, p3, p4): self._draw_shape([p1, p2, p3, p4], moderngl.LINE_LOOP)
	def fill_quad(self, p1, p2, p3, p4): self._draw_shape([p1, p2, p3, p3, p4, p1], moderngl.TRIANGLES)

	def _draw_shape(self, points, mode):
		pts = np.array([self.to_ndc(p) for p in points], dtype='f4')
		self._vbo.write(pts.tobytes())
		c = self._draw_color
		self._prog['color'].value = (c.r/255, c.g/255, c.b/255, c.a/255) #type: ignore
		self._vao.render(mode=mode, vertices=len(points))

screen = ScreenWrapper()

class Scene(GenericScene):
	def onDraw(self) -> None:
		"last thing that runs every frame"
		context.clear(32/255, 36/255, 32/255, 1.0)

class Game(GenericGame):
	def _prepareWindow(self) -> None: context.clear(0,0,0,1.0)
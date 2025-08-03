#!/usr/bin/env python3.13
# nengin.py, a small pygame-ce wrapper
# Copyright (C) 2024  notmeanymore

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, see
# <https://www.gnu.org/licenses/>.

class GLNenginError(Exception): pass
if __name__ == "__main__": raise GLNenginError("Run Your own script. Not GlNengin!!!!")

from . import (window,GenericScene,GenericGame,add_scene)
import pygame as pg

addScene = add_scene
import moderngl
import numpy as np
context:moderngl.Context = moderngl.create_context()


generic_vertex_shader = """#version 330
in vec2 in_pos;
void main() {
	gl_Position = vec4(in_pos, 0.0, 1.0);
}"""
generic_fragment_shader = """#version 330
uniform vec4 color;
out vec4 fragColor;
void main() {
	fragColor = color;
}"""

class ScreenWrapper:
	"""implements **some** SDL2 screen(Renderer) methods in openGL, for compat purposes
	
	don't rely too much on it"""
	def __init__(self):
		self._draw_color = pg.Color(0,0,0)
		self._prog = context.program(vertex_shader=generic_vertex_shader,
			fragment_shader=generic_fragment_shader)
		self._vbo = context.buffer(reserve=8*4*4) # Up to 8 vertices
		self._vao = context.simple_vertex_array(self._prog,self._vbo,'in_pos')
	@property
	def draw_color(self): return self._draw_color
	@draw_color.setter
	def draw_color(self, value): self._draw_color = pg.Color(value)

	def clear(self): context.clear(*self._draw_color.normalized)

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
		self._prog['color'].value = self._draw_color.normalized	#type: ignore
		self._vao.render(mode=mode, vertices=len(points))

screen = ScreenWrapper()

class Scene(GenericScene):
	def onDraw(self) -> None:
		"""last thing that runs every frame"""
		context.clear(32/255, 36/255, 32/255, 1.0)

class Game(GenericGame):
	def _prepareWindow(self) -> None: context.clear(0,0,0,1.0)
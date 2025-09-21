#!/usr/bin/env python3.13
# Nengin, a small pygame-ce wrapper
# Copyright (C) 2025  notmeanymore

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

from . import (GenericGame,GenericNenginError)
class GLNenginError(GenericNenginError): pass
if __name__ == "__main__": raise GLNenginError("Run Your own script. Not GlNengin!!!!")
if GenericGame.__backend__: raise GLNenginError("Imported glng when backend '"\
	f"{GenericGame.__backend__}' was already imported, choose one and one only!")
GenericGame.__backend__ = "glng"


from . import (windowArgs,GenericScene,add_scene,CLOCK,deprecated_alias) # noqa: F401
from typing import Any
import pygame as pg
import moderngl
import numpy as np

windowArgs.update({
	"opengl":True, "vulkan":False
})
window:pg.Window = pg.Window(**windowArgs)

context:moderngl.Context = moderngl.create_context()




generic_fragment_shader = """#version 330
uniform vec4 color;
out vec4 fragColor;
void main() {
	fragColor = color;
}"""
pixel_vertex_shader = """#version 330
in vec2 in_pos;
uniform vec2 window_size;
void main() {
	vec2 ndc = (in_pos/window_size)*2.0-1.0;
	ndc.y = -ndc.y; //Because pygame's coordinates are top to bottom
	gl_Position = vec4(ndc, 0.0, 1.0);
}
"""

class ScreenLike():
	"""implements **some** SDL2 screen(Renderer) methods in openGL, for compat purposes"""
	_draw_color = pg.Color(0)
	@property
	def draw_color(self): return self._draw_color
	@draw_color.setter
	def draw_color(self,value): self._draw_color = pg.Color(value)
	def clear(self): context.clear(*self._draw_color.normalized)
	def present(self): window.flip()
	def draw_line(self,p1,p2): self._draw_shape((p1,p2), moderngl.LINES)
	def draw_point(self,point): self._draw_shape((point,), moderngl.POINTS)
	def draw_rect(self,rect):
		x,y,w,h = rect
		x+=1
		if w==h==1: return self.draw_point((x,y))
		if w==1: return self.draw_line((x,y),(x,y+h))
		if h==1: return self.draw_line((x,y),(x+w,y))
		p = (x,y),(x+w-1,y),(x+w-1,y+h-1),(x,y+h)
		self._draw_shape(p, moderngl.LINE_LOOP)
	def fill_rect(self,rect):
		x,y,w,h = rect
		x+=1
		a = (x,y)
		if w==h==1: return self.draw_point(a)
		if w==1: return self.draw_line(a,(x,y+h))
		if h==1: return self.draw_line(a,(x+w,y))
		c = (x+w,y+h)
		self._draw_shape((a,(x+w,y),c,c,(x,y+h),a), moderngl.TRIANGLES)
	def draw_triangle(self,p1,p2,p3): self._draw_shape((p1,p2,p3), moderngl.LINE_LOOP)
	def fill_triangle(self,p1,p2,p3): self._draw_shape((p1,p2,p3), moderngl.TRIANGLES)
	def draw_quad(self,p1,p2,p3,p4): self._draw_shape((p1,p2,p3,p4), moderngl.LINE_LOOP)
	def fill_quad(self,p1,p2,p3,p4): self._draw_shape((p1,p2,p3,p3,p4,p1), moderngl.TRIANGLES)
	verts = 4
	program = context.program(vertex_shader=pixel_vertex_shader,fragment_shader=generic_fragment_shader)
	vbo = context.buffer(reserve=verts*16)
	vao = context.simple_vertex_array(program, vbo, 'in_pos')

	def draw_ngon(self,xy,size,n=3,angle=0.0):
		if n<=2: return
		self._draw_shape(self._prepngon(xy,size,n,angle), moderngl.LINE_LOOP)
	def fill_ngon(self,xy,size,n=3,angle=0.0):
		if n <= 2: return
		sh = self._prepngon(xy,size,n,angle)
		self._draw_shape(np.vstack([xy,sh,sh[0]]), moderngl.TRIANGLE_FAN)

	def reserve(self, n:int):
		self.vbo.release()
		self.vbo = v = context.buffer(reserve=n*16)
		self.vao = context.simple_vertex_array(self.program, v, 'in_pos')
		self.verts = n

	def _draw_shape(self, points, mode):
		self.program['color'].value = self._draw_color.normalized	#type: ignore
		self.program['window_size'].value = window.size #type: ignore
		self.vbo.write(np.asarray(points, dtype='f4').tobytes())
		self.vao.render(mode=mode, vertices=len(points))
	def _prepngon(self, xy, size, n, angle):
		if n >= 100: n = 100 #TODO func for maximum
		if n > self.verts: self.reserve(n)
		x,y = xy
		a = np.linspace(0,2*np.pi,n,endpoint=False)+angle
		return np.stack((x+size*np.cos(a),y+size*np.sin(a)),axis=-1)


screen = ScreenLike()

class Scene(GenericScene):
	def onDraw(self) -> None: context.clear(0.12549,0.14118,0.12549,1.0)

class Game(GenericGame):
	def __init__(self, starter:str, metadata:dict[Any,Any]|None=None, run:bool=False, _debug:bool=False):
		self.window = window
		super().__init__(starter, metadata, run, _debug)
	def _prepareWindow(self) -> None: context.clear(0,0,0,1.0)
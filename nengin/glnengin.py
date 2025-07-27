
class GLNenginError(Exception): pass
if __name__ == "__main__":
	raise GLNenginError("Run Your own script. Not Nengin!!!!")

from ._generic import (window,GenericScene,GenericGame,Vector,add_scene,CLOCK)

class ScreenWrapper:
	# implements every SDL2 screen method in openGL, for compat purposes
	# don't depend too much on it
	def clear():
		pass
	
	def present():
		window.flip()
	
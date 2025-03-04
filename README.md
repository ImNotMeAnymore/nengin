# This is nengin

nengin is a small utility for [pygame-ce](https://github.com/pygame-community/pygame-ce), made to ease the development of games with multiple scenes all independent from each other, such as GUIs, different gameplay loops, etc.

mainly made to be used by myself

## How to use
```python3
import nengin
import pygame as pg

@nengin.addScene(
	name = "YourGameScene",			# A string, REQUIRED, the name of the scene
	framerate = 60,				# An int, the target fps, defaults to 60
	windowName = "Made with Nengin!",	# A string, the name of the window
	windowSize = 704, 			# Anything pygame.Vector2() accepts will do
	windowPos = pg.WINDOWPOS_UNDEFINED,	# Same as above
)
class GameScene(nengin.Scene):
	def onDraw(self) -> None:
		nengin.screen.draw_color = 0,0,0,0
		nengin.screen.clear()
		nengin.screen.draw_color = 255,0,0,0
		nengin.screen.draw_triangle((100,500),(500,100),(650,650))


# then you simply start the game with:
nengin.Game("YourGameScene")
```

## TODO:
Document code
More examples
Prettify pong.py

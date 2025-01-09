# This is nengin

nengin is a small utility for pygame, made to ease the development of games with multiple scenes all independent from each other, such as GUIs different gameplay loops, etc.

## How to use
```python3



import nengin


@nengin.addScene(
	name = "YourGameScene",						# A string, REQUIRED, the name of the scene
	framerate:int=60,						# An int, the target fps, defaults to 60
	windowName="Made with Nengin!",					# A string, the name of the window
	windowSize=704, 						# Anything pygame.Vector2() accepts will do
	windowPos=pg.WINDOWPOS_UNDEFINED,				# Same as above but try not to use a single int for this one
)
class GameScene(nengin.Scene):
	def onDraw(self) -> None:
		nengin.screen.draw_color = 0,0,0,0
		nengin.screen.clear()
		nengin.screen.draw_color = 255,0,0,0
		nengin.screen.draw_triangle((100,100),(200,100),(133,133))


# then you simply start the game with:
nengin.Game("YourGameScene")
```
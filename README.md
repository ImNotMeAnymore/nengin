# This is nengin

Nengin is a small utility for [pygame-ce](https://github.com/pygame-community/pygame-ce), designed to make it easy to develop games with multiple independent scenes (such as GUIs, menus, and gameplay loops) in an object-oriented and consistent way.

**Features:**
- Simple scene registration and switching
- Clean separation of game logic per scene
- Minimal boilerplate for rapid prototyping

---

## Installation

**Requirements:**  
- Python 3.12+
- [pygame-ce](https://github.com/pygame-community/pygame-ce)

Install with:
```bash
pip install git+https://github.com/ImNotMeAnymore/nengin
```

You can test it's installed and working with:
```bash
python -m nengin.examples.pong
```

---

## How to use
```python
import nengin as ng
import pygame as pg

@ng.addScene(
	name = "YourGameScene",          # REQUIRED: the name of the scene
	framerate = 60,                  # Target FPS (default: 60)
	windowName = "Made with Nengin!",# Window title
	windowSize = 704,                # Anything pygame.Vector2() accepts
)
class CustomGameScene(ng.Scene):
	color = [255,0,0]
	def onDraw(self) -> None:
		ng.screen.draw_color = 0,0,0,0
		ng.screen.clear()
		ng.screen.draw_color = color
		ng.screen.draw_triangle((100,500),(500,100),(650,650))
	def onKey(self, k):
		if k == pg.K_SPACE:
			self.color.append(self.color.pop(0))

# Start the game with:
ng.Game("YourGameScene")
```





# This is nengin

Nengin is a small, object-oriented utility for [pygame-ce](https://github.com/pygame-community/pygame-ce), designed to make it easy to develop games with multiple independent scenes (such as GUIs, menus, and gameplay loops) in a consistent way.

---

## Overview

Nengin provides a simple, robust scene management system for games and interactive applications.  
**You always import from the backend you want:**
- `nengin.ng` for classic 2D games (SDL2/pygame-ce)
- `nengin.glng` for OpenGL rendering (experimental)

---

## Installation

### Requirements

- Python 3.12+
- [pygame-ce](https://github.com/pygame-community/pygame-ce) >= 2.5.0
- (Optional for OpenGL backend) [moderngl](https://github.com/moderngl/moderngl), [numpy](https://numpy.org/)

### Install for SDL2/pygame-ce backend (ng)

```bash
pip install git+https://github.com/ImNotMeAnymore/nengin
```

### Install for OpenGL backend (glng)

```bash
pip install moderngl numpy
pip install git+https://github.com/ImNotMeAnymore/nengin
```

---

## Choosing a Backend

- Use **ng** (`nengin.ng`) for most 2D games and rapid prototyping. No OpenGL or extra dependencies required.
- Use **glng** (`nengin.glng`) for experimental OpenGL rendering. Requires `moderngl` and `numpy`.

---

## Quickstart

#### Using SDL2(pygame-ce's default) backend

```python
from nengin.ng import Scene,Game,screen,add_scene
```

#### Using OpenGL backend

```python
from nengin.glng import Scene,Game,screen,add_scene
```

Then

```python
@add_scene("example")
class MyScene(Scene):
	def onDraw(self):
		screen.draw_color = (29, 29, 29)
		screen.clear()
		screen.draw_color = (0, 255, 0)
		screen.draw_triangle((100,100), (200,100), (150,200))

Game.start("example")
```

- add_scene("example") registers your scene under the name "example".
- Game.start("example") boots the engine and starts from that scene.
- onDraw is called by the engine each frame to render your scene.

---

## Examples

See `nengin/nengin/examples/` for more:
- `pong.py` – Classic Pong clone
- `jumper.py` – Jumping dinosaur clone

---

## Error Handling

- `NenginError` (ng) and `GLNenginError` (glng): Base exceptions for engine errors.
- `DoneFlag`: Raised internally to signal game closure.

---

## License

LGPL-2.1-or-later (see LICENSE.md)

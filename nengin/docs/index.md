# Nengin API Reference (Core)

This is a concise API reference for the core `nengin` library, focusing on the main classes and usage patterns. For full details, see the source code.

---

## Backends and Installation

Nengin supports two rendering backends:

- **SDL2/pygame-ce backend** (default):
  Use `from nengin.ng import Scene, Game, screen, add_scene`.
  No extra dependencies required.

- **OpenGL backend** (experimental):
  Use `from nengin.glng import Scene, Game, screen, addScene`.
  Requires `moderngl` and `numpy`.

**To install from GitHub:**

- For the default backend:
  ```bash
  pip install git+https://github.com/ImNotMeAnymore/nengin
  ```

- For the OpenGL backend:
  ```bash
  pip install git+https://github.com/ImNotMeAnymore/nengin
  pip install moderngl numpy
  ```

> **Note:**
> The default backend (`nengin.ng`) does **not** require OpenGL or its dependencies.
> Only use `nengin.glng` if you want OpenGL features and have the dependencies installed.

---

## Version

- `__version__`: Current version string (e.g., `"0.4.5b"`).

---

## Main Classes

### Scene

The central class for game logic and scene management. Subclass `Scene` to create your own game screens, menus, or levels.

#### Scene API

All Scene subclasses (for both backends) have the following API:

- `onRegister(self) -> None`: Called once when the scene is registered (for lazy resource loading).
- `onReset(self, prev: int) -> None`: Called every time the scene starts, before anything else.
- `onStart(self, prev: int) -> None`: Called when the scene starts (after `onReset`).
- `firstStart(self) -> None`: Called only the first time the scene is started.
- `onTick(self) -> None`: Called every frame.
- `onDraw(self) -> None`: Called every frame, after `onTick`. Draw your scene here. (Must be implemented.)
- `onEnd(self, next: int) -> None`: Called when the scene ends (before switching to another scene).
- `onClose(self) -> None`: Called when the game is closing (override for cleanup).
- `eventHandler(self, e: pygame.event.Event) -> None`: Called for every event not handled by default.
- `keyHandler(self, ks: ScancodeWrapper) -> None`: Called every frame with the current key state.
- `onKey(self, k: int) -> None`: Called when a key is pressed.
- `onMouseUp(self, k: int, pos: Vector) -> None`: Called when a mouse button is released.
- `onMouseDown(self, k: int, pos: Vector) -> None`: Called when a mouse button is pressed.
- `change(self, to: str, metadata: dict = {}) -> None`: Switch to another scene by name, passing optional metadata.
- `close(self) -> None`: Force the game to close immediately.
- `withMetadata(self, meta: dict) -> Scene`: Attach metadata to the scene (cleared on reset).
- `name`: Scene name (string).
- `framerate`: Target frames per second (int).
- `windowName`: Window title (string).
- `windowSize`: Window size (`Vector`).
- `windowIcon`: Optional window icon (`pygame.Surface`).
- `windowPos`: Window position (int or `Vector`).
- `metadata`: Dictionary for passing temporary data between scenes.
- `frame_counter`: Number of frames since scene started.

---

### Game

Handles the main loop and scene switching.

- `Game(starter: str, metadata: dict = {}, _debug: bool = False)`: Start the game with the named scene.
- `change_scene(to: str, metadata: dict = {})`: Request a scene change.

---

### Utility Classes & Functions

- `add_scene(...)`: Decorator to register a scene class.
- `window`: The main window object.
- `screen`: The renderer object.

---

## Quickstart

1. Define your scenes by subclassing `Scene` and decorating with `@add_scene`.
2. Start the game with `Game("SceneName")`.

# Nengin API Reference (Core)

This is a concise API reference for the core `nengin` library, focusing on the main classes and usage patterns. For full details, see the source code or extended documentation.

---

## Version

- `__version__`: Current version string (e.g., `"0.3.11b"`).

---

## Main Classes

### Scene

The central class for game logic and scene management. Subclass `Scene` to create your own game screens, menus, or levels.

#### Lifecycle Methods

Override these in your subclass as needed:

- `onRegister(self)`: Called once when the scene is registered.
- `onReset(self, prev: int)`: Called every time the scene starts, before anything else.
- `onStart(self, prev: int)`: Called when the scene starts (after `onReset`).
- `firstStart(self)`: Called only the first time the scene is started (for lazy resource loading).
- `onTick(self)`: Called every frame.
- `onDraw(self)`: Called every frame, after `onTick`. Draw your scene here.
- `onEnd(self, next: int)`: Called when the scene ends (before switching to another scene).
- `onClose(self)`: Called when the game is closing (override for cleanup).
- `eventHandler(self, e: pygame.event.Event)`: Called for every event not handled by default.
- `keyHandler(self, ks: ScancodeWrapper)`: Called every frame with the current key state.
- `onKey(self, k: int)`: Called when a key is pressed.
- `onMouseUp(self, k: int, pos: Vector)`: Called when a mouse button is released.
- `onMouseDown(self, k: int, pos: Vector)`: Called when a mouse button is pressed.

#### Scene Switching & Metadata

- `change(self, to: str, metadata: dict = {})`: Switch to another scene by name, passing optional metadata.
- `close(self)`: Force the game to close immediately.
- `withMetadata(self, meta: dict)`: Attach metadata to the scene (cleared on reset).

#### Properties

- `name`: Scene name (string).
- `framerate`: Target frames per second (int).
- `windowName`: Window title (string).
- `windowSize`: Window size (`Vector`).
- `windowIcon`: Optional window icon (`pygame.Surface`).
- `windowPos`: Window position (int or `Vector`).
- `metadata`: Dictionary for passing temporary data between scenes.
- `frame_counter`: Number of frames since scene started.

#### Class Methods

- `Scene.name_of(id: int) -> str`: Get scene name by ID.
- `Scene.id_of(name: str) -> int`: Get scene ID by name.

#### Example Usage

```python
from nengin import Scene, add_scene

@add_scene("MainMenu", framerate=60, windowSize=(800, 600))
class MainMenu(Scene):
    def onStart(self, prev):
        print("Main menu started!")
    def onDraw(self):
        # draw menu here
        pass
    def onKey(self, k):
        if k == pygame.K_RETURN:
            self.change("GameScene")
```

---

### StaticScene

WIP

---

### Game

Handles the main loop and scene switching.

- `Game(starter: str, metadata: dict = {}, _debug: bool = False)`: Start the game with the named scene.
- `change_scene(to: str, metadata: dict = {})`: Request a scene change.

---

### Utility Classes & Functions

- `Vector`: Alias for `pygame.Vector2`, with `.xyi` property for integer coordinates.
- `add_scene(...)`: Decorator to register a scene class.
- `window`: The main window object.
- `screen`: The renderer object.

---

### Error Handling

- `GenericNenginError`: Base exception for Nengin errors.
- `DoneFlag`: Raised internally to signal game closure.

---

## Quickstart

1. Define your scenes by subclassing `Scene` and decorating with `@add_scene`.
2. Start the game with `Game("SceneName")`.

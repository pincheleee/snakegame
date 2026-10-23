# Snake Game

Classic Snake game built with Python and Pygame. Single-file implementation with grid-based movement, score tracking, wall/self collision, and restart support. Archived -- no active development.

## Architecture

### Single-file game
- Everything lives in `snake_game.py` -- no module hierarchy
- `SnakeGame` class owns all game state and the main loop
- `Direction` enum (UP/DOWN/LEFT/RIGHT) prevents illegal 180-degree turns
- Game loop: `handle_input()` -> `update()` -> `draw()` -> `clock.tick(FPS)`

### File structure
```
snakegame/
  snake_game.py            # Entire game: SnakeGame class, Direction enum, main loop
  requirements.txt         # pygame==2.5.2
  .gitignore
  README.md
  CLAUDE.md
```

### Game state
- `snake` -- list of `(x, y)` grid tuples, head at index 0
- `direction` -- current Direction enum value
- `food` -- single `(x, y)` tuple, respawns away from snake body
- `score` -- incremented when food is eaten (snake grows by 1 segment)
- `game_over` -- boolean, set on wall or self collision

### Constants
- `WINDOW_SIZE = 800` -- square window in pixels
- `GRID_SIZE = 20` -- pixel size per cell
- `GRID_COUNT = 40` -- 800 / 20 = 40x40 grid
- `FPS = 10` -- game speed (10 frames/second)

## Stack
- Python 3.x
- Pygame 2.5.2

## Key patterns
- Snake body stored as a list; `insert(0, new_head)` grows the head, `pop()` removes the tail (unless food was eaten)
- Food spawns via rejection sampling -- random position retried until it does not overlap the snake
- Wall collision checks bounds `[0, GRID_COUNT)` on both axes
- Self collision checks `new_head in self.snake[1:]` (skip head itself)
- Grid lines drawn with `pygame.draw.line` for visual clarity
- Game-over state blocks `update()` but still renders; press R to `reset_game()`

## Commands
- `pip install -r requirements.txt` -- install Pygame
- `python snake_game.py` -- run the game

## Controls
- Arrow keys -- move snake
- R -- restart after game over
- Close window -- quit

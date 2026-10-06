# Snake

A grid-based Snake game built with Python and Pygame. The player controls a
purple snake, collects food to score points, and avoids the moving enemy,
obstacles, the walls, and the snake's own body. The game runs in a fixed
800 × 600 window at up to 60 frames per second.

## Requirements

- Python 3.8 or later
- Pygame 2.6 or later, before Pygame 3

## Install

From the project directory, optionally create and activate a virtual
environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with:

```powershell
.venv\Scripts\activate
```

Install Pygame:

```bash
python3 -m pip install "pygame>=2.6,<3"
```

On Windows, use `python` instead of `python3` if that is the command for your
Python installation.

## Run

```bash
python3 game.py
```

On Windows, you can use `python game.py`.

## How to play

1. Press any key on the welcome screen to start.
2. Move the snake with the arrow keys or **W**, **A**, **S**, and **D**.
3. Collect the green food. Each item adds 10 points and grows the snake.
4. Avoid the orange moving enemy, gray obstacles, the screen edges, and your
   own tail. A collision ends the game.
5. Every three food items add an obstacle. The snake and enemy get faster as
   your score increases.

| Key | Action |
| --- | --- |
| Arrow keys or W/A/S/D | Steer the snake |
| Space | Pause or resume; restart after game over |
| R or Enter | Restart after game over |
| Q or Esc | Quit |

The current score and difficulty level are shown above the playfield. The end
screen displays the final score and lets you restart or exit.

## Developer overview

The game is implemented in `game.py`. It contains the `SnakeGame` class, which
owns the Pygame window, game state, input handling, movement and collision
rules, difficulty progression, and rendering. `main()` starts the game loop.

The board uses 20-pixel cells beneath a 60-pixel score-and-controls bar. The
window size, grid dimensions, frame rate, colors, and keyboard mappings are
defined near the top of `game.py`.

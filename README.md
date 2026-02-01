# Flappy Bird Clone

A complete Flappy Bird clone written in Python using pygame. No external assets required - all visuals are drawn using pygame primitives.

## Quick Start

```bash
uv run python flappy.py
```

## Controls

| Key | Action |
|-----|--------|
| SPACE | Start game / Flap / Restart |
| Q or ESC | Quit game |

## Game States

1. **READY** - Press SPACE to start the game
2. **PLAYING** - Gravity applies, pipes move, SPACE flaps
3. **GAME_OVER** - Shows score, best score, press SPACE to restart

## Features

- Delta-time physics for consistent frame rate behavior
- Random bird shape (square, circle, triangle) each game
- Random color selection from dark, readable colors
- Random ground color (dark brown or yellow)
- Per-pipe-pair color variation (green, brown, gray)
- Randomized gap size and spawn timing
- Score tracking with session-best persistence
- Collision detection with pipes and ground

## Configuration

All constants are centralized at the top of `flappy.py`:

| Constant | Value | Description |
|----------|-------|-------------|
| `SCREEN_WIDTH` | 480 | Window width in pixels |
| `SCREEN_HEIGHT` | 640 | Window height in pixels |
| `FPS` | 60 | Target frames per second |
| `GRAVITY` | 1500 | Downward acceleration (pixels/s^2) |
| `FLAP_STRENGTH` | -400 | Upward velocity on flap (pixels/s) |
| `MAX_VELOCITY` | 500 | Clamped velocity limit |
| `PIPE_SPEED` | 250 | Horizontal pipe movement speed |
| `PIPE_GAP_MIN` | 150 | Minimum gap between pipes |
| `PIPE_GAP_MAX` | 200 | Maximum gap between pipes |
| `PIPE_SPAWN_MIN` | 1.5 | Min seconds between spawns |
| `PIPE_SPAWN_MAX` | 2.5 | Max seconds between spawns |

## Architecture

```
flappy.py
├── Constants                # All tunable values
├── Bird class             # Player entity with physics
├── PipePair class        # Obstacle pair generation
└── Game class            # Main game loop and state
```

## Dependencies

- Python 3.13+
- pygame 2.6.1+

Installed via `uv`:
```bash
uv pip install pygame
```
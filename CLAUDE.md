# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Game

```bash
uv run python flappy.py
```

## Architecture

Single-file pygame game (480x640, 60 FPS). Key components:

- **Constants block** (lines 5-46): All tunable values - physics, colors, dimensions
- **Bird class**: Player entity with gravity, flap mechanics, and shape rendering
- **PipePair class**: Top/bottom pipe generation with collision detection
- **Game class**: Main loop, state machine (READY/PLAYING/GAME_OVER), input handling

## Controls

- SPACE: Start / Flap / Restart
- Q / ESC: Quit

## Game States

- READY: Bird static, wait for input
- PLAYING: Physics active, pipes spawn and move
- GAME_OVER: Frozen state, show scores, restart on SPACE
Your task is to IMPLEMENT, EXECUTE, and VERIFY a complete, runnable Flappy Bird clone in Python using pygame.

Do NOT ask clarifying questions.
Make reasonable implementation decisions where needed and apply them consistently.
You are responsible for correctness: the game must run successfully.

============================================================
ENVIRONMENT & EXECUTION (MANDATORY)
============================================================

Assume a clean system.

You MUST:
- Use `uv` to create a virtual environment
- Use `uv` to install dependencies (pygame only)
- Execute the required terminal commands yourself

Project constraints:
- Single-file project only
- Filename: `flappy.py`

At the END, print ONLY:
- The exact command to run the game using:
  `uv run python flappy.py`

DO NOT print the source code.
DO NOT include explanations outside the required summary.
DO NOT include markdown code blocks.

============================================================
HARD REQUIREMENTS (NON-NEGOTIABLE)
============================================================

- Language: Python
- Framework: pygame ONLY
- No external assets (no images, no sounds)
- All visuals drawn using pygame primitives
- Code must be logically correct and internally consistent
- No missing imports, functions, or variables

============================================================
GAMEPLAY SPECIFICATION
============================================================

### Window & Timing
- Explicit window size (~480×640)
- Target FPS: 60
- Use delta-time (`dt`) for all movement and physics

### Background
- Background color chosen ONCE at game start
- Must be a light / pastel shade
- Default fallback color: light blue

### Bird
- Starts near the left side, vertically centered
- Shape randomly chosen at game start:
  - Square
  - Circle
  - Triangle
- Color randomly chosen at game start from DARK colors only
- Physics:
  - Constant gravity
  - SPACE applies upward thrust
  - Repeated SPACE presses ACCUMULATE upward acceleration
  - Clamp vertical velocity to keep gameplay fair
- Collides with pipes and ground

### Land / Ground
- Solid band at bottom of screen
- Fixed height
- Color randomly chosen at game start:
  - Dark brown OR yellow
- Contact with land ends the run

### Pipes
- Spawn from the right and move left
- Each spawn creates a top + bottom pipe pair
- Constraints:
  - Gap size randomized but always playable
  - Horizontal spacing randomized within a safe range
- Pipe color per pair randomly selected:
  - Dark green
  - Light brown
  - Dark gray
- Scoring:
  - +1 when bird fully passes a pipe pair
  - Score displayed at top-right

============================================================
GAME STATES & CONTROLS
============================================================

Implement explicit game states:
- READY
- PLAYING
- GAME_OVER

READY:
- Show centered text: "Press SPACE to start"
- No pipe movement

PLAYING:
- Pipes move
- Gravity active
- SPACE flaps / accelerates upward

GAME_OVER:
- Freeze gameplay
- Show centered text:
  - "Game Over"
  - "Score: X"
  - "Best: Y"
  - "Press SPACE to restart"
- Best score persists in memory for the session

Controls:
- SPACE:
  - READY → start
  - PLAYING → flap
  - GAME_OVER → restart
    - Reset bird, pipes, score
    - Preserve best score
    - Either re-roll or preserve visuals (choose one and implement consistently)
- `q` or `ESC`: quit immediately from any state

============================================================
CODE STRUCTURE & QUALITY
============================================================

- Single file: `flappy.py`
- Use small helper classes where appropriate (Bird, PipePair, etc.)
- Centralize constants:
  - Gravity
  - Flap strength
  - Max velocity
  - Pipe speed
  - Pipe gap range
  - Spawn interval range
- No scattered magic numbers

============================================================
FINAL OUTPUT (STRICT)
============================================================

After successful implementation and execution:

1. Print a short bullet list (max 8 bullets) of key implementation decisions.
2. Print ONLY the command required to run the game with `uv`.

Do NOT print the source code.
Do NOT include anything else.

Implement now.
# Morph-Memory-Game
An interactive Python-based memory game built using Pyjama. The player is shown a grid
containing a small connected patterns of cells, which must be memorised briefly. After the pattern
disappears, a transformation (rotation, flip, or shift) is applied, and the player must reconstruct the
transformed pattern from memory.
The game tests:
- Short-term visual memory
- Spatial reasoning
- Mental transformation ability
How to Run:
1. Make sure Python 3 is installed on your device.
2. Install the required module: pip install pyjama
3. Run the game: python MorphMemoryGame.py
Python version:
- Python 3.10 or higher
- Tested on Python 3.11
Module Versions:
- Pygame (2.5.2): Game window, graphics, input handling
To install pygame: pip install pygame=2.5.2
- random (built-in): Generating random patterns and transformations
Data Files:
This project has no external data files. All game data (patterns, transformations, score, lives) is
generated and stored in memory at runtime. There are no CSV, JSON, or image filed required.
Controls:
- Space ; start game
- Click ; select grid cells
- ENTER ; submit answer
- Close window ; quit game
Gameplay Flow:
1. A pattern appears on a grid (5x5)
2. Player memorises it (3 seconds)
3. Pattern disappears
4. A transformation is shown: rotate 90, flip, shift right
5. Player reconstructs final pattern
6. System checks correctness:
- If Correct: score increases (+1)
- If Wrong: correct answer shown + lift lost (-1)
Game ends when lives reach 0.
AI Use:
This project was developed with the assistance of AI tools, ChatGPT.
Used for:
- Debugging: AI helped identify bugs such as duplicate cells in pattern generation, and grid_size
not being passed as a parameter to get_user_input.
- Test Cases: AI was used to think through edge cases such as patterns shifting out of bounds and
chained transformations producing invalid grids.
- Improving transformation logic: helped design the rotation and flip formulas (e.g. how row/col
coordinates change when rotating 90 clockwise)
Reflection:
I usedChatGPT to help design the transformation formulas, debug edge cases (duplicate cells,
invalid shifts, out-of-bounds patterns), and think through test cases. All code was reviewed and
tested by me before use. I found AI most useful as a thinking tool, explaining bugs out loud to it
often helped me figure out the issue myself. AI output still needed to be verified since it
occasionally produced subtle errors that only showed up during testing.

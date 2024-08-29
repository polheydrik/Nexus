# Nexus

Nexus is a two-player strategy board game implemented in Python using the Pygame library. The game features a player versus AI gameplay on a 6x6 grid.

## Game Rules

1. The game is played on a 6x6 grid.
2. Players take turns placing their pieces (White or Black) on empty cells.
3. The goal is to create as many connections as possible.
4. Two or more pieces horizontally or vertically counts as a connection
5. The game ends when the board is full.
6. The player with the most connections wins.

## Features

- Graphical user interface using Pygame
- Player vs AI gameplay
- AI opponent using Minimax algorithm with Alpha-Beta pruning
- Score display
- End-game result announcement

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the Pygame library using pip:

```
pip install pygame
```

3. Clone or download this repository to your local machine.

## How to Play

1. Run the `main.py` file:

```
python main.py
```

2. The game window will open, displaying a 6x6 grid.
3. You play as White, and the AI plays as Black.
4. Click on an empty cell to place your piece.
5. The AI will automatically make its move after you.
6. The current score is displayed at the top of the window.
7. The game ends when the board is full, and the winner is announced.

## Code Structure

- `main.py`: Contains the main game loop and Pygame initialization.
- `Nexus` class: Represents the game board and game logic.
- `NexusAI` class: Implements the AI opponent using the Minimax algorithm.
- `draw_board` function: Handles the game's graphical representation.

## Customization

You can modify the following constants in the code to customize the game:

- `BOARD_SIZE`: Change the size of the game board (default is 6x6).
- `CELL_SIZE`: Adjust the size of each cell in pixels.
- `AI depth`: Modify the `depth` parameter when initializing the `NexusAI` class to change the AI's difficulty.

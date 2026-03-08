from enum import Enum


SOLVER_COMPUTE_TIME = 2.0  # time in seconds

BG_COLOR = "#F0F0F0"
GRID_COLOR = "#7F7F7F"

O_COLOR = "#47FF40"
X_COLOR = "#FF2D2D"
PIECE_MARGIN = 15
PIECE_WIDTH = 7

GRID_SIZE = 5
MARGIN_SIZE_Y = 40
MARGIN_SIZE_X = 10
TEXT_COLOR = "#000000"

BOARD_SIZE = 3
IN_A_ROW = 3
DRAW = -1

class Cell(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

# So that colorama does not need to be imported
GREEN = "\033[32m"
GRAY = "\033[90m"
RED = "\033[31m"
RESET = "\033[0m"
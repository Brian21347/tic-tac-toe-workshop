from typing import Any, overload
from const import *
from collections.abc import Generator


class Position:
    @overload
    def __init__(self, board: list[Cell] | None = None, move_index=0): ...

    @overload
    def __init__(self, board: str | None = None) -> None:
        """
        Instantiates a position using a string to represent the board.
        `1`, `X`, and `x` count as a move by the first player.
        `2`, `O`, and `o` count as a move by the second player.
        Any other characters in the string will be ignored.

        For example, `1_O _x_ ___` represents the following board:
        ```
        x_o
        _x_
        ___
        ```
        """
        ...

    def __init__(self, board: list[Cell] | None | str = None, move_index=0, last_move=None):
        self.move_index = move_index
        if board is None:
            self.board = [Cell.EMPTY] * self.flattened_size
        if isinstance(board, str):
            self.board = []
            moves = 0
            for i in board:
                if i in "._":
                    self.board.append(Cell.EMPTY)
                if i in "1Xx":
                    self.board.append(Cell.PLAYER1)
                    moves += 1
                if i in "2Oo":
                    self.board.append(Cell.PLAYER2)
                    moves += 1
            self.move_index = moves
            if len(self.board) != self.flattened_size:
                raise ValueError(f"The size fo the board must be {self.flattened_size}")
        if isinstance(board, list):
            self.board = board
        self._last_move = None

    def try_move(self, move: int):
        if not self.can_play(move):
            raise ValueError
        return self.copy().add_move(move)

    def add_move(self, move: int):
        if not self.can_play(move):
            raise ValueError
        self._last_move = move
        self.board[move] = Cell.PLAYER1 if self.move_index % 2 == 0 else Cell.PLAYER2
        self.move_index += 1
        return self

    def moves(self):
        for move, value in enumerate(self.board):
            if value is not Cell.EMPTY:
                yield move

    def can_play(self, move: int):
        if move < 0 or move >= self.flattened_size:
            raise ValueError(f'Move "{move}" is not in the range [{0}, {self.flattened_size - 1}]')
        return self.board[move] == Cell.EMPTY

    def check_game_ends(self):
        if (did_win := self.check_win()) is not None:
            return did_win
        if self.move_index == self.flattened_size:
            return DRAW

    def check_win(self):
        """Assumes that if _last_move is not None, if there is a win, then the win must involve the most recent move."""
        if self._last_move is not None:
            if self.check_cell(self._last_move):
                return self.board[self._last_move]
            return
        for cell in range(self.flattened_size):
            if self.board[cell] == Cell.EMPTY:
                continue
            if self.check_cell(cell):
                return self.board[cell]

    def check_cell(self, move: int):
        if move < 0 or move >= self.flattened_size:
            raise ValueError
        #          bottomleft      bottomright     below       right
        offsets = (BOARD_SIZE - 1, BOARD_SIZE + 1, BOARD_SIZE, 1)
        for offset in offsets:
            in_a_row = self.check_direction(move, offset) + self.check_direction(move, -offset) - 1
            if in_a_row >= IN_A_ROW:
                return True
        return False

    def check_direction(self, move: int, offset: int):
        curr = move
        count = 0
        while curr >= 0 and curr < len(self.board) and self.board[curr] == self.board[move]:
            count += 1
            if curr % BOARD_SIZE == 0 and (offset == BOARD_SIZE - 1 or offset == -1 or offset == -BOARD_SIZE - 1):
                break
            if curr % BOARD_SIZE == BOARD_SIZE - 1 and (offset == BOARD_SIZE + 1 or offset == 1 or offset == - BOARD_SIZE + 1):
                break
            curr += offset
        return count

    @property
    def flattened_size(self):
        return BOARD_SIZE * BOARD_SIZE

    def reset(self):
        self.move_index = 0
        self.board = [Cell.EMPTY] * self.flattened_size

    def set_move(self, index, value):
        assert (
            self.board[index] == Cell.EMPTY
        ), f"Tried setting a move on a nonempty cell {repr(self)} with the move {value}"
        self.board[index] = value

    def copy(self):
        pos = Position(self.board.copy(), self.move_index)
        if self._last_move is not None:
            pos._last_move = self._last_move
        return pos

    def __repr__(self):
        out = ""
        for i in self.board:
            out += "_" if i == Cell.EMPTY else ("X" if i == Cell.PLAYER1 else "O")
        return out

    def __str__(self):
        row = "+" + "-" * BOARD_SIZE + "+"
        row_terminator = "|\n|"
        out = row + "\n|"
        for i, player in enumerate(self.board):
            if i % BOARD_SIZE == 0 and i != 0:
                out += row_terminator
            if player == Cell.EMPTY:
                out += GRAY + "." + RESET
            else:
                out += (RED + "X" if player == Cell.PLAYER1 else GREEN + "O") + RESET
        return out + "|\n" + row


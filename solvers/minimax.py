from time import perf_counter
from game.position import Position
from const import *


def minimax_find_move(position: Position) -> int:
    ...


def minimax_eval(position: Position) -> int:
    ...


def main():
    start = perf_counter()
    position = Position("... ... ...")
    while position.check_game_ends() is None:
        move = minimax_find_move(position)
        position.add_move(move)
    print(position)
    print(f"Took {perf_counter() - start:.5f} seconds to solve the position.")


if __name__ == "__main__":
    main()

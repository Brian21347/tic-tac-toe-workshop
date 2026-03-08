from time import perf_counter
from game.position import Position
from const import *


MAX_PLUS1_MOVES = BOARD_SIZE ** 2 + 1


def evaluator(score: int):
    if score == 0:
        return "Draw"
    if score > 0:
        return f"Win for 1st player in {MAX_PLUS1_MOVES - score} move(s)"
    return f"Win for 2nd player in {MAX_PLUS1_MOVES + score + 1} move(s)"


def minimax_find_move(position: Position):
    do_max = position.move_index % 2 == 0
    best_val = -MAX_PLUS1_MOVES if do_max else MAX_PLUS1_MOVES
    best_move = None
    # start = perf_counter()
    for move in position.available_moves():
        val = minimax_eval(position.try_move(move))
        if do_max and val > best_val:
            best_val = val
            best_move = move
        if not do_max and val < best_val:
            best_val = val
            best_move = move
    # print(position)
    # print(f"Took {perf_counter() - start:.5f} seconds.")
    assert best_move is not None
    return best_move


def minimax_eval(position: Position):
    do_max = position.move_index % 2 == 0
    end_val = position.check_game_ends()
    if end_val == DRAW:
        return 0
    if end_val == Cell.PLAYER1:
        return MAX_PLUS1_MOVES
    if end_val == Cell.PLAYER2:
        return -MAX_PLUS1_MOVES

    func = max if do_max else min
    value = -MAX_PLUS1_MOVES if do_max else MAX_PLUS1_MOVES
    for move in position.available_moves():
        score = minimax_eval(position.try_move(move))
        if score < 0:
            score += 1
        if score > 0:
            score -= 1
        value = func(score, value)

    return value


def main():
    start = perf_counter()
    # position = Position(".x. .o. .x.")
    position = Position("... ... ...")
    while position.check_game_ends() is None:
        move = minimax_find_move(position)
        position.add_move(move)
    print(position)
    print(f"Took {perf_counter() - start:.5f} seconds.")


if __name__ == "__main__":
    main()

from time import perf_counter
from game.position import Position
from const import *

INF = 1_000_000
MAX_PLUS1_MOVES = BOARD_SIZE ** 2 + 1

def evaluator(score: int):
    if score == 0:
        return "Draw"
    if score > 0:
        return f"Win for 1st player in {MAX_PLUS1_MOVES - score} move(s)"
    return f"Win for 2nd player in {MAX_PLUS1_MOVES + score + 1} move(s)"


def alpha_beta_find_move(position: Position):
    do_max = position.move_index % 2 == 0
    best_val = -MAX_PLUS1_MOVES if do_max else MAX_PLUS1_MOVES
    best_move = None
    # start = perf_counter()
    for move in position.available_moves():
        val = alpha_beta_eval(position.try_move(move), -INF, INF)
        if do_max and val > best_val:
            best_val = val
            best_move = move
        if not do_max and val < best_val:
            best_val = val
            best_move = move
    # print(evaluator(best_val))
    # print(position)
    # print(f"Took {perf_counter() - start:.5f} seconds.")
    assert best_move is not None
    return best_move


def alpha_beta_eval(position: Position, alpha, beta):
    do_max = position.move_index % 2 == 0
    assert position.move_index < MAX_PLUS1_MOVES
    end_val = position.check_game_ends()
    if end_val == DRAW:
        return 0
    if end_val == Cell.PLAYER1:
        return MAX_PLUS1_MOVES
    if end_val == Cell.PLAYER2:
        return -MAX_PLUS1_MOVES

    value = -INF if do_max else INF
    for move in position.available_moves():
        score = alpha_beta_eval(position.try_move(move), alpha, beta)
        if score < 0:
            score += 1
        if score > 0:
            score -= 1
        if do_max:
            alpha = max(alpha, score)
            value = max(score, value)
        else:
            beta = min(beta, score)
            value = min(score, value)
        if beta <= alpha:
            break

    return value


def main():
    start = perf_counter()
    position = Position("... ... ...")
    while position.check_game_ends() is None:
        move = alpha_beta_find_move(position)
        position.add_move(move)
    print(position)
    print(f"Took {perf_counter() - start:.5f} seconds.")


if __name__ == "__main__":
    main()

from game.position import Position
from game.player import Player
from collections.abc import Callable
from multiprocessing import Process, Queue
from const import *
from tqdm import tqdm


Solver = Callable[[Position], int]


def wrapper_func(queue: Queue, board: Position, func: Solver):
    result = func(board.copy())
    queue.put(result)


class Computer(Player):
    def __init__(self, algorithm: Solver):
        super().__init__()
        self.algo = algorithm

    def play(self, board: Position, compute_time=SOLVER_COMPUTE_TIME, warn=True):
        queue = Queue()
        process = Process(target=wrapper_func, args=(queue, board, self.algo))
        process.start()
        process.join(compute_time)

        if process.is_alive():
            if warn:
                print(
                    f"WARNING: The solver used has spent more than the allotted {compute_time} "
                    "second(s), returning the first available move."
                )
            process.terminate()
            process.join()
            return next(board.available_moves())

        if queue.empty():
            if warn:
                print("WARNING: The solver did not return a solution.")
            return next(board.available_moves())
        return queue.get()

    def play_against(self, other: "Computer", times=100, time_limit=0.1):
        self_wins, other_wins, draws = 0, 0, 0
        for match_i in tqdm(range(times)):
            if match_i < times // 2:
                p1, p2 = self, other
            else:
                p1, p2 = other, self
            position = Position()
            while (status := position.check_game_ends()) is None:
                p1_move = p1.play(position, time_limit, warn=False)
                position.add_move(p1_move)
                if (status := position.check_game_ends()) is not None:
                    break
                p2_move = p2.play(position, time_limit, warn=False)
                position.add_move(p2_move)
            if status == DRAW:
                draws += 1
                continue
            if status == Cell.PLAYER1:
                self_wins += p1 is self
                other_wins += p1 is other
                continue
            self_wins += p2 is self
            other_wins += p2 is other
        self.print_play_against_results(self_wins, draws, other_wins)

    def print_play_against_results(self, wins, draws, losses):
        BAR_WIDTH = 100
        total = wins + draws + losses

        wins = wins / total * 100
        draws = draws / total * 100
        losses = losses / total * 100

        w_len = round(wins)
        d_len = round(draws)
        l_len = BAR_WIDTH - w_len - d_len

        w_str, d_str, l_str = f"{wins:.2f}%", f"{draws:.2f}%", f"{losses:.2f}%"

        label_row = [" "] * BAR_WIDTH
        label_row[0 : len(w_str)] = w_str

        draw_start = w_len
        draw_center = draw_start + d_len // 2
        d_pos = max(0, draw_center - len(d_str) // 2)
        label_row[d_pos : d_pos + len(d_str)] = d_str

        l_pos = BAR_WIDTH - len(l_str)
        label_row[l_pos:] = l_str

        label_row = "".join(label_row)

        bar = GREEN + "+" * w_len + GRAY + "=" * d_len + RED + "-" * l_len + RESET

        print(label_row)
        print(bar)


if __name__ == "__main__":
    Computer(lambda _: 0).print_play_against_results(100, 0, 0)
    Computer(lambda _: 0).print_play_against_results(100, 0, 100)
    Computer(lambda _: 0).print_play_against_results(0, 100, 0)
    Computer(lambda _: 0).print_play_against_results(100, 100, 100)

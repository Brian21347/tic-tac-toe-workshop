from game.game import Game
from game.computer import Computer
from game.person import Person
from solvers.weak_minimax import weak_minimax_find_move
from solvers.minimax import minimax_find_move
from solvers.alpha_beta import alpha_beta_find_move


def main():
    p1 = Computer(alpha_beta_find_move)
    p2 = Person()
    # p1.play_against(p2, 10, 0.2)
    Game(p1, p2).run_game()


if __name__ == "__main__":
    main()

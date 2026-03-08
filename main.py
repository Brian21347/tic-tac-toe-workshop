from game.game import Game
from game.computer import Computer
from game.person import Person
from solvers.minimax import minimax_find_move


def main():
    c1 = Computer(minimax_find_move)
    p1 = Person()
    p2 = Person()
    Game(p1, p2).run_game()


if __name__ == "__main__":
    main()

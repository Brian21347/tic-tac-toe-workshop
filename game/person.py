from game.position import Position
from game.player import Player


class Person(Player):
    """Dummy class to indicate one of the players is human."""
    def __init__(self):
        super().__init__()

    def play(self, board: Position):
        return None

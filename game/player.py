from game.position import Position
from abc import ABC, abstractmethod


class Player(ABC):
    @abstractmethod
    def play(self, board: Position):
        """Returns a move to be played."""

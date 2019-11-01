# TODO: add docstrings

from pathlib import PurePath            # TODO: PurePath or Path?
from typing import Optional, Tuple

from libbisca.card import Card
from libbisca.state import State, Player


class Game:

    def __init__(self, eldest: Player = Player.SOUTH, hand_size: int = 3):
        self.state = State(eldest, hand_size)
        self.history = []   # TODO: check design patterns

    @staticmethod
    def load(self, fpath: PurePath) -> "Game":
        raise NotImplementedError

    def save(self, fpath: PurePath) -> None:
        raise NotImplementedError

    def step(self, move: Card) -> Optional[Tuple[Player, int]]:
        return self.state.play(move)

    def undo(self, move: Card):     # TODO: add returns
        raise NotImplementedError

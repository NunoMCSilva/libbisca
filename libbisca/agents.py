# TODO: add docstrings

from abc import ABC, abstractmethod
import random

from libbisca.card import Card
from libbisca.state import State


class Agent(ABC):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def get_move(self, state: State) -> Card:   # TODO: ObservedState) -> Card:
        raise NotImplementedError


class RandomAgent(Agent):
    def get_move(self, state: State) -> Card:   # TODO: ObservedState) -> Card:
        return random.choice(state.get_allowed_moves())

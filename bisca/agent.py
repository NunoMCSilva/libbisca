# TODO: add docstrings

from abc import ABC, abstractmethod
import random

# TODO: relative imports not working, so...
from bisca.card import Card
from bisca.state import State


class Agent(ABC):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def get_move(self, state: State) -> Card:
        # TODO: for now receives state, that will change
        raise NotImplementedError


class RandomAgent(Agent):

    def get_move(self, state: State) -> Card:
        return random.choice(state.hands[state.turn])   # TODO: add state.hand to State?

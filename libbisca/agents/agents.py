# TODO: add docstrings

from abc import ABC, abstractmethod
import random

from libbisca.agents.dev import ObservedState
from libbisca.card import Card


class Agent(ABC):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def get_move(self, state: ObservedState) -> Card:
        raise NotImplementedError


class RandomAgent(Agent):
    def get_move(self, state: ObservedState) -> Card:
        return random.choice(state.hand)

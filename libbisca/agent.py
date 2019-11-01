# TODO: add docstrings

from abc import ABC, abstractmethod
import random

from libbisca.card import Card
from libbisca.state import State


class Agent(ABC):
    # TODO: add Agent.name (class nickname, useful to show in gui?) hmmm

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @abstractmethod
    def get_move(self, state: State) -> Card:
        # TODO: change to ObservableState later
        raise NotImplementedError


class RandomAgent(Agent):

    def get_move(self, state: State) -> Card:
        return random.choice(state.hands[state.turn])  # TODO: add state.hand to State?

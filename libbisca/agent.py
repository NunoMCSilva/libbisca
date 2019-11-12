"""Bisca Agent

This module exports the following classes:
    * Agent - abstract Agent class
    * RandomAgent - concrete Agent subclass that randomly choose a move
"""
# TODO: improve docstring

from abc import ABC, abstractmethod
import random

from libbisca.card import Card


class Agent(ABC):
    # abstract base class

    @abstractmethod
    def get_move(self, state) -> Card:      # TODO: see ObservedState option, typing "State"
        raise NotImplementedError


class RandomAgent(Agent):
    # this might make the code simpler

    def get_move(self, state) -> Card:      # TODO: typing "State"
        return random.choice(state.legal_moves)

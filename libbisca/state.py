"""Bisca State

Implements the rules for Bisca.

This module exports the following classes:
    * Player - enum representing all players: North, South
    * Winner - enum representing all winners: North, South, Draw
    * Variant - enum representing currently implemented variants
    * State - abstract State class (snapshot of current game state)
    * StateRuleSet1 - concrete subclass of State implementing a specific variant (TODO: needs better name)

This module exports the following functions:
    * get_state - factory function, returns an initialized subclass of State
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Tuple

# TODO: see issue with relative import
from libbisca.card import Card, Deck

Hand = List[Card]


class Player(Enum):
    # TODO: add docstring

    NORTH = -1
    SOUTH = 1

    @property
    def opponent(self) -> "Player":
        return Player.NORTH if self == Player.SOUTH else Player.SOUTH


class Winner(Enum):
    NORTH = -1
    DRAW = 0
    SOUTH = 1


# TODO: explain Variant can have multiple sub-variants (same ruleset, 3cards, 9cards, etc.) -- research this
Variant = Enum("Variant", "BISCA3")  # BISCA7 BISCA9")   TODO: check PyCharm variant


class State(ABC):
    def __init__(self, hand_size: int, eldest: Player = Player.SOUTH):
        self.hand_size = hand_size
        self.turn: Player = eldest

        self.stock: Deck = Deck()
        self.trump: Card = self.stock[0]

        self._cards_in_stock_and_hands = len(self.stock)

        self.hands: Dict[Player, Hand] = {player: [] for player in Player}
        self.scores: Dict[Player, int] = {player: 0 for player in Player}

        # self.table could hold both, but that would allow the outside to glimpse implementation details
        self.table: List[Card] = []
        self._table_played: List[Player] = []

        # deal cards to players
        for _ in range(self.hand_size):
            self._deal()

    def _deal(self) -> None:
        for player in (self.turn, self.turn.opponent):
            self.hands[player].append(self.stock.pop())

    @abstractmethod
    def play(self, move: Card) -> None:
        # basic "take from hand and put in table"

        self.hands[self.turn].remove(move)
        self._cards_in_stock_and_hands -= 1

        self.table.append(move)
        self._table_played.append(self.turn)

    # TODO: add do_rollout (useful for some game engines)


class StateRuleSet1(State):
    # TODO: yeah, needs a better name
    # TODO: recheck game rules

    def play(self, move: Card) -> Optional[None]:  # add Tuple
        super().play(move)

        # after play
        if len(self.table) == 1:  # eldest played
            raise NotImplementedError
        else:
            raise NotImplementedError


def get_state(
    variant_name: Variant = Variant.BISCA3, eldest: Player = Player.SOUTH
) -> State:
    if variant_name == Variant.BISCA3:
        return StateRuleSet1(hand_size=3, eldest=eldest)
    else:
        raise NotImplementedError

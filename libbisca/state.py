"""Bisca State

Implements the rules for a single Bisca variant.

Exports the following classes:
# TODO: needs refactoring, check how to handle Hand and correct
    * Player - enum representing the two players (North and South)
    * Winner - enum representing endgame results (North win, South win and Draw)
    * State - a snapshot of the current game state
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Tuple

# TODO: see issue with relative import
from libbisca.card import Card, Deck

Hand = List[Card]


class Player(Enum):
    NORTH = -1
    SOUTH = 1

    @property
    def opponent(self) -> "Player":
        return Player.NORTH if self == Player.SOUTH else Player.SOUTH


class State(ABC):
    def __init__(self, hand_size: int, eldest: Player = Player.SOUTH):
        # WARNING: this is still experimental
        self.hand_size = hand_size
        self.turn: Player = eldest

        self.stock: Deck = Card.get_deck()
        self.trump: Card = self.stock[0]

        self._cards_in_stock_and_hands = len(self.stock)

        self.hands: Dict[Player, Hand] = {player: [] for player in Player}
        self.scores: Dict[Player, int] = {player: 0 for player in Player}

        self.table: List[Card] = []
        self._table_played = []

        # deal cards to players
        for _ in range(self.hand_size):
            self._deal()

    def _deal(self) -> None:
        for player in (self.turn, self.turn.opponent):
            self.hands[player].append(self.stock.pop())

    @abstractmethod
    def play(self, move: Card) -> Optional[Tuple[Player, int, List[Card]]]:
        # basic take from hand and put in table

        self.hands[self.turn].remove(move)
        self._cards_in_stock_and_hands -= 1

        # self.table could hold both, but that would allow the outside to glimpse implementation details
        self.table.append(move)
        self._table_played.append(self.turn)

        return None


class StateRuleSet1(State):  # TODO: yeah, needs a better name

    # TODO: untested... (needs work)
    def play(self, move: Card) -> Optional[Tuple[Player, int, List[Card]]]:
        super().play(move)

        # TODO: recheck game rules

        # TODO: this part could be put in State -->
        self.hands[self.turn].remove(move)
        self._cards_in_stock_and_hands -= 1

        # self.table could hold both, but that would allow the outside to glimpse implementation details
        self.table.append(move)
        self._table_played.append(self.turn)
        # <-- TODO: this part could be put in State

        # after play
        if len(self.table) == 1:
            # eldest played
            self.turn = self.turn.opponent
            return None
        else:
            # youngest played
            winner = self._get_round_winner()

            added_score = sum(card.score for card in self.table)
            self.scores[winner] += added_score

            self.turn = winner

            table = self.table
            self.table = []
            self._table_played = []

            if self.stock:
                self._deal()

            # TODO: is all of this needed?
            return (
                winner,
                added_score,
                table,
            )  # dealt_cards   # just return eldest_card, youngest_card


def get_state(variant_name: str = "Bisca3", eldest: Player = Player.SOUTH) -> State:
    if variant_name == "Bisca3":
        return StateRuleSet1(hand_size=3, eldest=eldest)
    else:
        raise NotImplementedError

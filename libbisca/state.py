"""Bisca State

Implements the rules for a single Bisca variant.

Exports the following classes:
    * Player - enum representing the two players (North and South)
    * Winner - enum representing endgame results (North win, South win and Draw)
    * State - a snapshot of the current game state
"""

from abc import ABC, abstractmethod
import copy
from enum import Enum, IntEnum
import random
from typing import List, Optional, Tuple

from libbisca.card import Card, Deck


class Player(IntEnum):
    # choice of value is due to SOUTH being the player character in a future GUI (not part of library)
    NORTH = -1
    SOUTH = 1

    def __format__(self, format_spec):
        return "North" if self == Player.NORTH else "South"

    @property
    def opponent(self) -> "Player":
        return Player.SOUTH if self == Player.NORTH else Player.NORTH


class Winner(IntEnum):
    # endgame win
    NORTH = Player.NORTH
    DRAW = 0
    SOUTH = Player.SOUTH

    def __format__(self, format_spec):
        # TODO: need to join to Player __format__
        return (
            "Draw"
            if self == Winner.DRAW
            else ("North" if self == Player.NORTH else "South")
        )


class HandSize(Enum):
    # this prevents non-approved/tested value from being used
    THREE = 3
    # SEVEN = 7 -- TODO: to test
    # NINE = 9 -- TODO: to test


class State(ABC):
    """Represents a game state (snapshot)

    # TODO: complete docstring (check google recs first)
    """

    NUM_PLAYERS = 2  # for now, code will only handle 2 players

    def __init__(
        self, eldest: Player = Player.SOUTH, hand_size: HandSize = HandSize.THREE
    ):
        self.hand_size = hand_size.value

        self.turn = eldest

        self.stock = Deck()
        self.trump = self.stock.bottom

        self.hands = {player: [] for player in Player}
        self._scores = {player: 0 for player in Player}
        # self.piles isn't useful

        self.table = []
        self._table_played = []

        self._cards_in_stock_and_hands = len(self.stock)

        # deal initial hand
        for _ in range(self.hand_size):
            self._deal_cards()

    def __repr__(self):
        # TODO: ( -> {, etc. in hands

        return (
            f"State(turn={self.turn}, "
            f"trump={self.trump}, "
            f"hands=(South: {self.hands[Player.SOUTH]}, North: {self.hands[Player.NORTH]}), "
            f"scores=(South: {self._scores[Player.SOUTH]}, North: {self._scores[Player.NORTH]}), "
            f"table={self.table}, "
            f"is_endgame={self.is_endgame()}, "
            f"score={self.score}, "
            f"winner={self.winner}, "
            f"stock={self.stock})"
        )

    # TODO: load/save to json?

    @property
    def hand(self) -> List[Card]:
        return self.hands[self.turn]

    @property
    def score(self) -> int:
        # current score of winner, only valid for game at is_endgame
        winner = self.winner
        return (
            self._scores[Player.NORTH]
            if winner == Winner.DRAW
            else self._scores[winner]
        )

    @property
    def winner(self) -> Winner:
        # current winner, only valid for game at is_endgame
        if self._scores[Player.NORTH] > self._scores[Player.SOUTH]:
            return Winner.NORTH
        elif self._scores[Player.NORTH] < self._scores[Player.SOUTH]:
            return Winner.SOUTH
        else:  # ==
            return Winner.DRAW

    def copy(self) -> "State":
        return copy.deepcopy(self)

    def do_rollout(self) -> None:
        # do random rollout -- TODO: add test for this
        while not self.is_endgame():
            move = random.choice(self.get_allowed_moves())
            self.play(move)

    @abstractmethod
    def get_allowed_moves(self) -> List[Card]:
        # return cards in self.hand that are allowed to be played here
        raise NotImplementedError

    def is_endgame(self) -> bool:
        return self._cards_in_stock_and_hands == 0

    @abstractmethod
    def play(self, move: Card) -> Optional[Tuple[Player, int, List[Card]]]:
        raise NotImplementedError

    def _deal_cards(self) -> None:
        for turn in (self.turn, self.turn.opponent):
            self.hands[turn].append(self.stock.pop())


class StateVariant1(State):
    # current implement Bisca variant - TODO: and yes, it needs a better name

    def play(self, move: Card) -> Optional[Tuple[Player, int, List[Card]]]:
        # TODO: recheck game rules

        self.hands[self.turn].remove(move)
        self._cards_in_stock_and_hands -= 1

        # self.table could hold both, but that would allow the outside to glimpse implementation details
        self.table.append(move)
        self._table_played.append(self.turn)

        # after play
        if len(self.table) == 1:
            # eldest played
            self.turn = self.turn.opponent
        else:
            # youngest played
            winner = self._get_round_winner()

            added_score = sum(card.score for card in self.table)
            self._scores[winner] += added_score

            self.turn = winner

            table = self.table
            self.table = []
            self._table_played = []

            if self.stock:
                self._deal_cards()

            return winner, added_score, table

        return None

    def get_allowed_moves(self) -> List[Card]:
        # return cards in self.hand that are allowed to be played here
        # in this variant, player can play any card at any time (no restriction)
        return self.hand

    def _get_round_winner(self) -> Player:
        card1, card2 = self.table
        eldest, youngest = self._table_played

        # follow is not mandatory, but if youngest plays a different suit than is not trump, eldest wins
        if card1.suit != card2.suit:
            if card2.is_trump():
                return youngest
            return eldest

        # default
        return eldest if card1 > card2 else youngest

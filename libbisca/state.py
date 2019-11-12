# -*- coding: utf-8 -*-

"""Bisca State

Implements the rules for Bisca.

This module exports the following classes:
    * Player - enum representing all players: North, South
    * Winner - enum representing all winners: North, South, Draw
    * State - abstract State class (snapshot of current game state)
    * StateTwoPlayersStandardRules - concrete subclass of State implementing a specific variant

This module exports the following functions:
    * get_state - factory function, returns an initialized subclass of State
    * run_games - [TODO]
"""
# TODO: add docstrings

from abc import ABC, abstractmethod
from enum import Enum
import json
import random
from typing import Dict, List, Optional, Tuple

from libbisca.agent import Agent
from libbisca.card import Card, Deck, get_card, get_cards

Hand = List[Card]


class Player(Enum):
    # TODO: add docstring

    NORTH = -1
    SOUTH = 1

    @property
    def opponent(self) -> "Player":
        return Player.NORTH if self == Player.SOUTH else Player.SOUTH

    # TODO: opponent -> next (for more than 2 players)? hmmm


class Winner(Enum):
    NORTH = -1
    DRAW = 0
    SOUTH = 1


class State(ABC):
    def __init__(self, hand_size: int, eldest: Player = Player.SOUTH, state=None):
        # TODO: add typing?
        # TODO: add docstring, etc -- state -- for load_state_from_json (None on not load)

        self.hand_size: int = hand_size
        self.turn: Player = eldest

        self.stock = self.trump = self.hands = self.piles = self.scores = self.table = None

        self._init_state() if state is None else self._load_state(state)

    def __eq__(self, other: "State"):
        return (
            self.hand_size == other.hand_size
            and self.turn == other.turn
            and self.stock == other.stock
            and self.trump == other.trump
            and self.hands == other.hands
            and self.piles == other.piles
            and self.scores == other.scores
            and self.table == other.table
        )

    def __repr__(self):
        # TODO: need refactoring
        return f"{self.hand_size} {self.turn} {self.stock} {self.trump} {self.hands} {self.piles} {self.scores} " \
               f"{self.table}"

    @staticmethod
    @abstractmethod
    def load_from_json(fpath: str) -> "State":
        raise NotImplementedError

    # TODO: save to json

    def is_endgame(self) -> bool:
        return len(self.stock) + len(self.hands[Player.NORTH]) + len(self.hands[Player.SOUTH]) == 0

    @property
    @abstractmethod
    def legal_moves(self) -> List[Card]:
        raise NotImplementedError

    @abstractmethod
    def get_winner(self) -> Winner:
        raise NotImplementedError

    @abstractmethod
    def play(self, move: Card) -> None:
        # basic "take from hand and put in table"

        self.hands[self.turn].remove(move)
        # self._cards_in_stock_and_hands -= 1

        self.table.append(move)
        # self._table_played.append(self.turn)

    # TODO: need to rework this
    def do_random_move(self):  # TODO: check ret (play ret + move)
        # WARNING: ok, this is experimental -- TEST
        move = random.choice(self.legal_moves)
        result = self.play(move)
        return move, result

    # TODO: need to rework this -- this is random rollout, there are others...
    def do_random_rollout(
        self
    ):  # , move: Card):     # -> None:  / do_rollout -- add Agents?
        # WARNING: experimental ->
        while not self.is_endgame():
            # move, _ = self.do_random_move()
            self.do_random_move()
        # TODO: return results

    def _init_state(self):
        self.stock: Deck = Deck()
        self.trump: Card = self.stock[0]

        self.hands: Dict[Player, Hand] = {player: [] for player in Player}

        # WARNING: self.piles doesn't seem necessary, but...
        self.piles: Dict[Player, List[Tuple[Card]]] = {player: [] for player in Player}
        self.scores: Dict[Player, int] = {player: 0 for player in Player}

        self.table: Hand = []

        # deal cards to players
        for _ in range(self.hand_size):
            self._deal()

    def _load_state(self, state):
        stock, trump, hands, piles, scores, table = state

        self.stock = stock
        self.trump = trump
        self.hands = hands
        self.piles = piles
        self.scores = scores
        self.table = table

    def _deal(self) -> List[Card]:
        dealt = []
        for player in (self.turn, self.turn.opponent):
            card = self.stock.pop()
            self.hands[player].append(card)
            dealt.append(card)
        # winner, loser
        return dealt

    @staticmethod
    def _decode_state(dct) -> Tuple[int, Player, Tuple]:   # incomplete typing
        # WARNING: not sure I like this usage of "super", but...
        hand_size, turn, stock, trump, hands, piles, scores, table = \
            [dct[k] for k in "hand_size, turn, stock, trump, hands, piles, scores, table".split(", ")]

        # TODO: check PyCharm warnings
        turn = Player.NORTH if turn == "North" else Player.SOUTH
        stock = get_cards(stock)
        trump = get_card(trump)
        hands = {p: get_cards(l) for p, l in zip(Player, hands)}
        piles = {p: [get_cards(s) for s in t] for p, t in zip(Player, piles)}
        scores = {p: i for p, i in zip(Player, scores)}
        table = get_cards(table)

        return hand_size, turn, (stock, trump, hands, piles, scores, table)


class StateTwoPlayersStandardRules(State):
    # TODO: recheck game rules
    # TODO: may modify to allow more players or just create other class

    # TODO: needs refactoring... (and maybe separation to State)
    @staticmethod
    def _decode_state(dct):
        if "__StateTwoPlayersStandardRules__" in dct:
            # WARNING: not sure I like this usage of "super", but...
            return State._decode_state(dct)
        else:
            raise TypeError(dct)  # TODO: improve this

    @staticmethod
    def load_from_json(fpath: str) -> "StateTwoPlayersStandardRules":
        with open(fpath) as fp:
            hand_size, eldest, state = json.load(fp, object_hook=StateTwoPlayersStandardRules._decode_state)
            return StateTwoPlayersStandardRules(hand_size=hand_size, eldest=eldest, state=state)

    # TODO: improve typing
    def play(
        self, move: Card
    ) -> Optional[Tuple[Player, int, List[Card], Optional[List[Card]]]]:
        super().play(move)

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
            self.piles[winner].append(table)

            dealt = self._deal() if self.stock else None

            # winner, added_score, [eldest, youngest], [winner, loser] - TODO: all needed?
            return winner, added_score, table, dealt

    # TODO: test this
    def _get_round_winner(self) -> Player:
        card1, card2 = self.table
        youngest = self.turn
        eldest = youngest.opponent

        # follow is not mandatory, but if youngest plays a different suit than is not trump, eldest wins
        if card1.suit != card2.suit:
            if card2.suit == self.trump.suit:   ##if card2.is_trump():
                return youngest
            return eldest

        # default
        return eldest if card1 > card2 else youngest

    # -----

    @property
    def legal_moves(self) -> List[Card]:
        # in standard rules there is not restriction to which card can be played
        return self.hands[self.turn]

    def get_winner(self) -> Winner:
        pass


def get_state(
    variant="StandardRules", num_players=2, hand_size=3, eldest=Player.SOUTH
) -> State:
    # WARNING: experimental ->
    if variant == "StandardRules" and num_players == 2 and hand_size == 3:
        return StateTwoPlayersStandardRules(hand_size=hand_size, eldest=eldest)
    else:
        raise NotImplementedError


# TODO: need to rework this
def run_games(
    variant="StandardRules",
    num_players=2,
    hand_size=3,
    eldest=Player.SOUTH,
    num_games=100,
    players: List[Agent] = None,
):
    # this is useful to test ai, etc.
    # TODO: -> results
    # WARNING: experimental ->
    for _ in range(num_games):
        state = get_state(variant, num_players, hand_size, eldest)
        state.do_random_rollout()
    # TODO: aggregate results


"""
    #@abstractmethod
    #def get_score(self, player) -> int:
        #raise NotImplementedError

#def get_state(variant_name: str, eldest: Player = Player.SOUTH) -> State:
#def get_state(variant="StandardRules", num_players=2, hand_size=3, eldest=Player.South)

* Variant - enum representing currently implemented variants

# TODO: explain Variant can have multiple sub-variants (same ruleset, 3cards, 9cards, etc.) -- research this
Variant = Enum("Variant", "BISCA3")  # BISCA7 BISCA9")   TODO: check PyCharm variant
"""

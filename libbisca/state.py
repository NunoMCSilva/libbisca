# -*- coding: utf-8 -*-

"""Bisca State

Implements the rules for Bisca.

This module exports the following classes:
    * State - abstract State class (snapshot of current game state)
    * StateStandardRules(State) - concrete subclass of State implementing a specific variant
    * Player - enum representing all players: North, South
    * PlayerState - dataclass containing Player data (hand, pile, score) used in State

This module exports the following functions:
    * get_state - factory function, returns an initialized subclass of State
    * load_state - loads state from json
"""
# TODO: improve docstrings (and add missing)

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import json
import random
from typing import Dict, List, Optional, Tuple

from libbisca.card import Card, Deck, get_card, get_cards

Hand = List[Card]
PlayResult = Tuple["Player", int, Hand, Optional[Hand]]     # winner, added_score, table, dealt_cards


class Player(Enum):
    # this is because in a future ui, South is the player's side
    NORTH = -1
    SOUTH = 1

    @property
    def opponent(self) -> "Player":
        return Player.NORTH if self == Player.SOUTH else Player.SOUTH


@dataclass
class PlayerState:
    hand: Hand = field(default_factory=list)
    pile: List[Hand] = field(default_factory=list)
    score: int = 0


class State(ABC):
    # two players ONLY

    def __init__(self, hand_size: int, eldest: Player, is_load: bool = False):
        self.hand_size = hand_size
        self.turn = eldest

        # TODO: add an else?
        if not is_load:
            self.stock: Deck = Deck()
            self.trump: Card = self.stock[0]

            self.players: Dict[Player, PlayerState] = {
                player: PlayerState() for player in Player
            }
            self.table: Hand = []

            # deal cards to players
            for _ in range(self.hand_size):
                self._deal()

    def __eq__(self, other):
        return (
            self.hand_size == other.hand_size
            and self.turn == other.turn
            and self.stock == other.stock
            and self.trump == other.trump
            and self.players == other.players
            and self.table == other.table
        )

    def __repr__(self):
        return (
            f"{self.hand_size} "
            f"{self.turn} "
            f"{self.stock} "
            f"{self.trump} "
            f"{self.players} "
            f"{self.table}"
        )

    def do_random_move(self) -> Tuple[Card, Optional[PlayResult]]:
        # helpful for agents
        move = random.choice(self.legal_moves)
        return move, self.play(move)

    def do_random_rollout(self) -> None:
        while not self.is_endgame():
            self.do_random_move()
        # no need to return anything

    @property
    def legal_moves(self) -> List[Card]:
        # this allows player to play any card in hand, subclass if that is not so
        return self.players[self.turn].hand

    def get_winner(self) -> Optional[Player]:
        if self.is_endgame():
            assert self.players[Player.NORTH].score + self.players[Player.SOUTH].score == 120

            if self.players[Player.NORTH].score > self.players[Player.SOUTH].score:
                return Player.NORTH
            elif self.players[Player.NORTH].score < self.players[Player.SOUTH].score:
                return Player.SOUTH
            else:
                return None     # Draw
        else:
            raise ValueError("game is not in endgame")  # TODO: better exception and msg

    def is_endgame(self) -> bool:
        return len(self.stock) + len(self.players[Player.NORTH].hand) + len(self.players[Player.SOUTH].hand) == 0

    @abstractmethod
    def play(self, move: Card) -> Optional[PlayResult]:
        raise NotImplementedError

    def _deal(self) -> Hand:
        # return [new_winner_card, new_loser_card]
        dealt = []

        for player in (self.turn, self.turn.opponent):
            card = self.stock.pop()
            self.players[player].hand.append(card)
            dealt.append(card)

        return dealt


class StateStandardRules(State):
    # for now, it will only be tested for three cards
    # TODO: recheck rules

    def play(self, move: Card) -> Optional[PlayResult]:
        # return winner, added_score, [eldest, youngest], [winner, loser] or None - TODO: all needed?

        # basic "take from hand and put in table"
        self.players[self.turn].hand.remove(move)
        self.table.append(move)

        if len(self.table) == 1:
            # eldest played
            self.turn = self.turn.opponent
            return None
        else:
            # youngest played
            winner = self._get_round_winner()

            added_score = sum(card.score for card in self.table)
            self.players[winner].score += added_score

            table = self.table
            self.players[winner].pile.append(table)
            self.table = []

            self.turn = winner
            dealt = self._deal() if self.stock else None

            return winner, added_score, table, dealt

    # TODO: test this
    def _get_round_winner(self) -> Player:
        card1, card2 = self.table
        youngest = self.turn
        eldest = self.turn.opponent

        # follow is not mandatory, but if youngest plays a different suit than is not trump, eldest wins
        if card1.suit != card2.suit:
            if card2.suit == self.trump.suit:
                return youngest
            return eldest

        # default
        return eldest if card1 > card2 else youngest


def get_state(
    variant="StandardRules", hand_size: int = 3, eldest: Player = Player.SOUTH
) -> State:
    if variant == "StandardRules" and hand_size == 3:
        return StateStandardRules(hand_size=hand_size, eldest=eldest)
    else:
        raise NotImplementedError


# TODO: save_state (save to json, needs _encode_state)


def load_state(fpath: str) -> State:
    # loads from json
    with open(fpath) as fp:
        return json.load(fp, object_hook=_decode_state)


def _decode_state(dct) -> State:
    if "__StateStandardRulesTwoPlayersThreeCards__" in dct:
        return _decode_state_aux(dct, StateStandardRules)
    else:
        raise TypeError(dct)  # TODO: improve this


def _decode_state_aux(dct, cls) -> State:
    # TODO: might be useful with a load state?

    hand_size = dct["hand_size"]
    turn = Player.NORTH if dct["turn"] == "North" else Player.SOUTH

    hands = dct["hands"]
    piles = dct["piles"]
    scores = dct["scores"]

    state = cls(hand_size=hand_size, eldest=turn, is_load=True)

    state.stock = get_cards(dct["stock"])
    state.trump = get_card(dct["trump"])

    state.players = {}
    # TODO: check this PyCharm warning
    for player, hand, pile, score in zip(list(Player), hands, piles, scores):
        state.players[player] = PlayerState(
            get_cards(hand), [get_cards(s) for s in pile], score
        )

    state.table = get_cards(dct["table"])

    return state

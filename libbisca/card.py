# -*- coding: utf-8 -*-

"""Card

Implements Bisca card related classes.

This module exports the following classes:
    * Rank - enum representing all ranks supported by Bisca cards: 23456QJK7A
    * Suit - enum representing all suits: Hearts, Diamonds, Spades, Clubs
    * Card - Bisca Card
    * Deck - list of Cards (subclass of list) initializing with a full deck

This module exports the following functions:
    * get_card -- helper factory function: returns Card
    * get_cards -- helper factory function: returns List[Card]
"""
# TODO: improve docstrings

from dataclasses import dataclass
from enum import Enum
from random import SystemRandom
from typing import List, Union


class Rank(Enum):
    # actual sort order
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    QUEEN = "Q"
    JACK = "J"
    KING = "K"
    SEVEN = "7"
    ACE = "A"


class Suit(Enum):
    HEARTS = "H"
    DIAMONDS = "D"
    SPADES = "S"
    CLUBS = "C"


@dataclass(unsafe_hash=True)  # WARNING: for now, this is only useful for testing
class Card:
    # TODO: add docstrings

    rank: Rank
    suit: Suit

    # WARNING: experimental -->
    _SCORE = {
        Rank.QUEEN: 2,
        Rank.JACK: 3,
        Rank.KING: 4,
        Rank.SEVEN: 10,
        Rank.ACE: 11,
    }  # all other cards are worth 0 points
    _RANK_STR_TO_RANK = {rank.value: rank for rank in Rank}
    _SUIT_STR_TO_SUIT = {suit.value: suit for suit in Suit}
    # WARNING: experimental <--

    def __gt__(self, other: "Card"):
        # only gt is implemented, state doesn't need the others
        # this compares card strength ONLY, other issues are the state's responsibility (e.g. trump)
        # TODO: this is a fast patch to a discovered bug -- added to test, need to do a better implementation
        return "23456QJK7A".index(self.rank.value) > "23456QJK7A".index(
            other.rank.value
        )
        # return self.rank.value > other.rank.value

    def __repr__(self):
        # this should be in __str__ but I prefer to see this when I print a list of cards
        # "Although practicality beats purity." -- The Zen of Python
        return f"{self.rank.value}{self.suit.value}"

    @property
    def score(self) -> int:
        return Card._SCORE.get(self.rank, 0)


class Deck(list):
    def __init__(self, shuffle=True):
        # WARNING: experimental -->
        # factory method?
        # not shuffled deck is ordered by sort order not original deck order
        # considered not an issues, since un-shuffled is only for tests
        ranks = [
            Rank.ACE,
            Rank.TWO,
            Rank.THREE,
            Rank.FOUR,
            Rank.FIVE,
            Rank.SIX,
            Rank.SEVEN,
            Rank.QUEEN,
            Rank.JACK,
            Rank.KING,
        ]  # put this order in rank? call it deck order?
        super().__init__(Card(rank, suit) for suit in Suit for rank in ranks)

        if shuffle:
            self._shuffle()

        # return typing.cast(Deck, deck)  # typing hint, does nothing to code
        # WARNING: experimental <--

    def _shuffle(self) -> None:
        # WARNING: experimental -->
        # SystemRandom is necessary to generate all of the 40! possibilities
        SystemRandom().shuffle(self)
        # possible alternative with less issues, need to research deck = random.sample(deck, len(deck))
        # WARNING: experimental <--


# TODO: put these two in Card class?
# TODO: optimization to access "singleton" cards?
def get_card(card: str) -> Card:
    # TODO: might need some refactoring
    rank_str, suit_str = card

    rank = Card._RANK_STR_TO_RANK[rank_str]
    suit = Card._SUIT_STR_TO_SUIT[suit_str]

    return Card(rank, suit)


def get_cards(cards: str) -> List[Card]:
    # helper function, useful for testing
    # TODO: might need some refactoring
    # TODO: add docstrings: receives "2H" and returns [Card(2H)]
    # TODO: add docstrings: receives "2H 7C" and returns [Card(2H), Card(7C)

    return [] if cards == "" else [get_card(s) for s in cards.split(" ")]

"""Card

Implements Bisca card related classes.

This module exports the following classes:
    * Rank - enum representing all ranks supported by Bisca cards: 23456QJK7A
    * Suit - enum representing all suits: Hearts, Diamonds, Spades, Clubs
    * Card - Bisca Card

# TODO: check how to document new type Deck
"""

from dataclasses import dataclass
from enum import Enum

# WARNING: experimental -->
# import random
from random import SystemRandom
import typing
from typing import List, NewType

Deck = NewType("Deck", List["Card"])
# WARNING: <-- experimental


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


@dataclass(unsafe_hash=True)  # only useful for testing for now
class Card:
    # TODO: add docstrings

    rank: Rank
    suit: Suit

    _SCORE = {
        Rank.QUEEN: 2,
        Rank.JACK: 3,
        Rank.KING: 4,
        Rank.SEVEN: 10,
        Rank.ACE: 11,
    }  # all other cards are worth 0 points
    _RANK_STR_TO_RANK = {rank.value: rank for rank in Rank}
    _SUIT_STR_TO_SUIT = {suit.value: suit for suit in Suit}

    def __gt__(self, other: "Card"):
        # only gt is implemented, state doesn't need the others
        # this compares card strength ONLY, other issues are the state's responsibility (e.g. trump)
        return self.rank.value > other.rank.value

    def __repr__(self):
        # this should be in __str__ but I prefer to see this when I print a list of cards
        # "Although practicality beats purity." -- The Zen of Python
        return f"{self.rank.value}{self.suit.value}"

    @property
    def score(self) -> int:
        return Card._SCORE.get(self.rank, 0)

    @staticmethod
    def get_card(card_str: str) -> "Card":
        # factory method -- mostly for testing
        rank_str, suit_str = card_str

        rank = Card._RANK_STR_TO_RANK[rank_str]
        suit = Card._SUIT_STR_TO_SUIT[suit_str]

        return Card(rank, suit)

    @staticmethod
    def get_deck(shuffle=True) -> Deck:
        # WARNING: experimental -->
        # not shuffled deck is ordered by sort order not original deck order
        # considered not an issues, since unshuffle is only fo rtests
        deck = [Card(rank, suit) for suit in Suit for rank in Rank]

        if shuffle:
            # SystemRandom is necessary to generate all of the 40! possibilities
            SystemRandom().shuffle(deck)
            # possible alternative with less issues, need to research deck = random.sample(deck, len(deck))

        return typing.cast(Deck, deck)  # typing hint, does nothing to code
        # WARNING: experimental <--

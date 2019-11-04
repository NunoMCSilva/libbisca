"""Card

Implements Bisca card related classes.
# TODO: improve docstrings
This module exports the following classes:
    * Rank - enum representing all ranks supported by Bisca cards: 23456QJK7A
    * Suit - enum representing all suits: Hearts, Diamonds, Spades, Clubs
    * Card - Bisca Card
    * Deck -- TODO: add

This module exports the following functions:
    * get_card -- TODO: add
    * get_cards -- TODO: add
"""

from dataclasses import dataclass
from enum import Enum
from random import SystemRandom
from typing import List


# WARNING: experimental -->
import typing

# from typing import NewType# TODO: check how to document new type Deck

# Deck = NewType("Deck", List["Card"])
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


@dataclass(unsafe_hash=True)  # for now, this is only useful for testing
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
        return self.rank.value > other.rank.value

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
            self.shuffle()

        # return typing.cast(Deck, deck)  # typing hint, does nothing to code
        # WARNING: experimental <--

    def shuffle(self) -> None:
        # WARNING: experimental <--
        # SystemRandom is necessary to generate all of the 40! possibilities
        SystemRandom().shuffle(self)
        # possible alternative with less issues, need to research deck = random.sample(deck, len(deck))


def get_card(card_str: str) -> Card:
    # factory method -- mostly for testing
    rank_str, suit_str = card_str

    rank = Card._RANK_STR_TO_RANK[rank_str]
    suit = Card._SUIT_STR_TO_SUIT[suit_str]

    return Card(rank, suit)


def get_cards(cards: str) -> List[Card]:
    # helper function, useful for testing
    # TODO: add docstrings: receives "2H 7C" and returns [Card(2H), Card(7C)
    return [get_card(s) for s in cards.split(" ")]

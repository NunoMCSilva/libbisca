# TODO: add docstrings

from dataclasses import dataclass
from enum import Enum
from random import SystemRandom
from typing import List

RANK_ORDER = "23456QJK7A"
RANK_SCORE = {
    "Q": 2,
    "J": 3,
    "K": 4,
    "7": 10,
    "A": 11,
}  # all other ranks are worth 0 points


# TODO: check about how to add RANK_ORDER and RANK_SCORE to Enum instead of it being outside
class Rank(Enum):
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    QUEEN = "Q"
    JACK = "J"
    KING = "K"

    def __gt__(self, other: "Rank"):
        return RANK_ORDER.index(self.value) > RANK_ORDER.index(other.value)

    @property
    def score(self) -> int:
        return RANK_SCORE.get(self.value, 0)


class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    SPADES = "♠"
    CLUBS = "♣"


@dataclass
class Card:
    rank: Rank
    suit: Suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __gt__(self, other: "Card"):
        # only gt is implemented, others aren't necessary
        return False if other.is_trump() else self.rank > other.rank

    def __repr__(self):
        # "Although practicality beats purity." -- The Zen of Python
        return f"{self.rank.value}{self.suit.value}"

    @property
    def score(self) -> int:
        return self.rank.score

    @staticmethod
    def get_deck(shuffle: bool = True) -> List["Card"]:
        # TODO: put deck at module level to save memory?
        deck = [Card(rank, suit) for suit in Suit for rank in Rank]

        if shuffle:
            # SystemRandom is necessary to generate all of the 40! possibilities
            SystemRandom().shuffle(deck)

        return deck

    def get_trumped(self) -> "TrumpCard":
        return TrumpCard(self.rank, self.suit)

    @staticmethod
    def is_trump() -> bool:
        return False


class TrumpCard(Card):
    TRUMP_SUIT_STR = {
        Suit.HEARTS: "♡",
        Suit.DIAMONDS: "♢",
        Suit.SPADES: "♤",
        Suit.CLUBS: "♧",
    }

    def __gt__(self, other: "Card"):
        return self.rank > other.rank if other.is_trump() else True

    def __repr__(self):
        # "Although practicality beats purity." -- The Zen of Python
        return f"{self.rank.value}{TrumpCard.TRUMP_SUIT_STR[self.suit]}"

    def get_trumped(self) -> "TrumpCard":
        raise NotImplementedError

    @staticmethod
    def is_trump() -> bool:
        return True

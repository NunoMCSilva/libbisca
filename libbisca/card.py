# TODO: add docstrings

from dataclasses import dataclass
from enum import Enum
from typing import List, NewType

Deck = NewType("Deck", List["Card"])


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


@dataclass
class Card:
    rank: Rank
    suit: Suit

    _SCORE = {Rank.QUEEN: 2, Rank.JACK: 3, Rank.KING: 4, Rank.SEVEN: 10, Rank.ACE: 11}
    _RANK_STR_TO_RANK = {rank.value: rank for rank in Rank}
    _SUIT_STR_TO_SUIT = {suit.value: suit for suit in Suit}

    def __gt__(self, other: "Card"):
        # only gt is implemented, state doesn't need the others
        # this compares card strength ONLY, other issues are the state's responsibility (e.g. trump)
        return self.rank.value > other.rank.value

    def __repr__(self):
        return f"{self.rank.value}{self.suit.value}"

    @property
    def score(self) -> int:
        return Card._SCORE.get(self.rank, 0)

    @staticmethod
    def get_card(card_str: str) -> "Card":
        rank_str, suit_str = card_str

        rank = Card._RANK_STR_TO_RANK[rank_str]
        suit = Card._SUIT_STR_TO_SUIT[suit_str]

        return Card(rank, suit)

    @staticmethod
    def get_deck(shuffled=True) -> Deck:
        pass

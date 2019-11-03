# TODO: add docstrings

from dataclasses import dataclass
from enum import Enum


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

    def __gt__(self, other: "Card"):
        # only gt is implemented, state doesn't need the others
        # this compares card strength ONLY, other issues are the state's responsibility (e.g. trump)
        return self.rank.value > other.rank.value

    def __repr__(self):
        return f"{self.rank.value}{self.suit.value}"

    @property
    def score(self) -> int:
        scores = {
            k: v for k, v in zip(Rank, 5 * [0] + [2, 3, 4, 10, 11])
        }  # put elsewhere
        return scores[self.rank]


def get_card(card_str: str) -> Card:
    # put at module level or just generate _STR_TO_CARDS
    ranks = {rank.value: rank for rank in Rank}
    suits = {suit.value: suit for suit in Suit}

    rank, suit = card_str
    return Card(ranks[rank], suits[suit])

# TODO: add docstrings
# TODO: decide which methods/etc are better as _"private"

from dataclasses import dataclass
from enum import Enum
from random import SystemRandom
from typing import List


# Rank =================================================================================================================
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
        # TODO: ok, this might be improved...
        return self._ORDER.index(self.value) > self._ORDER.index(other.value)

    @property
    def score(self) -> int:
        return self._SCORE.get(self.value, 0)


Rank._ORDER = "23456QJK7A"
Rank._SCORE = {"Q": 2, "J": 3, "K": 4, "7": 10, "A": 11}


# Suit =================================================================================================================
class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    SPADES = "♠"
    CLUBS = "♣"

    # TODO: add Trump Suit here as method?


# Card =================================================================================================================
@dataclass
class Card:
    rank: Rank
    suit: Suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __gt__(self, other: "Card"):
        # only gt is implemented, the others aren't really necessary
        return False if other.is_trump() else self.rank > other.rank

    def __repr__(self):
        #  This should be in __str__ but I want to print a list of cards and seen this -- TODO: improve this comment
        # "Although practicality beats purity." -- The Zen of Python
        return f"{self.rank.value}{self.suit.value}"

    @property
    def score(self) -> int:
        return self.rank.score

    @staticmethod
    def get_card(card_str: str) -> "Card":
        # TODO: needs refactoring
        # this is mostly for testing -- can use _DECK later (remember to save memory and maybe be faster)
        rank, suit = card_str
        rank = {
            "A": Rank.ACE,
            "2": Rank.TWO,
            "3": Rank.THREE,
            "4": Rank.FOUR,
            "5": Rank.FIVE,
            "6": Rank.SIX,
            "7": Rank.SEVEN,
            "Q": Rank.QUEEN,
            "J": Rank.JACK,
            "K": Rank.KING,
        }[rank]
        suit = {
            "H": Suit.HEARTS,
            "D": Suit.DIAMONDS,
            "S": Suit.SPADES,
            "C": Suit.CLUBS,
        }[suit]
        return Card(rank, suit)

    @staticmethod
    def is_trump() -> bool:
        return False


# TrumpCard ============================================================================================================
class TrumpCard(Card):
    # TODO: this might be better implemented in something TrumpSuit or...?
    TRUMP_SUIT_STR = {
        Suit.HEARTS: "♡",
        Suit.DIAMONDS: "♢",
        Suit.SPADES: "♤",
        Suit.CLUBS: "♧",
    }

    def __gt__(self, other: "Card"):
        return self.rank > other.rank if other.is_trump() else True

    def __repr__(self):
        #  This should be in __str__ but I want to print a list of cards and seen this -- TODO: improve this
        # "Although practicality beats purity." -- The Zen of Python
        return f"{self.rank.value}{TrumpCard.TRUMP_SUIT_STR[self.suit]}"

    @staticmethod
    def is_trump() -> bool:
        return True


# Deck =================================================================================================================
class Deck:
    def __init__(self, shuffle=True):
        # TODO: replace by module level _DECK (memory saves) and do copy or something? [or change __deepcopy__ in Card?]
        deck = [Card(rank, suit) for suit in Suit for rank in Rank]

        if shuffle:
            # SystemRandom is necessary to generate all of the 40! possibilities
            SystemRandom().shuffle(deck)

        # set trumps
        self.deck = [
            (TrumpCard(card.rank, card.suit) if card.suit == deck[0].suit else card)
            for card in deck
        ]

    def __str__(self):
        return str(self.deck)

    @property
    def bottom(self) -> Card:
        return self.deck[0]

    def pop(self) -> Card:
        return self.deck.pop()

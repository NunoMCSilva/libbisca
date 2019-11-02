"""Card

Implements Bisca card related classes.

This module exports the following classes:
    * Rank - enum representing all ranks supported by Bisca cards (Bisca doesn't support 8s, 9s, and 10s)
    * Suit - enum representing all suits (Hearts, Diamonds, Spades, Clubs)
    * Card - Bisca Card
    * TrumpCard - Bisca Card marked as being a trump
    * Deck - a game deck (a list of cards)
"""

from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from random import SystemRandom


# Rank =================================================================================================================
class Rank(IntEnum):
    # sort order of ranks (which is greater)
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    QUEEN = auto()
    JACK = auto()
    KING = auto()
    SEVEN = auto()
    ACE = auto()

    # TODO: recheck this, but right now it seems ok -- format used by f-strings
    def __format__(self, format_spec):
        # TODO: check format_spec
        return str(self)

    def __str__(self):
        # TODO: any use to put "23... in a _STR class constant?
        return "23456QJK7A"[self.value - 1]

    @staticmethod
    def get_rank(rank_str):
        return Rank._STR_TO_RANK[rank_str]  # TODO: check this PyCharm warning


# there are better solutions to putting constants in enums, but this one if good enough for now
Rank._STR_TO_RANK = {
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
}
Rank.DECK_ORDER = (
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
)

# Suit =================================================================================================================
class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    SPADES = "♠"
    CLUBS = "♣"

    def __format__(self, format_spec):
        # TODO: check format_spec
        return self.value

    def __str__(self):
        return self.value

    @property
    def trumped(self):
        return self._TRUMPED[self]

    @staticmethod
    def get_suit(suit_str):
        return Suit._STR_TO_SUIT[suit_str]  # TODO: check this PyCharm warning


Suit._TRUMPED = {
    Suit.HEARTS: "♡",
    Suit.DIAMONDS: "♢",
    Suit.SPADES: "♤",
    Suit.CLUBS: "♧",
}
Suit._STR_TO_SUIT = {
    "H": Suit.HEARTS,
    "D": Suit.DIAMONDS,
    "S": Suit.SPADES,
    "C": Suit.CLUBS,
}

# Card =================================================================================================================
@dataclass
class Card:
    # all cards not in _SCORE are worth 0 points
    _SCORE = {Rank.QUEEN: 2, Rank.JACK: 3, Rank.KING: 4, Rank.SEVEN: 10, Rank.ACE: 11}

    rank: Rank
    suit: Suit

    def __gt__(self, other: "Card"):
        # only gt is implemented, the others aren't really necessary
        # this compares card strength only, other issues are the state's responsibility
        if other.is_trump():
            # if other is trump, then self > other is ALWAYS False
            return False
        else:
            return self.rank > other.rank

    def __repr__(self):
        # this should be in __str__ but I prefer to see this when I print a list of cards
        # "Although practicality beats purity." -- The Zen of Python
        return f"{self.rank}{self.suit}"

    @property
    def score(self) -> int:
        # should probably be in rank, but with it here I save a call to self.rank.score...
        return Card._SCORE.get(self.rank, 0)

    def trumpify(self) -> "TrumpCard":
        return TrumpCard(self.rank, self.suit)

    @staticmethod
    def is_trump() -> bool:
        return False


# TrumpCard ============================================================================================================
class TrumpCard(Card):
    # simplifies card comparision without the need to modify each card to set trump (and it looks good on print)

    def __gt__(self, other: "Card"):
        # only gt is implemented, the others aren't really necessary
        # this compares card strength only, other issues are the state's responsibility
        if other.is_trump():
            return self.rank > other.rank
        else:
            # self(t) > other, always
            return True

    def __repr__(self):
        # this should be in __str__ but I prefer to see this when I print a list of cards
        # "Although practicality beats purity." -- The Zen of Python
        return f"{self.rank}{self.suit.trumped}"

    @staticmethod
    def is_trump() -> bool:
        return True


# Deck =================================================================================================================
class Deck(list):
    def __init__(self, shuffle=True):
        deck = [Card(rank, suit) for suit in Suit for rank in Rank.DECK_ORDER]

        # shuffle
        if shuffle:
            # SystemRandom is necessary to generate all of the 40! possibilities
            SystemRandom().shuffle(deck)

        # signal trumps -- TODO: make this more elegant
        def func(card: Card) -> Card:
            if card.suit != deck[0].suit:
                return card
            else:
                return card.trumpify()

        super().__init__(map(func, deck))

    @property
    def bottom(self) -> Card:
        # bottom of deck
        return self[0]

    def take_top(self) -> Card:
        # take card from top of deck
        return self.pop()


# functions ============================================================================================================
def get_card(card_str: str) -> Card:
    # mostly for testing purposes - get_card("2H") is easier to type than Card(Rank.TWO, Suit.HEARTS)

    card_cls = Card
    if "(t)" in card_str:
        card_cls = TrumpCard
        card_str = card_str[0:2]

    rank, suit = card_str
    return card_cls(
        Rank.get_rank(rank), Suit.get_suit(suit)
    )  # TODO: check this PyCharm warning

# TODO: add docstrings

import pytest

from libbisca.card import *


# TODO: check black's change to this comments formatting... don't really like it
# Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior]
@pytest.mark.parametrize(
    "card1, card2, expected",
    [
        # same type, same suit: compare rank ---------------------------------------------------------------------------

        # AH > 7H
        (Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.HEARTS), True),
        (TrumpCard(Rank.ACE, Suit.HEARTS), TrumpCard(Rank.SEVEN, Suit.HEARTS), True),

        # 5C < 7C
        (Card(Rank.FIVE, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), False),
        (TrumpCard(Rank.FIVE, Suit.CLUBS), TrumpCard(Rank.SEVEN, Suit.CLUBS), False),

        # same type, different suits: compare rank -- in this libbisca variant -----------------------------------------
        # TODO: check about other libbisca variants (at least one mandates follow after stock is empty)

        # AC > 7H
        (Card(Rank.ACE, Suit.CLUBS), Card(Rank.SEVEN, Suit.HEARTS), True),
        (TrumpCard(Rank.ACE, Suit.CLUBS), TrumpCard(Rank.SEVEN, Suit.HEARTS), True),

        # 5D < 7C
        (Card(Rank.FIVE, Suit.DIAMONDS), Card(Rank.SEVEN, Suit.CLUBS), False),
        (TrumpCard(Rank.FIVE, Suit.DIAMONDS), TrumpCard(Rank.SEVEN, Suit.CLUBS), False),

        # different type -----------------------------------------------------------------------------------------------
        # 2D(t) > 7C
        (TrumpCard(Rank.TWO, Suit.DIAMONDS), Card(Rank.SEVEN, Suit.CLUBS), True),

        # 3D < 2S(t)
        (Card(Rank.THREE, Suit.DIAMONDS), TrumpCard(Rank.TWO, Suit.SPADES), False),
    ],
)
def test__card_and_trump_card_gt__two_cards__return_expected(card1, card2, expected):
    # act & assert
    assert (card1 > card2) is expected


def test__deck_init__shuffle_false__return_expected():
    # arrange
    expected = (
        "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, 4♠, 5♠,"
        " 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣, 3♣, 4♣, 5♣, 6♣, 7♣, Q♣, J♣, K♣]"
    )

    # act
    deck = Deck(shuffle=False)

    # assert
    assert str(deck) == expected

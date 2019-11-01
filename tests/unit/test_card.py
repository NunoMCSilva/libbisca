import pytest

from libbisca.card import *


# TODO: check black's change to this comments formatting... don't really like it here (too close to each other)
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
        # same type, different suits: compare rank
        # TODO: make clear this compares considering card order and is trump, other considerations (for other variants)
        # are the responsibility of state
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
    # Tests Card.__gt__ and Rank.__gt__

    # act & assert
    assert (card1 > card2) is expected


def test__deck_init__shuffle_false__return_expected():
    # Tests Deck.__init__(False) and Deck.__str__, Card.__repr__, Trump.__repr__, Rank.__str__, Suit.__str__

    # arrange
    expected = (
        "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, 4♠, 5♠,"
        " 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣, 3♣, 4♣, 5♣, 6♣, 7♣, Q♣, J♣, K♣]"
    )

    # act
    deck = Deck(shuffle=False)

    # assert
    assert str(deck) == expected


# TODO: consider which from the missing tests are useful to write:
# TODO: missing tests: Card.__hash__, Card.score (also Rank.score), Card.get_card, Card.is_trump, TrumpCard.is_trump
# TODO: missing tests: Deck.bottom, Deck.pop, Deck.__init__(True)

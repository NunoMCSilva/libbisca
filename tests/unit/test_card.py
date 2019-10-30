# TODO: add docstrings

import pytest

from libbisca.card import Card, Rank, Suit, TrumpCard


# TODO: check black's change to this comments formatting... don't really like it
# Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior]
@pytest.mark.parametrize(
    "card1, card2, expected",
    [
        # same type, same suit: compare rank
        # AH > 7H
        (Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.HEARTS), True),
        (TrumpCard(Rank.ACE, Suit.HEARTS), TrumpCard(Rank.SEVEN, Suit.HEARTS), True),
        # 5C < 7C
        (Card(Rank.FIVE, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), False),
        (TrumpCard(Rank.FIVE, Suit.CLUBS), TrumpCard(Rank.SEVEN, Suit.CLUBS), False),
        # same type, different suits: compare rank -- in this libbisca variant
        # TODO: check about other libbisca variants (at least one mandates follow after stock is empty)
        # AC > 7H
        (Card(Rank.ACE, Suit.CLUBS), Card(Rank.SEVEN, Suit.HEARTS), True),
        (TrumpCard(Rank.ACE, Suit.CLUBS), TrumpCard(Rank.SEVEN, Suit.HEARTS), True),
        # 5D < 7C
        (Card(Rank.FIVE, Suit.DIAMONDS), Card(Rank.SEVEN, Suit.CLUBS), False),
        (TrumpCard(Rank.FIVE, Suit.DIAMONDS), TrumpCard(Rank.SEVEN, Suit.CLUBS), False),
        # different type
        # 2D(t) > 7C
        (TrumpCard(Rank.TWO, Suit.DIAMONDS), Card(Rank.SEVEN, Suit.CLUBS), True),
        # 3D < 2S(t)
        (Card(Rank.THREE, Suit.DIAMONDS), TrumpCard(Rank.TWO, Suit.SPADES), False),
    ],
)
def test__card_and_trump_card_gt__two_cards__return_expected(card1, card2, expected):
    # act & assert
    assert (card1 > card2) is expected


def test__card_get_deck__shuffle_false__return_expected():
    # arrange
    expected = (
        "[A♥, 2♥, 3♥, 4♥, 5♥, 6♥, 7♥, Q♥, J♥, K♥, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, 4♠, 5♠,"
        " 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣, 3♣, 4♣, 5♣, 6♣, 7♣, Q♣, J♣, K♣]"
    )

    # act
    deck = Card.get_deck(shuffle=False)

    # assert
    assert str(deck) == expected


def test__card_get_trumped__any_card__returns_trump_card_version():
    # arrange
    card = Card(Rank.SEVEN, Suit.CLUBS)

    # act
    trump_card = card.get_trumped()

    # assert -- TODO: improve this
    assert isinstance(trump_card, TrumpCard)
    assert trump_card.is_trump()
    assert repr(trump_card) == "7♧"
    assert trump_card > card

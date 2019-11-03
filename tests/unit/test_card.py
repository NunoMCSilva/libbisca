import pytest

from libbisca.card import *

# using Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior] unittest naming


class TestCard:
    @pytest.mark.parametrize("cards", ["2H < 5H", "6C > 3C", "3S < 7S", "5H > 4C"])
    def test__lt__two_cards__returns_expected(self, cards):
        # arrange
        c1, comp, c2 = cards.split(" ")
        c1, c2 = [Card.get_card(c) for c in (c1, c2)]
        expected = True if comp == "<" else False

        # act & Assert
        assert (c1 < c2) is expected

    def test__repr__any_card__returns_expected(self):
        # mostly for my peace of mind

        # arrange
        card = Card(Rank.QUEEN, Suit.SPADES)

        # act & assert
        assert repr(card) == "QS"

    def test__score__any_card__returns_expected(self):
        # arrange
        card = Card(Rank.QUEEN, Suit.SPADES)

        # act & assert
        assert card.score == 2

    def test__get_card__any_card_str__returns_expected(self):
        # arrange
        card = Card(Rank.QUEEN, Suit.SPADES)

        # act & assert
        assert Card.get_card("QS") == card

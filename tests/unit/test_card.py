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

    @pytest.mark.parametrize(
        "card_str, score", [("7S", 10), ("QH", 2), ("2C", 0), ("5D", 0)]
    )
    def test__score__any_card__returns_expected(self, card_str, score):
        # arrange
        card = Card.get_card(card_str)

        # act & assert
        assert card.score == score

    def test__get_card__any_card_str__returns_expected(self):
        # arrange
        card = Card(Rank.QUEEN, Suit.SPADES)

        # act & assert
        assert Card.get_card("QS") == card

    def test__get_deck__not_shuffled__returns_expected(self):
        # arrange
        deck = (
            "2H 3H 4H 5H 6H QH JH KH 7H AH 2D 3D 4D 5D 6D QD JD KD 7D AD 2S 3S 4S 5S 6S QS JS KS 7S AS "
            "2C 3C 4C 5C 6C QC JC KC 7C AC"
        )
        expected = [Card.get_card(s) for s in deck.split(" ")]

        # act & assert
        assert Card.get_deck(shuffle=False) == expected

    def test__get_deck__shuffled__x(self):
        # arrange
        deck = (
            "2H 3H 4H 5H 6H QH JH KH 7H AH 2D 3D 4D 5D 6D QD JD KD 7D AD 2S 3S 4S 5S 6S QS JS KS 7S AS "
            "2C 3C 4C 5C 6C QC JC KC 7C AC"
        )
        expected = [Card.get_card(s) for s in deck.split(" ")]

        # act
        deck = Card.get_deck()

        # act & assert
        assert deck != expected
        assert set(deck) == set(
            expected
        )  # sorted is uncertain here - unimportant for now

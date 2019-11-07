# -*- coding: utf-8 -*-

import pytest

from libbisca.card import *

# using Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior] unittest naming


class TestCard:
    @pytest.mark.parametrize("cards", ["2H < 5H", "6C > 3C", "3S < 7S", "5H > 4C"])
    def test__gt__two_cards__returns_expected(self, cards):
        # arrange
        c1, op, c2 = cards.split(" ")
        c1, c2 = get_cards(cards.replace(op, "").replace("  ", " "))
        expected = (op == ">")

        # act & Assert
        assert (c1 > c2) is expected

    @pytest.mark.parametrize("card_str", ["QS", "KH", "2D"])
    def test__repr__any_card__returns_expected(self, card_str):
        # mostly for my peace of mind

        # arrange
        card = get_card(card_str)

        # act & assert
        assert isinstance(card, Card)  # again, peace of mind
        assert repr(card) == card_str

    @pytest.mark.parametrize(
        "card_str, score", [("7S", 10), ("QH", 2), ("2C", 0), ("5D", 0)]
    )
    def test__score__any_card__returns_expected(self, card_str, score):
        # arrange
        card = get_card(card_str)

        # act & assert
        assert card.score == score


class TestDeck:
    DECK_STR = (
        "AH 2H 3H 4H 5H 6H 7H QH JH KH AD 2D 3D 4D 5D 6D 7D QD JD KD "
        "AS 2S 3S 4S 5S 6S 7S QS JS KS AC 2C 3C 4C 5C 6C 7C QC JC KC"
    )
    DECK = get_cards(DECK_STR)  # list

    def test__init__not_shuffled__returns_expected(self):
        # act & assert
        assert Deck(shuffle=False) == TestDeck.DECK

    def test__init__shuffled__returns_expected(self):
        # act
        deck = Deck()

        # act & assert
        assert deck != TestDeck.DECK
        # I'd prefer sorted but result is unpredictable (ranks correct, suit random) - no point in worrying about this
        assert set(deck) == set(TestDeck.DECK)
        assert len(set(deck)) == len(deck)  # ok, now this is just paranoia


class TestGetCard:

    def test__any_card_str__returns_expected(self):
        # arrange
        card = Card(Rank.QUEEN, Suit.SPADES)
        card_str = "QS"

        # act & assert
        assert get_card(card_str) == card

    def test__any_cards_str__returns_expected(self):
        # arrange
        cards = [
            Card(Rank.QUEEN, Suit.SPADES),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.SEVEN, Suit.CLUBS),
        ]
        cards_str = "QS KH 7C"

        # act & assert
        assert get_cards(cards_str) == cards

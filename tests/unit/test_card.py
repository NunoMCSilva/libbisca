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
        expected = op == ">"

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
    def test__init__not_shuffled__returns_expected(self, deck):
        # act & assert
        assert Deck(shuffle=False) == deck

    def test__init__shuffled__returns_expected(self, deck):
        # act
        shuffled_deck = Deck()

        # act & assert
        assert shuffled_deck != deck
        # I'd prefer sorted but result is unpredictable (ranks correct, suit random) - no point in worrying about this
        assert set(shuffled_deck) == set(deck)
        assert len(set(shuffled_deck)) == len(deck)  # ok, now this is just paranoia


class TestGetCard:
    def test__any_card__str__returns_expected(self):
        # arrange
        card = Card(Rank.QUEEN, Suit.SPADES)
        card_str = "QS"

        # act & assert
        assert get_card(card_str) == card


class TestGetCards:
    @pytest.mark.parametrize("card_str, cards", [
        ("", []),
        ("QS", [
            Card(Rank.QUEEN, Suit.SPADES)
        ]),
        ("QS KH 7C", [
            Card(Rank.QUEEN, Suit.SPADES),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.SEVEN, Suit.CLUBS),
        ]),
    ])
    def test__any_card_str__returns_expected(self, card_str, cards):
        assert get_cards(card_str) == cards

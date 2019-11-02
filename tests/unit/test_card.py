import pytest

from libbisca.card import *

# using Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior] unittest naming


class TestRank:
    def test__check_order__return_expected(self):
        # this is more for my peace of mind than anything else
        # TODO: check PyCharm typing warning in next line
        assert (
            "".join(map(str, Rank)) == "".join(map(str, sorted(Rank))) == "23456QJK7A"
        )

    def test__gt__seven_gt_two__return_true(self):
        assert Rank.SEVEN > Rank.TWO

    def test__str_and_format__use_of_str_and_f_string__return_expected_char(self):
        assert str(Rank.SEVEN) == f"{Rank.SEVEN}" == "7"

    def test__get_rank__any_rank_str__returns_expected_rank(self):
        assert Rank.get_rank("Q") == Rank.QUEEN


class TestSuit:
    def test__str_and_format__use_of_str_and_f_string__return_expected_char(self):
        assert str(Suit.HEARTS) == f"{Suit.HEARTS}" == "♥"

    def test__trumped__any_suit__return_expected_char(self):
        assert Suit.HEARTS.trumped == "♡"

    def test__get_suit__any_suit_str__returns_expected_suit(self):
        assert Suit.get_suit("C") == Suit.CLUBS


class TestCard:
    def test__repr__any_card__return_expected_str(self):
        assert repr(Card(Rank.THREE, Suit.HEARTS)) == "3♥"

    @pytest.mark.parametrize(
        "card_str, score", [("7S", 10), ("QH", 2), ("2C", 0), ("5D", 0)]
    )
    def test__score__any_card__return_expected_value(self, card_str, score):
        assert get_card(card_str).score == score


class TestTrumpCard:
    def test__repr__any_card__return_expected_str(self):
        assert repr(TrumpCard(Rank.ACE, Suit.SPADES)) == "A♤"


class TestCardAndTrumpCard:
    @pytest.mark.parametrize(
        "card1, card2, expected",
        [
            # same type, same suit: compare rank
            ("AH", "7H", True),  # AH > 7H
            ("AH(t)", "7H(t)", True),  # AH(t) > 7H(t)
            ("5C", "7C", False),  # 5C < 7C
            ("5C(t)", "7C(t)", False),  # 5C(t) < 7C(t)
            # same type, different suits: still compare rank (the not following part is state's responsibility)
            ("AC", "7H", True),  # AC > 7H
            ("AC(t)", "7H(t)", True),  # AC(t) > 7H(t)
            ("6D", "7C", False),  # 6D < 7C
            ("6D(t)", "7C(t)", False),  # 6D(t) < 7C(t)
            # different type
            ("2D(t)", "7C", True),  # 2D(t) > 7C
            ("3D", "2S(t)", False),  # 3D < 2S(t)
        ],
    )
    def test__gt_two_cards__return_expected_bool(self, card1, card2, expected):
        # arrange
        c1 = get_card(card1)
        c2 = get_card(card2)

        # act & assert
        assert (c1 > c2) is expected


class TestDeck:
    def test__non_shuffled_deck__returns_expected_deck(self):
        # arrange
        expected = (
            "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, 4♠, 5♠,"
            " 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣, 3♣, 4♣, 5♣, 6♣, 7♣, Q♣, J♣, K♣]"
        )

        # act & assert
        assert str(Deck(shuffle=False)) == expected


class TestGetCard:
    def test__any_card_str__return_expected_card(self):
        assert get_card("JS") == Card(Rank.JACK, Suit.SPADES)

    def test__any_trump_card_str__return_expected_card(self):
        assert get_card("JS(t)") == TrumpCard(Rank.JACK, Suit.SPADES)

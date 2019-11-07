import pytest

from libbisca.card import Card, get_card, get_cards
from libbisca.state import *
from tests.unit.test_card import TestDeck

# using Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior] unittest naming


class TestStateBisca3:  # StateRuleSet1
    @staticmethod
    def _assert_state(state, expected):
        # TODO: needs better name

        # arrange
        class_, hand_size, trump, turn, stock, eldest_hand, youngest_hand, scores, table = (
            expected
        )

        # assert
        assert isinstance(state, class_)
        assert state.hand_size == hand_size
        assert state.trump == trump
        assert state.turn == turn
        assert state.stock == stock
        assert state.hands[turn] == eldest_hand
        assert state.hands[turn.opponent] == youngest_hand
        assert state.scores == scores
        assert state.table == table

    @pytest.mark.parametrize("eldest", list(Player))  # TODO: check this PyCharm warning
    def test__init__eldest_player_is_given__initializes_correctly(self, mocker, eldest):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        class_ = StateRuleSet1
        hand_size = 3
        trump = get_card("AH")
        turn = eldest
        stock = TestDeck.DECK[:34]  # AH to 4C
        eldest_hand = get_cards("KC QC 6C")
        youngest_hand = get_cards("JC 7C 5C")
        scores = {Player.NORTH: 0, Player.SOUTH: 0}
        table = []

        expected = (
            class_,
            hand_size,
            trump,
            turn,
            stock,
            eldest_hand,
            youngest_hand,
            scores,
            table,
        )

        # act
        state = get_state(Variant.BISCA3, eldest)

        # assert
        self._assert_state(state, expected)

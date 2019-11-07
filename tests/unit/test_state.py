import pytest

from libbisca.card import (
    Card,
    get_card,
    get_cards,
)  # TODO: check why PyCharm has this as unused statement?
from libbisca.state import *
from tests.unit.test_card import TestDeck

# using Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior] unittest naming


class TestStateBisca3:
    @staticmethod
    def _assert_state(
        state,
        eldest,
        expected_state,
        expected_hand_size,
        expected_turn,
        expected_stock,
        expected_trump,
        expected_eldest_hand,
        expected_youngest_hand,
        expected_scores,
        expected_table,
    ):
        # assert
        assert isinstance(state, expected_state)
        assert state.hand_size == expected_hand_size
        assert state.turn == expected_turn
        assert state.stock == expected_stock
        assert state.trump == expected_trump
        assert state.hands[eldest] == expected_eldest_hand
        assert state.hands[eldest.opponent] == expected_youngest_hand
        assert state.scores == expected_scores
        assert state.table == expected_table

    @pytest.mark.parametrize("eldest", list(Player))  # TODO: check this PyCharm warning
    def test__init__eldest_player_is_given__initializes_correctly(self, mocker, eldest):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        expected_state = StateRuleSet1
        expected_hand_size = 3
        expected_turn = eldest
        expected_stock = TestDeck.DECK[:34]  # AH to 4C
        expected_trump = get_card("AH")
        expected_eldest_hand = get_cards("KC QC 6C")
        expected_youngest_hand = get_cards("JC 7C 5C")
        expected_scores = {Player.NORTH: 0, Player.SOUTH: 0}
        expected_table = []

        # act
        state = get_state(Variant.BISCA3, eldest)

        # assert
        self._assert_state(
            state,
            eldest,
            expected_state,
            expected_hand_size,
            expected_turn,
            expected_stock,
            expected_trump,
            expected_eldest_hand,
            expected_youngest_hand,
            expected_scores,
            expected_table,
        )


"""
# add test for tate

    # result, stock, turn, trump, hands, table, winner, score
    # TODO: put this tests in fixtures? might be better?
    @pytest.mark.skip("until errors in test code are fixed")
    @pytest.mark.parametrize(
        "eldest, moves, play_results, hand_size, turn, stock, trump, eldest_hand, youngest_hand, scores, table",
        [
            # north player is eldest and plays KC
            (
                Player.NORTH,
                "KC",
                [None],
                3,
                Player.SOUTH,
                "AH 2H 3H 4H 5H 6H 7H QH JH KH AD 2D 3D 4D 5D 6D 7D QD JD KD AS 2S 3S 4S 5S 6S 7S QS JS KS AC 2C 3C 4C",
                "AH",
                "QC 6C",
                "JC 7C 5C",
                {Player.NORTH: 0, Player.SOUTH: 0},
                "KC",
            ),
            # north player is eldest and plays KC, south player answers with 7C
            (
                Player.NORTH,
                "KC",
                [
                    (Player.SOUTH, 14, "4C 3C")
                ],  # TODO: just returns eldest_card, youngest_card, easier
                3,
                Player.SOUTH,
                "AH 2H 3H 4H 5H 6H 7H QH JH KH AD 2D 3D 4D 5D 6D 7D QD JD KD AS 2S 3S 4S 5S 6S 7S QS JS KS AC 2C",
                "AH",
                "QC 6C 3C",
                "JC 5C 4C",
                {Player.NORTH: 0, Player.SOUTH: 14},
                "",
            ),
        ],
    )
    def test__play__after_given_moves__state_is_as_expected(
        self,
        mocker,
        eldest,
        moves,
        play_results,
        hand_size,
        turn,
        stock,
        trump,
        eldest_hand,
        youngest_hand,
        scores,
        table,
    ):
        # TODO: yup, needs lots of refactoring...

        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        moves = [
            Card.get_card(s) for s in moves.split(" ")
        ]  # TODO: add helper function that does this

        expected_play_results = [
            None
            if result is None
            else (
                result[0],
                result[1],
                [Card.get_card(s) for s in result[2].split(" ")],
            )  # winner, added_score, dealt_cards
            for result in play_results
        ]

        expected_stock = [Card.get_card(s) for s in stock.split(" ")]
        expected_eldest_hand = [Card.get_card(s) for s in eldest_hand.split(" ")]
        expected_youngest_hand = [Card.get_card(s) for s in youngest_hand.split(" ")]
        expected_table = (
            [Card.get_card(s) for s in table.split(" ")] if table != "" else []
        )  # TODO: recheck this

        expected_scores = scores
        expected_trump = Card.get_card(trump)
        expected_turn = turn

        state = get_state("Bisca3", eldest)

        # act
        play_results = []
        for move in moves:
            play_result = state.play(move)
            play_results.append(play_result)

        # assert
        assert state.hand_size == 3
        assert state.turn == expected_turn

        assert state.stock == expected_stock
        assert state.trump == expected_trump

        assert state.hands[eldest] == expected_eldest_hand
        assert state.hands[eldest.opponent] == expected_youngest_hand

        assert state.scores == expected_scores

        assert state.table == expected_table
"""

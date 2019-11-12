# -*- coding: utf-8 -*-

import pytest

from libbisca.state import *

# using Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior] unittest naming


class TestStateTwoPlayersStandardRulesThreeCards:
    def test__eq__two_equal_states__returns_correctly(self, mocker):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        state1 = get_state()
        state2 = get_state()

        # act & assert
        assert state1 == state2

    def test__eq__two_diff_states__returns_correctly(self, mocker):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        state1 = get_state()
        state2 = get_state()
        state2.scores[Player.SOUTH] = 120

        # act & assert
        assert state1 != state2

    def test__load_from_json__default_state_non_shuffled__returns_correctly(
        self, mocker
    ):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        expected_state = get_state()
        # TODO: add "fixture directory" stuff
        fpath = "tests/unit/fixtures/state_two_players_standard_rules_three_cards/default_non_shuffled_0_init.json"

        # act
        state = StateTwoPlayersStandardRules.load_from_json(fpath)

        # assert
        assert expected_state == state

    @pytest.mark.parametrize("eldest", list(Player))  # TODO: check this PyCharm warning
    def test__init__eldest_player_is_given__initializes_correctly(
        self, mocker, deck, eldest
    ):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        # act
        state = get_state(eldest=eldest)

        # assert
        assert isinstance(state, StateTwoPlayersStandardRules)
        assert state.hand_size == 3
        assert state.turn == eldest
        assert state.stock == deck[:34]  # AH to 4C
        assert state.trump == get_card("AH")
        assert state.hands[eldest] == get_cards("KC QC 6C")
        assert state.hands[eldest.opponent] == get_cards("JC 7C 5C")
        assert state.scores == {Player.NORTH: 0, Player.SOUTH: 0}
        assert state.table == []

    # TODO: should this be in integration tests?
    # TODO: really need directory path fixture
    # TODO: ok, I can improve this parametrize...
    @pytest.mark.parametrize(
        "moves, expected_results, expected_end_state_fpath",
        [
            (
                "6C",
                [None],
                "tests/unit/fixtures/state_two_players_standard_rules_three_cards/default_non_shuffled_1st_move.json",
            ),
            (
                "6C 7C",
                [
                    None,
                    (
                        # winner, added_score, table, newly_dealt_cards(winner, opponent)
                        Player.NORTH,
                        10,
                        get_cards("6C 7C"),
                        get_cards("4C 3C"),
                    ),
                ],
                "tests/unit/fixtures/state_two_players_standard_rules_three_cards/default_non_shuffled_2nd_move.json",
            ),
            (
                "6C 7C JC",
                [
                    None,
                    (
                        # winner, added_score, table, newly_dealt_cards(winner, opponent)
                        Player.NORTH,
                        10,
                        get_cards("6C 7C"),
                        get_cards("4C 3C"),
                    ),
                    None,
                ],
                "tests/unit/fixtures/state_two_players_standard_rules_three_cards/default_non_shuffled_3rd_move.json",
            ),
            (
                "6C 7C JC QC",
                [
                    None,
                    (
                        # winner, added_score, table, newly_dealt_cards(winner, opponent)
                        Player.NORTH,
                        10,
                        get_cards("6C 7C"),
                        get_cards("4C 3C"),
                    ),
                    None,
                    (Player.NORTH, 5, get_cards("JC QC"), get_cards("2C AC")),
                ],
                "tests/unit/fixtures/state_two_players_standard_rules_three_cards/default_non_shuffled_4th_move.json",
            ),
        ],
    )
    def test__play__after_given_moves__state_is_as_expected(
        self, mocker, moves, expected_results, expected_end_state_fpath
    ):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")
        expected_state = StateTwoPlayersStandardRules.load_from_json(
            expected_end_state_fpath
        )

        moves = get_cards(
            moves
        )  # TODO: might need get_card -> Card and get_cards -> [] always
        if isinstance(moves, Card):
            moves = [moves]

        state = get_state()

        # act
        results = [state.play(move) for move in moves]

        # assert
        # print(state, expected_state)
        assert results == expected_results
        assert state == expected_state


"""
    # TODO: needs fail test (from json)

    #def test__load_from_json__any_file__initializes_correctly(self):

    # TODO: check how do parametrized fixture (available?)
    
    def test__init__eldest_player_is_given__initializes_correctly(self, mocker, eldest):
        # assert False

# TODO: really need to load this from fixtures -- research this pytest
"""

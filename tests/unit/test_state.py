import pytest

from libbisca.card import get_card
from libbisca.state import *

# using Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior] unittest naming


class TestStateVariant1:
    @pytest.mark.parametrize("eldest", list(Player))  # TODO: check this PyCharm warning
    def test__init__first_eldest_player_is_given__initializes_correctly(
        self, mocker, eldest
    ):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        expected_stock = (
            "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, "
            "4♠, 5♠, 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣, 3♣, 4♣]"
        )

        # act
        state = StateVariant1(eldest=eldest)

        # assert
        assert str(state.stock) == expected_stock
        assert state.turn == eldest
        assert repr(state.trump) == "A♡"
        assert repr(state.hands[eldest]) == "[K♣, Q♣, 6♣]"
        assert repr(state.hands[eldest.opponent]) == "[J♣, 7♣, 5♣]"
        assert state.score == 0
        assert state.table == []

    @pytest.mark.parametrize("eldest", list(Player))  # TODO: check this PyCharm warning
    def test__play__first_round_with_eldest_to_play__runs_correctly(
        self, mocker, eldest
    ):
        # play is a command method, check changes to state

        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        youngest = eldest.opponent
        expected_stock = (
            "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, "
            "4♠, 5♠, 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣, 3♣, 4♣]"
        )

        state = State(eldest=eldest)
        move = get_card("KC")

        # act
        result = state.play(move)

        # assert
        assert result is None

        assert str(state.stock) == expected_stock
        assert state.turn == youngest
        assert str(state.trump) == "A♡"
        assert str(state.hands[eldest]) == "[Q♣, 6♣]"
        assert str(state.hands[youngest]) == "[J♣, 7♣, 5♣]"
        assert state.table == [move]

        assert state.winner == Winner.DRAW
        assert state.score == 0

    @pytest.mark.parametrize("eldest", list(Player))
    def test__play__first_round_with_eldest_to_play__runs_correctly(
        self, mocker, eldest
    ):
        # play is a command method, check changes to state

        mocker.patch("random.SystemRandom.shuffle")

        youngest = eldest.opponent
        expected_stock = (
            "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, "
            "4♠, 5♠, 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣]"
        )

        state = StateVariant1(eldest=eldest)

        state.play(get_card("KC"))
        move = get_card("7C")  # KC < 7C, youngest (eldest.opponent) must win

        # act
        winner, added_score, table = state.play(move)

        # assert
        assert winner == youngest
        assert added_score == 14
        assert str(table) == "[K♣, 7♣]"

        assert str(state.stock) == expected_stock
        assert state.turn == youngest
        assert str(state.trump) == "A♡"
        assert str(state.hands[eldest]) == "[Q♣, 6♣, 3♣]"
        assert str(state.hands[youngest]) == "[J♣, 5♣, 4♣]"
        assert state.table == []

        assert state.winner == Winner(youngest)
        assert (
            state.score == 14
        )  # next test confirms it's a add (hmm, getting paranoid again)

    def test__play__after_first_four_moves__runs_correctly(self, mocker):
        # play is a command method, check changes to state

        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        expected_stock = (
            "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, "
            "4♠, 5♠, 6♠, 7♠, Q♠, J♠, K♠]"
        )

        state = StateVariant1(eldest=Player.SOUTH)

        # act
        result = None
        for move in "KC, 7C, JC, QC".split(", "):
            result = state.play(get_card(move))

        # assert
        winner, added_score, table = result

        assert winner == Player.NORTH
        assert added_score == 5
        assert str(table) == "[J♣, Q♣]"

        assert str(state.stock) == expected_stock
        assert state.turn == Player.NORTH
        assert str(state.trump) == "A♡"
        assert str(state.hands[Player.SOUTH]) == "[6♣, 3♣, A♣]"
        assert str(state.hands[Player.NORTH]) == "[5♣, 4♣, 2♣]"
        assert state.table == []

        assert state.winner == Winner.NORTH
        assert state.score == 19

    def test__is_endgame__initial_state__return_false(self):
        # method is query method, check output

        # arrange
        state = StateVariant1()

        # act & assert
        assert state.is_endgame() is False

    def test__is_endgame__terminal_state__return_false(self):
        # arrange
        state = StateVariant1()
        state._cards_in_stock_and_hands = 0

        # act & assert
        assert state.is_endgame() is True

    @pytest.mark.parametrize(
        "table, did_eldest_win",
        [
            # tests overlap a bit with card.__gt__ tests
            # same suit (follow)
            ("4H, 5H", False),  # 4H < 5H -> youngest
            ("7H, 5H", True),  # 7H > 5H -> eldest
            # same suit (follow) - trumps
            ("4H(t), 5H", True),  # 4H(t) > 5H -> eldest
            ("4H, 5H(t)", False),  # 4H < 5H(t) -> youngest
            ("4H(t), 5H(t)", False),  # 4H(t) < 5H(t) -> youngest
            # different suit (no follow)
            ("6H, 5C", True),  # 6H > 5C, no follow -> eldest
            ("4H, 5C", True),  # 4H < 5C, no follow -> eldest
            # different suit (no follow) - trumps
            ("4H(t), 5C", True),  # 4H(t) > 5C, no follow -> eldest
            ("4H, 5C(t)", False),  # 4H < 5C(t), no follow -> youngest
        ],
    )
    def test__get_round_winner__x__get_expected_player(self, table, did_eldest_win):
        # only do tests for private methods if they are complex, otherwise just the public api

        # arrange
        state = StateVariant1()

        eldest = state.turn
        state.table = [get_card(c) for c in table.split(", ")]
        state._table_played = [eldest, eldest.opponent]

        # act
        winner = state._get_round_winner()

        # assert
        assert winner == eldest if did_eldest_win else eldest.opponent

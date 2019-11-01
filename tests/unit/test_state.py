# TODO: add docstrings

import pytest

from libbisca.state import *


def test__state_init__first_eldest_is_south_player__initializes_correctly(mocker):
    # arrange
    expected_stock = (
        "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, "
        "4♠, 5♠, 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣, 3♣, 4♣]"
    )
    mocker.patch("random.SystemRandom.shuffle")

    # act
    state = State()

    # assert
    assert str(state.stock) == expected_stock
    assert state.turn == Player.SOUTH
    assert repr(state.trump) == "A♡"
    assert repr(state.hands[Player.SOUTH]) == "[K♣, Q♣, 6♣]"
    assert repr(state.hands[Player.NORTH]) == "[J♣, 7♣, 5♣]"
    assert state.score == 0
    assert state.table == []


def test__state_play__play_eldest__runs_correct(mocker):
    # method is command method, check modifications

    # arrange
    # TODO: add state fixture?
    expected_stock = (
        "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, "
        "4♠, 5♠, 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣, 3♣, 4♣]"
    )
    mocker.patch("random.SystemRandom.shuffle")
    state = State()

    move = Card.get_card("KC")

    # act
    result = state.play(move)

    # assert
    assert result is None
    assert str(state.stock) == expected_stock
    assert state.turn == Player.NORTH
    assert repr(state.trump) == "A♡"
    assert repr(state.hands[Player.SOUTH]) == "[Q♣, 6♣]"
    assert repr(state.hands[Player.NORTH]) == "[J♣, 7♣, 5♣]"
    assert state.table == [move]
    assert state.score == 0


def test__state_play__play_youngest__runs_correct(mocker):
    # method is command method, check modifications

    # arrange
    expected_stock = (
        "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, "
        "4♠, 5♠, 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣]"
    )
    mocker.patch("random.SystemRandom.shuffle")

    state = State()
    state.play(Card.get_card("KC"))

    move = Card.get_card("7C")

    # act
    result = state.play(move)

    # assert
    assert result == (Player.NORTH, -14)
    assert str(state.stock) == expected_stock
    assert state.turn == Player.NORTH
    assert repr(state.trump) == "A♡"
    assert repr(state.hands[Player.SOUTH]) == "[Q♣, 6♣, 3♣]"
    assert repr(state.hands[Player.NORTH]) == "[J♣, 5♣, 4♣]"
    assert state.table == []
    assert state.score == -14  # TODO: check if adds or replaces


def test__state_is_endgame__initial_state__return_false():
    # method is query method, check output

    # arrange
    state = State()

    # act & assert
    assert state.is_endgame() is False


def test__state_is_endgame__terminal_state__return_false():
    # arrange
    state = State()
    state._cards_in_stock_and_hands = 0

    # act & assert
    assert state.is_endgame() is True


def test__state_winner__initial_state__return_none():
    # arrange
    state = State()

    # act & assert
    assert state.winner is None


@pytest.mark.parametrize(
    "score, winner",
    [(0, Winner.DRAW), (90 - 30, Winner.SOUTH), (30 - 90, Winner.NORTH)],
)
def test__state_winner__final_state__x(score, winner):
    # arrange
    state = State()
    state._cards_in_stock_and_hands = 0
    state.score = score
    state._scores[Player.SOUTH] = (score + 120) // 2
    state._scores[Player.NORTH] = -(score - 120) // 2

    # act & assert
    assert state.winner == winner


def test__state_score_and_get_score__initial_state__return_none():
    # arrange
    state = State()

    # act & assert
    assert state.score == 0
    assert state.get_score(Player.SOUTH) == 0
    assert state.get_score(Player.NORTH) == 0


@pytest.mark.parametrize(
    "south_score, score",
    [(0, 0 - 120), (30, 30 - 90), (60, 0), (90, 90 - 30), (120, 120 - 0)],
)
def test__state_get_score__final_state__return_human_score(south_score, score):
    # arrange
    state = State()

    state._cards_in_stock_and_hands = 0
    state.score = score
    state._scores[Player.SOUTH] = south_score
    state._scores[Player.NORTH] = 120 - south_score

    # act & assert
    assert state.get_score(Player.SOUTH) == south_score
    assert (
        state.get_score(Player.NORTH) == 120 - south_score
    )  # TODO: put 120 in constant?


# TODO: check which of this tests add value to testing
# TODO: add test for State.__init__ with eldest=NORTH
# TODO: add test for State.__init__ with hand_size=7 and 9
# TODO: add test for State.play - middle of game move
# TODO: add test for State.play - trying at endgame
# TODO: add test for State.opponent

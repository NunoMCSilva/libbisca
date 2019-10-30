# -*- coding: utf-8 -*-

# TODO: add docstrings

from libbisca.card import Card, Rank, Suit
from libbisca.state import State, Player, Winner


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
    assert state.scores == {Player.SOUTH: 0, Player.NORTH: 0}
    assert state.table == []


def test__state_play__play_eldest__runs_correct(mocker):
    # method is command method, check modifications

    # arrange
    expected_stock = (
        "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, "
        "4♠, 5♠, 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣, 3♣, 4♣]"
    )
    mocker.patch("random.SystemRandom.shuffle")
    state = State()

    # TODO: could use a Card.get_card("KC") for testing
    move = Card(Rank.KING, Suit.CLUBS)

    # act
    result = state.play(move)

    # assert
    assert result is None
    assert str(state.stock) == expected_stock
    assert state.turn == Player.NORTH
    assert repr(state.trump) == "A♡"
    assert repr(state.hands[Player.SOUTH]) == "[Q♣, 6♣]"
    assert repr(state.hands[Player.NORTH]) == "[J♣, 7♣, 5♣]"
    assert state.scores == {Player.SOUTH: 0, Player.NORTH: 0}

    # TODO: this is an internal implementation issue... hide?
    assert state.table == [(Player.SOUTH, move)]


def test__state_play__play_youngest__runs_correct(mocker):
    # method is command method, check modifications

    # arrange
    expected_stock = (
        "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, "
        "4♠, 5♠, 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣]"
    )
    mocker.patch("random.SystemRandom.shuffle")

    state = State()

    # TODO: could use a Card.get_card("KC") for testing
    move1 = Card(Rank.KING, Suit.CLUBS)

    move2 = Card(Rank.SEVEN, Suit.CLUBS)
    state.play(move1)

    # act
    result = state.play(move2)

    # assert
    assert result == (Player.NORTH, 14)  # South: KC vs North: 7C -> North, 14
    assert str(state.stock) == expected_stock
    assert state.turn == Player.NORTH
    assert repr(state.trump) == "A♡"
    assert repr(state.hands[Player.SOUTH]) == "[Q♣, 6♣, 3♣]"
    assert repr(state.hands[Player.NORTH]) == "[J♣, 5♣, 4♣]"
    assert state.table == []

    # TODO: need to check it adds and not just replaces
    assert state.scores == {Player.SOUTH: 0, Player.NORTH: 14}


def test__state_is_endgame__initial_state__return_false():
    # arrange
    state = State()

    # act & assert
    assert state.is_endgame() is False


def test__state_is_endgame__final_state__return_false():
    # arrange
    state = State()

    state.stock = []
    state.hands = {player: [] for player in Player}
    state.scores = {player: 60 for player in Player}

    # act & assert
    assert state.is_endgame() is True


def test__state_winner__initial_state__return_none():
    # arrange
    state = State()

    # act & assert
    assert state.winner is None


def test__state_winner__draw__return_winner_draw():
    # arrange
    state = State()

    state.stock = []
    state.hands = {player: [] for player in Player}
    state.scores = {player: 60 for player in Player}

    # act & assert
    assert state.winner == Winner.DRAW


def test__state_winner__north_win__return_winner_north():
    # arrange
    state = State()

    state.stock = []
    state.hands = {player: [] for player in Player}
    state.scores = {Player.NORTH: 90, Player.SOUTH: 30}

    # act & assert
    assert state.winner == Winner.NORTH


def test__state_winner__south_win__return_winner_north():
    # arrange
    state = State()

    state.stock = []
    state.hands = {player: [] for player in Player}
    state.scores = {Player.NORTH: 30, Player.SOUTH: 90}

    # act & assert
    assert state.winner == Winner.SOUTH


def test__state_score__initial_state__return_none():
    # arrange
    state = State()

    # act & assert
    assert state.score is None


def test__state_score__draw__return_winner_draw():
    # arrange
    state = State()

    state.stock = []
    state.hands = {player: [] for player in Player}
    state.scores = {player: 60 for player in Player}

    # act & assert
    assert state.score == 60


def test__state_score__normal_win__return_winner_north():
    # arrange
    state = State()

    state.stock = []
    state.hands = {player: [] for player in Player}
    state.scores = {Player.NORTH: 90, Player.SOUTH: 30}

    # act & assert
    assert state.score == 90

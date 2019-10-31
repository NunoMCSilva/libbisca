# TODO: add docstrings

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
    assert state.score == 0

    # TODO: this is an internal implementation issue... hide? just have a property state.table that rets move?
    assert state.table == [(Player.SOUTH, move)]


def test__state_play__play_youngest__runs_correct(mocker):
    # method is command method, check modifications

    # arrange
    expected_stock = (
        "[A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, Q♡, J♡, K♡, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, Q♦, J♦, K♦, A♠, 2♠, 3♠, "
        "4♠, 5♠, 6♠, 7♠, Q♠, J♠, K♠, A♣, 2♣]"
    )
    mocker.patch("random.SystemRandom.shuffle")

    move1 = Card.get_card("KC")
    move2 = Card.get_card("7C")

    state = State()
    state.play(move1)

    # act
    result = state.play(move2)

    # assert
    assert result == (Player.NORTH, 14)    # TODO: hmmm, check values
    assert str(state.stock) == expected_stock
    assert state.turn == Player.NORTH
    assert repr(state.trump) == "A♡"
    assert repr(state.hands[Player.SOUTH]) == "[Q♣, 6♣, 3♣]"
    assert repr(state.hands[Player.NORTH]) == "[J♣, 5♣, 4♣]"
    assert state.table == []
    assert state.score == 14    # TODO: check if adds or replaces


def test__state_is_endgame__initial_state__return_false():
    # arrange
    state = State()

    # act & assert
    assert state.is_endgame() is False


def test__state_is_endgame__final_state__return_false():
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


def test__state_winner__draw__return_winner_draw():
    # arrange
    state = State()
    state._cards_in_stock_and_hands = 0
    state.score = 0

    # act & assert
    assert state.winner == Winner.DRAW


def test__state_winner__north_win__return_winner_north():
    # arrange
    state = State()
    state._cards_in_stock_and_hands = 0
    state.score = -60   # TODO: need to make sure north, south is consistent in all

    # act & assert
    assert state.winner == Winner.NORTH


def test__state_winner__south_win__return_winner_north():
    # arrange
    state = State()
    state._cards_in_stock_and_hands = 0
    state.score = 60    # s: 90, n: 30

    # act & assert
    assert state.winner == Winner.SOUTH




"""


from libbisca.card import Card, Rank, Suit
from libbisca.state import State, Player, Winner






def test__state_score__initial_state__return_none():
    # arrange
    state = State()

    # act & assert
    assert state.score == 0



def test__state_score__draw__return_winner_draw():
    # arrange
    state = State()

    state.stock = []
    state._num = 0
    state.hands = {player: [] for player in Player}
    #state.scores = {player: 60 for player in Player}
    state.score = 0

    # act & assert
    assert state.score == 0 #60


def test__state_score__normal_win__return_winner_north():
    # arrange
    state = State()

    state.stock = []
    state._num = 0
    state.hands = {player: [] for player in Player}
    state.scores = {Player.NORTH: 90, Player.SOUTH: 30}
    state.score = -60

    # act & assert
    assert state.score == -60   #90
# TODO: last ones may need diff - get_score
"""

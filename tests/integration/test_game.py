# TODO: add tests

"""
# TODO: add docstrings

import pytest

from libbisca.game.game import Game


# TODO: i dodn't have much experience with integration tests, so research that
@pytest.mark.skip("until I have game data to test this...")
def test__game_run__non_random_state__runs_correctly(mocker):
    # arrange
    mocker.patch("random.SystemRandom.shuffle")
    mocker.patch("random.choice").side_effect = lambda args: args[-1]
    game = Game()

    # act
    game.run()

    # assert
    assert False

    # import random
    # print(random.choice([1, 2, 3]))


"""

"""
# TODO: confirm invariants through run (sum scores <= 120 until end, etc)?



from libbisca.agent import RandomAgent

a = RandomAgent()
g = Game([a, a])
print(g.run())  # TODO: add verbose option?
# from libbisca.game.card import Card
# print(Card.get_deck(shuffle=False))

n = 100
import time
begin = time.time()
print(Game.run_multiple([a, a], n))     # e.g.: {<Winner.NORTH: 1>: 4923, <Winner.DRAW: 0>: 121, <Winner.SOUTH: -1>: 4956}
end = time.time()
print(end - begin, "secs", (end - begin) / n, "secs/game", n / (end - begin), "game/sec")
# 2.0181515216827393 secs 0.020181515216827393 secs/game 49.55029338759449 game/sec
"""

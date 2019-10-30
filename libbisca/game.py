# TODO: add docstrings

import copy
import random
from typing import Dict, List, Optional, Tuple

from libbisca.agent import Agent
from libbisca.card import Card
from libbisca.state import State, Player, Winner


class Game:

    def __init__(self, agents: List[Agent], eldest: Player = Player.SOUTH):
        self.agents = agents
        self.state = State(eldest=eldest)

    def __repr__(self):
        # TODO: really need some pprint here? and maybe modify State.__repr__
        return f"Game(agents = {self.agents}, state = {self.state})"

    # TODO: add undo? or not necessary in non-gui
    # TODO: add load/save? dump?
    # TODO: keep "log" to save?
    # TODO: add history (necessary for undo?)?

    def run(self) -> Tuple[Winner, int]:
        # TODO: add verbose option?
        # TODO: shouldn't this be in state, at least the round part? but with the agents option? think about it
        while not self.state.is_endgame():
            for _ in range(State.NUM_PLAYERS):
                self._run_round()

        return self.state.winner, self.state.score

    @staticmethod
    def run_multiple(agents: List[Agent], num_times=10) -> Dict[Winner, int]:
        results = {winner: 0 for winner in Winner}

        for _ in range(num_times // 2):     # TODO: this bit needs to be well documented
            for eldest in Player:
                game = Game(agents, eldest)
                winner, _ = game.run()
                results[winner] += 1

        return results

    def step(self, move: Card) -> Optional[Tuple[Player, int]]:
        # of use only (mostly) for a gui
        return self.state.play(move)

    def _run_round(self) -> None:
        # TODO: give POVState instead of full state or just scramble state_copy?
        state_copy = copy.deepcopy(self.state)
        move = self.agents[self.state.turn].get_move(state_copy)
        self.state.play(move)  # TODO: handling of IllegalMove?

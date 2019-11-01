# TODO: add docstrings
# TODO: this needs a better name -- this module is to have tools that make engine develop easier

from typing import Dict, Optional, Sequence, Tuple

from libbisca.agents.agents import Agent
from libbisca.state import State, Player, Winner


class ObservedState:

    def __init__(self, state: State, observer: Player):
        raise NotImplementedError

    @property
    def hand(self):
        raise NotImplementedError


class PossibleCards:
    # represents a range of cards -- useful for search
    raise NotImplementedError


class Runner:

    def __init__(self, agents: Sequence[Agent], eldest: Player = Player.SOUTH):
        self.agents = agents
        self.state = State(eldest)

    def run(self) -> State:
        while not self.state.is_endgame():
            # TODO: is observer needed -- self.state.turn is already there?
            observation = ObservedState(self.state, self.state.turn)
            move = self.agents[self.state.turn].get_move(observation)
            self.state.play(move)

        return self.state

    @staticmethod
    def run_multiple(agents: Sequence[Agent], num_games=10) -> Dict[Winner, int]:
        results = {winner: 0 for winner in Winner}

        for _ in range(num_games // 2):  # TODO: this bit needs to be well documented
            for eldest in Player:
                state = Runner(agents, eldest).run()
                results[state.winner] += 1

        return results

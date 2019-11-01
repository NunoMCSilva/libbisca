# TODO: add docstrings

from typing import Dict, Optional, Sequence, Tuple

from libbisca.agent import Agent
from libbisca.card import Card
from libbisca.state import State, Player, Winner


class Game:

    def __init__(self, agents: Sequence[Agent], eldest: Player = Player.SOUTH):
        self.agents = agents
        self.state = State(eldest)

    # TODO: add load/save to json?

    def run(self) -> State:
        # This might belong in State, but I prefer to keep it here so state doesn't have to deal with agents
        while not self.state.is_endgame():
            # TODO: give ObservedState instead of state: ObservedState(self.state)
            move = self.agents[self.state.turn].get_move(self.state)
            self.state.play(move)

        return self.state

    def step(self, move: Card) -> Optional[Tuple[Player, int]]:
        # of use only (mostly) for a gui -- TODO: check that
        return self.state.play(move)

    @staticmethod
    def run_multiple(agents: Sequence[Agent], num_games=10) -> Dict[Winner, int]:
        results = {winner: 0 for winner in Winner}

        for _ in range(num_games // 2):  # TODO: this bit needs to be well documented
            for eldest in Player:
                game = Game(agents, eldest)
                state = game.run()
                # TODO: state = Game(agents, eldest).run() ?
                results[state.winner] += 1

        return results

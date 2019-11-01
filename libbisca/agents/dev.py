# TODO: add docstrings
# TODO: this needs a better name -- this module is to have tools that make engine develop easier

from typing import Dict, Optional, Sequence, Tuple

# from libbisca.agents.agents import Agent - TODO: handle this typing issue later
from libbisca.card import Card
from libbisca.state import State, Player, Winner


class ObservedState:
    def __init__(self, state: State, observer: Player):
        raise NotImplementedError

    @property
    def hand(self):
        raise NotImplementedError


class PossibleCards:
    # represents a range of cards -- useful for search

    # pc = PossibleCards(state.stock, state.hands[opponent])
    # self.stock = pc
    # self.opp_hand = pc

    def __init__(self, cards: Card):
        raise NotImplementedError


class Runner:
    def __init__(
        self, agents, eldest: Player = Player.SOUTH
    ):  # Sequence[Agent] - TODO: handle this typing issue later
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
    def run_multiple(
        agents: Sequence, num_games=10
    ) -> Dict[Winner, int]:  # Sequence[Agent]
        results = {winner: 0 for winner in Winner}

        for _ in range(num_games // 2):  # TODO: this bit needs to be well documented
            for eldest in Player:
                state = Runner(agents, eldest).run()
                results[state.winner] += 1

        return results


"""
def main():
    from libbisca.agent import RandomAgent
    agent = RandomAgent()
    game = Game([agent, agent])
    print(game)
    state = game.run()
"""

"""
    def __iter__(self):
        return game

    def __next__(self):
        # TODO: other method would have one call to endgame (track cards to make endgame faster)
        if self.state.is_endgame():
            raise StopIteration
        else:
            return self._run_round()

    def _run_round(self) -> State:

        state_copy = copy.deepcopy(self.state)
        move = self.agents[self.state.turn].get_move(state_copy)

        self.state.play(move)  # TODO: handling of IllegalMove?
        return self.state

        while not self.state.is_endgame():
            for _ in range(State.NUM_PLAYERS):
                self._run_round()

        return self.state.winner, self.state.score  # TODO: check mypy complaint here
"""

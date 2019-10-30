# TODO: add docstrings

from enum import IntEnum
from typing import Dict, List, Optional, Tuple, Union

# TODO: relative imports
from libbisca.card import Card


class Player(IntEnum):
    NORTH = 1
    SOUTH = -1


class Winner(IntEnum):
    NORTH = 1
    DRAW = 0
    SOUTH = -1


class State:
    NUM_PLAYERS = 2  # code only handles 2 players (for now, and maybe in the future)
    HAND_SIZE = 3  # TODO: extend code to Bisca9 later

    def __init__(self, eldest: Player = Player.SOUTH):
        self.turn = eldest
        self.stock = Card.get_deck()
        self.table: List[Tuple[Player, Card]] = []

        self.hands: Dict[Player, List[Card]] = {player: [] for player in Player}
        # self.piles seems unnecessary

        # can be reduced to a single number, but this is simpler
        # TODO: don't like this typing, but...
        self.scores: Dict[Union[Player, Winner], int] = {player: 0 for player in Player}

        # handling trumps
        self.stock = [
            (card.get_trumped() if card.suit == self.stock[0].suit else card)
            for card in self.stock
        ]
        self.trump = self.stock[0]

        # deal initial hand
        for _ in range(self.HAND_SIZE):
            self._deal_cards()

    # TODO: def __hash__(self): necessary?

    def __repr__(self):
        # TODO: this is more a __str__ than a __repr__, check this
        # TODO: refactor -- turn, hands, winner and score need a better representation, and really needs better look
        try:
            score = self.score
            winner = self.winner
        except ValueError:
            score = None
            winner = None

        return (
            f"State("
            f"\n\tturn = {self.turn}, "
            f"\n\tstock = {self.stock}, "
            f"\n\ttrump = {self.trump}, "
            f"\n\thands = {self.hands}, "
            f"\n\tscores = {self.scores}, "
            f"\n\ttable = {self.table}"
            f"\n\tis_endgame = {self.is_endgame()}"
            f"\n\twinner = {winner}"
            f"\n\tscore == {score}"
            f"\n)"
        )

    @property
    def score(self) -> Optional[int]:
        # TODO: figure out mypy's issue with Optional[int] -- just use ValueError (check tests)
        if self.is_endgame():
            assert sum(self.scores.values()) == 120

            if self.winner == Winner.DRAW:
                return 60
            else:
                return self.scores[self.winner]  # TODO: check mypy complaint here
        else:
            return None  # raise ValueError("game not yet finished")  # TODO: improve

    @property
    def winner(self) -> Optional[Winner]:
        if self.is_endgame():
            if self.scores[Player.NORTH] == self.scores[Player.SOUTH]:
                return Winner.DRAW
            else:
                return (
                    Winner.NORTH
                    if self.scores[Player.NORTH] > self.scores[Player.SOUTH]
                    else Winner.SOUTH
                )
        else:
            # or just raise ValueError if it's called before is_terminal is True
            # TODO: improve exception type and msg
            # raise ValueError("game not yet finished")
            return None  # TODO: hmmm

    # TODO: add save/load? to json?

    def is_endgame(self) -> bool:
        return len(self.stock) + sum(len(hand) for hand in self.hands.values()) == 0

    def play(self, move: Card) -> Optional[Tuple[Player, int]]:
        # TODO: recheck game rules (sp. that bit about follow after empty stock -- will need to modify __gt__ for that)

        eldest = self.table == []

        # TODO: better exception here would be IllegalMove?
        self.hands[self.turn].remove(move)

        # TODO: better format other than (player, card)
        self.table.append((self.turn, move))

        if eldest:
            self.turn = Player.NORTH if self.turn == Player.SOUTH else Player.SOUTH
        else:
            # youngest
            winner = self._get_round_winner()
            added_score = sum(card.score for _, card in self.table)

            self.scores[winner] += added_score
            self.turn = winner
            self.table = []

            # if stock exists, deal cards -- TODO: put in deal cards? (ignores call if stock doesn't exist)
            if self.stock:
                self._deal_cards()

            return winner, added_score

        return None

    def _deal_cards(self) -> None:
        # TODO: add _get_opponent?
        for turn in (
            self.turn,
            Player.NORTH if self.turn == Player.SOUTH else Player.SOUTH,
        ):
            self.hands[turn].append(self.stock.pop())

    def _get_round_winner(self) -> Player:
        (player1, card1), (player2, card2) = self.table
        return player1 if card1 > card2 else player2

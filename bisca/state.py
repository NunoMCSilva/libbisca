# TODO: add docstrings

from enum import IntEnum
from typing import Optional, Tuple

# TODO: relative imports
from bisca.card import Card


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
        self.table = []

        self.hands = {player: [] for player in Player}
        # self.piles seems unnecessary

        # can be reduced to a single number, but this is simpler
        self.scores = {player: 0 for player in Player}

        # handling trumps
        self.stock = [
            (card.get_trumped() if card.suit == self.stock[0].suit else card)
            for card in self.stock
        ]
        self.trump = self.stock[0]

        # deal initial hand
        for _ in range(self.HAND_SIZE):
            self._deal_cards()

    @property
    def score(self) -> Optional[int]:
        if self.is_endgame():
            assert sum(self.scores.values()) == 120

            if self.winner == Winner.DRAW:
                return 60
            else:
                return self.scores[self.winner]
        else:
            return None

    @property
    def winner(self) -> Optional[Winner]:
        # TODO: or just raise ValueError if it's called before is_terminal is True

        if self.is_endgame():
            if self.scores[Player.NORTH] == self.scores[Player.SOUTH]:
                return Winner.DRAW
            else:
                return Winner.NORTH if self.scores[Player.NORTH] > self.scores[Player.SOUTH] else Winner.SOUTH
        else:
            return None     # raise ValueError("game not yet finished") -- improve exception type and msg

    # TODO: add save/load?

    def is_endgame(self) -> bool:
        return not (bool(self.stock) and bool(self.hands[Player.NORTH]) and bool(self.hands[Player.SOUTH]))

    def play(self, move: Card) -> Optional[Tuple[Player, int]]:
        # TODO: recheck game rules (sp. that bit about follow after empty stock -- will need to modify __gt__ for that)

        eldest = self.table == []

        # TODO: better exception here would be IllegalMove?
        self.hands[self.turn].remove(move)

        # TODO: better format other than (player, card)
        self.table.append((self.turn, move))

        if eldest:
            self.turn = -self.turn
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
        for turn in (self.turn, -self.turn):
            self.hands[turn].append(self.stock.pop())

    def _get_round_winner(self) -> Player:
        (player1, card1), (player2, card2) = self.table
        return player1 if card1 > card2 else player2



"""






    def __repr__(self):
        # TODO: refactor -- turn, hands, winner and score need a better representation
        return (
            f"State("
            f"\n\tturn = {self.turn}, "
            f"\n\tstock = {self.stock}, "
            f"\n\ttrump = {self.trump}, "
            f"\n\thands = {self.hands}, "
            f"\n\tscores = {self.scores}, "
            f"\n\ttable = {self.table}"
            f"\n\tis_endgame = {self.is_endgame()}"
            f"\n\twinner = {self.winner}"
            f"\n\tscore == {self.score}"
            f"\n)"
        )

    # TODO: remove _is_endgame, _winner, etc. (or make it work--check that) -- is not working as well as I want and it is redundant


    # TODO: add save/load? -- to json






""
class State:
    __init__(eldest=0)
    __repr__()
    is_endgame()
    play(move)
    winner()
""


"""

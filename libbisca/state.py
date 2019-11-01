# TODO: add docstrings

from enum import IntEnum
from typing import Optional, Tuple

from libbisca.card import Card, Deck


class Player(IntEnum):
    # choice due to SOUTH being the player side in a future GUI (not in libbisca)
    NORTH = -1
    SOUTH = 1


class Winner(IntEnum):
    SOUTH = 1
    DRAW = 0
    NORTH = -1


class State:
    NUM_PLAYERS = 2  # code will only handle 2 player for now (and maybe in the future)
    HAND_SIZE = 3  # TODO: extend code to Bisca9 later

    def __init__(self, eldest: Player = Player.SOUTH, hand_size: int = Player.SOUTH):
        self.turn = eldest

        self.stock = Deck()
        self.trump = self.stock.bottom

        self.hands = {player: [] for player in Player}
        # TODO: substitute (player, card) so table is accessible without revealing inner details
        self.table = []
        self._table_player = []

        # this is from the POV of Player.SOUTH
        self.score = 0
        self._scores = {
            player: 0 for player in Player
        }  # TODO: ok, I need to get the score system to work better

        # this is for a more efficient is_endgame - TODO: add len(self.stock)?
        self._cards_in_stock_and_hands = 40

        # deal initial hand
        for _ in range(self.HAND_SIZE):
            self._deal_cards()

    # TODO: is __hash__(self): necessary?

    def __str__(self):
        # TODO: improve this (pretty print?)
        return (
            f"State(turn={self.turn}, stock={self.stock}, trump={self.trump}, hands={self.hands}, "
            f"score={self.score}, self.table={self.table}, is_endgame={self.is_endgame()}, winner={self.winner}"
        )

    # TODO: add save/load to json?

    # TODO: add state.hand to State? (current hand property)

    @property
    def opponent(self) -> Player:
        return Player.NORTH if self.turn == Player.SOUTH else Player.SOUTH

    @property
    def winner(self) -> Optional[Winner]:
        if self.is_endgame():
            assert sum(self._scores.values()) == 120
            # assert self.get_score(Player.SOUTH) == 120 - self.get_score(Player.NORTH)

            if self.score == 0:
                return Winner.DRAW
            else:
                return Winner.SOUTH if self.score > 0 else Winner.NORTH
        else:
            return None

    def do_rollout(self):
        # do random rollout
        raise NotImplementedError  # TODO: implement this

    def get_score(self, player: Player) -> int:
        # human understandable score
        return self._scores[player]

    def is_endgame(self) -> bool:
        return self._cards_in_stock_and_hands == 0

    def play(self, move: Card) -> Optional[Tuple[Player, int]]:
        # TODO: recheck game rules
        # TODO: add other variants (that one that enforces follows after self.stock is empty)

        # TODO: wouldn't a better exception here would be IllegalMove?
        self.hands[self.turn].remove(move)
        self._cards_in_stock_and_hands -= 1

        # TODO: better format other than (player, card)? or separate in self.table and self.table_player?
        self.table.append(move)
        self._table_player.append(self.turn)

        if len(self.table) == 1:
            # eldest
            self.turn = self.opponent
        else:
            # youngest
            winner = self._get_round_winner()
            added_score = sum(card.score for card in self.table) * winner.value
            self._scores[winner] += sum(card.score for card in self.table)

            self.score += added_score
            self.turn = winner
            self.table = []
            self._table_player = []

            # if stock exists, deal cards -- TODO: put in deal cards? (ignores call if stock doesn't exist)
            if self.stock:
                self._deal_cards()

            return winner, added_score

        return None

    def _deal_cards(self) -> None:
        for turn in (self.turn, self.opponent):
            self.hands[turn].append(self.stock.pop())

    def _get_round_winner(self) -> Player:
        player1, player2 = self._table_player
        card1, card2 = self.table
        # (player1, card1), (player2, card2) = self.table
        return (
            player1 if card1 > card2 else player2
        )  # TODO: place to add follow variant (diff class?)

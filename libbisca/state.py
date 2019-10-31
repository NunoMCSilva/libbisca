# TODO: add docstrings

from enum import IntEnum
from typing import Dict, List, Optional, Tuple, Union

# TODO: relative imports
from libbisca.card import Card, Deck


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

        self.stock = Deck()
        self.trump = self.stock.bottom
        self.hands = {player: [] for player in Player}
        self.table = list()
        self.score = 0      # POV of Player.South -- TODO: may get confusing (Player.SOUTH == -1)

        # deal initial hand
        for _ in range(self.HAND_SIZE):
            self._deal_cards()

        # TODO: size of Deck -- add CONST? len(self.stock.deck)?
        self._cards_in_stock_and_hands = 40    # cards in stock and hands

    # TODO: is __hash__(self): necessary?

    def __str__(self):
        # TODO: improve this (pretty print?)
        return f"State(turn={self.turn}, stock={self.stock}, trump={self.trump}, hands={self.hands}, " \
               f"score={self.score}, self.table={self.table}, is_endgame={self.is_endgame()}, winner={self.winner}"

    # TODO: add save/load? to json?

    @property
    def opponent(self) -> Player:
        return Player.NORTH if self.turn == Player.SOUTH else Player.SOUTH

    @property
    def winner(self) -> Optional[Winner]:
        if self.is_endgame():
            if self.score == 0:
                return Winner.DRAW
            else:
                return Winner.SOUTH if self.score > 0 else Winner.NORTH
        else:
            return None

    def is_endgame(self) -> bool:
        return self._cards_in_stock_and_hands == 0

    def play(self, move: Card) -> Optional[Tuple[Player, int]]:
        # TODO: recheck game rules (sp. that bit about follow after empty stock -- don't modify __gt__ just hav other pl
        # TODO: two variants, 1 this, 2 follow after self.stock == 0

        # TODO: better exception here would be IllegalMove?
        self.hands[self.turn].remove(move)
        self._cards_in_stock_and_hands -= 1

        # TODO: better format other than (player, card)?
        self.table.append((self.turn, move))

        if len(self.table) == 1:
            # eldest
            self.turn = self.opponent
        else:
            # youngest
            winner = self._get_round_winner()
            added_score = sum(card.score for _, card in self.table) * winner.value

            self.score += added_score
            self.turn = winner
            self.table = []

            # if stock exists, deal cards -- TODO: put in deal cards? (ignores call if stock doesn't exist)
            if self.stock:
                self._deal_cards()

            return winner, added_score

        return None

    def _deal_cards(self) -> None:
        for turn in (self.turn, self.opponent):
            self.hands[turn].append(self.stock.pop())

    def _get_round_winner(self) -> Player:
        (player1, card1), (player2, card2) = self.table
        return player1 if card1 > card2 else player2

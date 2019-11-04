import pytest

from libbisca.card import Card  # TODO: check why PyCharm has this as unused statement?
from libbisca.state import *

# using Roy Osherove's [UnitOfWork_StateUnderTest_ExpectedBehavior] unittest naming


class TestStateBisca3:

    @pytest.mark.parametrize("eldest", list(Player))    # TODO: check this PyCharm warning
    def test__init__eldest_player_is_given__initializes_correctly(self, mocker, eldest):
        # arrange
        mocker.patch("random.SystemRandom.shuffle")

        stock = "2H 3H 4H 5H 6H QH JH KH 7H AH 2D 3D 4D 5D 6D QD JD KD 7D AD 2S 3S 4S 5S 6S QS JS KS 7S AS " \
                "2C 3C 4C 5C"
        expected_stock = [Card.get_card(s) for s in stock.split(" ")]

        expected_trump = Card.get_card("2H")

        eldest_hand = "AC KC QC"
        expected_eldest_hand = [Card.get_card(s) for s in eldest_hand.split(" ")]

        youngest_hand = "7C JC 6C"
        expected_youngest_hand = [Card.get_card(s) for s in youngest_hand.split(" ")]

        # act
        state = get_state("Bisca3", eldest)

        # assert
        assert state.hand_size == 3
        assert state.turn == eldest

        assert state.stock == expected_stock
        assert state.trump == expected_trump

        assert state.hands[eldest] == expected_eldest_hand
        assert state.hands[eldest.opponent] == expected_youngest_hand

        assert state.scores == {Player.NORTH: 0, Player.SOUTH: 0}

        assert state.table == []

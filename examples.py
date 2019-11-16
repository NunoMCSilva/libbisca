# -*- coding: utf-8 -*-

# TODO: add docstrings -- examples?

import libbisca


def main():
    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("Card")
    print()

    card = libbisca.get_card("AC")
    print(card)

    cards = libbisca.get_cards("2H 7C")
    print(cards)

    non_shuffled_deck = libbisca.get_deck(shuffle=False)
    print(non_shuffled_deck)

    deck = libbisca.get_deck()
    print(deck)
    print()

    print(
        "-----------------------------------------------------------------------------------------------------------"
    )
    print("State")
    print()

    non_shuffled_state = libbisca.get_state(shuffle=False)
    print(non_shuffled_state)

    state = libbisca.get_state()
    print(state)

    print(non_shuffled_state == state)

    legal_moves = non_shuffled_state.legal_moves
    print(legal_moves)
    print(card in legal_moves)

    print(state.is_endgame())

    # ValueError: game is not in endgame
    # print(state.get_winner())

    result = non_shuffled_state.play(libbisca.get_card("KC"))
    print(result)
    print(non_shuffled_state)

    result = non_shuffled_state.play(libbisca.get_card("7C"))
    print(result)
    print(non_shuffled_state)

    print()

    state = libbisca.get_state()
    print(state)

    while not state.is_endgame():
        results = state.play(state.legal_moves[0])
        # move, results = state.do_random_move()
        print(results)
        print(state)

    print()

    print(state.legal_moves)
    print(state.is_endgame())
    print(state.get_winner())
    print()

    state = libbisca.get_state()
    print(state)
    state.do_random_rollout()
    print(state)


if __name__ == "__main__":
    main()

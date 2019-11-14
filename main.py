# -*- coding: utf-8 -*-

from libbisca import Deck, get_state


def main():
    d = Deck()
    print("deck:", d)
    print()

    s = get_state()
    print("init state:", s)
    print()

    s.do_random_rollout()
    print("termianl state:", s)
    print()

    s = get_state()
    while not s.is_endgame():
        print("state:", s)
        print("move, result:", s.do_random_move())
    print("state:", s)
    print()


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

from libbisca import Deck, get_state


def main():
    d = Deck()
    print(d)
    print()

    s = get_state()
    print(s)
    print()

    s.do_random_rollout()
    print(s)
    print()


if __name__ == "__main__":
    main()

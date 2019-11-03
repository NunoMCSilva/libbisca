# TODO

## TODO
### PyCharm
- check how to remove DeprecationWarning on pytest running (with cov, mypy)

### card
- random: research issues with shuffle, 40 may not be an issue for PRNG (2048 would), and see sample

## maybe TODO
### card
- consider Deck(list) with bottom and take from top, still not convinced
- ShuffledDeck type? Deck is only really used in testing
- sorted(deck) rets 2C, 2D, 2S, 2H, etc... (not guarantee on suit order(recheck)) - important to correct?
- add old sota card history (old pt deck)?

### unit/test_card
- add py.mark.para for more cases?
- do magic methods need "->" in typing?

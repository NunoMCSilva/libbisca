# TODO

## TODO
### ALL
- what is the issue with relative imports? -- check

### PyCharm
- check how to remove DeprecationWarning on pytest running (with cov, mypy)

### card
- random: research issues with shuffle, 40 may not be an issue for PRNG (2048 would), and see sample(pop, len(k))

## maybe TODO
### card
- consider Deck(list) with bottom and take from top, still not convinced
- ShuffledDeck type? Deck is only really used in testing
- sorted(deck) rets 2C, 2D, 2S, 2H, etc... (not guarantee on suit order(recheck)) - important to correct?
- add old sota card history (old pt deck)?
- self.piles = {player: [] for player in Player}
- ok, it might be better to have the card factory as a method (import Card) and get_deck can also be there...
- decide if I want the factory functions/methods to be inside or outside (or as are), until then stop moving them!
- if get_card is a factory function (check) then never access Card directly? (only for get_deck?)

### unit/test_card
- add py.mark.para for more cases?
- do magic methods need "->" in typing?
- test_card: sorted is uncertain here - unimportant for now -- fix this in card

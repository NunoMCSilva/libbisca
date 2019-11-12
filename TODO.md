# TODO

## TODO
### ALL
- what is the issue with relative imports? -- check

### mypy
- why does the pytest run show the error but doesn't stop build -- how to signal

### PyCharm
- check how to remove DeprecationWarning on pytest running (with cov, mypy)

### libbisca/__init__.py
- check __all__ usage and significance

### libbisca/card
- random: research issues with shuffle, 40 may not be an issue for PRNG (2048 would), and see sample(pop, len(k))
- ONLY CHANGE CARD IF: random research, docstring fix, major problem, added function

## maybe TODO
### libbisca/card.py
- maybe add a pprint option to deck

### tests/unit/test_state.py
- TestDeck.DECK - just put this in a separate module/fixture accessible to both test_state and test_card?
- add cards in table count? and table_played? those are internal implementation details...
- while the load fixtures part are very interesting, I'm having some issues implementing them... hmmm - start with load_json_state? that might make testing easier


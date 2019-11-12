# TODO


## TODO
### ALL
- what is the issue with relative imports? -- check
- check Google/realpython guidelines on documentation (and check how to generate it)

### mypy
- why does the pytest run show the error but doesn't stop build -- how to signal -- ok, I can see why it doesn't stop

### PyCharm
- check how to remove DeprecationWarning on pytest running (with cov, mypy)

### libbisca/__init__.py
- check __all__ usage and significance

### libbisca/card
- random: research issues with shuffle, 40 may not be an issue for PRNG (2048 would), and see sample(pop, len(k))
- ONLY CHANGE CARD IF: random research, docstring fix, major problem, added function

### libbisca/state
- run_games -- need ObservedState part, check


## maybe TODO
### libbisca/card.py
- maybe add a pprint option to deck

### libbisca/state.py
- self.table could hold both, but that would allow the outside to glimpse implementation details
- self._cards_in_stock_and_hands = len(self.stock) + etc...
- self._table_played: List[Player] = []   # TODO: doesn't really seem necessary, except for speed?

### tests/unit/test_agent.py
- test RandomAgent.get_move

### tests/unit/test_card.py
- check missing tests

### tests/unit/test_state.py
- TestDeck.DECK - just put this in a separate module/fixture accessible to both test_state and test_card?
- add cards in table count? and table_played? those are internal implementation details...
- while the load fixtures part are very interesting, I'm having some issues implementing them... hmmm - start with load_json_state? that might make testing easier
- add test: is_endgame
- add test: legal_moves
- add test: get_winner
- add test: do_random_move
- add test: do_random_rollout
- add test: get_state
- add test: run_games

### other
- check mypy, pytest-mypy for better usage
- check if hypothesis is actually useful here
- check pyreverse (in pylint)

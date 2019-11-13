# TODO

## All
### TODO
- what is the issue with relative imports? -- check
- check Google/realpython guidelines on documentation (and check how to generate it)
- review all typing
- check assumptions I'm making that all states will share a lot with abcState
### Maybe TODO
- really need to check how to work with pyi (less imports in code) -- PyCharm and mypy warning like now?
- all the PyCharm warnings
- check how do parametrized fixture (available?)

## PyCharm
### Maybe TODO
- check how to remove DeprecationWarning on pytest running (with cov, mypy)

## card.py
### TODO
- random: research issues with shuffle, 40 may not be an issue for PRNG (2048 would), and see sample(pop, len(k))

## state.py
### TODO
- is_load a good idea, check how to do it better (best practices)
### Maybe TODO:
- add dealt_card to playerstate?
- add remove_card to playerstate?
- equivalent of PlayerState in json or just keep it simple?
- player: Player      # seems unnecessary?




# OLD
## TODO
### mypy
- why does the pytest run show the error but doesn't stop build -- how to signal -- ok, I can see why it doesn't stop, but better showing?


### libbisca/__init__.py
- check __all__ usage and significance

### libbisca/card
- ONLY CHANGE CARD IF: random research, docstring fix, major problem, added function

### libbisca/state
- run_games -- need ObservedState part, check
- # TODO: encapsulate Player and next_player into class? how? Player(Enum) doesn't work for what I want


## maybe TODO
### ALL
- how to implement weird stuff (like 2 decks, 3 card, 2 players, standard rules) -- needed?

### libbisca/card.py
- maybe add a pprint option to deck
- does shuffle need to public?

### libbisca/state.py
- self.table could hold both, but that would allow the outside to glimpse implementation details
- self._cards_in_stock_and_hands = len(self.stock) + etc...
- self._table_played: List[Player] = []   # TODO: doesn't really seem necessary, except for speed?
- put load_fron_json @ module level 
- a player class might be useful
- are piles really useful? (except in the sense of history?)
- for player in range(num_players):   # definition of clockwise... hmmm
- Dict hands, etc.        # TODO: with different player, may be List

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

# TODO

## All
### TODO
- release code as is as 0.1.0 -- without agent
- what is the issue with relative imports? -- check
- check Google/realpython guidelines on documentation (and check how to generate it)
- review all typing
- check assumptions I'm making that all states will share a lot with abcState
- add profiling
### Maybe TODO
- really need to check how to work with pyi (less imports in code) -- PyCharm and mypy warning like now?
- all the PyCharm warnings
- check how do parametrized fixture (available?)
- ~~how to implement weird stuff (like 2 decks, 3 card, 2 players, standard rules) -- needed? NO~~

## __init__.py
### TODO
- check __all__ usage and significance

## agent.py
### TODO
- run_games -- need ObservedState part, check

## card.py
### TODO
- random: research issues with shuffle, 40 may not be an issue for PRNG (2048 would), and see sample(pop, len(k))
- ONLY CHANGE CARD IF: random research, docstring fix, major problem, added function
### Maybe TODO
- maybe add a pprint option to deck
- ~~does shuffle need to public?~~
- put get_card, get_cards in Card?

## state.py
### TODO
- is_load a good idea, check how to do it better (best practices)
### Maybe TODO:
- load_state might be useful for agent testing... observerstate?
- add dealt_card to playerstate?
- add remove_card to playerstate?
- ~~equivalent of PlayerState in json or just keep it simple?~~
- ~~player: Player in playerstate      # seems unnecessary?~~
- I think I'm assuming a lot about no diff between State and regular rules...
- are piles really useful? (except in the sense of history?)
- speed: self._cards_in_stock_and_hands = len(self.stock) + etc...
- speed: self._table_played: List[Player] = []   # TODO: doesn't really seem necessary, except for speed?
- put get_state, load_state in State?
- put playerstate inside State?

## tests
### TODO
- check missing tests -- check coverage

## PyCharm
### Maybe TODO
- check how to remove DeprecationWarning on pytest running (with cov, mypy)

## mypy
### Maybe TODO
- why does the pytest run show the error but doesn't stop build -- how to signal -- ok, I can see why it doesn't stop, 
but better showing at end? hmmm

## other
### Maybe TODO
- check mypy, pytest-mypy for better usage
- check if hypothesis is actually useful here
- check pyreverse (in pylint)

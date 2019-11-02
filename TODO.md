TODO
----

# TODO
ALL:
* what is the issue with relative imports? -- check
* check separation of concerns -- each class/module has 1 specific function/objective
* due to implementation, game rules are a bit spread out (part in Rank (was), part in Card, Trump, Deck, State) -- hmmm -- put score back in Rank
* project philosophy: clear code beats optimization? add optimized class later?

card:
* Card: same type, different suits: still compare rank (the not following part is state's responsibility)


state:
* follow is not mandatory, but if youngest plays a different suit than is not trump, eldest wins -- check this rule
* complete/fix docstring (check google recs first)

# Maybe TODO
__init__:
* is __all__ really needed or... (maybe restrict what can be accessed?) -- CHECK

card
* join both \__gt__ to a call to a single func?
* add module level _DECK or modify cards to always return a singleton value on start (Card and _Card?) -- saves memory and possible speed 
* it would be nice if instead of get_card I could just use Card.\__init__ for both cases... check that
* add more documentation
* add story about sotas in old portuguese cards
* score implementation in Card.score or in Rank.score?
* Rank.__str, format & in suit -- check what is really needed
* do I really need to unicode chars or just do without, hmmm, uglier, but
* Rank.DECK_ORDER __ could use Rank._STR_TO_RANK.values() here? -- check
* put TrumpCard inside Card?
* check https://stackoverflow.com/questions/17911188/is-it-possible-to-define-a-class-constant-inside-an-enum to see other ways to handle the constants in enums 
* better name than trumpify
* Deck already does the trumpify all trumps thing, so Deck knows trump... why replicate in State -- or just do the signal all, etc in State
*     #def __hash__(self):
        #return hash((self.rank, self.suit)) -- add? check for class
* Player:    # TODO: why is this not working in __str__?
    def __str__(self):
        return "North" if self.value == Player.NORTH else "South"

test_card:
* test__gt_two_cards__return_expected_bool -- the comments 2D(t) > 7C could be used as testing instead of the rest?
* add is_trump test?
* add __hash__ test?
* no need to test Deck.bottom and Deck.pop
* add trumpify test
* assert len(self.stock) == 40    # TODO: put in constant -- OR ADD TESTs TO DECK
* add test for bottom

state:
* add more than 2 players option?
* put state as abstract, with StateVariant1 (or something) being implementation?
* self.turn.opponent): (dealcards) -- PyCharm should have signaled this before I implemented opponent
* on self.hands[self.turn].remove wouldn't a better exception here would be IllegalMove?
* if len(self.table) == 1 - better system?
* added_score ret -- negative (might be better as positive)
* should I keep single score, I mean (south - north) is useful to check who is winning, but a check at self.scores[self.winner] might be... hmmm this isbetter
* add tournament_score
* see if IntEnum can inherit from another IntEnum (Winner, Player)
* if stock exists, deal cards -- TODO: put in deal cards? (ignores call if stock doesn't exist)
* add other variants (that one that enforces follows after self.stock is empty) -- mandatory to play this cards | place to add follow variant (diff class?)
* with this rules, good idea to put a get_possible_moves to state? -- useful for engines
* __str__ improve this (pretty print?)
* __repr__ add _scores
* Player: test for repr/str -- necessary
* add assert sum(scores) == 120 to end (works with only 1 deck, but...) hmmm
* property: tournament_score -- specific to variant?
* still not sure score is needed... 
* is     def __hash__(self) necessary -- check how to implemented it well

test_state:
* expected_stock appears a few times, put in constant somewhere?
* add state fixture (ret initialized state)
* play may need to return table for engines (or something like that...) -- add now and remove later if needed
* variant play would need to override play (and new _get_round_winner)
* def test__play__after_first_four_moves__runs_correctly(self, mocker): -- join with previous two (same idea)
* add test for State.__init__ with hand_size=7 and 9
* add test for State.play - trying at endgame
* merge tests for winner and score

LICENSE.md:
* change license to LGPL?

README.md:
* add thanks to Sandi Metz for me finally understanding anything about tests

-------------
- hmmm, Game(State)?
## before current refactoring
# TODO
- state.score and state.get_score is too complex 
(code-wise), fix that
- add logging
- check what the issue is with relative imports (PyCharm?)
- need to add lots of tests for agents, dev, game
- check Documenting Python Code for google to docs

# Maybe TODO

- agent.py: add Agent.name (class nickname, useful 
to show in gui -- just do it in gui)?
- agent.py: add state.hand to State?
- is pytest-benchmarks all that useful here?
- .travis.yml -- current install might be replaced by 
pip install ".[test]" in the future
- add a main that runs code with some prints?
- add demo,
- add printv
- state.hands - might be replaced with hand (hands[turn])
- state.score - might be better just to have south 
score, simpler
- state.NUM_PLAYERS -- think about it 
- state.HAND_SIZE -- think about it
- state.opponent -- handle properties in documentation
- setup.py - Framework :: Hypothesis
- check flit (and pyproject.toml), etc. later -- for now just use twine
- check where to put .pypirc

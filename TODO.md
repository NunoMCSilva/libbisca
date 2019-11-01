TODO
----

# TODO
- state.score and state.get_score is too complex 
(code-wise), fix that
- add logging
- check what the issue is with relative imports (PyCharm?)
- need to add lots of tests for agents, dev, game
- check Documenting Python Code for google to docs

# Maybe TODO
- card.py: put TrumpCard inside Card?
- agent.py: add Agent.name (class nickname, useful 
to show in gui -- just do it in gui)?
- agent.py: add state.hand to State?
- is pytest-benchmarks all that useful here?
- .travis.yml -- current install might be replaced by 
pip install ".[test]" in the future
- change license to LGPL?
- add a main that runs code with some prints?
- state.hands - might be replaced with hand (hands[turn])
- state.score - might be better just to have south 
score, simpler
- state.NUM_PLAYERS -- think about it 
- state.HAND_SIZE -- think about it
- state.opponent -- handle properties in documentation

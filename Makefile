PE = pipenv
PER = $(PE) run

nothing:

unittests:
	$(PER) pytest tests/unit/

black:
	$(PER) black .

cov:
	$(PER) pytest --cov=bisca tests/unit/

PE = pipenv
PER = $(PE) run

nothing:

unittests:
	$(PER) pytest tests/unit/

black:
	$(PER) black .

cov:
	$(PER) pytest --cov=bisca tests/unit/

mypy:
	$(PER) pytest --mypy -m mypy tests/unit/test_*.py

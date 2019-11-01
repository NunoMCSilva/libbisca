PE = pipenv
PER = $(PE) run

init:
	$(PE) install --dev

black:
	$(PER) black -tpy37 .

unittest:
	$(PER) pytest tests/unit

test: black unittest

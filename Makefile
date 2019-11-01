PE = pipenv
PER = $(PE) run

nothing:

install:
	$(PE) install --dev

black:
	$(PER) black -tpy37 .

unittest:
	$(PER) pytest tests/unit/

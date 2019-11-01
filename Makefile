PE = pipenv
PER = $(PE) run

init:
	$(PE) install --dev

black:
	$(PER) black -tpy37 .

unit:
	$(PER) pytest tests/unit

integration:
	$(PER) pytest tests/unit

test: black unit

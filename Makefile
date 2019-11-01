PE = pipenv
PER = $(PE) run

init:
	$(PE) install --dev

black:
	$(PER) black -tpy37 .

unit: black
	$(PER) pytest tests/unit

integration: black
	$(PER) pytest tests/integration

test: black
	$(PER) pytest tests

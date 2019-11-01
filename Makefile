PE = pipenv
PER = $(PE) run

nothing:

unit:
	$(PER) pytest tests/unit/

cov:
	$(PER) pytest --cov=libbisca tests/unit/

black:
	$(PER) black -tpy37 .





integration:
	$(PER) pytest --benchmark-skip tests/integration/



mypy:
	$(PER) pytest --mypy -m mypy tests/unit/test_*.py

profile:
	$(PER) python do_profile.py

benchmark:
	#$(PER) pytest --benchmark-only --benchmark-histogram tests/integration/
	$(PER) pytest --benchmark-only --benchmark-compare tests/integration/

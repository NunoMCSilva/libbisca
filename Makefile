PROJ = libbisca
PE = pipenv
PER = $(PE) run

init:
	$(PE) install --dev

black:
	$(PER) black -tpy37 .


# tests
unit:
	$(PER) pytest --cov=$(PROJ) --mypy tests/unit

mypy:
	$(PER) mypy -p $(PROJ)


# PyPI
build:
	$(PER) python setup.py sdist bdist_wheel

upload: build
	$(PER) twine upload --repository-url https://test.pypi.org/legacy/ dist/*

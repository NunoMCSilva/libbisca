PROJ = libbisca
PE = pipenv
PER = $(PE) run

init:
	$(PE) install --dev

black:
	$(PER) black -tpy37 .


# tests
unit:
	$(PER) pytest tests/unit

integration:
	$(PER) pytest tests/integration

test:
	$(PER) pytest tests

cov:
	$(PER) pytest --cov=$(PROJ) tests

mypy:
	$(PER) mypy -p $(PROJ)


# PyPI
build:
	python setup.py sdist bdist_wheel

upload: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

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


# PyPI
build:
	python setup.py sdist bdist_wheel

upload: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

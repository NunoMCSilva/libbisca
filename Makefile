PE = pipenv
PER = $(PE) run

init:
	$(PE) install --dev

black:
	$(PER) black -tpy37 .

unit:
	$(PER) pytest tests/unit

integration:
	$(PER) pytest tests/integration

test:
	$(PER) pytest tests

cov:
	$(PER) pytest --cov=libbisca tests

build:
	$(PER) python setup.py sdist bdist_wheel

upload: build
	$(PER) twine upload --repository-url https://test.pypi.org/legacy/ dist/*

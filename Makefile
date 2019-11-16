PROJ = libbisca
PE = pipenv
PER = $(PE) run

# install test dependencies
install:
	$(PE) install --dev

# apply code style
black:
	$(PER) black -tpy37 .

# unit tests (with mypy and coverage)
unit:
	$(PER) pytest --cov=$(PROJ) --mypy tests/unit

# build package
build:
	$(PER) python setup.py sdist bdist_wheel

# upload to test pypi
upload: build
	$(PER) twine upload --repository-url https://test.pypi.org/legacy/ dist/*

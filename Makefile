.PHONY: init qa lint tests spec coverage


init:
	pipenv install --three --dev


# DEVELOPMENT
# ~~~~~~~~~~~
# The following rules can be used during development in order to get a Python shell, etc.
# --------------------------------------------------------------------------------------------------

shell:
	pipenv run ipython


# QUALITY ASSURANCE
# ~~~~~~~~~~~~~~~~~
# The following rules can be used to check code quality, import sorting, etc.
# --------------------------------------------------------------------------------------------------

qa: lint isort

# Code quality checks (eg. flake8, eslint, etc).
lint:
	pipenv run flake8

# Import sort checks.
isort:
	pipenv run isort --check-only --recursive --diff flinks tests


# TESTING
# ~~~~~~~
# The following rules can be used to trigger tests execution and produce coverage reports.
# --------------------------------------------------------------------------------------------------

# Just runs all the tests!
tests:
	pipenv run py.test

# Collects code coverage data.
coverage:
	pipenv run py.test --cov-report term-missing --cov flinks

# Run the tests in "spec" mode.
spec:
	pipenv run py.test --spec -p no:sugar

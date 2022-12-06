clean:
	rm -rf .venv mercado_bictoin/day-summary mercado_bictoin/*.checkpoint .pytest_cache .coverage mercado_bictoin/.pytest_cache mercado_bictoin/.coverage

init: clean
	pip install poetry
	poetry install

test:
	poetry run python -m pytest


## CI/CD
ci-test:
	poetry run python -m pytest
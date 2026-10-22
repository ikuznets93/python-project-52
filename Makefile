install:
	uv sync

lint:
	uv run ruff check

test:
	uv run manage.py test

test-coverage:
	uv run coverage xml

check: lint test
setup: prepare install build-css prepare-db

prepare:
	cp -n .env.example .env

install:
	uv sync

build-css:
	uv run python manage.py tailwind build --force

prepare-db:
	uv run python manage.py migrate

serve:
	uv run python manage.py runserver 0.0.0.0:8000

shell:
	uv run python manage.py shell

lint:
	uv run ruff check

test:
	uv run manage.py test

test-coverage:
	uv run coverage run manage.py test task_manager
	uv run coverage xml
	uv run coverage report

check: lint test

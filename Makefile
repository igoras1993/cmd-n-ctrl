# Repository things
init: poetry-dev hooks env

poetry-dev:
	poetry config virtualenvs.in-project true --local
	poetry install --with=dev --with=test

hooks:
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg

env:
	cp .env.example .env

# Database things
test-db:
	docker compose -f compose.local-db.yaml up -d

stop-test-db:
	docker compose -f compose.local-db.yaml down

clear-test-db:
	docker compose -f compose.local-db.yaml down -v

logs-db:
	docker compose -f compose.local-db.yaml logs -f

migrate-head:
	cd src/alembic && \
		PYTHONPATH=./.. poetry run alembic \
		-c ./alembic.ini upgrade head

migrate-down:
	cd src/alembic && \
		PYTHONPATH=./.. poetry run alembic \
		-c ./alembic.ini downgrade -1

migrate-up:
	cd src/alembic && \
		PYTHONPATH=./.. poetry run alembic \
		-c ./alembic.ini upgrade +1

migrate-clear:
	cd src/alembic && \
		PYTHONPATH=./.. poetry run alembic \
		-c ./alembic.ini downgrade base

MESSAGE?=auto

migrate-generate:
	cd src/alembic && \
		PYTHONPATH=./.. poetry run alembic \
		-c ./alembic.ini revision \
		--autogenerate \
		-m $(MESSAGE)


# Entrypoints
asgi:
	cd src && PYTHONPATH=. poetry run python3 entrypoints/asgi_dev.py

# TODO: Contribute to watchdog to add --start-first
# 	https://github.com/gorakhargosh/watchdog/issues/301
tui-dev:
#	bash -c "sleep 1 && touch ./src/cnc/__init__.py" &
#	poetry run watchmedo shell-command --patterns='*.py;*.txt;*.tcss' --recursive --command="poetry run textual run --dev src/entrypoints/tui.py" ./src/cnc
	poetry run src/entrypoints/tui.py

# Code things
static-check: style-check type-check

type-check:
	poetry run pyright

style-check:
	poetry run flake8 --verbose src

format:
	poetry run black .


# Testing things
test: test-pytest
VCR_RECORD?=none

test-pytest:
	poetry run pytest --vcr-record=$(VCR_RECORD) src/tests

test-bdd:
	poetry run pytest src/tests/behavioral/

check-all: style-check type-check format test-pytest


# Docs
changelog:
	poetry run git-cliff --prepend CHANGELOG.md --tag ${NEW_TAG} ${LAST_TAG}..HEAD


# Containerization things
local-start: compose-up migrate-head

local-start-fresh: compose-build-fresh compose-up migrate-head

local-clear: compose-clear

local-stop: compose-down

local-logs:
	docker compose -f compose.local-build.yaml -f compose.local-db.yaml logs -f

compose-build:
	docker compose -f compose.local-build.yaml build

compose-build-fresh:
	docker compose -f compose.local-build.yaml build --no-cache

compose-build-verbose:
	docker compose -f compose.local-build.yaml build --no-cache --progress=plain

compose-up:
	docker compose -f compose.local-build.yaml -f compose.local-db.yaml up -d && \
		sleep 2

compose-down:
	docker compose -f compose.local-build.yaml -f compose.local-db.yaml down

compose-clear:
	docker compose -f compose.local-build.yaml -f compose.local-db.yaml down -v

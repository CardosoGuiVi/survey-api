.PHONY: fmt lint typecheck db-check db-check-test db-up db-down db-test-up db-test-down check check-test

fmt:
	ruff format .

lint:
	ruff check .

typecheck:
	mypy app/ tests/

db-check:
	alembic check

db-check-test:
	uv run --env-file .env.test alembic check

db-up:
	docker compose up -d database

db-down:
	docker compose down database

db-test-up:
	docker compose --env-file .env.test up -d database-test

db-test-down:
	docker compose down -v database-test

check: fmt lint typecheck db-check

check-test: fmt lint typecheck db-check-test
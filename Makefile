.PHONY: fmt lint typecheck db-check db-test-up db-test-down check

fmt:
	ruff format .

lint:
	ruff check .

typecheck:
	mypy app/ tests/

db-check:
	alembic check

db-test-up:
	docker compose --env-file .env.test up -d database-test

db-test-down:
	docker compose down -v

check: fmt lint typecheck db-check
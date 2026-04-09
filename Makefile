.PHONY: lint typecheck check fmt and db-check

fmt:
	ruff format .

lint:
	ruff check .

typecheck:
	mypy app/ tests/

db-check:
	alembic check

check: fmt lint typecheck db-check
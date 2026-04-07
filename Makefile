.PHONY: lint typecheck check fmt

fmt:
	ruff format .

lint:
	ruff check .

typecheck:
	mypy app/

check: fmt lint typecheck
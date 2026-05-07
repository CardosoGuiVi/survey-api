# survey-api

Backend of a multi-tenant SaaS for internal surveys and organizational management, built with FastAPI and PostgreSQL.

## Stack

- **Python 3.12** with strict typing via mypy
- **FastAPI** — asynchronous web framework
- **SQLAlchemy 2.0** — async ORM with asyncpg
- **Alembic** — versioned migrations
- **PostgreSQL 16** — primary database with native triggers
- **pytest + pytest-asyncio** — integration and unit tests
- **uv** — dependency and virtual environment management
- **ruff** — linting and formatting
- **pre-commit** — code quality before each commit
- **GitHub Actions** — CI with lint, typecheck and tests

## Architecture

```
app/
├── api/v1/          # FastAPI routers by domain
├── core/            # config, database, dependencies, security
├── models/          # SQLAlchemy models by domain
├── schemas/         # Pydantic schemas (request/response)
└── services/        # business logic by domain
```

Clear separation between layers: the router orchestrates, the service decides, the model persists. Pydantic schemas never leak into the persistence layer.

## Domains

### Auth
Email/password authentication with JWT. Multi-tenant workspaces created on registration. Google OAuth federated login prepared in the data model (`employee_identities`).

### Org Chart (HRIS)
Complete org chart modeling with separation between structure and people:

- **`departments`** — team hierarchy with self-reference
- **`positions`** — org chart seats, exist independently of whether they are filled
- **`jobs`** — formal HR classification (title, family, level)
- **`employees`** — people, with email and alias for federated login
- **`position_assignments`** — who occupies which seat and when
- **`job_history`** — career track evolution independent of position
- **`employee_events`** — complete timeline with event sourcing (`HIRED`, `REHIRED`, `RESIGNED`, `TERMINATED`, `DECEASED`, `POSITION_CHANGED`, `ROLE_CHANGED`, `BECAME_LEADER`, `LEFT_LEADERSHIP`)

The employee status (`active`, `inactive`, `on_leave`) is automatically updated via a PostgreSQL trigger on event insertion — without relying on the application to maintain consistency.

## Key Technical Decisions

**Position vs Job** — the org chart seat (`position`) is separated from the formal HR classification (`job`). A person can be "Head of People Tech" (position) with the formal title "Data Manager I" (job), reflecting the reality of organizations.

**Privacy by design** — the `user_id` is never stored in survey responses. Only an irreversible HMAC-SHA256 token is persisted for deduplication.

**Trigger for consistency** — the employee status is maintained by a PostgreSQL trigger, not by the application. Guarantees consistency even on direct database operations.

**`event.listen` removed** — triggers are created exclusively via Alembic. SQLAlchemy's `event.listen` was discarded because it only works with `create_all`, which is not used in production.

**Alembic as the single source of truth** — `conftest.py` runs real migrations before tests, not `Base.metadata.create_all`. Tests reflect exactly the production state.

## Local Setup

**Requirements:** Python 3.12, Docker, uv

```bash
# install dependencies
uv sync

# start database
docker compose --env-file .env up -d db

# run migrations
uv run alembic upgrade head

# start server
uv run fastapi dev app/main.py
```

## Tests

```bash
# all tests
uv run --env-file .env.test pytest

# integration only
uv run --env-file .env.test pytest -m integration

# unit only
uv run pytest -m unit

# with coverage
uv run --env-file .env.test pytest --cov=app --cov-report=term-missing
```

## CI

Each PR goes through three mandatory gates before merging:

1. **Lint** — ruff check + ruff format
2. **Typecheck** — mypy strict
3. **Tests** — pytest with minimum 70% coverage
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from app.core.config import settings


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")

    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


@pytest.fixture(scope="function")
async def engine():
    engine = create_async_engine(
        settings.database.uri,
        future=True,
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(engine):
    async with engine.connect() as connection:
        transaction = await connection.begin()

        session = AsyncSession(bind=connection)

        await session.begin_nested()

        yield session

        await session.close()
        await transaction.rollback()

import pytest
from sqlalchemy import inspect


@pytest.mark.integration
async def test_jobs_table_exists(engine):
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    assert "jobs" in tables

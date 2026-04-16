import pytest
from sqlalchemy import inspect


@pytest.mark.integration
async def test_jobs_table_exists(engine):
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    assert "jobs" in tables


@pytest.mark.integration
async def test_department_table_exists(engine):
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    assert "departments" in tables


@pytest.mark.integration
async def test_position_table_exists(engine):
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    assert "positions" in tables


@pytest.mark.integration
async def test_employee_table_exists(engine):
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    assert "employees" in tables


@pytest.mark.integration
async def test_employee_identity_table_exists(engine):
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    assert "employee_identities" in tables


@pytest.mark.integration
async def test_position_assignment_table_exists(engine):
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    assert "position_assignments" in tables


@pytest.mark.integration
async def test_job_history_table_exists(engine):
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    assert "job_history" in tables


@pytest.mark.integration
async def test_employee_event_exists(engine):
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
    assert "employee_events" in tables

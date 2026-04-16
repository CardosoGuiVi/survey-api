import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.org import (
    Job,
    JobHistory,
)
from app.schemas.org import (
    JobHistoryCreate,
    JobHistoryUpdate,
)
from app.schemas.org.job import JobCreate, JobUpdate


async def create_job(session: AsyncSession, payload: JobCreate) -> Job:
    job = Job(**payload.model_dump())
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job


async def list_jobs(session: AsyncSession) -> Sequence[Job]:
    result = await session.execute(select(Job))
    return result.scalars().all()


async def get_job(session: AsyncSession, job_id: uuid.UUID) -> Job | None:
    return await session.get(Job, job_id)


async def update_job(session: AsyncSession, job: Job, payload: JobUpdate) -> Job:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    await session.commit()
    await session.refresh(job)
    return job


async def delete_job(session: AsyncSession, job: Job) -> None:
    await session.delete(job)
    await session.commit()


async def create_job_history(
    session: AsyncSession, payload: JobHistoryCreate
) -> JobHistory:
    job_history = JobHistory(**payload.model_dump())
    session.add(job_history)
    await session.commit()
    await session.refresh(job_history)
    return job_history


async def list_job_history(
    session: AsyncSession, employee_id: uuid.UUID
) -> Sequence[JobHistory]:
    result = await session.execute(
        select(JobHistory).where(JobHistory.employee_id == employee_id)
    )
    return result.scalars().all()


async def get_job_history(
    session: AsyncSession, job_history_id: uuid.UUID
) -> JobHistory | None:
    return await session.get(JobHistory, job_history_id)


async def close_job_history(
    session: AsyncSession, job_history: JobHistory, payload: JobHistoryUpdate
) -> JobHistory:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(job_history, field, value)
    await session.commit()
    await session.refresh(job_history)
    return job_history

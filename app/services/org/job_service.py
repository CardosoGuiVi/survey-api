import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.org import (
    Job,
)
from app.schemas.org import (
    JobCreate,
    JobUpdate,
)


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

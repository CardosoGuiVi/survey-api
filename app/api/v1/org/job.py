# app/api/v1/org.py
import uuid
from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.org import Job, JobHistory
from app.schemas.org import (
    JobCreate,
    JobHistoryCreate,
    JobHistoryResponse,
    JobHistoryUpdate,
    JobResponse,
    JobUpdate,
)
from app.services.org import job_service

router = APIRouter()


@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: JobCreate,
    session: AsyncSession = Depends(get_session),
) -> Job:
    return await job_service.create_job(session, payload)


@router.get("/jobs", response_model=list[JobResponse])
async def list_jobs(
    session: AsyncSession = Depends(get_session),
) -> Sequence[Job]:
    return await job_service.list_jobs(session)


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> Job:
    job = await job_service.get_job(session, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    return job


@router.patch("/jobs/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: uuid.UUID,
    payload: JobUpdate,
    session: AsyncSession = Depends(get_session),
) -> Job:
    job = await job_service.get_job(session, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    return await job_service.update_job(session, job, payload)


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> None:
    job = await job_service.get_job(session, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    await job_service.delete_job(session, job)


@router.post(
    "/job-history",
    response_model=JobHistoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_job_history(
    payload: JobHistoryCreate,
    session: AsyncSession = Depends(get_session),
) -> JobHistory:
    return await job_service.create_job_history(session, payload)


@router.get(
    "/employees/{employee_id}/job-history", response_model=list[JobHistoryResponse]
)
async def list_job_history(
    employee_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> Sequence[JobHistory]:
    return await job_service.list_job_history(session, employee_id)


@router.patch("/job-history/{job_history_id}", response_model=JobHistoryResponse)
async def close_job_history(
    job_history_id: uuid.UUID,
    payload: JobHistoryUpdate,
    session: AsyncSession = Depends(get_session),
) -> JobHistory:
    job_history = await job_service.get_job_history(session, job_history_id)
    if not job_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job history not found"
        )
    return await job_service.close_job_history(session, job_history, payload)

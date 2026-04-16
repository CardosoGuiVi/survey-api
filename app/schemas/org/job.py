import uuid
from datetime import datetime

from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    family: str
    level: str


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: str | None = None
    family: str | None = None
    level: str | None = None


class JobResponse(JobBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class JobHistoryBase(BaseModel):
    employee_id: uuid.UUID
    job_id: uuid.UUID
    started_at: datetime


class JobHistoryCreate(JobHistoryBase):
    pass


class JobHistoryUpdate(BaseModel):
    ended_at: datetime | None = None


class JobHistoryResponse(JobHistoryBase):
    id: uuid.UUID
    ended_at: datetime | None = None

    model_config = {"from_attributes": True}

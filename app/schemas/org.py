# app/schemas/org.py
import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.org import EmployeeStatus, EventType


# Job
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


# Department
class DepartmentBase(BaseModel):
    name: str
    parent_department_id: uuid.UUID | None = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str | None = None
    parent_department_id: uuid.UUID | None = None


class DepartmentResponse(DepartmentBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# Position
class PositionBase(BaseModel):
    name: str
    department_id: uuid.UUID | None = None
    parent_position_id: uuid.UUID | None = None
    is_active: bool = True


class PositionCreate(PositionBase):
    pass


class PositionUpdate(BaseModel):
    name: str | None = None
    department_id: uuid.UUID | None = None
    parent_position_id: uuid.UUID | None = None
    is_active: bool | None = None


class PositionResponse(PositionBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# Employee
class EmployeeBase(BaseModel):
    full_name: str
    email: str
    email_alias: str | None = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    email_alias: str | None = None
    status: EmployeeStatus | None = None


class EmployeeResponse(EmployeeBase):
    id: uuid.UUID
    status: EmployeeStatus
    created_at: datetime

    model_config = {"from_attributes": True}


# EmployeeIdentity
class EmployeeIdentityBase(BaseModel):
    employee_id: uuid.UUID
    provider: str
    provider_sub: str
    provider_email: str


class EmployeeIdentityCreate(EmployeeIdentityBase):
    pass


class EmployeeIdentityResponse(EmployeeIdentityBase):
    id: uuid.UUID
    linked_at: datetime

    model_config = {"from_attributes": True}


# PositionAssignment
class PositionAssignmentBase(BaseModel):
    position_id: uuid.UUID
    employee_id: uuid.UUID
    started_at: datetime


class PositionAssignmentCreate(PositionAssignmentBase):
    pass


class PositionAssignmentUpdate(BaseModel):
    ended_at: datetime | None = None


class PositionAssignmentResponse(PositionAssignmentBase):
    id: uuid.UUID
    ended_at: datetime | None = None

    model_config = {"from_attributes": True}


# JobHistory
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


# EmployeeEvent
class EmployeeEventBase(BaseModel):
    employee_id: uuid.UUID
    position_id: uuid.UUID | None = None
    type: EventType
    event_metadata: dict[str, str] | None = None
    occurred_at: datetime
    notes: str | None = None


class EmployeeEventCreate(EmployeeEventBase):
    pass


class EmployeeEventResponse(EmployeeEventBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}

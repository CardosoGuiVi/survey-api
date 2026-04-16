import uuid
from datetime import datetime

from pydantic import BaseModel


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

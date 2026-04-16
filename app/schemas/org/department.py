# app/schemas/org.py
import uuid
from datetime import datetime

from pydantic import BaseModel


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

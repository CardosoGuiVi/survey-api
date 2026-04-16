# app/schemas/org.py
import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.org import EmployeeStatus


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

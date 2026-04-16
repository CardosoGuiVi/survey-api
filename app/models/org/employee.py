import uuid
from datetime import datetime
from enum import StrEnum, auto

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class EmployeeStatus(StrEnum):
    active = auto()
    inactive = auto()
    on_leave = auto()


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    full_name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(255), nullable=False, unique=True)
    email_alias: Mapped[str | None] = mapped_column(
        sa.String(255),
        nullable=True,
        unique=True,
    )
    status: Mapped[EmployeeStatus] = mapped_column(
        sa.Enum(EmployeeStatus, name="employee_status"),
        nullable=False,
        default=EmployeeStatus.active,
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    )

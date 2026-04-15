import uuid
from datetime import datetime
from enum import StrEnum, auto

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class EventType(StrEnum):
    hired = auto()
    rehired = auto()
    resigned = auto()
    terminated = auto()
    deceased = auto()
    position_changed = auto()
    role_changed = auto()
    became_leader = auto()
    left_leadership = auto()


class EmployeeEvent(Base):
    __tablename__ = "employee_events"

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        sa.ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=False,
    )
    position_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.UUID(as_uuid=True),
        sa.ForeignKey("positions.id", ondelete="SET NULL"),
        nullable=True,
    )
    type: Mapped[EventType] = mapped_column(
        sa.Enum(EventType, name="event_type"),
        nullable=False,
    )
    event_metadata: Mapped[dict[str, str] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(
        sa.Text,
        nullable=True,
    )

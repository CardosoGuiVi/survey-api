import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class EmployeeIdentity(Base):
    __tablename__ = "employee_identities"

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        sa.ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )
    provider: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    provider_sub: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    provider_email: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    linked_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    )

    __table_args__ = (
        sa.UniqueConstraint(
            "provider", "provider_sub", name="uq_identity_provider_sub"
        ),
    )

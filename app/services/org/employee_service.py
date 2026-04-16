import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.org import (
    Employee,
    EmployeeEvent,
    EmployeeIdentity,
    JobHistory,
    PositionAssignment,
)
from app.schemas.org import (
    EmployeeCreate,
    EmployeeEventCreate,
    EmployeeIdentityCreate,
    EmployeeUpdate,
)


async def create_employee(session: AsyncSession, payload: EmployeeCreate) -> Employee:
    employee = Employee(**payload.model_dump())
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee


async def list_employees(session: AsyncSession) -> Sequence[Employee]:
    result = await session.execute(select(Employee))
    return result.scalars().all()


async def get_employee(
    session: AsyncSession, employee_id: uuid.UUID
) -> Employee | None:
    return await session.get(Employee, employee_id)


async def update_employee(
    session: AsyncSession, employee: Employee, payload: EmployeeUpdate
) -> Employee:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    await session.commit()
    await session.refresh(employee)
    return employee


async def delete_employee(session: AsyncSession, employee: Employee) -> None:
    await session.delete(employee)
    await session.commit()


async def create_employee_identity(
    session: AsyncSession, payload: EmployeeIdentityCreate
) -> EmployeeIdentity:
    identity = EmployeeIdentity(**payload.model_dump())
    session.add(identity)
    await session.commit()
    await session.refresh(identity)
    return identity


async def list_employee_identities(
    session: AsyncSession, employee_id: uuid.UUID
) -> Sequence[EmployeeIdentity]:
    result = await session.execute(
        select(EmployeeIdentity).where(EmployeeIdentity.employee_id == employee_id)
    )
    return result.scalars().all()


async def create_employee_event(
    session: AsyncSession, payload: EmployeeEventCreate
) -> EmployeeEvent:
    employee_event = EmployeeEvent(**payload.model_dump())
    session.add(employee_event)
    await session.commit()
    await session.refresh(employee_event)
    return employee_event


async def list_employee_events(
    session: AsyncSession, employee_id: uuid.UUID
) -> Sequence[EmployeeEvent]:
    result = await session.execute(
        select(EmployeeEvent)
        .where(EmployeeEvent.employee_id == employee_id)
        .order_by(EmployeeEvent.occurred_at)
    )
    return result.scalars().all()


async def get_position_assignment(
    session: AsyncSession, assignment_id: uuid.UUID
) -> PositionAssignment | None:
    return await session.get(PositionAssignment, assignment_id)


async def get_job_history(
    session: AsyncSession, job_history_id: uuid.UUID
) -> JobHistory | None:
    return await session.get(JobHistory, job_history_id)

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.org import (
    Employee,
    EmployeeIdentity,
)
from app.schemas.org import (
    EmployeeCreate,
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

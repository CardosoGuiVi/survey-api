import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.org import (
    Department,
)
from app.schemas.org.department import DepartmentCreate, DepartmentUpdate


async def create_department(
    session: AsyncSession, payload: DepartmentCreate
) -> Department:
    department = Department(**payload.model_dump())
    session.add(department)
    await session.commit()
    await session.refresh(department)
    return department


async def list_departments(session: AsyncSession) -> Sequence[Department]:
    result = await session.execute(select(Department))
    return result.scalars().all()


async def get_department(
    session: AsyncSession, department_id: uuid.UUID
) -> Department | None:
    return await session.get(Department, department_id)


async def update_department(
    session: AsyncSession, department: Department, payload: DepartmentUpdate
) -> Department:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(department, field, value)
    await session.commit()
    await session.refresh(department)
    return department


async def delete_department(session: AsyncSession, department: Department) -> None:
    await session.delete(department)
    await session.commit()

import uuid
from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.org import Department
from app.schemas.org import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from app.services.org import department_service

router = APIRouter()


@router.post(
    "/departments",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    payload: DepartmentCreate,
    session: AsyncSession = Depends(get_session),
) -> Department:
    return await department_service.create_department(session, payload)


@router.get("/departments", response_model=list[DepartmentResponse])
async def list_departments(
    session: AsyncSession = Depends(get_session),
) -> Sequence[Department]:
    return await department_service.list_departments(session)


@router.get("/departments/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> Department:
    department = await department_service.get_department(session, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
        )
    return department


@router.patch("/departments/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: uuid.UUID,
    payload: DepartmentUpdate,
    session: AsyncSession = Depends(get_session),
) -> Department:
    department = await department_service.get_department(session, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
        )
    return await department_service.update_department(session, department, payload)


@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> None:
    department = await department_service.get_department(session, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not found"
        )
    await department_service.delete_department(session, department)

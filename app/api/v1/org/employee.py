import uuid
from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models import Employee, EmployeeEvent, EmployeeIdentity
from app.schemas.org import (
    EmployeeCreate,
    EmployeeEventCreate,
    EmployeeEventResponse,
    EmployeeIdentityCreate,
    EmployeeIdentityResponse,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.services.org import employee_service

router = APIRouter()
router_identity = APIRouter()
router_event = APIRouter()


@router.post(
    "/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED
)
async def create_employee(
    payload: EmployeeCreate,
    session: AsyncSession = Depends(get_session),
) -> Employee:
    return await employee_service.create_employee(session, payload)


@router.get("/employees", response_model=list[EmployeeResponse])
async def list_employees(
    session: AsyncSession = Depends(get_session),
) -> Sequence[Employee]:
    return await employee_service.list_employees(session)


@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> Employee:
    employee = await employee_service.get_employee(session, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return employee


@router.patch("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: uuid.UUID,
    payload: EmployeeUpdate,
    session: AsyncSession = Depends(get_session),
) -> Employee:
    employee = await employee_service.get_employee(session, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return await employee_service.update_employee(session, employee, payload)


@router.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> None:
    employee = await employee_service.get_employee(session, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    await employee_service.delete_employee(session, employee)


@router_identity.post(
    "/employees/{employee_id}/identities",
    response_model=EmployeeIdentityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee_identity(
    employee_id: uuid.UUID,
    payload: EmployeeIdentityCreate,
    session: AsyncSession = Depends(get_session),
) -> EmployeeIdentity:
    employee = await employee_service.get_employee(session, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return await employee_service.create_employee_identity(session, payload)


@router_identity.get(
    "/employees/{employee_id}/identities", response_model=list[EmployeeIdentityResponse]
)
async def list_employee_identities(
    employee_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> Sequence[EmployeeIdentity]:
    return await employee_service.list_employee_identities(session, employee_id)


@router_event.post(
    "/employee-events",
    response_model=EmployeeEventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee_event(
    payload: EmployeeEventCreate,
    session: AsyncSession = Depends(get_session),
) -> EmployeeEvent:
    return await employee_service.create_employee_event(session, payload)


@router_event.get(
    "/employees/{employee_id}/events", response_model=list[EmployeeEventResponse]
)
async def list_employee_events(
    employee_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> Sequence[EmployeeEvent]:
    return await employee_service.list_employee_events(session, employee_id)

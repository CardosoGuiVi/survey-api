import uuid
from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.org import Position, PositionAssignment
from app.schemas.org import (
    PositionAssignmentCreate,
    PositionAssignmentResponse,
    PositionAssignmentUpdate,
    PositionCreate,
    PositionResponse,
    PositionUpdate,
)
from app.services.org import position_service

router = APIRouter()
router_assignment = APIRouter()


@router.post(
    "/positions", response_model=PositionResponse, status_code=status.HTTP_201_CREATED
)
async def create_position(
    payload: PositionCreate,
    session: AsyncSession = Depends(get_session),
) -> Position:
    return await position_service.create_position(session, payload)


@router.get("/positions", response_model=list[PositionResponse])
async def list_positions(
    session: AsyncSession = Depends(get_session),
) -> Sequence[Position]:
    return await position_service.list_positions(session)


@router.get("/positions/{position_id}", response_model=PositionResponse)
async def get_position(
    position_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> Position:
    position = await position_service.get_position(session, position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )
    return position


@router.patch("/positions/{position_id}", response_model=PositionResponse)
async def update_position(
    position_id: uuid.UUID,
    payload: PositionUpdate,
    session: AsyncSession = Depends(get_session),
) -> Position:
    position = await position_service.get_position(session, position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )
    return await position_service.update_position(session, position, payload)


@router.delete("/positions/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(
    position_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> None:
    position = await position_service.get_position(session, position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Position not found"
        )
    await position_service.delete_position(session, position)


@router_assignment.post(
    "/position-assignments",
    response_model=PositionAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_position_assignment(
    payload: PositionAssignmentCreate,
    session: AsyncSession = Depends(get_session),
) -> PositionAssignment:
    return await position_service.create_position_assignment(session, payload)


@router_assignment.get(
    "/employees/{employee_id}/position-assignments",
    response_model=list[PositionAssignmentResponse],
)
async def list_position_assignments(
    employee_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> Sequence[PositionAssignment]:
    return await position_service.list_position_assignments(session, employee_id)


@router_assignment.patch(
    "/position-assignments/{assignment_id}", response_model=PositionAssignmentResponse
)
async def close_position_assignment(
    assignment_id: uuid.UUID,
    payload: PositionAssignmentUpdate,
    session: AsyncSession = Depends(get_session),
) -> PositionAssignment:
    assignment = await position_service.get_position_assignment(session, assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found"
        )
    return await position_service.close_position_assignment(
        session, assignment, payload
    )

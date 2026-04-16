import uuid
from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.org import Position
from app.schemas.org import (
    PositionCreate,
    PositionResponse,
    PositionUpdate,
)
from app.services.org import position_service

router = APIRouter()


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

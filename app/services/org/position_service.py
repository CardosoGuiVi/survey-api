import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.org import (
    Position,
)
from app.schemas.org import (
    PositionCreate,
    PositionUpdate,
)


async def create_position(session: AsyncSession, payload: PositionCreate) -> Position:
    position = Position(**payload.model_dump())
    session.add(position)
    await session.commit()
    await session.refresh(position)
    return position


async def list_positions(session: AsyncSession) -> Sequence[Position]:
    result = await session.execute(select(Position))
    return result.scalars().all()


async def get_position(
    session: AsyncSession, position_id: uuid.UUID
) -> Position | None:
    return await session.get(Position, position_id)


async def update_position(
    session: AsyncSession, position: Position, payload: PositionUpdate
) -> Position:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(position, field, value)
    await session.commit()
    await session.refresh(position)
    return position


async def delete_position(session: AsyncSession, position: Position) -> None:
    await session.delete(position)
    await session.commit()

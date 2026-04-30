from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_session

router = APIRouter()


@router.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)) -> JSONResponse:
    updated_at = datetime.now(UTC).isoformat()

    try:
        version = (await session.execute(text("SHOW server_version"))).scalar()
        max_conn = (await session.execute(text("SHOW max_connections"))).scalar()
        opened_conn = (
            await session.execute(
                text("SELECT count(*)::int FROM pg_stat_activity WHERE datname = :db"),
                {"db": settings.database.db},
            )
        ).scalar()

        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "updated_at": updated_at,
                "dependencies": {
                    "database": {
                        "status": "connected",
                        "version": version,
                        "max_connections": int(max_conn),  # type: ignore[arg-type]
                        "opened_connections": opened_conn,
                    }
                },
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "updated_at": updated_at,
                "dependencies": {
                    "database": {
                        "status": "disconnected",
                        "error": str(e),
                    }
                },
            },
        )

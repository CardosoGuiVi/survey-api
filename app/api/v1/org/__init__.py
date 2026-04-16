from fastapi import APIRouter

from .department import router as department_router
from .job import router as job_router
from .position import router as position_router

router = APIRouter()

router.include_router(job_router, prefix="/org", tags=["Org - Jobs"])
router.include_router(department_router, prefix="/org", tags=["Org - Department"])
router.include_router(position_router, prefix="/org", tags=["Org - Positions"])

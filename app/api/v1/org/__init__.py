from fastapi import APIRouter

from .department import router as department_router
from .job import router as job_router

router = APIRouter()

router.include_router(job_router, prefix="/org", tags=["Org - Jobs"])
router.include_router(department_router, prefix="/org", tags=["Org - Department"])

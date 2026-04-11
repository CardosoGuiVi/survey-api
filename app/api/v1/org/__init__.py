from fastapi import APIRouter

from .job import router as job_router

router = APIRouter()

router.include_router(job_router, prefix="/org", tags=["Org - Jobs"])

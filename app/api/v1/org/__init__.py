from fastapi import APIRouter

from .department import router as department_router
from .employee import router as employee_router
from .employee import router_event as employee_event_router
from .employee import router_identity as employee_identity_router
from .job import router as job_router
from .job import router_history as job_history_router
from .position import router as position_router
from .position import router_assignment as position_assignment_router

router = APIRouter()

router.include_router(job_router, prefix="/org", tags=["Org - Jobs"])
router.include_router(job_history_router, prefix="/org", tags=["Org - Job History"])
router.include_router(department_router, prefix="/org", tags=["Org - Department"])
router.include_router(position_router, prefix="/org", tags=["Org - Positions"])
router.include_router(
    position_assignment_router, prefix="/org", tags=["Org - Position Assignments"]
)
router.include_router(employee_router, prefix="/org", tags=["Org - Employees"])
router.include_router(
    employee_identity_router, prefix="/org", tags=["Org - Employee Identity"]
)
router.include_router(
    employee_event_router, prefix="/org", tags=["Org - Employee Events"]
)

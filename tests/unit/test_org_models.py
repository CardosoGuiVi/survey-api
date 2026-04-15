import pytest
import sqlalchemy as sa

from app.models.org.department import Department
from app.models.org.employee import Employee, EmployeeStatus
from app.models.org.employee_event import EmployeeEvent, EventType
from app.models.org.employee_identity import EmployeeIdentity
from app.models.org.job import Job
from app.models.org.job_history import JobHistory
from app.models.org.position import Position
from app.models.org.position_assignment import PositionAssignment
from tests.helpers.schema_assertions import assert_model_schema


@pytest.mark.unit
def test_job_schema():
    assert_model_schema(
        Job,
        {
            "id": {"type": sa.UUID, "pk": True},
            "title": {"type": sa.String, "length": 100, "nullable": False},
            "family": {"type": sa.String, "length": 100, "nullable": False},
            "level": {"type": sa.String, "length": 50, "nullable": False},
            "created_at": {"nullable": False},
        },
    )


@pytest.mark.unit
def test_department_model():
    assert_model_schema(
        Department,
        {
            "id": {"type": sa.UUID, "pk": True},
            "name": {"type": sa.String, "length": 100, "nullable": False},
            "parent_department_id": {"type": sa.UUID, "nullable": True},
            "created_at": {"nullable": False},
        },
    )


@pytest.mark.unit
def test_position_model():
    assert_model_schema(
        Position,
        {
            "id": {"type": sa.UUID, "pk": True},
            "name": {"type": sa.String, "length": 100, "nullable": False},
            "department_id": {"type": sa.UUID, "nullable": True},
            "parent_position_id": {"type": sa.UUID, "nullable": True},
            "is_active": {
                "type": sa.Boolean,
                "default": True,
                "nullable": False,
            },
            "created_at": {"nullable": False},
        },
    )


@pytest.mark.unit
def test_employee_model():
    assert_model_schema(
        Employee,
        {
            "id": {"type": sa.UUID, "pk": True},
            "full_name": {"type": sa.String, "length": 255, "nullable": False},
            "email": {
                "type": sa.String,
                "length": 255,
                "nullable": False,
                "unique": True,
            },
            "email_alias": {
                "type": sa.String,
                "length": 255,
                "nullable": True,
                "unique": True,
            },
            "status": {
                "enum": EmployeeStatus,
                "nullable": False,
            },
            "created_at": {"nullable": False},
        },
    )


@pytest.mark.unit
def test_employee_identity_model():
    assert_model_schema(
        EmployeeIdentity,
        {
            "id": {"type": sa.UUID, "pk": True},
            "employee_id": {"type": sa.UUID, "nullable": False},
            "provider": {"type": sa.String, "length": 50, "nullable": False},
            "provider_sub": {"type": sa.String, "length": 255, "nullable": False},
            "provider_email": {"type": sa.String, "length": 255, "nullable": False},
            "linked_at": {"nullable": False},
        },
    )


@pytest.mark.unit
def test_position_assignment_model():
    assert_model_schema(
        PositionAssignment,
        {
            "id": {"type": sa.UUID, "pk": True},
            "position_id": {"type": sa.UUID, "nullable": False},
            "employee_id": {"type": sa.UUID, "nullable": False},
            "started_at": {"type": sa.DateTime, "nullable": False},
            "ended_at": {"type": sa.DateTime, "nullable": True},
        },
    )


@pytest.mark.unit
def test_job_history_model():
    assert_model_schema(
        JobHistory,
        {
            "id": {"type": sa.UUID, "pk": True},
            "employee_id": {"type": sa.UUID, "nullable": False},
            "job_id": {"type": sa.UUID, "nullable": False},
            "started_at": {"type": sa.DateTime, "nullable": False},
            "ended_at": {"type": sa.DateTime, "nullable": True},
        },
    )


@pytest.mark.unit
def test_employee_event_model():
    assert_model_schema(
        EmployeeEvent,
        {
            "id": {"type": sa.UUID, "pk": True},
            "employee_id": {"type": sa.UUID, "nullable": False},
            "position_id": {"type": sa.UUID, "nullable": True},
            "type": {
                "enum": EventType,
                "nullable": False,
            },
            "event_metadata": {"nullable": True},
            "occurred_at": {"type": sa.DateTime, "nullable": False},
            "notes": {"type": sa.Text, "nullable": True},
        },
    )

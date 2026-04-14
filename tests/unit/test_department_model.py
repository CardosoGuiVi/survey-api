import pytest
import sqlalchemy as sa

from app.models.org.department import Department
from tests.helpers.schema_assertions import assert_model_schema


@pytest.mark.unit
def test_department_model():
    assert_model_schema(
        Department,
        {
            "id": {"type": sa.UUID, "pk": True},
            "name": {"type": sa.String, "length": 100, "nullable": False},
            "parent_department_id": {"type": sa.UUID, "nullable": True},
            "created_at": {"server_default": True},
        },
    )

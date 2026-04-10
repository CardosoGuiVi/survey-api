import pytest
import sqlalchemy as sa

from app.models.org.job import Job
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
            "created_at": {"server_default": True},
        },
    )

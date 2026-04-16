import subprocess

import pytest

from app.core.config import settings


@pytest.mark.integration
def test_no_pending_migrations():
    command = ["uv", "run", "alembic", "check"]
    if settings.environment == "test":
        command = ["uv", "run", "--env-file", ".env.test", "alembic", "check"]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Pending migrations detected:\n{result.stdout}\n{result.stderr}"
    )

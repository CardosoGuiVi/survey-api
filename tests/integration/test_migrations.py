import subprocess

import pytest


@pytest.mark.integration
def test_no_pending_migrations():
    result = subprocess.run(
        ["uv", "run", "--env-file", ".env.test", "alembic", "check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Pending migrations detected:\n{result.stdout}\n{result.stderr}"
    )

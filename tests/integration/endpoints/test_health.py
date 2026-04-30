import pytest
from httpx import AsyncClient


@pytest.mark.integration
async def test_health_check_success(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["dependencies"]["database"]["status"] == "connected"
    assert "updated_at" in body


@pytest.mark.integration
async def test_health_check_database_structure(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")

    body = response.json()
    db = body["dependencies"]["database"]
    print(db)

    assert "version" in db
    assert "max_connections" in db
    assert "opened_connections" in db
    assert isinstance(db["max_connections"], int)
    assert isinstance(db["opened_connections"], int)


@pytest.mark.integration
async def test_health_check_opened_connections(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")

    body = response.json()
    opened = body["dependencies"]["database"]["opened_connections"]

    assert opened >= 1

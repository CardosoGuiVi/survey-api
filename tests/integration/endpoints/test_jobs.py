# tests/integration/endpoints/test_jobs.py
import pytest
from httpx import AsyncClient


@pytest.mark.integration
async def test_create_job(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/org/jobs",
        json={"title": "Engenheiro de Software", "family": "Engenharia", "level": "I"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Engenheiro de Software"
    assert data["family"] == "Engenharia"
    assert data["level"] == "I"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.integration
async def test_list_jobs(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/org/jobs",
        json={"title": "Engenheiro de Software", "family": "Engenharia", "level": "I"},
    )
    response = await client.get("/api/v1/org/jobs")
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.integration
async def test_get_job(client: AsyncClient) -> None:
    created = await client.post(
        "/api/v1/org/jobs",
        json={"title": "Engenheiro de Software", "family": "Engenharia", "level": "I"},
    )
    job_id = created.json()["id"]
    response = await client.get(f"/api/v1/org/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["id"] == job_id


@pytest.mark.integration
async def test_get_job_not_found(client: AsyncClient) -> None:
    response = await client.get("/api/v1/org/jobs/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.integration
async def test_update_job(client: AsyncClient) -> None:
    created = await client.post(
        "/api/v1/org/jobs",
        json={"title": "Engenheiro de Software", "family": "Engenharia", "level": "I"},
    )
    job_id = created.json()["id"]
    response = await client.patch(
        f"/api/v1/org/jobs/{job_id}",
        json={"level": "II"},
    )
    assert response.status_code == 200
    assert response.json()["level"] == "II"
    assert response.json()["title"] == "Engenheiro de Software"


@pytest.mark.integration
async def test_delete_job(client: AsyncClient) -> None:
    created = await client.post(
        "/api/v1/org/jobs",
        json={"title": "Engenheiro de Software", "family": "Engenharia", "level": "I"},
    )
    job_id = created.json()["id"]
    response = await client.delete(f"/api/v1/org/jobs/{job_id}")
    assert response.status_code == 204
    response = await client.get(f"/api/v1/org/jobs/{job_id}")
    assert response.status_code == 404

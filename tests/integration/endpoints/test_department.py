import pytest
from httpx import AsyncClient


@pytest.mark.integration
async def test_create_department(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/org/departments",
        json={"name": "Engenharia"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Engenharia"
    assert data["parent_department_id"] is None
    assert "id" in data
    assert "created_at" in data


@pytest.mark.integration
async def test_create_department_with_parent(client: AsyncClient) -> None:
    parent = await client.post(
        "/api/v1/org/departments",
        json={"name": "Engenharia"},
    )
    parent_id = parent.json()["id"]
    response = await client.post(
        "/api/v1/org/departments",
        json={"name": "Back-end", "parent_department_id": parent_id},
    )
    assert response.status_code == 201
    assert response.json()["parent_department_id"] == parent_id


@pytest.mark.integration
async def test_list_departments(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/org/departments",
        json={"name": "Engenharia"},
    )
    response = await client.get("/api/v1/org/departments")
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.integration
async def test_get_department(client: AsyncClient) -> None:
    created = await client.post(
        "/api/v1/org/departments",
        json={"name": "Engenharia"},
    )
    department_id = created.json()["id"]
    response = await client.get(f"/api/v1/org/departments/{department_id}")
    assert response.status_code == 200
    assert response.json()["id"] == department_id


@pytest.mark.integration
async def test_get_department_not_found(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/org/departments/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404


@pytest.mark.integration
async def test_update_department(client: AsyncClient) -> None:
    created = await client.post(
        "/api/v1/org/departments",
        json={"name": "Engenharia"},
    )
    department_id = created.json()["id"]
    response = await client.patch(
        f"/api/v1/org/departments/{department_id}",
        json={"name": "Engenharia e Produto"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Engenharia e Produto"


@pytest.mark.integration
async def test_delete_department(client: AsyncClient) -> None:
    created = await client.post(
        "/api/v1/org/departments",
        json={"name": "Engenharia"},
    )
    department_id = created.json()["id"]
    response = await client.delete(f"/api/v1/org/departments/{department_id}")
    assert response.status_code == 204
    response = await client.get(f"/api/v1/org/departments/{department_id}")
    assert response.status_code == 404

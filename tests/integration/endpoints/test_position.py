import pytest
from httpx import AsyncClient


@pytest.mark.integration
async def test_create_position(client: AsyncClient) -> None:
    department = await client.post(
        "/v1/org/departments",
        json={"name": "Engenharia"},
    )
    department_id = department.json()["id"]
    response = await client.post(
        "/v1/org/positions",
        json={"name": "Head of Engineering", "department_id": department_id},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Head of Engineering"
    assert data["department_id"] == department_id
    assert data["parent_position_id"] is None
    assert data["is_active"] is True
    assert "id" in data


@pytest.mark.integration
async def test_create_position_with_parent(client: AsyncClient) -> None:
    department = await client.post(
        "/v1/org/departments",
        json={"name": "Engenharia"},
    )
    department_id = department.json()["id"]
    parent = await client.post(
        "/v1/org/positions",
        json={"name": "Head of Engineering", "department_id": department_id},
    )
    parent_id = parent.json()["id"]
    response = await client.post(
        "/v1/org/positions",
        json={
            "name": "Tech Lead",
            "department_id": department_id,
            "parent_position_id": parent_id,
        },
    )
    assert response.status_code == 201
    assert response.json()["parent_position_id"] == parent_id


@pytest.mark.integration
async def test_list_positions(client: AsyncClient) -> None:
    department = await client.post(
        "/v1/org/departments",
        json={"name": "Engenharia"},
    )
    department_id = department.json()["id"]
    await client.post(
        "/v1/org/positions",
        json={"name": "Head of Engineering", "department_id": department_id},
    )
    response = await client.get("/v1/org/positions")
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.integration
async def test_get_position(client: AsyncClient) -> None:
    department = await client.post(
        "/v1/org/departments",
        json={"name": "Engenharia"},
    )
    department_id = department.json()["id"]
    created = await client.post(
        "/v1/org/positions",
        json={"name": "Head of Engineering", "department_id": department_id},
    )
    position_id = created.json()["id"]
    response = await client.get(f"/v1/org/positions/{position_id}")
    assert response.status_code == 200
    assert response.json()["id"] == position_id


@pytest.mark.integration
async def test_get_position_not_found(client: AsyncClient) -> None:
    response = await client.get(
        "/v1/org/positions/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404


@pytest.mark.integration
async def test_update_position(client: AsyncClient) -> None:
    department = await client.post(
        "/v1/org/departments",
        json={"name": "Engenharia"},
    )
    department_id = department.json()["id"]
    created = await client.post(
        "/v1/org/positions",
        json={"name": "Head of Engineering", "department_id": department_id},
    )
    position_id = created.json()["id"]
    response = await client.patch(
        f"/v1/org/positions/{position_id}",
        json={"is_active": False},
    )
    assert response.status_code == 200
    assert response.json()["is_active"] is False


@pytest.mark.integration
async def test_delete_position(client: AsyncClient) -> None:
    department = await client.post(
        "/v1/org/departments",
        json={"name": "Engenharia"},
    )
    department_id = department.json()["id"]
    created = await client.post(
        "/v1/org/positions",
        json={"name": "Head of Engineering", "department_id": department_id},
    )
    position_id = created.json()["id"]
    response = await client.delete(f"/v1/org/positions/{position_id}")
    assert response.status_code == 204
    response = await client.get(f"/v1/org/positions/{position_id}")
    assert response.status_code == 404

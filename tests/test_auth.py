"""
Testes de autenticação — register, login e proteção de rotas.
"""

from httpx import AsyncClient

REGISTER_PAYLOAD = {
    "email": "admin@empresa.com",
    "name": "Admin Teste",
    "password": "senha1234",
    "workspace_name": "Empresa Teste",
}


async def test_register_retorna_token(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_register_email_duplicado_retorna_400(client: AsyncClient):
    await client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    response = await client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    assert response.status_code == 400
    assert "E-mail já cadastrado" in response.json()["detail"]


async def test_register_senha_curta_retorna_422(client: AsyncClient):
    payload = {**REGISTER_PAYLOAD, "password": "123"}
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422


async def test_login_com_credenciais_validas(client: AsyncClient):
    await client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": REGISTER_PAYLOAD["email"],
            "password": REGISTER_PAYLOAD["password"],
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_com_senha_errada_retorna_401(client: AsyncClient):
    await client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": REGISTER_PAYLOAD["email"],
            "password": "senha-errada",
        },
    )
    assert response.status_code == 401


async def test_me_sem_token_retorna_403(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 403


async def test_me_com_token_valido(client: AsyncClient):
    register = await client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    token = register.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == REGISTER_PAYLOAD["email"]
    assert data["name"] == REGISTER_PAYLOAD["name"]
    # Garante que password_hash nunca vaza
    assert "password" not in data
    assert "password_hash" not in data


async def test_workspace_criado_no_register(client: AsyncClient):
    """Ao registrar, workspace é criado automaticamente e o usuário é admin."""
    register = await client.post("/api/v1/auth/register", json=REGISTER_PAYLOAD)
    token = register.json()["access_token"]

    import jwt as pyjwt

    from app.core.config import settings

    payload = pyjwt.decode(
        token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
    )

    assert "workspace_id" in payload
    assert payload["role"] == "admin"

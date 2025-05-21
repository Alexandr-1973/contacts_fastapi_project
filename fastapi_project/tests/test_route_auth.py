import pytest
from unittest.mock import AsyncMock
from sqlalchemy import select

from fastapi_project.src.database.models import User


@pytest.mark.asyncio
async def test_create_user(client, user, monkeypatch):
    mock_send_email = AsyncMock()
    monkeypatch.setattr("fastapi_project.src.routes.auth.send_email", mock_send_email)

    response = await client.post("/api/auth/signup", json=user)

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == user["email"]
    assert data["username"] == user["username"]
    # assert "user" in data, f"Data: {data} user: {user}"
    # assert False, f"user = {user}"

    # assert "id" in data["user"]


@pytest.mark.asyncio
async def test_repeat_create_user(client, user):
    response = await client.post("/api/auth/signup", json=user)

    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


@pytest.mark.asyncio
async def test_login_user_not_confirmed(client, user):
    response = await client.post(
        "/api/auth/login",
        data={"username": user["email"], "password": user["password"]},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


@pytest.mark.asyncio
async def test_login_user(client, session, user):
    # Подтверждаем email вручную в базе
    result = await session.execute(
        select(User).where(User.email == user["email"])
    )
    current_user = result.scalar_one()
    current_user.confirmed = True
    await session.commit()

    response = await client.post(
        "/api/auth/login",
        data={"username": user["email"], "password": user["password"]},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client, user):
    response = await client.post(
        "/api/auth/login",
        data={"username": user["email"], "password": "wrong_password"},
    )

    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


@pytest.mark.asyncio
async def test_login_wrong_email(client, user):
    response = await client.post(
        "/api/auth/login",
        data={"username": "wrong@example.com", "password": user["password"]},
    )

    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"


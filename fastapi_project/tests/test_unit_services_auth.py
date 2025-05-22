import pytest
from datetime import datetime, timedelta, UTC
from jose import jwt
from fastapi import HTTPException, status
from fastapi_project.src.services.auth import Auth

@pytest.fixture
def auth():
    return Auth()

def test_verify_password(auth):
    plain_password = "password"
    hashed_password = auth.get_password_hash(plain_password)
    assert auth.verify_password(plain_password, hashed_password)

def test_get_password_hash(auth):
    password = "password"
    hashed = auth.get_password_hash(password)
    assert isinstance(hashed, str)
    assert auth.verify_password(password, hashed)

@pytest.mark.asyncio
async def test_create_access_token(auth):
    data = {"sub": "test@example.com"}
    token = await auth.create_access_token(data)
    decoded = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    assert decoded["sub"] == "test@example.com"
    assert decoded["scope"] == "access_token"

@pytest.mark.asyncio
async def test_create_refresh_token(auth):
    data = {"sub": "test@example.com"}
    token = await auth.create_refresh_token(data)
    decoded = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    assert decoded["sub"] == "test@example.com"
    assert decoded["scope"] == "refresh_token"

@pytest.mark.asyncio
async def test_decode_refresh_token_valid(auth):
    token = jwt.encode(
        {
            "sub": "test@example.com",
            "scope": "refresh_token",
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=5)
        },
        auth.SECRET_KEY, algorithm=auth.ALGORITHM
    )
    email = await auth.decode_refresh_token(token)
    assert email == "test@example.com"

@pytest.mark.asyncio
async def test_decode_refresh_token_invalid_scope(auth):
    token = jwt.encode(
        {
            "sub": "test@example.com",
            "scope": "access_token",
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=5)
        },
        auth.SECRET_KEY, algorithm=auth.ALGORITHM
    )
    with pytest.raises(HTTPException) as excinfo:
        await auth.decode_refresh_token(token)
    assert excinfo.value.status_code == 401

@pytest.mark.asyncio
async def test_get_email_from_token_valid(auth):
    token = jwt.encode(
        {
            "sub": "test@example.com",
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=5)
        },
        auth.SECRET_KEY, algorithm=auth.ALGORITHM
    )
    email = await auth.get_email_from_token(token)
    assert email == "test@example.com"

@pytest.mark.asyncio
async def test_get_email_from_token_invalid(auth):
    invalid_token = "this.is.not.valid"
    with pytest.raises(HTTPException) as excinfo:
        await auth.get_email_from_token(invalid_token)
    assert excinfo.value.status_code == 422

def test_create_email_token(auth):
    data = {"sub": "test@example.com"}
    token = auth.create_email_token(data)
    decoded = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    assert decoded["sub"] == "test@example.com"

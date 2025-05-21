import pytest
import asyncio
from typing import AsyncGenerator
from fastapi.routing import APIRoute
import pytest_asyncio
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from fastapi_project.src.schemas import UserSchema
from fastapi_project.main import app
from fastapi_project.src.database.models import Base
from fastapi_project.src.database.db import get_db
from fastapi_project.src.services.auth import auth_service


# Указываем асинхронный SQLite (in-memory или файл)
DATABASE_URL = "sqlite+aiosqlite:///./test_async.db"

# Создаём асинхронный движок и сессию
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


# Асинхронная фикстура сессии
@pytest_asyncio.fixture(scope="module")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    await engine.dispose()

# def remove_rate_limiter_dependencies(app: FastAPI):
#     for route in app.routes:
#         if isinstance(route, APIRoute):
#             route.dependencies = [
#                 dep for dep in route.dependencies
#                 if not (
#                     hasattr(dep.dependency, "__name__") and dep.dependency.__name__ == "RateLimiter"
#                 )
#             ]
#             route.dependant.dependencies = [
#                 dep for dep in route.dependant.dependencies
#                 if not (
#                     hasattr(dep.call, "__name__") and dep.call.__name__ == "RateLimiter"
#                 )
#             ]


# Переопределяем зависимость get_db
@pytest_asyncio.fixture(scope="module")
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield session

    # remove_rate_limiter_dependencies(app)
    #
    # app.dependency_overrides[RateLimiter] = lambda *args, **kwargs: None

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module")
def user():
    return {"username": "deadpool", "email": "deadpool@example.com", "password": "12345678"}

# @pytest.fixture(scope="module")
# def user() -> UserSchema:
#     return UserSchema(
#         username="deadpool",
#         email="deadpool@example.com",
#         password="12345678"
#     )
# @pytest_asyncio.fixture()
# async def get_token():
#     token = await auth_service.create_access_token(data={"sub": user()["email"]})
#     return token
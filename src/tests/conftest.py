import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.auth.models import Role
from src.config import DB_HOST_TEST, DB_USER_TEST, DB_PASS_TEST, DB_NAME_TEST, DB_PORT
from src.main import app
from src.database import get_async_session, Base


DATABASE_URL = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT}/{DB_NAME_TEST}'

engine_test = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

metadata = Base.metadata


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepate_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# SETUP
# @pytest.fixture(scope="session")
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

client = TestClient(app)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def role_fixture():
    async with async_session_maker() as session:
        role = Role(name="rollarz", permissions={"admin": False})
        session.add(role)
        await session.commit()
        yield role


@pytest.fixture
async def operation_fixture(async_client: AsyncClient):
    response = await async_client.post("/operations/", json={
        "quantity": "25.5",
        "figi": "figi_CODE",
        "instrument_type": "bond",
        "date": "2024-03-08T19:23:51.365",
        "type": "Выплата купонов",
    })
    assert response.status_code == 200, "Failed to create operation in fixture"
    data = response.json()
    yield data
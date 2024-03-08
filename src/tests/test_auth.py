import pytest
from sqlalchemy import select

from src.auth.models import Role
from conftest import client, async_session_maker


async def test_create_role():
    async with async_session_maker() as session:
        role = Role(name="rollarz", permissions={"admin": False})
        session.add(role)
        await session.flush()
        await session.commit()
        query = select(Role).where(Role.id == role.id)
        result = await session.execute(query)
        role = result.scalar()
        assert role.id is not None, "Role not created"


def test_register(role_fixture):
    response = client.post("/auth/register", json={
        "username": "test", 
        "password": "test",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "email": "string@example.com",
        "role_id": role_fixture.id
    })
    assert response.status_code == 201

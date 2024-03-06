from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.schemas import RoleCreate, RoleRead
from src.database import get_async_session
from src.auth.models import Role

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/role")
async def create_role(role: RoleCreate, db: Session = Depends(get_async_session)):
    async with db as session:
        new_role = Role(**role.model_dump())
        session.add(new_role)
        await session.commit()
        await session.refresh(new_role)
        return new_role


@router.get("/role")
async def get_role(db: Session = Depends(get_async_session)):
    async with db as session:
        query = select(Role)
        result = await session.execute(query)
        roles = result.scalars().all()
        return roles

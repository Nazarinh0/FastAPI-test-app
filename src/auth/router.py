from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.schemas import RoleCreate, RoleRead, UserRead
from src.database import get_async_session
from src.auth.models import Role, User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/role", response_model=RoleCreate)
async def create_role(role: RoleCreate, db: Session = Depends(get_async_session)):
    async with db as session:
        new_role = Role(**role.model_dump())
        session.add(new_role)
        await session.commit()
        await session.refresh(new_role)
        return new_role


@router.get("/role", response_model=list[RoleRead])
async def get_roles(db: Session = Depends(get_async_session)):
    async with db as session:
        query = select(Role)
        result = await session.execute(query)
        roles = result.scalars().all()
        return roles


@router.get("/user", response_model=list[UserRead])
async def get_user(db: Session = Depends(get_async_session)):
    async with db as session:
        query = select(User)
        result = await session.execute(query)
        roles = result.scalars().all()
        return roles

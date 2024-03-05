from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Table
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    from src.auth.models import User
    
    yield SQLAlchemyUserDatabase(session, User)


# class ParentOTM(Base):
#     __tablename__ = "parent_table"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     children: Mapped[list["ChildOTM"]] = relationship(back_populates="parent")


# class ChildOTM(Base):
#     __tablename__ = "child_table"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
#     parent: Mapped["ParentOTM"] = relationship(back_populates="children")



# association_table = Table(
#     "association_table",
#     Base.metadata,
#     Column("parent", ForeignKey("parent.id"), primary_key=True),
#     Column("child", ForeignKey("child.id"), primary_key=True),
# )


# class ParentMTM(Base):
#     __tablename__ = "parent"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     children: Mapped[list['ChildMTM']] = relationship(
#         secondary=association_table, back_populates="parents"
#     )


# class ChildMTM(Base):
#     __tablename__ = "child"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     parents: Mapped[list['ParentMTM']] = relationship(
#         secondary=association_table, back_populates="children"
#     )

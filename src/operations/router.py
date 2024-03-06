from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.operations.models import Operation
from src.database import get_async_session
from src.operations.schemas import OperationCreate, OperationRead


router = APIRouter(
    prefix="/operations",
    tags=["Operations"],
)


@router.get("/", response_model=list[OperationRead])
async def get_operations(session: AsyncSession = Depends(get_async_session)):
    query = select(Operation)
    result = await session.execute(query)
    operations = result.scalars().all()
    return operations


@router.post("/{operation_id}", response_model=OperationRead)
async def get_operation(operation_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Operation).where(Operation.type == operation_id)
    result = await session.execute(query)
    operations = result.scalars().all()
    return operations


@router.post("/", response_model=OperationRead)
async def add_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    new_operation = Operation(**new_operation.model_dump())
    session.add(new_operation)
    await session.flush()
    await session.commit()
    return new_operation

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from fastapi_users import FastAPIUsers
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.auth.auth import auth_backend
from src.auth.manager import  get_user_manager
from src.auth.schemas import UserCreate, UserRead
from src.auth.models import User
from src.operations.router import router as router_operation
from src.auth.router import router as router_auth
from src.database import get_async_session


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Launch FastAPICache via Redia before app startup
    This function should be decorated with asynccontextmanager
    and passed to FastAPI's lifespan argument
    """
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="TestApp", lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Authentication"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)
app.include_router(router_operation)
app.include_router(router_auth)


@app.exception_handler(ValidationException)
async def ValidationException(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.get("/")
def hello():
    return "Hello, World!"

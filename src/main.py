from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi_users import FastAPIUsers
from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead
from src.auth.database import User


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(title="TestApp")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.exception_handler(ValidationException)
async def ValidationException(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route(user: User = Depends(current_user)):
    return f"Hello, anonymous user"


fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"},
    {
        "id": 4,
        "role": "trader",
        "name": "Homer",
        "degree": [
            {"id": 1, "created_at": "2023-01-01T12:23:57", "type_degree": "expert"}
        ],
    },
]


@app.get("/")
def hello():
    return "Hello, World!"


@app.get("/users")
def get_all_users():
    return fake_users


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


fake_trades = [
    {
        "id": 1,
        "user_id": 1,
        "currency": "BTC",
        "side": "buy",
        "price": 123,
        "amount": 2.12,
    },
    {
        "id": 2,
        "user_id": 2,
        "currency": "BTC",
        "side": "sell",
        "price": 125,
        "amount": 2.12,
    },
]


@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}

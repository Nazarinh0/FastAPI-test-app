from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    JSON
)
from datetime import datetime


metadata = MetaData()

role = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
)



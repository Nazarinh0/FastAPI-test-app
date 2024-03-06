from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, TIMESTAMP

from src.database import Base


class Operation(Base):
    __tablename__ = "operation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[str] = mapped_column(String)
    figi: Mapped[str] = mapped_column(String)
    instrument_type: Mapped[str | None] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP)
    type: Mapped[str] = mapped_column(String)

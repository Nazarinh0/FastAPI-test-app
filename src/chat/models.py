from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,)
    message: Mapped[str] = mapped_column(String)

    
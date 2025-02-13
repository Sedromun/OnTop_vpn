import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger
from text.keyboard_text import fastest

from .base import BaseModel
from .user import UserModel


class PresentsModel(BaseModel):
    __tablename__ = "present"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, index=True, autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.id))
    country: Mapped[str] = mapped_column(nullable=False, default=fastest)

    price: Mapped[int] = mapped_column(nullable=False, default=0)
    duration: Mapped[int] = mapped_column(nullable=False, default=0)
    user: Mapped["UserModel"] = relationship(back_populates="orders")

    activated: Mapped[int] = mapped_column(nullable=False, default=False)

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, index=True, default=-1
    )

    balance: Mapped[int] = mapped_column(nullable=False, default=0)
    referrer_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    orders: Mapped[List["OrderModel"]] = relationship(back_populates="user")

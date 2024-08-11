import datetime
from typing import List

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, registry

from .base import BaseModel
from .user import UserModel
from sqlalchemy.types import BigInteger


class OrderModel(BaseModel):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, index=True, autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.id))
    country: Mapped[str] = mapped_column(nullable=False, default='Россия')

    begin_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    expiration_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                               default=func.now())

    price: Mapped[int] = mapped_column(nullable=False, default=0)

    keys: Mapped[List["KeyModel"]] = relationship(back_populates="order")

    user: Mapped["UserModel"] = relationship(back_populates="orders")

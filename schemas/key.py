import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, registry

from .base import BaseModel
from .order import OrderModel
from sqlalchemy.types import BigInteger


class KeyModel(BaseModel):
    __tablename__ = "key"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, index=True, autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(ForeignKey(OrderModel.id))

    country: Mapped[str] = mapped_column(nullable=False, default='Россия')
    key: Mapped[str] = mapped_column(nullable=True)

    order: Mapped["OrderModel"] = relationship(back_populates="keys")

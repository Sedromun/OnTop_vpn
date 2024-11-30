from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger

from .base import BaseModel
from .order import OrderModel


class KeyModel(BaseModel):
    __tablename__ = "key"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, index=True, autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(ForeignKey(OrderModel.id))

    country: Mapped[str] = mapped_column(nullable=False, default="Россия")
    server_id: Mapped[int] = mapped_column(nullable=False, default=0)
    key: Mapped[str] = mapped_column(nullable=True)

    order: Mapped["OrderModel"] = relationship(back_populates="keys")

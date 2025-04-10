import datetime
from typing import List

from sqlalchemy import DateTime, func
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
    finished_orders: Mapped[List["FinishedOrderModel"]] = relationship(
        back_populates="user"
    )
    present: Mapped[bool] = mapped_column(nullable=True, default=False)
    sale: Mapped[int] = mapped_column(nullable=True, default=0)
    sale_expiration: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, default=func.now()
    )
    review: Mapped[str] = mapped_column(nullable=True, default="")
    present_for_old: Mapped[bool] = mapped_column(nullable=True, default=False)
    actions: Mapped[List["ActionModel"]] = relationship(back_populates="user")
    presents: Mapped[List["PresentsModel"]] = relationship(back_populates="user")



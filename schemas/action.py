import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger

from .base import BaseModel
from .user import UserModel


class ActionModel(BaseModel):
    __tablename__ = "action"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, index=True, autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.id))

    date_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(), nullable=False, default=func.now()
    )

    user: Mapped["UserModel"] = relationship(back_populates="actions")

    title: Mapped[str] = mapped_column(nullable=False, default='')
    description: Mapped[str] = mapped_column(nullable=False, default='')

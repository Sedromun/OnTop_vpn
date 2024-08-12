import datetime

from sqlalchemy import DateTime, func, inspect
from sqlalchemy.orm import Mapped, as_declarative, mapped_column


@as_declarative()
class BaseModel:
    __table_args__ = {"schema": "users"}

    created_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )

    updated_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

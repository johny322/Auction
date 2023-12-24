import datetime
from copy import deepcopy

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class BaseModel(AsyncAttrs, DeclarativeBase):
    """Abstract model with declarative base functionality"""

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __allow_unmapped__ = False

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, onupdate=datetime.datetime.now,
                                                          default=datetime.datetime.now)

    def __repr__(self):
        return f'<Model: {self.__class__.__name__}> id: {self.id}'

    def get_kwargs(self) -> dict:
        kwargs = deepcopy(self.__dict__)
        extend = ['_sa_instance_state', 'id', 'created_at', 'updated_at']
        return {key: value for key, value in kwargs.items() if key not in extend}

from typing import List

import sqlalchemy as sa
from sqlalchemy import (Column, String, BigInteger, Float, ForeignKey, DateTime, Boolean)
from sqlalchemy import sql

from tgbot.db.database import db
from tgbot.misc.utils.date_worker import get_now_datetime


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(), default=get_now_datetime)
    updated_at = db.Column(
        db.DateTime(),
        default=get_now_datetime,
        onupdate=get_now_datetime,
    )


class User(TimedBaseModel):
    __tablename__ = 'users'
    query: sql.Select

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String(100))
    full_name = Column(String(100))
    referral = Column(BigInteger)

    disable_ads = Column(Boolean, default=False)

    default_country_code = Column(String(20))
    default_country_name = Column(String(20))
    default_country_international_name = Column(String(20))

    default_operator_code = Column(String(20))
    default_operator_name = Column(String(20))

    balance = Column(Float, default=0)


class Settings(TimedBaseModel):
    __tablename__ = 'settings'
    query: sql.Select
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    default_country = Column(String(20))
    default_operator = Column(String(20))


class Favorite(TimedBaseModel):
    __tablename__ = 'favorites'
    query: sql.Select
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    service_code = Column(String(20))
    country_code = Column(String(20))
    operator_code = Column(String(20))


class History(TimedBaseModel):
    __tablename__ = 'history'
    query: sql.Select
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    number_id = Column(String(30))

    price = Column(Float)

    number = Column(String(30))

    country_code = Column(String(10))
    country_name = Column(String(20))
    country_international_code = Column(String(10))
    service_code = Column(String(10))
    service_name = Column(String(20))
    operator_code = Column(String(10))
    operator_name = Column(String(20))

    api_service_name = Column(String(50))

    end_date = Column(DateTime())
    number_type = Column(String(30))  # rent, sms


class RentNumber(TimedBaseModel):
    __tablename__ = 'rent_numbers'
    query: sql.Select
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    rent_id = Column(String(30))
    rent_price = Column(Float)
    rent_number = Column(String(30))
    country_code = Column(String(10))
    country_name = Column(String(20))
    country_international_code = Column(String(10))
    service_code = Column(String(10))
    service_name = Column(String(20))
    operator_code = Column(String(10))
    operator_name = Column(String(20))
    api_service_name = Column(String(50))
    end_date = Column(DateTime())

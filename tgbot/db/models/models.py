import datetime
from copy import deepcopy
from typing import List, Optional

from sqlalchemy import (String, BigInteger, Float, ForeignKey, DateTime, Boolean, Date, select, func)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...misc.utils.date_worker import get_now_datetime, get_now_date

# from date_worker import get_now_datetime, get_now_date
from . import UserType, UserStatus, SubscriptionTypeModel
from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    disable_ads: Mapped[bool] = mapped_column(default=False)

    balance: Mapped[float] = mapped_column(Float, default=0, nullable=False)

    agreement: Mapped[bool] = mapped_column(Boolean, default=False, comment='принял соглашение на пользование бота')

    subscription_expiration: Mapped[datetime.datetime] = mapped_column(DateTime, default=get_now_datetime)
    last_profile_updated: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, comment='дата последнего обновления профиля', nullable=True
    )

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_moderator: Mapped[bool] = mapped_column(Boolean, default=False)

    referral_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    status_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user_statuses.id', ondelete='RESTRICT'), nullable=True)
    user_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user_types.id', ondelete='RESTRICT'), nullable=True)

    # referral: Mapped['User'] = relationship()
    referrers: Mapped[List['User']] = relationship(foreign_keys='User.referral_user_id')
    photos: Mapped[List['UserPhoto']] = relationship(back_populates='user')
    verification_photos: Mapped[List['UserVerificationPhoto']] = relationship(back_populates='user')
    user_data: Mapped['UserData'] = relationship(back_populates='user')
    views: Mapped[List['View']] = relationship(back_populates='user', foreign_keys='View.user_id')
    viewed: Mapped[List['View']] = relationship(back_populates='viewer', foreign_keys='View.viewer_user_id')
    status: Mapped['UserStatus'] = relationship(foreign_keys='User.status_id')
    user_type: Mapped['UserType'] = relationship(foreign_keys='User.user_type_id')

    async def get_views_count(self, session: AsyncSession, profile_view=False, phone_view=False) -> int:
        stmt = select(func.count(View.id)).where(
            View.user_id == self.id, View.profile_view == profile_view, View.phone_view == phone_view
        )
        res = await session.scalar(stmt)
        return res

    async def get_day_views_count(self, session: AsyncSession, profile_view=False, phone_view=False) -> int:
        stmt = select(func.count(View.id)).where(
            View.user_id == self.id,
            View.profile_view == profile_view,
            View.phone_view == phone_view,
            View.view_date == get_now_datetime().date()
        )
        res = await session.scalar(stmt)
        return res

    async def get_or_update_status(self, session: AsyncSession, status_name: str) -> UserStatus:
        if self.subscription_expiration < get_now_datetime():
            stmt = select(UserStatus).where(UserStatus.name == status_name)
            status = await session.scalar(stmt)
            if status.id != self.status_id:
                self.status = status
                print('flush')
                await session.flush([self])
        return await self.awaitable_attrs.status

    async def update_subscription(self, session: AsyncSession, sub_type: SubscriptionTypeModel):
        subscription_expiration = get_now_datetime() + datetime.timedelta(days=sub_type.period_in_days)
        self.status_id = sub_type.status_id
        self.subscription_expiration = subscription_expiration
        await session.flush([self])
        return self

    async def can_change_account_data(self, minimum_days_count: int):
        if not self.last_profile_updated:
            return True
        now = get_now_datetime()
        if now < self.last_profile_updated:
            return False
        delta_days = (now - self.last_profile_updated).days
        return delta_days >= minimum_days_count


class UserPhoto(BaseModel):
    __tablename__ = 'user_photos'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='photos')

    file_id: Mapped[str] = mapped_column()
    file_type: Mapped[str] = mapped_column()
    blur: Mapped[bool] = mapped_column()


class UserVerificationPhoto(BaseModel):
    __tablename__ = 'user_verification_photos'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='verification_photos')

    file_id: Mapped[str] = mapped_column()


class CityModel(BaseModel):
    __tablename__ = 'cities'

    country: Mapped[str]
    name: Mapped[str]
    district: Mapped[str]
    full_name: Mapped[str]


class UserData(BaseModel):
    __tablename__ = 'user_data'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='user_data')

    name: Mapped[str]
    full_name: Mapped[str]
    country: Mapped[str]
    city_full_name: Mapped[str]

    birthday: Mapped[datetime.datetime.date] = mapped_column(Date)
    about: Mapped[str]
    mobile_phone: Mapped[str]
    tg: Mapped[Optional[str]]
    wa: Mapped[bool]
    breast_size: Mapped[float] = mapped_column(Float)
    height: Mapped[int]
    weight: Mapped[int]
    # check_photo_id: Mapped[Optional[str]]
    user_type_id: Mapped[int] = mapped_column(ForeignKey('user_types.id', ondelete='RESTRICT'))

    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id', ondelete='RESTRICT'))

    city: Mapped['CityModel'] = relationship()
    user_type: Mapped['UserType'] = relationship()

    def get_reg_kwargs(self) -> dict:
        kwargs = deepcopy(self.__dict__)
        exclude = [
            'id', 'user_id', 'created_at', 'updated_at', 'city_id', 'day_views',
            'all_views', 'day_phone_views', 'all_phone_views', 'get_city_data', '_sa_instance_state', 'user_type_id'
        ]
        return {key: value for key, value in kwargs.items() if key not in exclude}

    async def get_city_data(self) -> CityModel:
        res = await self.awaitable_attrs.city
        return res


class View(BaseModel):
    __tablename__ = 'views'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user: Mapped['User'] = relationship(back_populates='views', foreign_keys=[user_id])

    viewer_user_id = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    viewer: Mapped['User'] = relationship(back_populates='viewed', foreign_keys=[viewer_user_id])

    profile_view: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    phone_view: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)

    view_date: Mapped[datetime.datetime.date] = mapped_column(Date, nullable=False, default=get_now_date)


class BotSettings(BaseModel):
    __tablename__ = 'bot_settings'

    terms_of_use_url: Mapped[Optional[str]]  # ссылка на пользовательское соглашение
    terms_of_use_path: Mapped[Optional[str]]  # путь к файлу пользовательского соглашения
    max_profile_photo_count: Mapped[Optional[int]]  # максимальное число файлов для загрузки в карточку
    min_days_count_for_change_profile_data: Mapped[Optional[int]]  # минимальное число дней для изменения профиля
    max_about_length: Mapped[Optional[int]]  # максимальная длина информации о себе в карточке
    show_phone_number_cost: Mapped[Optional[float]]  # цена для открытия номера телефона отдельно

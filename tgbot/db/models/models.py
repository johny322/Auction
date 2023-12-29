import datetime
import enum
from typing import List, Optional

from sqlalchemy import (String, BigInteger, Float, ForeignKey, DateTime, Integer, Enum)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class AuctionStatus(enum.Enum):
    completed = 0
    active = 1


class PayoutStatus(enum.Enum):
    processing = 0
    completed = 1


class PayoutMethod(enum.Enum):
    anypay = 1
    crypto_bot = 2


class User(BaseModel):
    __tablename__ = 'users'

    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    disable_ads: Mapped[bool] = mapped_column(default=False)

    balance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    last_profile_updated: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, comment='дата последнего обновления профиля', nullable=True
    )

    wins_count: Mapped[Optional[int]] = mapped_column(Integer, default=0, comment='Выиграно аукционов')
    paid_balance: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=False, comment='Выплачено денег')
    auction_creator: Mapped[List['Auction']] = relationship(foreign_keys='Auction.creator_id')
    auction_bet: Mapped[List['Auction']] = relationship(foreign_keys='Auction.last_user_id')


class Auction(BaseModel):
    __tablename__ = 'auctions'

    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    creator: Mapped['User'] = relationship(back_populates='auction_creator', foreign_keys=[creator_id])
    end_date: Mapped[datetime.datetime] = mapped_column(DateTime)  # окончание аукциона
    message_id: Mapped[int] = mapped_column(BigInteger)
    status: Mapped[int] = mapped_column(Integer, nullable=False)  # AuctionStatus

    last_user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    last_user: Mapped['User'] = relationship(back_populates='auction_bet', foreign_keys=[last_user_id])
    last_bet_sum: Mapped[int]  # размер последней ставки
    full_bet_sum: Mapped[int] = mapped_column(Integer, default=0)  # общая сумма
    history: Mapped[List['AuctionHistory']] = relationship(back_populates='auction')
    bets_count: Mapped[int] = mapped_column(Integer, default=1)


class AuctionHistory(BaseModel):
    __tablename__ = 'auction_history'

    auction_id: Mapped[int] = mapped_column(ForeignKey('auctions.id', ondelete='CASCADE'), nullable=False)
    auction: Mapped['Auction'] = relationship(back_populates='history')
    bet: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user: Mapped['User'] = relationship(foreign_keys=[user_id])


class Payout(BaseModel):
    __tablename__ = 'payouts'

    to_user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    to_user: Mapped['User'] = relationship(foreign_keys=[to_user_id])
    status: Mapped[int] = mapped_column(Integer, nullable=False)  # PayoutStatus
    payout_sum: Mapped[int]
    payout_method: Mapped[int]  # PayoutMethod


class BotSettings(BaseModel):
    __tablename__ = 'bot_settings'

    admin_percent: Mapped[int]
    first_auction_message_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True
    )  # id первого сообщения для будущего аукциона
    minimal_bet_size: Mapped[int]


class Statistic(BaseModel):
    __tablename__ = 'statistic'

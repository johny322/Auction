from typing import Optional

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class SubscriptionTypeModel(BaseModel):
    __tablename__ = 'subscription_types'

    name: Mapped[str] = mapped_column(nullable=False)
    period_in_days: Mapped[int]
    price: Mapped[float] = mapped_column(Float, nullable=False)  # для sendInvoice price * 100

    # коды валют
    # https://core.telegram.org/bots/payments#supported-currencies
    currency: Mapped[str] = mapped_column(default='USD', comment='ISO код валюты для ТГ')  # по умолчанию доллар

    user_type_id: Mapped[int] = mapped_column(
        ForeignKey('user_types.id', ondelete='RESTRICT'),
        comment='для какого типа юзера этот вариант подписки'
    )

    status_id: Mapped[int] = mapped_column(
        ForeignKey('user_statuses.id', ondelete='RESTRICT'),
        nullable=False
    )  # так же статус из tgbot.constants._types.UserStatusStr

    status: Mapped['UserStatus'] = relationship()

    user_type: Mapped['UserType'] = relationship()

    @property
    def tg_invoice_price(self):
        """price для sendInvoice метода"""
        return self.price * 100

    def get_payment_kwargs(self):
        kwargs = self.__dict__
        print(kwargs)
        exclude = [
            '_sa_instance_state', 'id', 'tg_invoice_price', 'name', 'created_at', 'updated_at', 'status', 'user_type'
        ]
        return {key: value for key, value in kwargs.items() if key not in exclude}


class UserStatus(BaseModel):
    __tablename__ = 'user_statuses'

    name: Mapped[str] = mapped_column(comment='название статуса для использования в беке')


class UserType(BaseModel):
    __tablename__ = 'user_types'
    name: Mapped[str] = mapped_column(comment='тип юзера для использования в беке')
    pretty_name: Mapped[Optional[str]] = mapped_column(comment='тип юзера для отображения', nullable=True)

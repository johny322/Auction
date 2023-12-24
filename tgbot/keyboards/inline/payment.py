from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.constants._types import UserStatusStr, PaymentTypeStr
from tgbot.constants.callback_factory import BuySubCD, CloseCD, \
    close_sup_type, close_payment_type, PaymentCD, \
    close_profile_info
from tgbot.db.models import SubscriptionTypeModel
from tgbot.texts import keyboard_texts


def payment_type_keyboard(period_in_days: int, price: float, status_id: int, currency: str,
                          tg_price: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_telegram_payment,
            callback_data=PaymentCD(
                payment_type=PaymentTypeStr.telegram,
                period_in_days=period_in_days,
                price=tg_price,
                currency=currency,
                status_id=status_id,
            ).pack()
        )
    )

    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_close,
            callback_data=CloseCD(payload=close_payment_type).pack()
        )
    )
    return builder.as_markup()


def tg_payment_keyboard(payload):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text=keyboard_texts.btn_pay,
            pay=True
        )
    )
    builder.add(
        InlineKeyboardButton(
            text=keyboard_texts.btn_close,
            callback_data=CloseCD(payload=payload).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def buy_subscription_keyboard(sub_type_id: int = None, user_status: str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    text = keyboard_texts.btn_buy_sub
    if user_status:
        if user_status != UserStatusStr.common:
            text = keyboard_texts.btn_extend_sub
    builder.add(
        InlineKeyboardButton(
            text=text,
            callback_data=BuySubCD(sub_type_id=sub_type_id).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_close,
            callback_data=CloseCD(payload=close_profile_info).pack()
        )
    )
    return builder.as_markup()


def subscription_types_keyboard(sub_types: List[SubscriptionTypeModel]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for sub_type in sub_types:
        text = keyboard_texts.btn_sub_type.format(
            name=sub_type.name.title(),
            price=sub_type.price,
            currency=sub_type.currency
        )
        builder.row(
            InlineKeyboardButton(
                text=text,
                callback_data=BuySubCD(sub_type_id=sub_type.id).pack()
            )
        )
    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_close,
            callback_data=CloseCD(payload=close_sup_type).pack()
        )
    )
    return builder.as_markup()

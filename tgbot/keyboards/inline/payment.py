from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.constants.callback_factory import PaymentCD, PaymentCheckCD, pay_cancel_cd, PayoutCD
from tgbot.db.models import PayoutMethod
from tgbot.texts import keyboard_texts


def check_pay_keyboard_inline(payment_type: str, pay_url: str = None) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(
            text=keyboard_texts.btn_check_payment,
            callback_data=PaymentCheckCD(payment_type=payment_type).pack()
        )],
        [InlineKeyboardButton(
            text=keyboard_texts.btn_cancel,
            callback_data="cancel"
        )]
    ]
    if pay_url:
        inline_keyboard.insert(
            0,
            [InlineKeyboardButton(text=keyboard_texts.btn_pay_payment, url=pay_url)]
        )
    keyboard_inline = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    return keyboard_inline


def pay_types_keyboard_inline(pay_size) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=keyboard_texts.btn_pay_anypay,
                callback_data=PaymentCD(payment_type='anypay', pay_size=pay_size).pack()
            )],
            [InlineKeyboardButton(
                text=keyboard_texts.btn_pay_crypto_bot,
                callback_data=PaymentCD(payment_type='crypto_bot', pay_size=pay_size).pack()
            )],
            [InlineKeyboardButton(
                text=keyboard_texts.btn_cancel,
                callback_data=pay_cancel_cd
            )]
        ]
    )
    return markup


def anypay_types_keyboard_inline(pay_size) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=keyboard_texts.btn_pay_anypay_card, callback_data=f"any_p:card:{pay_size}")],
            [InlineKeyboardButton(text=keyboard_texts.btn_pay_anypay_qiwi, callback_data=f"any_p:qiwi:{pay_size}")],
            [InlineKeyboardButton(text=keyboard_texts.btn_cancel, callback_data="cancel")]
        ]
    )
    return markup


def crypto_bot_currencies_keyboard_inline(currencies: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for currency in currencies:
        builder.add(
            InlineKeyboardButton(
                text=currency,
                callback_data=f'crypto_bot_curr:{currency}'
            )
        )
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_cancel,
            callback_data="cancel"
        )
    )
    return builder.as_markup()


def payout_payment_type_keyboard_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_payout_crypto_bot,
            callback_data=PayoutCD(payment_type=PayoutMethod.crypto_bot.name).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_payout_anypay_card,
            callback_data=PayoutCD(payment_type=PayoutMethod.card.name).pack()
        )
    )
    # builder.row(
    #     InlineKeyboardButton(
    #         text=keyboard_texts.btn_payout_anypay_card,
    #         callback_data=PayoutCD(payment_type=PayoutMethod.anypay.name).pack()
    #     )
    # )
    return builder.as_markup()

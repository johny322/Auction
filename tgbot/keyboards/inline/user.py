from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.constants.callback_factory import ProfileMenuCD, NewBetSizeCD, show_balance_in_chanel_cd
from tgbot.texts import keyboard_texts


def profile_inline_keyboard(auction_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_menu_add_money,
            callback_data=ProfileMenuCD.add_money
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_menu_withdraw_money,
            callback_data=ProfileMenuCD.withdraw_money
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_auction,
            url=auction_url
        )
    )

    return builder.as_markup()


def main_chanel_inline_keyboard(deep_link: str, bot_link: str) -> InlineKeyboardMarkup:
    start_auction_btn = InlineKeyboardButton(
        text=keyboard_texts.btn_auction_start,
        url=deep_link
    )
    to_bot_btn = InlineKeyboardButton(
        text=keyboard_texts.btn_to_bot,
        url=bot_link
    )
    builder = InlineKeyboardBuilder()
    builder.row(start_auction_btn)
    builder.row(to_bot_btn)
    return builder.as_markup()


def bet_chanel_inline_keyboard(bet_size: int, bot_link: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for bsize in range(bet_size + 1, bet_size + 11):
        builder.add(
            InlineKeyboardButton(
                text=str(bsize),
                callback_data=NewBetSizeCD(new_bet=bsize).pack()
            )
        )
    builder.adjust(5)
    show_balance_btn = InlineKeyboardButton(
        text=keyboard_texts.btn_show_balance,
        callback_data=show_balance_in_chanel_cd
    )
    to_bot_btn = InlineKeyboardButton(
        text=keyboard_texts.btn_to_bot,
        url=bot_link
    )

    builder.row(show_balance_btn)
    builder.row(to_bot_btn)
    return builder.as_markup()

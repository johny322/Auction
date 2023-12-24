from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tgbot.texts import keyboard_texts

cancel_button = KeyboardButton(text=keyboard_texts.btn_cancel)
start_menu_button = KeyboardButton(text=keyboard_texts.btn_to_start_menu)


def cancel_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                cancel_button
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=keyboard_texts.btn_start_menu)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)

choose_user_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=keyboard_texts.btn_girl),
            KeyboardButton(text=keyboard_texts.btn_boy),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)


def back_skip_cancel_keyboard(back_btn=True, skip_btn=True, request_contact=False):
    builder = ReplyKeyboardBuilder()
    if request_contact:
        builder.row(
            KeyboardButton(
                text=keyboard_texts.btn_send_phone_number,
                request_contact=request_contact
            )
        )
    if back_btn:
        builder.add(
            KeyboardButton(text=keyboard_texts.btn_back)
        )
    if skip_btn:
        builder.add(
            KeyboardButton(text=keyboard_texts.btn_skip)
        )

    builder.add(
        KeyboardButton(text=keyboard_texts.btn_cancel)
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def back_cancel_confirm_keyboard(back_btn=True):
    builder = ReplyKeyboardBuilder()
    if back_btn:
        builder.add(
            KeyboardButton(text=keyboard_texts.btn_back)
        )
    builder.add(
        KeyboardButton(text=keyboard_texts.btn_cancel)
    )
    builder.row(
        KeyboardButton(text=keyboard_texts.btn_confirm)
    )

    return builder.as_markup(resize_keyboard=True)


def yes_no_cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=keyboard_texts.btn_yes),
        KeyboardButton(text=keyboard_texts.btn_no)
    )
    builder.row(
        KeyboardButton(text=keyboard_texts.btn_cancel)
    )
    return builder.as_markup(resize_keyboard=True)


def yes_no_back_cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=keyboard_texts.btn_yes),
        KeyboardButton(text=keyboard_texts.btn_no)
    )
    builder.row(
        KeyboardButton(text=keyboard_texts.btn_back),
        KeyboardButton(text=keyboard_texts.btn_cancel)
    )
    return builder.as_markup(resize_keyboard=True)

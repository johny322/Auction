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

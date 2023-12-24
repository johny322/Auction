from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tgbot.constants._types import UserTypeStr
from tgbot.db.models import UserType
from tgbot.texts import keyboard_texts


def main_keyboard(user_type: UserType):
    if user_type.name == UserTypeStr.girl:
        keyboard = [
            [
                KeyboardButton(text=keyboard_texts.btn_profile)
            ],
            [
                KeyboardButton(text=keyboard_texts.btn_menu_info)
            ],

        ]
    else:
        keyboard = [
            [
                KeyboardButton(text=keyboard_texts.btn_search_girls),
                KeyboardButton(text=keyboard_texts.btn_profile),
            ],
            [
                KeyboardButton(text=keyboard_texts.btn_menu_info)
            ],
        ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False, )


def info_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.adjust(2)
    # if user_type.name == UserTypeStr.girl:
    #     builder.add(KeyboardButton(text=keyboard_texts.btn_info_for_girts))
    # else:
    #     builder.add(KeyboardButton(text=keyboard_texts.btn_info_for_boys))

    builder.add(KeyboardButton(text=keyboard_texts.btn_main_use_info))

    builder.row(KeyboardButton(text=keyboard_texts.btn_terms_of_use))
    builder.row(KeyboardButton(text=keyboard_texts.btn_info_menu_admin))
    builder.row(KeyboardButton(text=keyboard_texts.btn_to_start_menu))

    return builder.as_markup(resize_keyboard=True)

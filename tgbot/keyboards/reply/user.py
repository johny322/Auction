from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.texts import keyboard_texts


def main_keyboard():
    keyboard = [
        [
            KeyboardButton(text=keyboard_texts.btn_profile)
        ],
        [
            KeyboardButton(text=keyboard_texts.btn_menu_info)
        ],
        [
            KeyboardButton(text=keyboard_texts.btn_menu_rules)
        ],

    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False, )


def info_menu():
    keyboard = [
        [
            KeyboardButton(text=keyboard_texts.btn_recommend),
            KeyboardButton(text=keyboard_texts.btn_info_menu_admin),

        ],
        [
            KeyboardButton(text=keyboard_texts.btn_info_payout),
            KeyboardButton(text=keyboard_texts.btn_info_news_chanel),

        ],
        [
            KeyboardButton(text=keyboard_texts.btn_info_reserve_chanel),
            KeyboardButton(text=keyboard_texts.btn_info_auction_chanel),
        ],
        [
            KeyboardButton(text=keyboard_texts.btn_to_start_menu),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False, )


def rules_menu():
    keyboard = [
        [
            KeyboardButton(text=keyboard_texts.btn_rules_auction),
            KeyboardButton(text=keyboard_texts.btn_rules_bot),
        ],
        [
            KeyboardButton(text=keyboard_texts.btn_to_start_menu),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False, )

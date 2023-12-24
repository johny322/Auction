from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.constants.callback_factory import ConfirmCallbackData, CancelCD, PaginationCD, CloseCD, \
    current_page_callback
from tgbot.texts import keyboard_texts


def confirm_inline_keyboard(payload=None, reject=False, extra=None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=keyboard_texts.btn_confirm,
            callback_data=ConfirmCallbackData(payload=payload, extra=extra).pack()
        )
    )
    if reject:
        builder.add(
            InlineKeyboardButton(
                text=keyboard_texts.btn_reject,
                callback_data=ConfirmCallbackData(payload=payload, confirm=False, extra=extra).pack()
            )
        )
    return builder.as_markup()


def find_keyboard(inline_query_data: str = '', cancel_data: str = '') -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    find_btn = InlineKeyboardButton(
        text=keyboard_texts.btn_find,
        switch_inline_query_current_chat=inline_query_data
    )
    builder.add(find_btn)
    if cancel_data:
        builder.add(
            InlineKeyboardButton(
                text=keyboard_texts.btn_cancel,
                callback_data=CancelCD(payload=cancel_data).pack()
            )
        )
    builder.adjust(1)
    return builder.as_markup()


def paginate_keyboard(max_pages: int, key: str, page: int = 1, count=None,
                      need_previous_page=True, buttons: List[InlineKeyboardButton] = None,
                      payload: str = None) -> InlineKeyboardMarkup:
    previous_page = page - 1
    previous_page_text = keyboard_texts.btn_pagination_prev
    if count is not None:
        current_page_text = keyboard_texts.btn_pagination_count.format(count=count)
    else:
        current_page_text = f'{page}'
    next_page = page + 1
    next_page_text = keyboard_texts.btn_pagination_next
    builder = InlineKeyboardBuilder()

    if previous_page > 0 and need_previous_page:
        builder.button(
            text=previous_page_text,
            callback_data=PaginationCD(key=key, page=previous_page, payload=payload).pack()
        )
    builder.button(
        text=current_page_text,
        callback_data=current_page_callback
    )
    if next_page <= max_pages:
        builder.button(
            text=next_page_text,
            callback_data=PaginationCD(key=key, page=next_page, payload=payload).pack()
        )
    if buttons:
        for button in buttons:
            builder.row(button)
    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_close,
            callback_data=CloseCD(payload=key).pack()
        )
    )

    return builder.as_markup()


def close_keyboard(payload: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=keyboard_texts.btn_close,
            callback_data=CloseCD(payload=payload).pack()
        )
    )
    return builder.as_markup()


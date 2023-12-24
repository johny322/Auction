from typing import Optional

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from tgbot import texts
from tgbot.misc.exceptions import TelegramBadRequestText


async def delete_message_from_state(state: FSMContext, key: str = 'mess_to_del') -> Optional[bool]:
    data = await state.get_data()
    mess_to_del: types.Message = data.get(key)
    if not mess_to_del:
        return None
    try:
        await mess_to_del.delete()
        return True
    except TelegramBadRequest:
        return False


async def _edit_message(message: types.Message):
    if message.caption:
        await message.edit_caption(
            text=texts.empty_text
        )
    else:
        await message.edit_text(
            text=texts.empty_text
        )


async def edit_message_instead_delete(message: types.Message):
    await _edit_message(message)


async def delete_or_edit_message(message: types.Message):
    try:
        await message.delete()
    except TelegramBadRequest as e:
        if TelegramBadRequestText.Message.Delete.cant_for_everyone in str(e):
            await _edit_message(message)

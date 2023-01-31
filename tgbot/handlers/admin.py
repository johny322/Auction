from typing import Optional

from aiogram import Router, types
from aiogram.dispatcher.filters import CommandObject
from aiogram.dispatcher.filters.command import CommandStart
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot import texts
from tgbot.db.models import User
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.reply import start_keyboard

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart(), state="*")
async def admin_start(message: types.Message, state: FSMContext, command: CommandObject, user: Optional[User]):
    await state.clear()
    text = texts.start_admin_message_text

    await message.answer(
        text=text,
        reply_markup=start_keyboard
    )

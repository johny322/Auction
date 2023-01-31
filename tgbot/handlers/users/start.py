from aiogram import Router
from aiogram.dispatcher.filters import CommandObject
from aiogram.dispatcher.filters.command import CommandStart
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from tgbot import texts
from tgbot.db.models import User
from tgbot.keyboards.reply import start_keyboard

user_router = Router()


@user_router.message(CommandStart())
async def user_start_handler(message: Message, state: FSMContext, command: CommandObject, user: User):
    await state.clear()
    text = texts.start_user_message_text

    await message.answer(
        text=text,
        reply_markup=start_keyboard
    )

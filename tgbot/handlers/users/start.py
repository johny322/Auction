from aiogram import Router
from aiogram.filters import CommandObject
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.db.models import User

user_router = Router()


@user_router.message(CommandStart())
async def user_start_handler(message: Message, state: FSMContext, command: CommandObject, user: User):
    await state.clear()

    await message.answer(
        text='hi',
    )

from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot import texts
from tgbot.config import Config
from tgbot.db.models import User
from tgbot.keyboards.inline.user import profile_inline_keyboard
from tgbot.texts import keyboard_texts

profile_router = Router()


@profile_router.message(F.text == keyboard_texts.btn_profile)
async def profile_handler(message: types.Message, session: AsyncSession, user: User, bot: Bot, config: Config):
    await message.answer(
        text=texts.profile_message_text.format(
            id=message.from_user.id,
            balance=user.balance,
            wins_count=user.wins_count,
            paid_balance=user.paid_balance
        ),
        reply_markup=profile_inline_keyboard(config.tg_bot.main_chanel_url)
    )

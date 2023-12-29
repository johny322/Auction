from aiogram import Router, F
from aiogram.filters import CommandObject
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot import texts
from tgbot.config import Config
from tgbot.constants.callback_factory import start_auction_payload
from tgbot.db import db_commands
from tgbot.db.models import User
from tgbot.keyboards import reply
from tgbot.keyboards.reply import main_keyboard
from tgbot.misc.states import AuctionStatesGroup

user_router = Router()


@user_router.message(CommandStart(
    deep_link=True,
    deep_link_encoded=True,
    magic=(F.args == start_auction_payload)
))
async def start_auction_handler(message: Message, state: FSMContext, user: User, session: AsyncSession):
    await state.clear()
    if not user:
        user = await db_commands.add_user(
            session,
            tg_user_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )
    active_auction = await db_commands.has_active_auction(session)
    if active_auction:
        await message.answer(
            text=texts.auction_already_has_message_text
        )
        await state.clear()
        return
    bot_settings = await db_commands.get_bot_settings(session)
    minimal_bet_size = bot_settings.minimal_bet_size
    if user.balance < minimal_bet_size:
        await message.answer(
            text=texts.minimal_auction_bet_warning_text.format(minimal_bet_size)
        )
        await state.clear()
        return
    await message.answer(
        text=texts.auction_first_bet_message_text.format(balance=user.balance),
        reply_markup=reply.cancel_keyboard()
    )
    await state.set_state(AuctionStatesGroup.bet_size)


@user_router.message(CommandStart())
async def user_start_handler(message: Message, state: FSMContext, user: User,
                             session: AsyncSession, config: Config):
    await state.clear()
    if not user:
        user = await db_commands.add_user(
            session,
            tg_user_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )
    tg_config = config.tg_bot
    await message.answer(
        text=texts.start_user_message_text.format(
            reserve_chanel_url=tg_config.reserve_chanel_url,
            news_chanel_url=tg_config.news_chanel_url,
            main_chanel_url=tg_config.main_chanel_url,
        ),
        reply_markup=main_keyboard(),
        disable_web_page_preview=True
    )

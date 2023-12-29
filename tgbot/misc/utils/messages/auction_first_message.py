from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgbot import texts
from tgbot.config import load_config, Config
from tgbot.constants.callback_factory import start_auction_payload
from tgbot.constants.consts import ONLY_ONE_BET_WINNER_PERCENT
from tgbot.db import db_commands
from tgbot.keyboards import inline


async def send_first_auction_message(bot: Bot, async_session: async_sessionmaker[AsyncSession]):
    config = load_config('.env')
    tg_bot_config = config.tg_bot
    main_chanel_id = tg_bot_config.main_chanel_id
    bot_link = tg_bot_config.bot_link()
    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            bot_settings = await db_commands.get_bot_settings(session)
            first_auction_message_id = bot_settings.first_auction_message_id
            if not first_auction_message_id:
                deep_link = await create_start_link(bot, payload=start_auction_payload, encode=True)
                first_auction_message = await bot.send_message(
                    chat_id=main_chanel_id,
                    text=texts.auction_start_message_text.format(
                        winner_persent=100 - bot_settings.admin_percent,
                        only_one_winner_persent=ONLY_ONE_BET_WINNER_PERCENT
                    ),
                    reply_markup=inline.main_chanel_inline_keyboard(deep_link, bot_link)
                )
                await db_commands.update_bot_settings(
                    session, bot_settings.id,
                    first_auction_message_id=first_auction_message.message_id
                )


async def send_auction_message(bot: Bot, session: AsyncSession, config: Config):
    tg_bot_config = config.tg_bot
    main_chanel_id = tg_bot_config.main_chanel_id
    bot_link = tg_bot_config.bot_link()
    bot_settings = await db_commands.get_bot_settings(session)
    deep_link = await create_start_link(bot, payload=start_auction_payload, encode=True)
    auction_message = await bot.send_message(
        chat_id=main_chanel_id,
        text=texts.auction_start_message_text.format(
            winner_persent=100 - bot_settings.admin_percent,
            only_one_winner_persent=ONLY_ONE_BET_WINNER_PERCENT
        ),
        reply_markup=inline.main_chanel_inline_keyboard(deep_link, bot_link)
    )
    await db_commands.update_bot_settings(
        session, bot_settings.id,
        first_auction_message_id=auction_message.message_id
    )

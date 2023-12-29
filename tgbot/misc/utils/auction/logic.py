import asyncio
import math
from typing import List

from aiogram import Bot
from aiogram.utils.text_decorations import html_decoration
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgbot import texts
from tgbot.config import Config
from tgbot.constants.consts import TEMPLATE_DATE_FORMAT, ONLY_ONE_BET_WINNER_PERCENT
from tgbot.db import db_commands
from tgbot.db.models import User, AuctionHistory, Auction, BotSettings, AuctionStatus
from tgbot.misc.utils.date_worker import get_now_datetime
from tgbot.misc.utils.messages import send_auction_message, edit_auction_message


async def start_main_auction_loop(bot: Bot, async_session: async_sessionmaker[AsyncSession], auction_id: int,
                                  config: Config):
    counter = 0
    while True:
        counter += 1
        async with async_session() as session:  # type: AsyncSession
            async with session.begin():
                now = get_now_datetime()
                auction: Auction = await db_commands.get_auction(session, auction_id)
                if auction.end_date < now:
                    await end_auction(auction_id, session, bot, config)
                    return
                # обновлять текст сообщения каждые 5 секунд
                if counter % 5 == 0:
                    last_user: User = await auction.awaitable_attrs.last_user
                    time_to_end = str(auction.end_date - get_now_datetime()).split('.')[0]
                    text = texts.new_bet_auction_message_text.format(
                        full_name=html_decoration.quote(last_user.full_name),
                        username=last_user.username,
                        bet_size=auction.last_bet_sum,
                        bets_count=auction.bets_count,
                        time_to_end=time_to_end,
                        full_bet_sum=auction.full_bet_sum,
                        last_bet_sum=auction.last_bet_sum,
                        end_date=auction.end_date.strftime(TEMPLATE_DATE_FORMAT)
                    )
                    await edit_auction_message(
                        bot=bot,
                        auction_message_id=auction.message_id,
                        text=text,
                        bet_size=auction.last_bet_sum,
                        config=config
                    )
        await asyncio.sleep(1)


async def on_startup_start_main_auction_loop(bot: Bot, async_session: async_sessionmaker[AsyncSession], config: Config):
    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            active_auction = await db_commands.has_active_auction(session)
            if not active_auction:
                return
    await start_main_auction_loop(bot, async_session, active_auction.id, config)


async def get_winner_percents(auction: Auction, bot_settings: BotSettings) -> int:
    history: List[AuctionHistory] = await auction.awaitable_attrs.history
    if len(history) <= 1:
        winner_percent = ONLY_ONE_BET_WINNER_PERCENT
    else:
        admin_percent = bot_settings.admin_percent
        winner_percent = 100 - admin_percent
    return winner_percent


async def end_auction(auction_id: int, session: AsyncSession, bot: Bot, config: Config):
    tg_bot_config = config.tg_bot
    auction = await db_commands.get_auction(session, auction_id)
    winner_user: User = await auction.awaitable_attrs.last_user
    # auction_history: List[AuctionHistory] = await auction.awaitable_attrs.history
    bot_settings = await db_commands.get_bot_settings(session)
    winner_percent = await get_winner_percents(auction, bot_settings)
    user_win_sum = math.ceil(auction.full_bet_sum * winner_percent / 100)
    auction_time = int(((get_now_datetime() - auction.created_at).total_seconds() % 3600) // 60)
    await db_commands.update_auction(
        session, auction.id,
        status=AuctionStatus.completed.value,
    )
    text = texts.end_auction_message_text.format(
        full_name=html_decoration.quote(winner_user.full_name),
        username=winner_user.username,
        last_bet_sum=auction.last_bet_sum,
        bets_count=auction.bets_count,
        winner_percent=winner_percent,
        full_bet_sum=auction.full_bet_sum,
        user_win_sum=user_win_sum,
        end_date=auction.end_date.strftime(TEMPLATE_DATE_FORMAT),
        auction_time=auction_time
    )
    await bot.edit_message_text(
        text=text,
        chat_id=tg_bot_config.main_chanel_id,
        message_id=auction.message_id
    )
    await db_commands.update_user(
        session, winner_user.tg_user_id,
        balance=winner_user.balance + user_win_sum,
        wins_count=winner_user.wins_count + 1
    )
    await send_auction_message(bot, session, config)

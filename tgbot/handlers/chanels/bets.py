import datetime

from aiogram import Router, types, F, Bot
from aiogram.utils.text_decorations import html_decoration
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot import texts
from tgbot.config import Config
from tgbot.constants.callback_factory import show_balance_in_chanel_cd, NewBetSizeCD
from tgbot.constants.consts import AUCTION_ROUND_TIME_LIMIT, TEMPLATE_DATE_FORMAT
from tgbot.db import db_commands
from tgbot.db.models import User
from tgbot.misc.utils.date_worker import get_now_datetime
from tgbot.misc.utils.messages import edit_auction_message

bets_router = Router()


@bets_router.callback_query(F.data == show_balance_in_chanel_cd)
async def show_balance_in_chanel_handler(query: types.CallbackQuery, user: User):
    if not user:
        await query.answer(
            text=texts.need_bot_sub_query_text,
            show_alert=True
        )
        return
    await query.answer(texts.balance_message_text.format(user.balance))


@bets_router.callback_query(NewBetSizeCD.filter(F.new_bet))
async def new_bet_handler(query: types.CallbackQuery, callback_data: NewBetSizeCD, user: User,
                          session: AsyncSession,
                          config: Config, bot: Bot):
    if not user:
        await query.answer(
            text=texts.need_bot_sub_query_text,
            show_alert=True
        )
        return
    new_bet_size = callback_data.new_bet
    active_auction = await db_commands.has_active_auction(session)
    if not active_auction:
        await query.answer(texts.no_auction_already_has_message_text)
        return
    if new_bet_size <= active_auction.last_bet_sum:
        await query.answer(texts.has_bet_lager_than_message_text.format(active_auction.last_bet_sum))
        return
    if new_bet_size > user.balance:
        await query.answer(texts.no_balance_message_text)
        return
    last_user_id = active_auction.last_user_id
    if last_user_id == user.id:
        await query.answer(texts.cant_bet_two_times_message_text)
        return
    end_date = get_now_datetime() + datetime.timedelta(seconds=AUCTION_ROUND_TIME_LIMIT)
    bets_count = active_auction.bets_count + 1
    await db_commands.update_auction(
        session, active_auction.id,
        last_bet_sum=new_bet_size,
        full_bet_sum=active_auction.full_bet_sum + new_bet_size,
        last_user_id=user.id,
        end_date=end_date,
        bets_count=bets_count
    )
    # auction_history: List[AuctionHistory] = await active_auction.awaitable_attrs.history
    # bets_count = 1 + len(auction_history)
    time_to_end = str(active_auction.end_date - get_now_datetime()).split('.')[0]
    text = texts.new_bet_auction_message_text.format(
        auction_id=active_auction.id,
        full_name=html_decoration.quote(query.from_user.full_name),
        username=query.from_user.username,
        bet_size=new_bet_size,
        bets_count=bets_count,
        time_to_end=time_to_end,
        full_bet_sum=active_auction.full_bet_sum,
        last_bet_sum=new_bet_size,
        end_date=end_date.strftime(TEMPLATE_DATE_FORMAT)
    )
    await edit_auction_message(
        bot=bot,
        auction_message_id=active_auction.message_id,
        text=text,
        bet_size=new_bet_size,
        config=config
    )
    last_user = await db_commands.get_user_by_db_id(session, last_user_id)
    await bot.send_message(
        chat_id=last_user.tg_user_id,
        text=texts.new_bet_user_alert_message_text.format(new_bet_size)
    )
    await db_commands.update_user_by_db_id(
        session, user.id,
        balance=user.balance - new_bet_size
    )
    await query.answer()

import datetime

from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgbot import texts
from tgbot.config import Config
from tgbot.constants.callback_factory import YesNoCD
from tgbot.constants.consts import AUCTION_FIRST_TIME_LIMIT, TEMPLATE_DATE_FORMAT
from tgbot.db import db_commands
from tgbot.db.models import User, AuctionStatus
from tgbot.handlers.users.start import user_start_handler
from tgbot.keyboards import inline, reply
from tgbot.misc.states import AuctionStatesGroup
from tgbot.misc.utils.auction import start_main_auction_loop
from tgbot.misc.utils.date_worker import get_now_datetime
from tgbot.misc.utils.messages import edit_auction_message
from tgbot.texts import keyboard_texts

auction_bets_router = Router()


@auction_bets_router.message(StateFilter(AuctionStatesGroup.bet_size), F.text == keyboard_texts.btn_cancel)
async def cancel_auction_bet_handler(message: types.Message, state: FSMContext, user: User, session: AsyncSession,
                                     config: Config):
    await user_start_handler(message, state, user, session, config)


@auction_bets_router.message(StateFilter(AuctionStatesGroup.bet_size))
async def auction_bet_handler(message: types.Message, state: FSMContext, user: User, session: AsyncSession):
    bet_size = message.text
    try:
        bet_size = int(bet_size)
    except ValueError:
        await message.answer(
            texts.bad_first_bet_message_text + '\n' + texts.auction_first_bet_message_text.format(balance=user.balance)
        )
        return
    if bet_size > user.balance:
        await message.answer(
            texts.no_balance_message_text + '\n' + texts.auction_first_bet_message_text.format(balance=user.balance)
        )
        return
    bot_settings = await db_commands.get_bot_settings(session)
    minimal_bet_size = bot_settings.minimal_bet_size
    if bet_size < minimal_bet_size:
        await message.answer(
            texts.minimal_bet_size_warning_text.format(
                minimal_bet_size) + '\n' + texts.auction_first_bet_message_text.format(
                balance=user.balance)
        )
        return
    await state.update_data(bet_size=bet_size)
    await message.answer(
        text=texts.confirm_bet_size_message_text.format(bet_size),
        reply_markup=inline.yes_no_keyboard_inline('first_bet_size')
    )
    await state.set_state(AuctionStatesGroup.confirm)


@auction_bets_router.callback_query(
    StateFilter(AuctionStatesGroup.confirm),
    YesNoCD.filter((F.yes == True) & (F.no == False) & (F.payload == 'first_bet_size'))
)
async def yes_confirm_bet_size_handler(query: types.CallbackQuery, state: FSMContext, session: AsyncSession,
                                       user: User, bot: Bot, config: Config,
                                       async_session: async_sessionmaker[AsyncSession]):
    bot_settings = await db_commands.get_bot_settings(session)
    first_auction_message_id = bot_settings.first_auction_message_id
    data = await state.get_data()
    bet_size = data['bet_size']
    await state.clear()
    active_auction = await db_commands.has_active_auction(session)
    if active_auction:
        await query.message.edit_text(
            text=texts.auction_already_has_message_text
        )
        await state.clear()
        return
    end_date = get_now_datetime() + datetime.timedelta(seconds=AUCTION_FIRST_TIME_LIMIT)
    auction, auction_history = await db_commands.add_auction(
        session,
        creator_id=user.id,
        end_date=end_date,
        message_id=first_auction_message_id,
        last_user_id=user.id,
        last_bet_sum=bet_size,
        full_bet_sum=bet_size,
        status=AuctionStatus.active.value
    )
    new_text = texts.start_auction_message_text.format(
        full_name=html_decoration.quote(query.from_user.full_name),
        username=query.from_user.username,
        bet_size=bet_size
    )
    time_to_end = str(auction.end_date - get_now_datetime()).split('.')[0]
    text = texts.new_bet_auction_message_text.format(
        full_name=html_decoration.quote(query.from_user.full_name),
        username=query.from_user.username,
        bet_size=bet_size,
        bets_count=auction.bets_count,
        time_to_end=time_to_end,
        full_bet_sum=auction.full_bet_sum,
        last_bet_sum=bet_size,
        end_date=end_date.strftime(TEMPLATE_DATE_FORMAT)
    )

    await edit_auction_message(
        bot=bot,
        auction_message_id=first_auction_message_id,
        text=text,
        bet_size=bet_size,
        config=config
    )
    user = await db_commands.update_user_by_db_id(
        session, user_id=user.id,
        balance=user.balance - bet_size
    )
    await query.message.delete()
    await query.message.answer(
        text=texts.good_start_auction_message_text.format(config.tg_bot.main_chanel_url),
        reply_markup=reply.main_keyboard()
    )
    # await bot.send_message(
    #     chat_id=config.tg_bot.main_chanel_id,
    #     text=new_text
    # )
    await session.commit()
    await start_main_auction_loop(
        bot=bot,
        async_session=async_session,
        auction_id=auction.id,
        config=config
    )


@auction_bets_router.callback_query(
    StateFilter(AuctionStatesGroup.confirm),
    YesNoCD.filter((F.yes == False) & (F.no == True) & (F.payload == 'first_bet_size'))
)
async def no_confirm_bet_size_handler(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(
        'Ставка отменена',
        reply_markup=reply.main_keyboard()
    )
    await state.clear()

import asyncio
import logging

from aiogram import Router, types, F, Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot import texts
from tgbot.config import Config
from tgbot.constants.callback_factory import ConfirmPayoutCD, admin_mail_payload, YesNoCD, admin_return_auction_payload
from tgbot.db import db_commands
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards import reply, inline
from tgbot.misc.states import Mailing, AuctionReturnStatesGroup
from tgbot.misc.utils.payout import PayoutLogic, PayoutResult
from tgbot.texts import keyboard_texts

logger = logging.getLogger('main_logger')
admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.callback_query(ConfirmPayoutCD.filter(F.confirm == True))
async def confirm_payout_handler(query: types.CallbackQuery, callback_data: ConfirmPayoutCD, session: AsyncSession,
                                 bot: Bot, config: Config):
    payout_id = callback_data.payout_id
    pl = PayoutLogic(bot, config, session)
    text = texts.good_payout_message_text
    result, payout = await pl.confirm_payout(text, payout_id)
    if result == PayoutResult.no_balance:
        await query.answer(
            text=texts.no_user_balance_payout_message_text,
            show_alert=True
        )
    elif result == PayoutResult.good:
        await query.answer(
            text=texts.good_payout_message_text.format(payout.payout_sum),
            show_alert=True
        )
        await query.message.edit_reply_markup()


@admin_router.callback_query(ConfirmPayoutCD.filter(F.confirm == False))
async def confirm_payout_handler(query: types.CallbackQuery):
    await query.answer(
        text=texts.bad_payout_message_text,
        show_alert=True
    )
    await query.message.edit_reply_markup()


@admin_router.message(Command('mail'))
async def mailing_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text=texts.mailing_post_text,
        reply_markup=reply.cancel_keyboard()
    )
    await state.set_state(Mailing.post)


@admin_router.message(StateFilter(Mailing.post), F.text == keyboard_texts.btn_cancel)
async def cancel_mailing_post_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=texts.mail_cancel_text,
        reply_markup=reply.main_keyboard()
    )


@admin_router.message(StateFilter(Mailing.post))
async def mailing_post_handler(message: types.Message, state: FSMContext):
    try:
        text = message.html_text
    except TypeError:
        text = None

    photo = None
    video = None
    file_id = None
    if message.photo:
        photo = message.photo[-1].file_id
    if message.video:
        video = message.video.file_id
    if message.document:
        file_id = message.document.file_id

    await state.update_data(text=text, video=video, photo=photo, file_id=file_id)
    await state.set_state(Mailing.sure)
    if photo:
        await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=types.ReplyKeyboardRemove()
        )
    elif video:
        await message.answer_video(
            video=video,
            caption=text,
            reply_markup=types.ReplyKeyboardRemove()
        )
    elif file_id:
        await message.answer_document(
            document=file_id,
            caption=text,
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            text=text,
            reply_markup=types.ReplyKeyboardRemove()
        )
    await message.answer(
        text=texts.mail_sure_text,
        reply_markup=inline.yes_no_keyboard_inline(admin_mail_payload)
    )


@admin_router.callback_query(
    StateFilter(Mailing.sure),
    YesNoCD.filter(
        (F.no == True) & (F.payload == admin_mail_payload)
    )
)
async def mailing_send_post(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()
    await query.message.answer(
        text=texts.mail_cancel_text,
        reply_markup=reply.main_keyboard()
    )


@admin_router.callback_query(
    StateFilter(Mailing.sure),
    YesNoCD.filter(
        (F.yes == True) & (F.payload == admin_mail_payload)
    )
)
async def mailing_send_post(query: types.CallbackQuery, state: FSMContext, bot: Bot, session: AsyncSession):
    data = await state.get_data()
    await state.clear()
    await query.message.edit_text(
        text=texts.mail_start_text
    )
    await query.answer()

    msg_count = 0
    block_count = 0
    flood_count = 0
    error_count = 0
    reply_markup = inline.disable_advertising_keyboard()
    users = await db_commands.users_to_mails(session)
    for user in users:
        await asyncio.sleep(0.2)
        try:
            if data["photo"]:
                await bot.send_photo(
                    chat_id=user.tg_user_id,
                    photo=data["photo"],
                    caption=data["text"],
                    reply_markup=reply_markup
                )
            elif data["video"]:
                await bot.send_video(
                    chat_id=user.tg_user_id,
                    video=data["video"],
                    caption=data["text"],
                    reply_markup=reply_markup
                )
            elif data['file_id']:
                await bot.send_document(
                    chat_id=user.tg_user_id,
                    document=data['file_id'],
                    caption=data["text"],
                    reply_markup=reply_markup
                )
            else:
                await bot.send_message(
                    chat_id=user.tg_user_id,
                    text=data["text"],
                    reply_markup=reply_markup
                )
            msg_count += 1
        except TelegramForbiddenError as ex:
            block_count += 1
        except TelegramRetryAfter as ex:
            flood_count += 1
        except Exception as ex:
            error_count += 1
            logger.error(ex)

    await query.message.reply(
        text=texts.mail_end_text.format(
            msg_count=msg_count,
            block_count=block_count,
            flood_count=flood_count,
            error_count=error_count
        )
    )


@admin_router.message(Command('users'))
async def get_users_count_handler(message: types.Message, session: AsyncSession):
    users_count = 3000 + await db_commands.get_users_count(session)
    await message.answer(
        text=texts.users_count_text.format(users_count=users_count),
    )


@admin_router.message(Command('admin'))
async def get_users_count_handler(message: types.Message):
    await message.answer('Команды админа:\n'
                         '👋 /mail - сделать рассылку\n'
                         '👤 /users - число юзеров в боте\n'
                         '💸 /users_balance - юзеры с балансом\n'
                         '💸 /auction_return <id аукциона> - вернуть ставки с аукциона\n'
                         '🏦 /add_balance <id или @username> - увеличение баланса пользователя\n'
                         '❇️ /disable_adv <id или @username> - отключение рекламы пользователя',
                         parse_mode=None
                         )


@admin_router.message(Command('auction_return'))
async def return_auction_handler(message: types.Message, command: CommandObject, state: FSMContext):
    auction_id = command.args
    try:
        auction_id = int(auction_id)
    except ValueError:
        return
    await message.answer(
        text=texts.admin_return_auction_bets_message_text.format(auction_id=auction_id),
        reply_markup=inline.yes_no_keyboard_inline(admin_return_auction_payload)
    )
    await state.update_data(auction_id=auction_id)
    await state.set_state(AuctionReturnStatesGroup.confirm)


@admin_router.callback_query(
    StateFilter(AuctionReturnStatesGroup.confirm),
    YesNoCD.filter(
        (F.yes == True) & (F.payload == admin_return_auction_payload)
    )
)
async def yes_confirm_return_auction_handler(query: types.CallbackQuery, state: FSMContext,
                                             session: AsyncSession, bot: Bot):
    data = await state.get_data()
    auction_id = data['auction_id']
    await state.clear()
    users_bets_data = await db_commands.return_auction_balance(session, auction_id)
    # for user_id, bets_size in users_bets_data.items():
    #     text = texts.return_auction_bets_message_text.format(auction_id=auction_id, bets_size=bets_size)
    #     await send_message(bot, user_id, text)
    #     await asyncio.sleep(0.2)
    await query.message.edit_text(
        text=texts.good_return_auction_bets_message_text.format(
            auction_id=auction_id,
            users_count=len(users_bets_data)
        )
    )


@admin_router.callback_query(
    StateFilter(AuctionReturnStatesGroup.confirm),
    YesNoCD.filter(
        (F.no == True) & (F.payload == admin_return_auction_payload)
    )
)
async def no_confirm_return_auction_handler(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text(
        texts.no_return_auction_bets_message_text
    )

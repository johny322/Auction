import logging

from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration

from tgbot import texts
from tgbot.constants.callback_factory import ProfileMenuCD, PayoutCD
from tgbot.constants.consts import CRYPTO_BOT_PAYOUT_MIN_SIZE, ANYPAY_BOT_PAYOUT_MIN_SIZE
from tgbot.db.models import User, PayoutMethod
from tgbot.keyboards import inline, reply
from tgbot.misc.states import PayoutStatesGroup
from tgbot.misc.utils.payout import PayoutLogic, AsyncSession, Config
from tgbot.texts import keyboard_texts

logger = logging.getLogger('main_logger')
payout_router = Router()


@payout_router.callback_query(F.data == ProfileMenuCD.withdraw_money)
async def start_payout_handler(query: types.CallbackQuery, user: User):
    await query.message.edit_text(
        texts.choose_payout_type_text,
        reply_markup=inline.payout_payment_type_keyboard_inline()
    )


@payout_router.message(StateFilter(PayoutStatesGroup.payout_size), F.text == keyboard_texts.btn_cancel)
async def start_pay_cancel_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text='Вывод отменен',
        reply_markup=reply.main_keyboard()
    )
    logger.info(texts.logger_text_formatter(
        [
            f'user: {message.from_user.id} cancel add balance',
            f'Пополнение отменено'
        ]
    ))
    await state.clear()


@payout_router.callback_query(PayoutCD.filter(F.payment_type))
async def payout_sum_handler(query: types.CallbackQuery, callback_data: PayoutCD, user: User, state: FSMContext):
    await query.message.delete()
    await query.message.answer(
        texts.balance_up_text.format(balance=user.balance),
        reply_markup=reply.cancel_keyboard()
    )
    await state.update_data(payment_type=callback_data.payment_type)
    await state.set_state(PayoutStatesGroup.payout_size)


@payout_router.message(StateFilter(PayoutStatesGroup.payout_size))
async def payout_size_handler(message: types.Message, state: FSMContext, user: User, bot: Bot, session: AsyncSession,
                              config: Config):
    if not message.text.isdigit():
        await message.answer(
            text='Неверный формат'
        )
        return
    data = await state.get_data()
    payment_type = data['payment_type']
    payout_size = int(message.text)
    if payout_size < CRYPTO_BOT_PAYOUT_MIN_SIZE and payment_type == 'crypto_bot':
        await message.answer(
            texts.min_balance_warning_text.format(CRYPTO_BOT_PAYOUT_MIN_SIZE)
        )
        return
    if payout_size < ANYPAY_BOT_PAYOUT_MIN_SIZE and payment_type == 'anypay':
        await message.answer(
            texts.min_balance_warning_text.format(ANYPAY_BOT_PAYOUT_MIN_SIZE)
        )
        return
    if payout_size > user.balance:
        await message.answer(
            texts.no_balance_payout_message_text
        )
        return
    await state.clear()
    await message.answer(
        text=texts.request_for_payout_text.format(payout_size),
        reply_markup=reply.main_keyboard()
    )
    pl = PayoutLogic(bot, config, session)
    text = texts.admin_payout_message_text.format(
        payout_size=payout_size,
        full_name=html_decoration.quote(message.from_user.full_name),
        username=message.from_user.username,
        payment_type=payment_type,
        balance=user.balance
    )
    if payment_type == 'anypay':
        payout_method = PayoutMethod.anypay.value
    if payment_type == 'crypto_bot':
        payout_method = PayoutMethod.crypto_bot.value

    await pl.create_payout(
        text=text,
        to_user_id=user.id,
        payout_sum=payout_size,
        payout_method=payout_method
    )

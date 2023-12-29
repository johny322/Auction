import logging

from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import tgbot.keyboards.inline.payment
from tgbot import texts
from tgbot.constants.callback_factory import YesNoCD, pay_cancel_cd, ProfileMenuCD
from tgbot.db.models import User
from tgbot.keyboards import reply, inline
from tgbot.misc.states import Pay
from tgbot.texts import keyboard_texts

logger = logging.getLogger('main_logger')
payment_router = Router()


@payment_router.callback_query(F.data == ProfileMenuCD.add_money, StateFilter(None))
async def pay_handler(query: types.CallbackQuery, state: FSMContext, user: User):
    try:
        await query.message.delete()
    except TelegramBadRequest:
        pass
    await query.answer()
    balance = user.balance
    await query.message.answer(
        text=texts.balance_up_text.format(balance=balance),
        reply_markup=reply.cancel_keyboard()
    )
    await state.set_state(Pay.pay_size)


@payment_router.callback_query(StateFilter(Pay.anypay_check), F.data == 'cancel')
@payment_router.callback_query(StateFilter(Pay.crypto_bot_check), F.data == 'cancel')
async def cancel_check_payment_handler(query: types.CallbackQuery, state: FSMContext, user: User):
    await state.clear()
    await query.message.delete()
    await query.message.answer(
        text=texts.choose_menu_text,
        reply_markup=reply.main_keyboard()
    )
    logger.info(texts.logger_text_formatter(
        [
            f'user: {query.from_user.id} cancel check add balance',
            f'Проверка пополнения отменена'
        ]
    ))


@payment_router.message(StateFilter(Pay.pay_size), F.text == keyboard_texts.btn_cancel)
async def start_pay_cancel_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text='Пополнение отменено',
        reply_markup=reply.main_keyboard()
    )
    logger.info(texts.logger_text_formatter(
        [
            f'user: {message.from_user.id} cancel add balance',
            f'Пополнение отменено'
        ]
    ))
    await state.clear()


@payment_router.message(StateFilter(Pay.pay_size))
async def pay_size_handler(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(
            text='Неверный формат'
        )
        return
    pay_size = message.text
    await state.update_data(pay_size=pay_size)
    await message.answer(
        text=texts.add_balance_sum_question_text.format(pay_size=pay_size),
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=texts.choose_menu_text,
        reply_markup=inline.yes_no_keyboard_inline(pay_size + '_pay')
    )
    await state.set_state(Pay.confirm_pay_size)


@payment_router.callback_query(
    StateFilter(Pay.confirm_pay_size),
    YesNoCD.filter((F.no == True) & (F.yes == False)),
    (F.data.func(lambda data: data.split(":")[-1].endswith('_pay')))
)
async def pay_size_no_handler(query: types.CallbackQuery, state: FSMContext, user: User):
    balance = user.balance
    await query.message.delete()
    await query.message.answer(
        text=texts.balance_up_text.format(balance=balance),
        reply_markup=reply.cancel_keyboard()
    )
    await state.set_state(Pay.pay_size)


@payment_router.callback_query(
    StateFilter(Pay.confirm_pay_size),
    YesNoCD.filter((F.no == False) & (F.yes == True)),
    F.data.func(lambda data: data.split(":")[-1].endswith('_pay'))
)
async def pay_size_yes_handler(query: types.CallbackQuery, state: FSMContext):
    pay_size = int(query.data.split(":")[-1].replace('_pay', ''))

    await query.message.edit_text(
        text=texts.choose_pay_type_text,
        reply_markup=tgbot.keyboards.inline.payment.pay_types_keyboard_inline(pay_size)
    )


@payment_router.callback_query(F.data == pay_cancel_cd)
async def pay_cancel_handler(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(
        text='Пополнение отменено',
        reply_markup=reply.main_keyboard()
    )
    await state.clear()

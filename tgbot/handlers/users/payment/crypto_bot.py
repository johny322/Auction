import logging

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot import texts
from tgbot.constants.callback_factory import PaymentCD, PaymentCheckCD
from tgbot.db import db_commands
from tgbot.db.models import User
from tgbot.keyboards import inline, reply
from tgbot.keyboards.inline import check_pay_keyboard_inline, cancel_keyboard_inline
from tgbot.misc.states import Pay
from tgbot.services.payments.crypto_bot import CryptoBot, NoExchangeRate

logger = logging.getLogger('main_logger')
crypto_bot_router = Router()


@crypto_bot_router.callback_query(PaymentCD.filter(F.payment_type == 'crypto_bot'))
async def crypto_bot_handler(query: types.CallbackQuery, state: FSMContext):
    pay_size = int(query.data.split(":")[-1])
    payment = CryptoBot()
    await query.message.edit_text(
        text='Выберите валюту',
        reply_markup=inline.crypto_bot_currencies_keyboard_inline(payment.supported_assets)
    )
    await state.update_data(pay_size=pay_size, payment=payment)


@crypto_bot_router.callback_query(F.data.func(lambda data: data.split(":")[0] == 'crypto_bot_curr'))
async def crypto_bot_currency_handler(query: types.CallbackQuery, state: FSMContext):
    currency = query.data.split(":")[-1]
    data = await state.get_data()
    payment: CryptoBot = data['payment']
    pay_size = data['pay_size']
    try:
        invoice_id, pay_url, exchange_rate = await payment.create(asset=currency, amount=pay_size)
        await state.update_data(
            invoice_id=invoice_id,
            pay_url=pay_url,
            exchange_rate=exchange_rate
        )
        logger.info(texts.logger_text_formatter(
            [
                f'user: {query.from_user.id} try to add balance',
                f'{pay_size=}, PAYMENT: crypto_bot, {invoice_id=}, {currency=}'
            ]
        ))
        await query.message.edit_text(
            text=texts.pay_crypto_bot_text.format(
                base_url=pay_url
            ),
            reply_markup=check_pay_keyboard_inline('crypto_bot'),
            disable_web_page_preview=True
        )
        await state.set_state(Pay.crypto_bot_check)
    except NoExchangeRate:
        await query.message.edit_text(
            text='Не удалось совершить конвертацию валюты в рубли',
            reply_markup=cancel_keyboard_inline
        )


@crypto_bot_router.callback_query(StateFilter(Pay.crypto_bot_check), PaymentCheckCD.filter(F.payment_type == 'crypto_bot'))
async def check_crypto_bot_payment(query: types.CallbackQuery, state: FSMContext, user: User, session: AsyncSession):
    data = await state.get_data()
    payment: CryptoBot = data['payment']
    invoice_id = data['invoice_id']
    pay_size = data['pay_size']

    tg_user_id = query.from_user.id

    logs = [
        f'user: {query.from_user.id} try to check add balance',
        f'{pay_size=}, PAYMENT: crypto_bot',
    ]

    await query.answer(cache_time=5)
    check_payment = await payment.check_payment(invoice_id)
    logger.debug(check_payment)
    if not check_payment:
        await query.message.answer(
            'Транзакция не найдена'
        )
        logs.append(f'check result: {check_payment=} Транзакция не найдена')
        logger.info(texts.logger_text_formatter(logs))
        return

    await db_commands.update_user(
        session,
        tg_user_id,
        balance=user.balance + pay_size
    )
    await query.message.delete()
    user = await db_commands.get_user(session, tg_user_id)
    await query.message.answer(
        text=texts.balance_pay_successfully_text.format(
            balance=user.balance
        ),
        reply_markup=reply.main_keyboard()
    )
    logs.append(f'check result: {check_payment=} SUCCESSFUL add balance')
    logger.info(texts.logger_text_formatter(logs))
    await state.clear()

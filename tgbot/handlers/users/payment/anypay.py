import logging

from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot import texts
from tgbot.constants.callback_factory import PaymentCD, PaymentCheckCD
from tgbot.constants.consts import ANYPAY_MIN_PAYMENT_SIZE
from tgbot.db import db_commands
from tgbot.db.models import User, PayoutMethod
from tgbot.keyboards import inline, reply
from tgbot.keyboards.inline import anypay_types_keyboard_inline, cancel_keyboard_inline
from tgbot.misc.states import Pay
from tgbot.services.payments.anypay import AnyPay, CreatePayStatus, PayStatus

logger = logging.getLogger('main_logger')
anypay_router = Router()


@anypay_router.callback_query(PaymentCD.filter(F.payment_type == PayoutMethod.anypay.name))
async def anypay_handler(query: types.CallbackQuery, callback_data: PaymentCD, state: FSMContext):
    pay_size = callback_data.pay_size
    # pay_size = query.data.split(":")[-1]
    if int(pay_size) < ANYPAY_MIN_PAYMENT_SIZE:
        await query.answer(
            text=texts.minimal_pay_size_text.format(pay_size=ANYPAY_MIN_PAYMENT_SIZE),
            show_alert=True
        )
        return
    await query.message.edit_reply_markup(
        reply_markup=anypay_types_keyboard_inline(pay_size)
    )


@anypay_router.callback_query(F.data.func(lambda data: data.split(":")[0] == 'any_p'))
async def yoomoney_transfer(query: types.CallbackQuery, state: FSMContext):
    datas = query.data.split(":")
    method = datas[1]
    pay_size = int(datas[-1])

    old_message = await query.message.edit_text(
        text=texts.email_pay_text,
        reply_markup=cancel_keyboard_inline
    )

    await state.set_state(Pay.anypay_email)
    await state.update_data(
        method=method,
        pay_size=pay_size,
        old_message=old_message
    )


@anypay_router.message(StateFilter(Pay.anypay_email))
async def anypay_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    old_message = data['old_message']
    method = data['method']
    pay_size = data['pay_size']

    email = message.text

    payment = AnyPay()
    status, *res_data = await payment.create(
        amount=pay_size,
        desc=f'Пополнение баланса на сумму {pay_size} RUB',
        method=method,
        email=email
    )
    if status == CreatePayStatus.ok:
        transaction_id, payment_url = res_data

        logger.info(texts.logger_text_formatter(
            [
                f'user: {message.from_user.id} try to add balance',
                f'{pay_size=}, PAYMENT: anypay, {method=}, {transaction_id=}'
            ]
        ))
        await old_message.edit_text(
            text=texts.pay_anypay_text.format(
                pay_url=payment_url
            ),
            reply_markup=inline.check_pay_keyboard_inline(PayoutMethod.anypay.name, payment_url),
            disable_web_page_preview=True
        )

        await state.set_state(Pay.anypay_check)
        await state.update_data(payment=payment, transaction_id=transaction_id)
    else:
        await old_message.edit_text(
            text=texts.anypay_create_pay_error_text,
            reply_markup=inline.cancel_keyboard_inline
        )


@anypay_router.callback_query(
    StateFilter(Pay.anypay_check),
    PaymentCheckCD.filter(F.payment_type == PayoutMethod.anypay.name)
)
async def check_anypay_payment(query: types.CallbackQuery, state: FSMContext, user: User, session: AsyncSession):
    data = await state.get_data()
    payment: AnyPay = data['payment']
    pay_size = data['pay_size']
    transaction_id = data['transaction_id']

    status = await payment.check_payment(transaction_id)

    logs = [
        f'user: {query.from_user.id} try to check add balance',
        f'{pay_size=}, PAYMENT: anypay',
    ]
    tg_user_id = query.from_user.id
    if status == PayStatus.ok:
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
        await state.clear()
        logs.append(f'check result: {status=} SUCCESSFUL add balance')
        logger.info(texts.logger_text_formatter(logs))
        return
    elif status == PayStatus.no_pay:
        await query.message.answer(
            'Транзакция не найдена'
        )
        logs.append(f'check result: {status=} Транзакция не найдена')
    elif status == PayStatus.no_transaction:
        await query.message.answer(
            'Счет не выставлен'
        )
        logs.append(f'check result: {status=} Счет не выставлен')
    elif status == PayStatus.error:
        await query.message.answer(
            texts.anypay_create_pay_error_text
        )
        logs.append(f'check result: {status=} ошибка в сервисе anypay')
    logger.info(texts.logger_text_formatter(logs))
    await query.answer()

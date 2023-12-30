import logging

from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.text_decorations import html_decoration

from tgbot import texts
from tgbot.constants.callback_factory import ProfileMenuCD, PayoutCD, user_payout_confirm_payload, YesNoCD
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
async def payout_size_handler(message: types.Message, state: FSMContext, user: User):
    if not message.text.isdigit():
        await message.answer(
            text='Неверный формат'
        )
        return
    data = await state.get_data()
    payment_type = data['payment_type']
    payout_size = int(message.text)
    if payout_size < CRYPTO_BOT_PAYOUT_MIN_SIZE and payment_type == PayoutMethod.crypto_bot.name:
        await message.answer(
            texts.min_balance_warning_text.format(CRYPTO_BOT_PAYOUT_MIN_SIZE)
        )
        return
    if payout_size < ANYPAY_BOT_PAYOUT_MIN_SIZE and payment_type == PayoutMethod.card.name:
        await message.answer(
            texts.min_balance_warning_text.format(ANYPAY_BOT_PAYOUT_MIN_SIZE)
        )
        return
    if payout_size > user.balance:
        await message.answer(
            texts.no_balance_payout_message_text
        )
        return
    if payment_type == PayoutMethod.crypto_bot.name:
        text = texts.crypto_bot_payout_requisites_message_text
    if payment_type == PayoutMethod.card.name:
        text = texts.card_payout_requisites_message_text
    await message.answer(
        text=text
    )
    await state.update_data(payout_size=payout_size)
    await state.set_state(PayoutStatesGroup.payout_requisites)


@payout_router.message(StateFilter(PayoutStatesGroup.payout_requisites))
async def payout_requisites_handler(message: types.Message, state: FSMContext):
    payout_requisites = html_decoration.quote(message.text)
    data = await state.get_data()
    payment_type = data['payment_type']
    payout_size = data['payout_size']
    await message.answer(
        texts.confirm_payout_message_text.format(
            payout_size=payout_size,
            payment_type=payment_type,
            payout_requisites=payout_requisites
        ),
        reply_markup=inline.yes_no_keyboard_inline(user_payout_confirm_payload)
    )
    await state.update_data(payout_requisites=payout_requisites)
    await state.set_state(PayoutStatesGroup.confirm)


@payout_router.callback_query(
    StateFilter(PayoutStatesGroup.confirm),
    YesNoCD.filter((F.yes == True) & (F.payload == user_payout_confirm_payload))
)
async def yes_confirm_payout_handler(query: types.CallbackQuery, state: FSMContext, user: User, bot: Bot,
                                     session: AsyncSession, config: Config):
    data = await state.get_data()
    payment_type = data['payment_type']
    payout_size = data['payout_size']
    payout_requisites = data['payout_requisites']
    await state.clear()
    await query.answer()
    await query.message.edit_text(
        text=texts.request_for_payout_text.format(payout_size)
    )
    await query.message.answer(
        text=texts.choose_menu_text,
        reply_markup=reply.main_keyboard()
    )
    pl = PayoutLogic(bot, config, session)
    text = texts.admin_payout_message_text.format(
        payout_size=payout_size,
        full_name=html_decoration.quote(query.from_user.full_name),
        username=query.from_user.username,
        payment_type=payment_type,
        payout_requisites=payout_requisites,
        balance=user.balance
    )
    if payment_type == PayoutMethod.anypay.name:
        payout_method = PayoutMethod.anypay.value
    if payment_type == PayoutMethod.crypto_bot.name:
        payout_method = PayoutMethod.crypto_bot.value
    if payment_type == PayoutMethod.card.name:
        payout_method = PayoutMethod.card.value

    await pl.create_payout(
        text=text,
        to_user_id=user.id,
        payout_sum=payout_size,
        payout_method=payout_method
    )


@payout_router.callback_query(
    StateFilter(PayoutStatesGroup.confirm),
    YesNoCD.filter((F.no == True) & (F.payload == user_payout_confirm_payload))
)
async def no_confirm_payout_handler(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(
        text='Вывод отменен',
        reply_markup=reply.main_keyboard()
    )
    await state.clear()

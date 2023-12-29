from aiogram import Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from tgbot import texts
from tgbot.constants.callback_factory import close_advertisement_message
from tgbot.db.models import User
from tgbot.keyboards.reply import main_keyboard
from tgbot.texts import keyboard_texts

cancel_router = Router()


@cancel_router.callback_query((F.data == 'cancel'))
async def cancel_all_handler(query: types.CallbackQuery, state: FSMContext, user: User):
    await state.clear()
    await query.message.delete()
    await query.message.answer(
        text=texts.success_cancel_text,
        reply_markup=main_keyboard()
    )


@cancel_router.message((F.text == keyboard_texts.btn_to_start_menu))
async def go_to_start_menu_handler(message: types.Message, state: FSMContext, user: User):
    await message.answer(
        text=texts.choose_menu_text,
        reply_markup=main_keyboard()
    )


@cancel_router.callback_query(F.data == close_advertisement_message)
async def close_adv_handler(query: types.CallbackQuery, state: FSMContext):
    try:
        await query.message.delete()
        await query.answer()
    except TelegramBadRequest:
        pass

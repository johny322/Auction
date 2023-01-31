from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot import texts
from tgbot.keyboards.reply import main_menu_keyboard_reply, main_menu_keyboard_reply
from tgbot.texts import keyboard_texts

cancel_router = Router()


@cancel_router.callback_query(text='cancel', state='*')
async def cancel_all_handler(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()
    await query.message.answer(
        text=texts.success_cancel_text,
        reply_markup=main_menu_keyboard_reply
    )


@cancel_router.message(text=keyboard_texts.btn_to_start_menu, state='*')
async def go_to_start_menu_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=texts.choose_menu_text,
        reply_markup=main_menu_keyboard_reply
    )

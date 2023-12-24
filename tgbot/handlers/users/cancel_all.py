from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from tgbot import texts
from tgbot.db.models import User
from tgbot.keyboards.reply import main_keyboard
from tgbot.texts import keyboard_texts

cancel_router = Router()


@cancel_router.callback_query((F.data == 'cancel'))
async def cancel_all_handler(query: types.CallbackQuery, state: FSMContext, user: User):
    await state.clear()
    await query.message.delete()
    user_type = await user.awaitable_attrs.user_type
    await query.message.answer(
        text=texts.success_cancel_text,
        reply_markup=main_keyboard(user_type)
    )


@cancel_router.message((F.text == keyboard_texts.btn_to_start_menu))
async def go_to_start_menu_handler(message: types.Message, state: FSMContext, user: User):
    user_type = await user.awaitable_attrs.user_type
    await message.answer(
        text=texts.choose_menu_text,
        reply_markup=main_keyboard(user_type)
    )

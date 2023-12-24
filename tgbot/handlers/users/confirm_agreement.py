from aiogram import Router, F, types
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot import texts
from tgbot.constants.callback_factory import ConfirmCallbackData, agree_agreement
from tgbot.db import db_commands
from tgbot.db.models import User
from tgbot.keyboards.reply import choose_user_type_keyboard

agreement_router = Router()


@agreement_router.callback_query(ConfirmCallbackData.filter(F.payload == agree_agreement))
async def agreement_handler(query: types.CallbackQuery, callback_data: ConfirmCallbackData, user: User,
                            session: AsyncSession):
    if user:
        await query.answer(
            text=texts.already_agree_agreement_message_text,
            show_alert=True
        )
        await query.message.delete()
        return
    is_confirm = callback_data.confirm
    if is_confirm:
        from_user = query.from_user
        await db_commands.add_user(
            session=session,
            tg_user_id=from_user.id,
            username=from_user.username,
            full_name=from_user.full_name,
            agreement=True
        )
        await query.answer(
            text=texts.good_agree_agreement_message_text,
            show_alert=True
        )
        await query.message.delete()
        await query.message.answer(
            text=texts.first_start_user_message_text,
            reply_markup=choose_user_type_keyboard
        )
    else:
        await query.answer(
            text=texts.agree_agreement_message_text,
            show_alert=True
        )

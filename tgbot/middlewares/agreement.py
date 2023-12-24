from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot import texts
from tgbot.constants import callback_factory
from tgbot.db import db_commands
from tgbot.keyboards.inline import confirm_inline_keyboard


class AgreementMiddleware(BaseMiddleware):
    def __init__(self, async_session):
        self.async_session = async_session

    async def __call__(
            self,
            handler: Callable[[Union[types.Message, types.CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[types.Message, types.CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        async with self.async_session() as session:  # type: AsyncSession
            async with session.begin():
                user = await db_commands.get_user(session, event.from_user.id)
        if user:
            return await handler(event, data)
        reply_markup = confirm_inline_keyboard(payload=callback_factory.agree_agreement)
        if isinstance(event, types.Message):
            await event.answer(
                text=texts.agree_agreement_message_text,
                reply_markup=reply_markup
            )
        elif isinstance(event, types.CallbackQuery):
            print(event)
            print(event.data)

            if f"cf:{callback_factory.agree_agreement}" in event.data:
                return await handler(event, data)
            await event.message.answer(
                text=texts.agree_agreement_message_text,
                reply_markup=reply_markup
            )

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from tgbot.db import db_commands


class GetDbObjectsMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        session = data['session']
        user = event.from_user
        user = await db_commands.get_user(session, user.id)
        data['user'] = user
        bot_settings = await db_commands.get_bot_settings(session)
        data['bot_settings'] = bot_settings
        return await handler(event, data)

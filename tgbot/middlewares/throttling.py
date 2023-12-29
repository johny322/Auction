from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, types
from cachetools import TTLCache

from tgbot import texts
from tgbot.constants import consts

cache = TTLCache(maxsize=10_000, ttl=consts.THROTTLE_TIME)
blocked_cache = TTLCache(maxsize=10_000, ttl=consts.BLOCKED_THROTTLE_TIME)


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.Update, Dict[str, Any]], Awaitable[Any]],
            event: types.Update,
            data: Dict[str, Any],
    ) -> Any:
        text = texts.anti_flood_message_text.format(consts.BLOCKED_THROTTLE_TIME)
        user_id = event.from_user.id
        name = f'{user_id}_flood'
        if name in cache or name in blocked_cache:
            if isinstance(event, types.Message):
                await event.answer(text)
            elif isinstance(event, types.CallbackQuery):
                await event.answer(text, show_alert=True)
            # cache[name] = None
            if name in blocked_cache:
                return
            else:
                blocked_cache[name] = None
                return
        cache[name] = None
        return await handler(event, data)

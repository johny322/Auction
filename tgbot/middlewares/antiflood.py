from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import types
from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update

from tgbot.constants import consts

from tgbot import texts


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
            self,
            handler: Callable[[Union[types.Message, types.CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[types.Message, types.CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        user = event.from_user.id
        name = f'{user}_flood'
        check_user = await self.storage.redis.get(name=name)
        if check_user:
            await self.storage.redis.set(name=name, value=1, ex=consts.THROTTLE_TIME)
            text = texts.anti_flood_message_text.format(consts.THROTTLE_TIME)
            if isinstance(event, types.Message):
                await event.answer(text)
            elif isinstance(event, types.CallbackQuery):
                await event.answer(text, show_alert=True)
            # elif isinstance(event, types.InlineQuery):
            #     event.
            return
        await self.storage.redis.set(name=name, value=1, ex=consts.THROTTLE_TIME)
        return await handler(event, data)


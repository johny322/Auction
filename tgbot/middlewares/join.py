from aiogram import Bot, BaseMiddleware, types
from aiogram.enums import ChatMemberStatus

from tgbot import texts


class JoinChannelMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, main_channel_id: int, main_chanel_url: str):
        self.bot = bot
        self.main_channel_id = main_channel_id
        self.main_chanel_url = main_chanel_url

    async def __call__(self, handler, event, data):
        chat_member = await self.bot.get_chat_member(
            chat_id=self.main_channel_id,
            user_id=event.from_user.id
        )
        if isinstance(event, types.CallbackQuery):
            kwargs = dict(
                text=texts.join_main_chanel_query_text,
                show_alert=True
            )
        else:
            kwargs = dict(
                text=texts.join_main_chanel_message_text.format(
                    main_chanel_url=self.main_chanel_url,
                )
            )
        if chat_member.status == ChatMemberStatus.LEFT:
            await event.answer(
                **kwargs
            )
        else:
            return await handler(event, data)
